from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

    

class AddPostForm(FlaskForm):
    title = TextField('Title', [DataRequired(), Length(1, 40)])
    body = TextAreaField('Body', [DataRequired(), Length(1, 8192)])


