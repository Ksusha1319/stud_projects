# forms.py

from wtforms import Form, StringField, SelectField, validators, PasswordField, BooleanField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from models import User

class SearchForm(Form):
    choices = [('Все репорты'),
                ('Nickname'),
                ('ServiceLogin'),
               ('Game'),
               ('Incident type')]
    select = SelectField('', choices=choices)
    search = StringField('')


class ReportForm(Form):
    game_types = [(''),
                ('Lineage 2 ru'),
                ('Lineage 2 eu'),
                ('Lineage 2 Essence ru'),
                ('Lineage 2 Essence eu'),
                ('Lineage 2 Classic'),
                ('Ragnorok ru'),
                ('Ragnarok eu'),
                ('Ragnarok Prime'),
                ('Point Blank'),
                ('RF Online RU'),
                ('RF Online EU'),
                ('RF Online BR'),
                ('RF Online Latin America'),
                ('Aion'),
                ('R2'),
                ('BnS'),
                ('Crowfall')
                ]
    priority_types = [('Третий'),
                   ('Второй'),
                   ('Первый')
                   ]
    incident_types = [(''),
                   ('Бот'),
                   ('Стороннее ПО'),
                   ('Модификация клиента'),
                   ('Качер'),
                   ('Скупка предметов с помощью ПО'),
                   ('Нечестная автоматизация (макросы/автоюз)'),
                   ('Многооконка'),
                   ('Репорт'),
                   ('Спам'),
                   ('Другое (описание в комментариях)')
                   ]
    status_types = [('NEW'),
                    ('Проверяется'),
                    ('Готово'),
                    ('Нужна доп.проверка')]
    resolution_types = [('По результатам экспертизы'),
                    ('Временный бан'),
                    ('Нарушений нет'),
                    ('Бан без права восстановления')]
    nickname = StringField('Nickname', validators=[DataRequired()])
    service_login = StringField('ServiceLogin', validators=[DataRequired()])
    comment = StringField('Comment')
    incident_date = StringField('Incident Date')
    game_type = SelectField('Game', choices=game_types, validators=[DataRequired()])
    priority = SelectField('Приоритет', choices=priority_types)
    incident_type = SelectField('Incident type', choices=incident_types, validators=[DataRequired()])
    status = SelectField('Status', choices=status_types)
    resolution = SelectField('Resolution', choices=resolution_types)
    comment_soc = StringField('SOC Comment')
    ticket = StringField('Номер тикета')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),  Length(min=5)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, message='Password should be at least %(min)d characters long')])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired()]), EqualTo('password')
    submit = SubmitField('reg')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    remember_me = BooleanField ('remember_me')
    submit = SubmitField('Submit')
