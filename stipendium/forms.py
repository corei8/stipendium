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
    origin = SelectField(
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



# if __name__=='__main__':
    # app.debug=True
    # app.run()

