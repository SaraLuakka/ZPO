from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from app.auth import admin_required
from app.models import Category, db
from app.helpers import *
from sqlalchemy.exc import IntegrityError

category = Blueprint('category', __name__)

class CategoryForm(FlaskForm):
   category_name = StringField('Nazwa kategorii', validators=[DataRequired()])
   submit = SubmitField('Dodaj kategorię')

@category.route('/category_add', methods=['GET', 'POST'])
@login_required
@admin_required
def category_add():
    form = CategoryForm()

    if form.validate_on_submit():
        try:
            category = Category(category_name=form.category_name.data)
            db.session.add(category)
            db.session.commit()

            flash_bootstrap_success("Dodano kategorię")
            # return render_template('category_add.html', title='Add Category', form=form)
        except IntegrityError as e:
            db.session.rollback()
            flash_bootstrap_danger(e)
        except Exception as e:
            flash_bootstrap_danger(e)
        finally:
            return redirect(url_for('category.category_add'))

    return render_template('category_add.html', form=form)

@category.route('/category_list')
@login_required
@admin_required
def category_list():
   categories = Category.query.order_by(desc(Category.cid)).all()
   return render_template('category_list.html', categories=categories)