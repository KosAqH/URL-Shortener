from flask_wtf import FlaskForm
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, URL

class URLForm(FlaskForm):
    url = StringField('URL', validators=[DataRequired(), URL(False)])
