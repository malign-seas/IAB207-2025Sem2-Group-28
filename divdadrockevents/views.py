from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import db
from .models import User, Event, Booking
from datetime import datetime

main_bp = Blueprint('main', __name__)

#Home page where you can view all events
@main_bp.route('/')
def index():
    # home page: list all events
    events = db.session.scalars(db.select(Event)).all()
    check_event_dates(events)
    genres = sorted({event.genre for event in events})
    return render_template('index.html', events=events, genres=genres)

# Search functionality for events
@main_bp.route('/search')
def search():
    term = request.args.get('search', '')
    q = f"%{term}%"
    events = db.session.scalars(db.select(Event).where(Event.title.like(q))).all()
    genres = sorted({event.genre for event in events})
    return render_template('index.html', events=events, genres=genres)

# Function for filtering events by genre
@main_bp.route('/genre-sort')
def select_genre():
    genre = request.args.get('genre', 'all')
    if genre == "all" :
        return redirect(url_for('main.index'))
    else:
        events = db.session.scalars(db.select(Event).where(Event.genre.like(genre))).all()
        genres = sorted({event.genre for event in events})
    return render_template('index.html', events=events, genres=genres)

# Function for filtering events by status e.g. 'Open'
@main_bp.route('/status-sort')
def select_status():
    status = request.args.get('status', 'all')
    events = db.session.scalars(db.select(Event).where(Event.status.like(status))).all()
    return render_template('index.html', events=events)

@main_bp.route('/bookings')
@login_required
def bookings():
   
    rows = (
        db.session.query(Booking, Event)
        .join(Event, Booking.event_id == Event.id)
        .filter(Booking.user_id == current_user.id)
        .order_by(Booking.booking_date.desc())
        .all()
    )
    return render_template('bookings.html', bookings=rows)

from flask import redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Booking, Event
from . import db

@main_bp.route('/bookings/cancel_all', methods=['POST'])
@login_required
def cancel_all_bookings():
    
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    if not bookings:
        flash("You don't have any bookings to cancel.", "info")
        return redirect(url_for('main.bookings'))

    
    for b in bookings:
        ev = db.session.get(Event, b.event_id)
        if ev:
            ev.tickets_left += b.num_tickets
        db.session.delete(b)

    db.session.commit()
    flash("All your bookings have been cancelled.", "success")
    return redirect(url_for('main.bookings'))

@main_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):

    b = Booking.query.filter_by(id=booking_id, user_id=current_user.id).first_or_404()


    ev = db.session.get(Event, b.event_id)
    if ev:
        ev.tickets_left += b.num_tickets
    db.session.delete(b)
    db.session.commit()
    flash("Booking cancelled.", "success")
    return redirect(url_for('main.bookings'))

def check_event_dates(events):
    date_now = (datetime.now()).date()
    #Iterates through all events and checks if the event date has passed. Not ideal for efficiency but the webapp isn't being continuously run
    for event in events:
        #Only updates event status to Inactive if it hasn't been Cancelled. Reasoning: Users might want to know which previous events actually happened and which were cancelled
        if date_now > event.date and event.status != 'Cancelled':
            event.status = 'Inactive'
            event.tickets_left = 0
    db.session.commit()
    return