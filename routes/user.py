from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import Ticket, TicketComment
from forms import TicketForm, CommentForm

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    page = request.args.get('page', 1, type=int)
    tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(
        Ticket.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    # Get ticket statistics for the user
    total_tickets = Ticket.query.filter_by(user_id=current_user.id).count()
    open_tickets = Ticket.query.filter_by(user_id=current_user.id, status='open').count()
    closed_tickets = Ticket.query.filter_by(user_id=current_user.id, status='closed').count()
    in_progress_tickets = Ticket.query.filter_by(user_id=current_user.id, status='in_progress').count()
    
    stats = {
        'total': total_tickets,
        'open': open_tickets,
        'in_progress': in_progress_tickets,
        'closed': closed_tickets
    }
    
    return render_template('user/dashboard.html', tickets=tickets, stats=stats)

@user_bp.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            priority=form.priority.data,
            user_id=current_user.id
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been created successfully!', 'success')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/create_ticket.html', title='Create Ticket', form=form)

@user_bp.route('/ticket/<int:id>')
@login_required
def ticket_detail(id):
    ticket = Ticket.query.get_or_404(id)
    
    # Ensure user can only view their own tickets unless they're admin
    if ticket.user_id != current_user.id and not current_user.is_admin():
        flash('You do not have permission to view this ticket.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    # Get comments for this ticket
    comments = TicketComment.query.filter_by(ticket_id=ticket.id).order_by(
        TicketComment.created_at.asc()).all()
    
    # Filter out internal comments for non-admin users
    if not current_user.is_admin():
        comments = [comment for comment in comments if not comment.is_internal]
    
    form = CommentForm()
    if form.validate_on_submit():
        comment = TicketComment(
            content=form.content.data,
            ticket_id=ticket.id,
            user_id=current_user.id,
            is_internal=form.is_internal.data if current_user.is_admin() else False
        )
        db.session.add(comment)
        
        # Update ticket's updated_at timestamp
        from datetime import datetime
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Comment added successfully!', 'success')
        return redirect(url_for('user.ticket_detail', id=ticket.id))
    
    return render_template('user/ticket_detail.html', ticket=ticket, comments=comments, form=form)
