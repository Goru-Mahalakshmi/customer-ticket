from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app import db
from models import Ticket, User
from datetime import datetime, timedelta
from sqlalchemy import func

api_bp = Blueprint('api', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/stats/tickets')
@login_required
@admin_required
def ticket_stats():
    # Get ticket statistics by status
    status_stats = db.session.query(
        Ticket.status,
        func.count(Ticket.id).label('count')
    ).group_by(Ticket.status).all()
    
    # Get ticket statistics by priority
    priority_stats = db.session.query(
        Ticket.priority,
        func.count(Ticket.id).label('count')
    ).group_by(Ticket.priority).all()
    
    # Get ticket statistics by category
    category_stats = db.session.query(
        Ticket.category,
        func.count(Ticket.id).label('count')
    ).group_by(Ticket.category).all()
    
    return jsonify({
        'status': [{'label': stat.status, 'count': stat.count} for stat in status_stats],
        'priority': [{'label': stat.priority, 'count': stat.count} for stat in priority_stats],
        'category': [{'label': stat.category, 'count': stat.count} for stat in category_stats]
    })

@api_bp.route('/stats/timeline')
@login_required
@admin_required
def timeline_stats():
    # Get tickets created in the last 30 days
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    timeline_data = db.session.query(
        func.date(Ticket.created_at).label('date'),
        func.count(Ticket.id).label('count')
    ).filter(
        Ticket.created_at >= start_date
    ).group_by(
        func.date(Ticket.created_at)
    ).order_by('date').all()
    
    return jsonify([
        {
            'date': stat.date.strftime('%Y-%m-%d'),
            'count': stat.count
        } for stat in timeline_data
    ])

@api_bp.route('/stats/performance')
@login_required
@admin_required
def performance_stats():
    # Get average resolution time and other performance metrics
    closed_tickets = Ticket.query.filter_by(status='closed').all()
    
    if not closed_tickets:
        return jsonify({
            'avg_resolution_time': 0,
            'total_resolved': 0,
            'resolution_rate': 0
        })
    
    total_resolution_time = 0
    for ticket in closed_tickets:
        resolution_time = (ticket.updated_at - ticket.created_at).total_seconds() / 3600  # in hours
        total_resolution_time += resolution_time
    
    avg_resolution_time = total_resolution_time / len(closed_tickets)
    total_tickets = Ticket.query.count()
    resolution_rate = (len(closed_tickets) / total_tickets) * 100 if total_tickets > 0 else 0
    
    return jsonify({
        'avg_resolution_time': round(avg_resolution_time, 2),
        'total_resolved': len(closed_tickets),
        'resolution_rate': round(resolution_rate, 2)
    })
