
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db
from .models import Event
from .forms import EventCreationForm

events = Blueprint('events', __name__, url_prefix='/events')

@events.route('/')
def show():
    #event = db.session.scalar(db.select(Event).where(Event.id==id))
    event = {
        "name": "Local Rock Night",
        "date": "Fri 10 Oct 2025",
        "time": "7:00–10:30pm",
        "venue": "V Block · QUT Gardens Point",
        "genre": "Grunge Rock",
        "status": True,
        "tickets_left": 67,
        "description": "A chill night with covers and classics. Doors open 6:30.",
    }
    return render_template('detail.html', event=event)

@events.route('/create', methods=['GET', 'POST'])
def create():
    print('Method type: ', request.method)
    form = EventCreationForm()
    if form.validate_on_submit():
        title=form.title.data
        date=form.date.data
        time=form.time.data
        venue=form.venue.data
        genre=form.genre.data
        status=form.status.data
        description=form.description.data

        event = Event(title, date, time, venue, genre, status, description)
        db.session.add(event)
        print(title + date + time + venue + genre + status + description)
        db.session.commit()
        flash('Successfully created new event', 'success')
        return redirect(url_for('event.create'))
    return render_template('create.html', form=form)
