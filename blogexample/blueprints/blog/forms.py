from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
# from flask_ckeditor import CKEditorField
    

class AddPostForm(FlaskForm):
    title = TextField('Title', [DataRequired(), Length(1, 40)])
    body = TextAreaField('Body', [DataRequired(), Length(1, 8192)])
    tags = TextField('tags', [DataRequired(), Length(3, 100)])
    visible = BooleanField('Published')
    # body = CKEditorField('Body', [DataRequired(), Length(1, 8192)])


