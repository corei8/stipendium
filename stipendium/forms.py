from wtforms import (
        Form, BooleanField, StringField,
        PasswordField, SelectField, 
        DateTimeField, DecimalField, 
        IntegerField, DateField
        )
from wtforms.validators import (
        Length, InputRequired, Optional, NumberRange
        )
from wtforms.widgets import (
        CheckboxInput, DateTimeInput, DateInput
        )


class StipendForm(Form):
    intention = StringField(
            'Intention', 
            [Length(min=5, max=120)],
            render_kw={'placeholder': 'Intention'}
            )
    requester = StringField(
            'From', 
            [Length(min=5, max=25)],
            render_kw={'placeholder': 'Requester'}
            )
    priest_asked = StringField(
            'Priest Requested', 
            [Length(min=5, max=25)],
            render_kw={'placeholder': 'Priest Requested'}
            )
    origin = SelectField( # TODO: adjust these for place id
            'Location', 
            choices=[
                ('SLHFLA', 'Brooksville'),
                ('HBVPEN', 'Reading')
                ],
            )
    req_date = DateField(
            'Requested Date',
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
