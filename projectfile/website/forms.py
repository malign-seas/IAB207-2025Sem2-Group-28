from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, FormField, IntegerField, DateField, TimeField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo

# custom form for phone number field
#class TelephoneForm(FlaskForm):
#    country_code = IntegerField('Country Code', validators=[InputRequired()])
#    number       = StringField('Number', validators=[InputRequired()])

# creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email Address", validators=[InputRequired('Enter email address')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    firstname=StringField("First Name", validators=[InputRequired()])
    lastname=StringField("Last Name", validators=[InputRequired()])
    username=StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phonenumber=StringField("Phone Number", validators=[InputRequired(), Length(min=10, max=15, message="Phone number should be between 10 and 15 digits")])
    streetaddress=StringField("Street Address", validators=[InputRequired()])
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    #phone_no=FormField(TelephoneForm)
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")

# Form for creating an event
class EventCreationForm(FlaskForm):
    title=StringField("Title", validators=[InputRequired()])
    date=DateField("Date", format='%Y-%m-%d', validators=[InputRequired()]) 
    time=TimeField("Time", format='%H:%M')
    venue=IntegerField("Venue", validators=[InputRequired()]) #Currently integer instead of string. Change later
    genre=StringField("Genre", validators=[InputRequired()])
    status=SelectField("Status", choices=[('open','Open'), ('sold_out','Sold Out'), ('cancelled','Cancelled'), ('closed','Closed')], validators=[InputRequired()])
    description=TextAreaField("Description", validators=[InputRequired()])
    submit = SubmitField("Create Event")

#Form for creating a comment
class CommentForm(FlaskForm):
  content = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')