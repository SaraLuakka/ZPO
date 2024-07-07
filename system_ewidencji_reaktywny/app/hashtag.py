from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from app.auth import admin_required
from app.models import Hashtags, db
from app.helpers import *
from sqlalchemy.exc import IntegrityError

hashtag = Blueprint('hashtag', __name__)

class HashtagForm(FlaskForm):
   hashtag_name = StringField('#Hashtag', validators=[DataRequired()])
   submit = SubmitField('Dodaj hashtag')

@hashtag.route('/hashtag_add', methods=['GET', 'POST'])
@login_required
@admin_required
def hashtag_add():
    form = HashtagForm()

    if form.validate_on_submit():
        try:
            hashtag = Hashtags(hashtag_name=form.hashtag_name.data)
            db.session.add(hashtag)
            db.session.commit()

            flash_bootstrap_success("Dodano hashtag")
        except IntegrityError as e:
            db.session.rollback()
            flash_bootstrap_danger(e)
        except Exception as e:
            flash_bootstrap_danger(e)
        finally:
            return redirect(url_for('hashtag.hashtag_add'))

    return render_template('hashtag_add.html', form=form)

@hashtag.route('/hashtag_list')
@login_required
@admin_required
def hashtag_list():
   hashtags = Hashtags.query.order_by(desc(Hashtags.hid)).all()
   return render_template('hashtag_list.html', hashtags=hashtags)