from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    """Класс форма LoginForm для валидации данных для входа менеджера"""
    username = StringField('username', validators=[validators.DataRequired(), validators.Length(min=4, max=12)])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=5, max=16)])


class ClientOrder(Form):
    """Класс форма ClientOrder для валидации и сохранения данных в бд"""
    customer = StringField('customer', validators=[validators.DataRequired(), validators.Length(min=7, max=40)])
    phone_number = StringField('phone_number', validators=[validators.DataRequired(), validators.Length(min=10, max=11)])
    email = StringField('email', validators=[validators.DataRequired(), validators.Length(min=1, max=20)])
    description = StringField('description', validators=[validators.DataRequired(), validators.Length(min=1, max=35)])
    income = StringField('income', validators=[validators.DataRequired(), validators.Length(min=1, max=1000000)])
    status = StringField('status', validators=[validators.DataRequired(), validators.Length(min=1, max=12)])
