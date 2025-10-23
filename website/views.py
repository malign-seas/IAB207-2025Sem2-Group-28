from flask import Blueprint, render_template
from .forms import LoginForm
from .models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    login_form = LoginForm()
    users = get_user_list()
    #return render_template('base.html', html_form=login_form, title='login', users=users)
    return render_template('index.html')

def get_user_list():
    demo_user = User(username="testuser1", email="demouser@example.com", password="hashedpassword1")
    return [demo_user]

@main_bp.route('/bookings')
def bookings_page():
    return render_template('bookings.html')