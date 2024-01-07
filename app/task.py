from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sqlalchemy.orm import sessionmaker
from wtforms import StringField, TextAreaField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired
from sqlalchemy.exc import IntegrityError


from app import db
from app.auth import admin_required
from app.helpers import flash_bootstrap_danger, flash_bootstrap_success
from app.models import Task, Category, User

task = Blueprint('task', __name__)

class TaskForm(FlaskForm):
    #Fields
    title = StringField('Nazwa zadania', validators=[DataRequired()])
    description = TextAreaField('Opis zadania', validators=[DataRequired()])
    category = SelectField('Kategoria zadania', coerce=int, validators=[DataRequired()])
    user = SelectField('Przypisany użytkownik', coerce=int, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        # Query values
        self.category.choices = [(c.cid, c.category_name) for c in Category.query.all()]
        self.user.choices = [(u.uid, u.login) for u in User.query.all() if u.role != "admin"]

@task.route('/task_add', methods=['GET', 'POST'])
@login_required
@admin_required
def task_add():
    form = TaskForm()

    if form.validate_on_submit():

        try:
            task = Task(title=form.title.data, description=form.description.data, cid=form.category.data, uid=form.user.data)
            db.session.add(task)
            db.session.commit()

            flash_bootstrap_success("Dodano zadanie")
        except IntegrityError as e:
            db.session.rollback()
            flash_bootstrap_danger(e)
        except Exception as e:
            flash_bootstrap_danger(e)
        finally:
            return redirect(url_for('task.task_add'))

        return redirect(url_for('task_add'))
    return render_template('task_add.html', form=form)

@task.route('/task_list')
@login_required
def task_list():
    Session_db = sessionmaker(bind=db.engine)
    session = Session_db()

    tasks = session.query(Task.tid, Task.title, Task.description, User.login, Category.category_name).join(User, Task.uid == User.uid).join(Category, Task.cid == Category.cid)

    if current_user.role != 'admin':
        tasks = tasks.filter(User.uid == current_user.uid)

    tasks = tasks.order_by(User.uid).all()

    return render_template('task_list.html', tasks=tasks)


