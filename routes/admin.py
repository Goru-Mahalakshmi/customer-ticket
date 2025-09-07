from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, make_response
from flask_login import login_required, current_user
from functools import wraps
from app import db
from models import Ticket, User, TicketComment
from forms import UpdateTicketForm, CommentForm
import csv
import io
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('user.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get overall statistics
    total_tickets = Ticket.query.count()
    open_tickets = Ticket.query.filter_by(status='open').count()
    in_progress_tickets = Ticket.query.filter_by(status='in_progress').count()
    closed_tickets = Ticket.query.filter_by(status='closed').count()
    
    # Recent tickets
    recent_tickets = Ticket.query.order_by(Ticket.created_at.desc()).limit(5).all()
    
    # Unassigned tickets
    unassigned_tickets = Ticket.query.filter_by(assigned_to=None).count()
    
    stats = {
        'total': total_tickets,
        'open': open_tickets,
        'in_progress': in_progress_tickets,
        'closed': closed_tickets,
        'unassigned': unassigned_tickets
    }
    
    return render_template('admin/dashboard.html', stats=stats, recent_tickets=recent_tickets)

@admin_bp.route('/tickets')
@login_required
@admin_required
def tickets():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    
    query = Ticket.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)
    
    tickets = query.order_by(Ticket.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/tickets.html', tickets=tickets, 
                         status_filter=status_filter, priority_filter=priority_filter)

@admin_bp.route('/ticket/<int:id>')
@login_required
@admin_required
def ticket_detail(id):
    ticket = Ticket.query.get_or_404(id)
    comments = TicketComment.query.filter_by(ticket_id=ticket.id).order_by(
        TicketComment.created_at.asc()).all()
    
    # Get all admin users for assignment
    admins = User.query.filter_by(role='admin').all()
    
    # Create forms
    update_form = UpdateTicketForm()
    update_form.assigned_to.choices = [(0, 'Unassigned')] + [(admin.id, admin.username) for admin in admins]
    update_form.assigned_to.data = ticket.assigned_to or 0
    update_form.status.data = ticket.status
    
    comment_form = CommentForm()
    
    if update_form.validate_on_submit():
        ticket.status = update_form.status.data
        ticket.assigned_to = update_form.assigned_to.data if update_form.assigned_to.data != 0 else None
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('admin.ticket_detail', id=ticket.id))
    
    if comment_form.validate_on_submit():
        comment = TicketComment(
            content=comment_form.content.data,
            ticket_id=ticket.id,
            user_id=current_user.id,
            is_internal=comment_form.is_internal.data
        )
        db.session.add(comment)
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Comment added successfully!', 'success')
        return redirect(url_for('admin.ticket_detail', id=ticket.id))
    
    return render_template('admin/ticket_detail.html', ticket=ticket, comments=comments,
                         update_form=update_form, comment_form=comment_form)

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    return render_template('admin/reports.html')

@admin_bp.route('/export/tickets')
@login_required
@admin_required
def export_tickets():
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['ID', 'Title', 'Status', 'Priority', 'Category', 'Created By', 
                     'Assigned To', 'Created At', 'Updated At'])
    
    # Write ticket data
    tickets = Ticket.query.all()
    for ticket in tickets:
        writer.writerow([
            ticket.id,
            ticket.title,
            ticket.status,
            ticket.priority,
            ticket.category,
            ticket.creator.username,
            ticket.assignee.username if ticket.assignee else 'Unassigned',
            ticket.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            ticket.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = f'attachment; filename=tickets_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    response.headers['Content-Type'] = 'text/csv'
    
    return response
