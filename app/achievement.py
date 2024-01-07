from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy.orm import sessionmaker
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.fields.simple import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, Optional, NumberRange
from sqlalchemy.exc import IntegrityError

from app import db
from app.auth import admin_required
from app.models import Category, User, Hashtags, Achievement
from app.helpers import *

achievement = Blueprint('achievement', __name__)


class EndDateValidator(object):
    def __call__(self, form, field):
        if field.data < form.start_date.data:
            raise ValidationError("Data końcowa nie może być wcześniejsza niż początkowa.")


class AddAchievementForm(FlaskForm):
    title = StringField('Nazwa osiągnięcia', validators=[DataRequired(), Length(min=1, max=100)])
    description = StringField('Opis osiągnięcia', validators=[DataRequired(), Length(min=1, max=400)])
    start_date = DateField('Początek', validators=[DataRequired()])
    end_date = DateField('Koniec', validators=[DataRequired(), EndDateValidator()])
    category = SelectField('Kategoria', coerce=int)
    hashtag = SelectField('Hashtag', coerce=int)
    user = SelectField('Użytkownik', coerce=int)
    submit = SubmitField('Dodaj osiągnięcie')

    def __init__(self, *args, **kwargs):
        super(AddAchievementForm, self).__init__(*args, **kwargs)

        # Query values
        self.category.choices = [(c.cid, c.category_name) for c in Category.query.all()]
        self.hashtag.choices = [(h.hid, f"#{h.hashtag_name}") for h in Hashtags.query.all()]
        self.user.choices = [(u.uid, u.login) for u in User.query.all() if u.role != "admin"]

        # Conditionally apply the DataRequired validator
        if current_user.role == "admin":
            self.user.validators = [DataRequired()]
        else:
            self.user.validators = [Optional()]


@achievement.route('/achievement_add', methods=['GET', 'POST'])
def achievement_add():
    form = AddAchievementForm()
    if form.validate_on_submit():

        try:
            uid_form = form.user.data
            if current_user.role != "admin":
                uid_form = current_user.uid

            new_achievement = Achievement(
                title=form.title.data,
                description=form.description.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                rating=None,
                status=AchievementState.NEW.value,
                cid=form.category.data,
                hid=form.hashtag.data,
                uid=uid_form
            )
            db.session.add(new_achievement)
            db.session.commit()

            flash_bootstrap_success('Dodano osiągnięcie')
        except IntegrityError as e:
            db.session.rollback()
            flash_bootstrap_danger(e)
        except Exception as e:
            flash_bootstrap_danger(e)
        return redirect(url_for('achievement.achievement_add'))

    return render_template('achievement_add.html', form=form)


@achievement.route('/achievement_list')
@login_required
def achievement_list():
    Session_db = sessionmaker(bind=db.engine)
    session = Session_db()

    achievements = db.session.query(
        Achievement.aid,
        Achievement.title,
        Achievement.description,
        Achievement.start_date,
        Achievement.end_date,
        Achievement.rating,
        Achievement.status,
        Category.category_name,
        Hashtags.hashtag_name,
        User.login
    ).join(Category, Achievement.cid == Category.cid) \
        .join(Hashtags, Achievement.hid == Hashtags.hid) \
        .join(User, Achievement.uid == User.uid)

    if current_user.role != 'admin':
        achievements = achievements.filter(User.uid == current_user.uid)

    achievements = achievements.all()

    categories = Category.query.all()
    achievements_by_category = dict()

    for category in categories:
        if not category in achievements_by_category.keys():
            achievements_by_category[category.category_name] = list()

    for achievement in achievements:
        achievements_by_category[achievement.category_name].append(achievement)

    return render_template('achievement_list.html', achievements_by_category=achievements_by_category)


@achievement.route('/achievement_rate')
@login_required
@admin_required
def achievement_rate():
    Session_db = sessionmaker(bind=db.engine)
    session = Session_db()

    achievements = db.session.query(
        Achievement.aid,
        Achievement.title,
        Achievement.description,
        Achievement.start_date,
        Achievement.end_date,
        Achievement.rating,
        Achievement.status,
        Category.category_name,
        Hashtags.hashtag_name,
        User.login
    ).join(Category, Achievement.cid == Category.cid) \
        .join(Hashtags, Achievement.hid == Hashtags.hid) \
        .join(User, Achievement.uid == User.uid) \
        .filter(Achievement.status == 'NEW') \
        .all()

    return render_template('achievement_rate.html', achievements=achievements)


@achievement.route('/achievement_rate_helper/<int:aid>/<action>', methods=['GET'])
@login_required
@admin_required
def achievement_rate_helper(aid, action):
    try:
        achievement = Achievement.query.get(aid)
    except Exception as e:
        flash_bootstrap_danger("Nie odnaleziono osiągniecia o zadanym ID")
        return redirect(url_for('achievement.achievement_rate'))

    if achievement.status != AchievementState.NEW.value:
        flash_bootstrap_danger(f"Status początkowy jest rózny od: {AchievementState.NEW.value}")
        return redirect(url_for('achievement.achievement_rate'))

    if action == 'reject':
        achievement.status = AchievementState.REJECTED.value
        db.session.commit()
        flash_bootstrap_success("Pomyślnie odrzucono osiągnięcie")
    elif action == 'to_fix':
        achievement.status = AchievementState.TO_BE_FIXED.value
        db.session.commit()
        flash_bootstrap_success("Pomyślnie wysłano osiągnięcie do poprawy")
    else:
        flash_bootstrap_danger("Nie rozpoznano akcji")

    return redirect(url_for('achievement.achievement_rate'))


class AchievementRateSingleForm(FlaskForm):
    rating = FloatField("Rating (0.0 - 10.0)", validators=[NumberRange(min=0.0, max=10.0)])
    submit = SubmitField("Update Rating")


@achievement.route('/achievement_rate_single_form/<int:aid>', methods=['GET', 'POST'])
@login_required
@admin_required
def achievement_rate_single_form(aid):
    form = AchievementRateSingleForm()

    current_achieviement = Achievement.query.get(aid)

    if not current_achieviement:
        flash_bootstrap_danger("Nie odnaleziono osiągniecia o zadanym ID")
        return redirect(url_for('achievement.achievement_rate'))

    if current_achieviement.status != AchievementState.NEW.value:
        flash_bootstrap_danger("To nie jest osiągniecie w statusie nowy")
        return redirect(url_for('achievement.achievement_rate'))

    if form.validate_on_submit():
        try:
            current_achieviement.rating = form.rating.data
            current_achieviement.status = AchievementState.APPROVED.value
            db.session.commit()

            flash_bootstrap_success(f'Zatwierdzono pozytywnie osiągnięcie z ratingiem: {current_achieviement.rating}')
            return redirect(url_for('achievement.achievement_rate'))
        except IntegrityError as e:
            db.session.rollback()
            flash_bootstrap_danger(e)
        except Exception as e:
            flash_bootstrap_danger(e)

    return render_template('achievement_rate_single_form.html', achievement_fields=current_achieviement, form=form)


@achievement.route('/achievement_fix')
@login_required
def achievement_fix():
    Session_db = sessionmaker(bind=db.engine)
    session = Session_db()

    achievements = db.session.query(
        Achievement.aid,
        Achievement.title,
        Achievement.description,
        Achievement.start_date,
        Achievement.end_date,
        Achievement.rating,
        Achievement.status,
        Category.category_name,
        Hashtags.hashtag_name,
        User.login
    ).join(Category, Achievement.cid == Category.cid) \
        .join(Hashtags, Achievement.hid == Hashtags.hid) \
        .join(User, Achievement.uid == User.uid) \
        .filter(Achievement.status == 'TO_BE_FIXED') \
        .filter(User.uid == current_user.uid) \
        .all()

    return render_template('achievement_fix.html', achievements=achievements)


class AchievementFixSingleForm(FlaskForm):
    title = StringField('Nazwa osiągnięcia', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Opis osiągnięcia', validators=[DataRequired(), Length(min=1, max=400)])
    start_date = DateField('Początek', validators=[DataRequired()])
    end_date = DateField('Koniec', validators=[DataRequired(), EndDateValidator()])
    category = SelectField('Kategoria', coerce=int)
    hashtag = SelectField('Hashtag', coerce=int)
    submit = SubmitField('Popraw')

    def __init__(self, *args, obj=None, **kwargs):
        super(AchievementFixSingleForm, self).__init__(*args, **kwargs)

        # Query values
        self.category.choices = [(c.cid, c.category_name) for c in Category.query.all()]
        self.hashtag.choices = [(h.hid, f"#{h.hashtag_name}") for h in Hashtags.query.all()]

        if obj:
            self.title.data = obj.title
            self.description.data = obj.description
            self.start_date.data = obj.start_date
            self.end_date.data = obj.end_date
            self.category.data = obj.cid
            self.hashtag.data = obj.hid




@achievement.route('/achievement_fix_single_form/<int:aid>', methods=['GET', 'POST'])
@login_required
def achievement_fix_single_form(aid):

    current_achieviement = Achievement.query.get(aid)
    if not current_achieviement:
        flash_bootstrap_danger("Nie odnaleziono osiągniecia o zadanym ID")
        return redirect(url_for('achievement.achievement_fix'))

    if current_achieviement.status != AchievementState.TO_BE_FIXED.value:
        flash_bootstrap_danger("To nie jest osiągniecie w statusie do poprawy")
        return redirect(url_for('achievement.achievement_fix'))

    if current_achieviement.uid != current_user.uid:
        flash_bootstrap_danger("Nie możesz poprawiać cudzych osiągnięć")
        return redirect(url_for('achievement.achievement_fix'))

    if request.method == 'GET':
        form = AchievementFixSingleForm(obj=current_achieviement)
    else:
        form = AchievementFixSingleForm()

    if form.validate_on_submit():
        try:
            current_achieviement.title = form.title.data
            current_achieviement.description = form.description.data
            current_achieviement.start_date = form.start_date.data
            current_achieviement.end_date = form.end_date.data
            current_achieviement.cid = form.category.data
            current_achieviement.hid = form.hashtag.data

            # Reset
            current_achieviement.status = AchievementState.NEW.value
            current_achieviement.rating = None

            db.session.commit()

            flash_bootstrap_success(f'Pomyślnie zaktualizowano osiągnięcie')
            return redirect(url_for('achievement.achievement_fix'))
        except IntegrityError as e:
            db.session.rollback()
            flash_bootstrap_danger(e)
        except Exception as e:
            flash_bootstrap_danger(e)

    return render_template('achievement_fix_single_form.html', form=form, aid=aid)