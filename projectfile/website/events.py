
from flask import Blueprint, render_template

events = Blueprint('events', __name__, url_prefix='/events')

@events.route('/')
def show_event():

    event = {
        "name": "Local Rock Night",
        "date": "Fri 10 Oct 2025",
        "time": "7:00–10:30pm",
        "venue": "V Block · QUT Gardens Point",
        "category": "Rock",
        "open": True,
        "tickets_left": 67,
        "description": "A chill night with covers and classics. Doors open 6:30.",
    }
    return render_template('detail.html', event=event)
