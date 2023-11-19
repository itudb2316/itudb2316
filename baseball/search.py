from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    search = StringField(
        "search",
        [DataRequired(), Length(max=100)],
        render_kw={
            "class": "form-control",
            "placeholder": "Enter full name of the player",
        },
    )
    submit = SubmitField(
        "Search",
        render_kw={"class": "btn btn-outline-secondary"},
    )
