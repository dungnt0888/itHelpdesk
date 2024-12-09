from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.ticket import Ticket

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html', title="Helpdesk System")


@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        # Admin Dashboard
        total_tickets = Ticket.query.count()
        open_tickets = Ticket.query.filter_by(status='new').count()
        in_progress_tickets = Ticket.query.filter_by(status='in_progress').count()
        closed_tickets = Ticket.query.filter_by(status='closed').count()
        return render_template(
            'dashboard_admin.html',
            total_tickets=total_tickets,
            open_tickets=open_tickets,
            in_progress_tickets=in_progress_tickets,
            closed_tickets=closed_tickets
        )
    else:
        # User Dashboard
        user_tickets = Ticket.query.filter_by(created_by=current_user.id).all()
        return render_template(
            'dashboard_user.html',
            user_tickets=user_tickets
        )
