from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from datetime import datetime
from werkzeug.utils import secure_filename
import os

from . import db
from .models import Event, User, Booking
from .forms import EventCreationForm

events_bp = Blueprint('events', __name__, url_prefix='/events')



@events_bp.route('/<int:id>')
def show(id):
    event = db.session.get(Event, id)
    if not event:
        abort(404)
    return render_template('detail.html', event=event)


@events_bp.route('/<int:id>/book', methods=['POST'])
@login_required
def book(id):
    event = db.session.get(Event, id)
    if not event:
        flash("Event not found.", "danger")
        return redirect(url_for("main.index"))

  
    try:
        qty = int(request.form.get("tickets", 1))
    except (TypeError, ValueError):
        qty = 0

    if qty < 1:
        flash("Please select at least 1 ticket.", "warning")
        return redirect(url_for("events.show", id=id))

    if event.tickets_left is None or event.tickets_left < qty:
        flash("Not enough tickets left.", "danger")
        return redirect(url_for("events.show", id=id))


    booking = Booking(
        user_id=current_user.id,
        event_id=event.id,
        num_tickets=qty,
        booking_date=datetime.utcnow(),
    )
    db.session.add(booking)
    event.tickets_left -= qty
    db.session.commit()

    flash(f"You successfully booked {qty} ticket(s) for {event.title}.", "success")
    return redirect(url_for("main.bookings"))  



@events_bp.route('/<int:id>/create', methods=['GET', 'POST'])
def create(id):
    form = EventCreationForm()
    if form.validate_on_submit():
        title = form.title.data
        date = form.date.data
        start_time = form.starttime.data
        end_time = form.endtime.data
        genre = form.genre.data
        status = 'Open'
        description = form.description.data
        organiser_id = id
        venue = form.venue.data
        tickets_left = form.tickets.data

        db_file_path = check_upload_file(form)

        event = Event(
            title=title,
            date=date,
            start_time=start_time,
            end_time=end_time,
            genre=genre,
            status=status,
            description=description,
            organiser_id=organiser_id,
            venue=venue,
            tickets_left=tickets_left,
            image=db_file_path,
        )
        db.session.add(event)
        db.session.commit()
        flash('Successfully created new event', 'success')
        return redirect(url_for('events.create', id=id))

    return render_template('create.html', id=id, form=form)



def check_upload_file(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
    db_upload_path = '/static/img/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path