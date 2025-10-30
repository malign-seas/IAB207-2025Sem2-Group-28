
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import Event, Comment
from .forms import EventCreationForm
from .forms import CommentForm
from datetime import datetime

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

# @events.route('/<int:event_id>', methods=['GET', 'POST'])
# def event_detail(event_id):
#     event = Event.query.get_or_404(event_id)
#     form = CommentForm()

#     if form.validate_on_submit():
#         if current_user.is_authenticated:
#             new_comment = Comment(
#                 content=form.content.data,
#                 user_id=current_user.id,
#                 event_id=event.id,
#                 created_at=datetime.now()
#             )
#             db.session.add(new_comment)
#             db.session.commit()
#             return redirect(url_for('event.eventdetail', event_id=event.id))
#         else:
#             return redirect(url_for('auth.login')) 
    
#     comments = Comment.query.filter_by(event_id=event.id).order_by(Comment.created_at.desc()).all()

#     return render_template('eventdetail.html', event=event, form=form, comments=comments)

@events.route('/comment-test', methods=['GET', 'POST'])
def comment_test():
    form = CommentForm()

    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                content=form.content.data,
                user_id=current_user.id,
                event_id=1,
                created_at=datetime.now()
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('events.comment_test'))
        else:
            return redirect(url_for('auth.login'))

    comments = Comment.query.order_by(Comment.created_at.desc()).all()

    return render_template('eventdetail.html', form=form, comments=comments)

