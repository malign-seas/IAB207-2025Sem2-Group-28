from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from datetime import datetime
from werkzeug.utils import secure_filename
import os

from . import db
from .models import Event, User, Comment, Booking
from .forms import CancelEventForm, EventCreationForm, CommentForm, EventEditForm
from flask_login import current_user
import os
from werkzeug.utils import secure_filename
from datetime import datetime

events_bp = Blueprint('events', __name__, url_prefix='/events')



@events_bp.route('/<int:id>')
def show(id):
    event = db.session.get(Event, id)
    form = CommentForm()  
    if not event:
        abort(404)
    return render_template('detail.html', event=event, form=form)

@events_bp.route('/<id>/comment', methods=['GET', 'POST'])  
def comment(id):
    form = CommentForm()
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                content=form.content.data,
                user_id=current_user.id,
                event_id=event.id,
                created_at=datetime.now()
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('events.show', id=id))
        else:
            return redirect(url_for('auth.login'))

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


@events_bp.route('/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.organiser_id != current_user.id:
        flash("You don't have permission to edit this event.", "danger")
        return redirect(url_for('events.manage_events'))

    form = EventEditForm(obj=event)

    if form.validate_on_submit():
        event.title = form.title.data
        event.date = form.date.data
        event.start_time = form.starttime.data
        event.end_time = form.endtime.data
        event.genre = form.genre.data
        event.description = form.description.data
        event.venue = form.venue.data
        event.tickets_left = form.tickets.data

        if form.image.data:
            db_file_path = check_upload_file(form)
            event.image = db_file_path

        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('events.manage_events'))

    return render_template('edit.html', form=form, event=event)

@events_bp.route('/manage')
@login_required
def manage_events():
    organiser_id = current_user.id
    events = Event.query.filter_by(organiser_id=organiser_id).all()
    return render_template('manage_events.html', events=events, CancelEventForm=CancelEventForm)


@events_bp.route('/<int:event_id>/cancel', methods=['GET','POST'])
@login_required
def cancel_event(event_id):
    form = CancelEventForm()
    event = Event.query.get_or_404(event_id)

    if not form.validate_on_submit():
        flash('Invalid form submission.', 'danger')
        return redirect(url_for('events.manage_events'))

    if event.organiser_id != current_user.id:
        flash("You don't have permission to cancel this event.", "danger")
        return redirect(url_for('events.manage_events'))

    if event.status == 'Cancelled':
        flash('This event is already cancelled.', 'info')
        return redirect(url_for('events.manage_events'))

    event.status = 'Cancelled'
    db.session.commit()
    flash(f'Event "{event.title}" has been cancelled.', 'warning')
    return redirect(url_for('events.manage_events'))