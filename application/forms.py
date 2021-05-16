from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, FloatField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Length, InputRequired, Email, DataRequired, NumberRange, optional
from datetime import datetime, timedelta


class MyForm(FlaskForm):
    name = StringField('Name : ',  validators=[DataRequired()])
    submit = SubmitField("Start")


class AnalyzerForm(FlaskForm):
    stock = SelectField(
        "Stocks ", choices=[],  validators=[InputRequired(message="Please Select a stock")])
    startDate = DateField(
        "Start Date (within a 7-day frame from today)", default=datetime.today, validators=[InputRequired("start Date is required Field")])
    endDate = DateField(
        "End Date (between start date and today)", default=datetime.today, validators=[InputRequired("start Date is required Field")])
    analyze_button = SubmitField("Analyze")
