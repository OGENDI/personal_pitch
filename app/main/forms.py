from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import RadioField,StringField,SubmitField, TextAreaField
from wtforms.validators import InputRequired


class Pitch(FlaskForm):
    pitch_title = StringField('Pitch Title', validators=[InputRequired()])
    pitch_descrip = TextAreaField('Your pitch goes here ', validators=[InputRequired()])
    pitch_category = RadioField('Label', choices=[ 
                                                  ('Business','Business'),
                                                  ('Finance','Finance'),
                                                  ('Coding','Coding'),
                                                  ('Love','Love'),
                                                  ('Life','Life')
                                                  ],
                                validators=[InputRequired()])
    submit = SubmitField('Submit')
    
class Comment(FlaskForm):
    Comment_decrip =TextAreaField("Comment", validators=[InputRequired()])
    submit = SubmitField('Submit Comment')
    
class Upvote(FlaskForm):
    submit =SubmitField()

class Downvote(FlaskForm):
    submit =SubmitField()

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [InputRequired()])
    submit = SubmitField('Submit')