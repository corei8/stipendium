from wtforms import (
        Form, BooleanField, StringField,
        PasswordField, SelectField, 
        DateTimeField, DecimalField, 
        IntegerField, DateField, HiddenField
        )
from wtforms.validators import (
        Length, InputRequired, Optional, NumberRange,
        EqualTo, DataRequired
        )
from wtforms.widgets import (
        CheckboxInput, DateTimeInput, DateInput
        )


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
    # dead = SelectField(
            # 'Deceased?',
            # choices=[
                # (False, 'Living'),
                # (True, 'Deceased'),
                # ],
            # coerce=bool,
            # ) 
    requester = StringField(
            'From', 
            [Length(min=5, max=25)],
            render_kw={'placeholder': 'Requester'}
            )
    priest_asked = StringField(
            'Priest Requested', 
            [Length(min=0, max=25)],
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
    fullname = StringField(
            'Mass Center', 
            [Length(min=5, max=35)],
            render_kw={'placeholder': 'Mass Center'}
            )
    priests = IntegerField(
            'Number of Priests', 
            [NumberRange(min=1)],
            render_kw={'placeholder': 'Number of Priests'}
            )
    address = StringField(
            'Address',
            [Length(min=10, max=25)],
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
    # closed is not necessary
