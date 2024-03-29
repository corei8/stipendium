from wtforms import (
        Form, BooleanField, StringField,
        PasswordField, SelectField, 
        # DateTimeField, DecimalField, 
        IntegerField, DateField, HiddenField
        )
from wtforms.validators import (
        Length, Optional, NumberRange,
        EqualTo, DataRequired
        )
from wtforms.widgets import (
        DateInput
        )
from stipendium import db
# from stipendium.models import Center


class LoginForm(Form):
    name = StringField(
            'Name', 
            [Length(min=5, max=20)],
            render_kw={'placeholder': ''}
            )
    username = StringField(
            'Username', 
            [Length(min=5, max=120)],
            render_kw={'placeholder': ''}
            )
    password = PasswordField(
            'Password', 
            validators = [
                DataRequired(),
                EqualTo('password2', message='Passwords don\'t match'),
                Length(min=8, max=120)
                ],
            render_kw={'placeholder': ''}
            )
    password2 = PasswordField(
            'Confirm Password', 
            validators = [
                DataRequired(),
                Length(min=8, max=120)
                ],
            render_kw={'placeholder': ''}
            )


class QueueForm(Form):
    intention = StringField(
            'Intention', 
            [Length(min=5, max=120)],
            render_kw={'placeholder': 'Intention'}
            )
    dead = BooleanField(
            'Deceased?',
            )
    requester = StringField(
            'From', 
            [Length(min=5, max=25)],
            render_kw={'placeholder': 'Requester'}
            )
    # priest_asked = StringField(
            # 'Priest Requested', 
            # [Length(min=0, max=25)],
            # render_kw={'placeholder': 'Priest Requested'}
            # )
    priest_asked = SelectField(
            'Priest Requested',
            coerce = int,
            render_kw={'placeholder': 'Priest Requested'}
            )
    origin = SelectField( # TODO: adjust these for place id
            'Location', 
            choices=[
                ('SLHFLA', 'Brooksville'),
                ],
            )
    submitted = DateField(
            'Date Submitted',
            [Optional()],
            widget=DateInput(),
            )
    req_date = DateField(
            'Date Requested',
            [Optional()],
            widget=DateInput(),
            )
    amount = IntegerField(
            'Stipend',
            [NumberRange(message="Must be a number.")],
            render_kw={'placeholder': 'Amount'},
            ) 
    masses = IntegerField(
            'Number of Masses',
            [NumberRange(min=1,message="Must be a number.")],
            render_kw={'placeholder': 'Number'},
            )

class CenterForm(Form):
    name = StringField(
            'Mass Center', 
            [Length(min=5, max=35)],
            render_kw={'placeholder': 'Mass Center'}
            )
    address = StringField(
            'Address',
            [Length(min=10, max=50)],
            render_kw={'placeholder': 'Address'}
            )
    city = StringField(
            'City',
            [Length(min=4, max=25)],
            render_kw={'placeholder': 'City'}
            )
    state = StringField(
            'State or Province',
            [Length(min=4, max=25)],
            render_kw={'placeholder': 'State or Province'}
            )
    country = StringField(
            'Country',
            [Length(min=4, max=25)],
            render_kw={'placeholder': 'Country'}
            )

class PriestForm(Form):
    firstname = StringField(
            'First Name',
            [Length(min=1, max=15)],
            render_kw={'placeholder': 'First Name'}
            )
    lastname = StringField(
            'Last Name',
            [Length(min=1, max=15)],
            render_kw={'placeholder': 'Last Name'}
            )
    rank = SelectField(
            'Title',
            choices=[
                ('Fr.', 'Father'),
                ('Bp.', 'Bishop'),
                ],
            render_kw={'placeholder': 'Title'}
            )
    center = SelectField(
            'Mass Center',
            coerce = int,
            render_kw={'placeholder': 'Mass Center'}
            )

class DeleteForm(Form):
    id = HiddenField()
    intention = HiddenField()
    dead = HiddenField()
    requester = HiddenField()
    priest_asked = HiddenField()
    origin = HiddenField()
    accepted = HiddenField()
    req_date = HiddenField()
    amount = HiddenField() 
    masses = HiddenField()
