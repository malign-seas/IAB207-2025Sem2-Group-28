
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import Event, User
from .forms import EventCreationForm
from flask_login import current_user

events_bp = Blueprint('events', __name__, url_prefix='/events')

@events_bp.route('/<id>')
def show(id):
    event = db.session.get(Event, id)
    return render_template('detail.html', event=event)

@events_bp.route('/<id>/create', methods=['GET', 'POST'])
def create(id):
    print('Method type: ', request.method)
    form = EventCreationForm()
    if form.validate_on_submit():
        title=form.title.data
        date=form.date.data
        time=form.time.data
        genre=form.genre.data
        status='open'
        description=form.description.data
        organizer_id = id
        venue=form.venue.data

        event = Event(title=title, date=date, time=time, genre=genre, status=status, description=description, organizer_id=organizer_id, venue=venue)
        db.session.add(event)       
        db.session.commit()
        flash('Successfully created new event', 'success')
        return redirect(url_for('events.create', id=id))
    return render_template('create.html', id=id, form=form)
