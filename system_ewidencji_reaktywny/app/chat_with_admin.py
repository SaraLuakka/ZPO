import os
from dataclasses import dataclass
from datetime import datetime, timedelta

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request, jsonify
from rx.scheduler import ThreadPoolScheduler
from rx.subject import Subject, BehaviorSubject
from sqlalchemy import desc, func, text

from app.auth import admin_required
from app.models import User, ChatWithAdmin, ChatCategory
from app import db

# RxPY functions
@dataclass
class SingleAdminChatMessage:
    uid: int
    message: str
    topic_uid: int = None
    login: str = None
    entry_id: int = None
    commited_date: datetime = None

def update_latest_date_for_category_with_admin(sacm: SingleAdminChatMessage):
    global last_admin_dates

    # Admin won't see his own messages with notify
    if sacm.login == "admin":
        return

    # New dict
    last_admin_dates_new = last_admin_dates.value.copy()
    last_admin_dates_new[sacm.topic_uid] = sacm.commited_date

    # Set new value on BehaviorSubject
    last_admin_dates.on_next(last_admin_dates_new)

def one_time_fill_last_admin_date_of_chat_categories():
    global db
    output = {}

    # Step 1: Fetch all uid's
    all_topics = db.session.query(User).all()

    # Step 2: Check each category for messages and prepare the output
    for user in all_topics:
        if user.login == "admin":
            continue

        # Check if there are any messages for this category
        latest_admin_chat_date = db.session.query(func.max(ChatWithAdmin.date)).filter(ChatWithAdmin.topic_uid == user.uid).scalar()

        # Determine the date to use for this category
        if latest_admin_chat_date:
            # Keep the date as a datetime object
            date_obj = latest_admin_chat_date
        else:
            # Placeholder date for categories with no messages as a datetime object
            date_obj = datetime(1970, 1, 1)

        # Add the category and its date to the output
        output[user.uid] = date_obj

    return output

def update_in_memory_admin_chat_messages(sacm):
    global in_memory_admin_chat_messages
    global db

    if sacm.topic_uid not in in_memory_admin_chat_messages.keys():
        in_memory_admin_chat_messages[sacm.topic_uid] = list()

    in_memory_admin_chat_messages[sacm.topic_uid].append([sacm.login, sacm.message, sacm.entry_id, sacm.commited_date])

    # Review the list and remove messages later than 1 minute from , but only when adding new element to the list | msg[3] = commited_date
    filtered_messages = []
    one_minute_ago = datetime.now().utcnow() - timedelta(minutes=1)

    for msg in in_memory_admin_chat_messages[sacm.topic_uid]:
        if msg[3] >= one_minute_ago:
            filtered_messages.append(msg)

    in_memory_admin_chat_messages[sacm.topic_uid] = filtered_messages

def insert_new_admin_chat(sacm: SingleAdminChatMessage):
    global db

    try:
        # Database section
        new_chat = ChatWithAdmin(topic_uid=sacm.topic_uid, uid=sacm.uid, message=sacm.message)
        db.session.add(new_chat)
        db.session.commit()

        sacm.entry_id = new_chat.entry_id
        sacm.commited_date = new_chat.date

        # In memory section
        update_in_memory_admin_chat_messages(sacm)

        print("Dodano wpis chatu [admin]")
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        print(f"Błąd dodawania wpisu chatu [admin]: {e}")


in_memory_admin_chat_messages = dict()
incoming_messages_with_admin = Subject()
thread_scheduler = ThreadPoolScheduler(os.cpu_count())

last_admin_dates = None

incoming_messages_with_admin.subscribe(on_next=insert_new_admin_chat, scheduler=thread_scheduler)

# Flask functions
chat_with_admin = Blueprint('chat_with_admin', __name__)

@chat_with_admin.route('/chat_with_admin/channel/<topic_uid>')
@login_required
def chat_with_admin_channel(topic_uid):
    # global incoming_messages
    # global in_memory_chat_messages
    global db

    user_login = db.session.query(User).filter_by(uid=topic_uid).first()
    if user_login:
        user_login = user_login.login
    else:
        user_login = "<Critical error>"

    chats_query = db.session.query(
        ChatWithAdmin.message,
        User.login,
        ChatWithAdmin.entry_id
    ).join(
        User, ChatWithAdmin.uid == User.uid  # Assuming this is the correct relationship
    ).filter(
        ChatWithAdmin.topic_uid == topic_uid
    ).order_by(
        ChatWithAdmin.date.asc()
    )

    initial_messages = chats_query.all()

    return render_template('chat_with_admin_channel_show.html', topic_uid=topic_uid, user_login=user_login, initial_messages=initial_messages)

@chat_with_admin.route('/chat_with_admin/channel/<topic_uid>/new_message', methods=['POST'])
@login_required
def new_message(topic_uid):
    message = request.form.get('message')
    incoming_messages_with_admin.on_next(SingleAdminChatMessage(current_user.uid, message, topic_uid, current_user.login))
    return jsonify({"status": "OK", "message": "Your message was successfully submitted."})

@chat_with_admin.route('/chat_with_admin/channel/<topic_uid>/emit', methods=['GET', "POST"])
@login_required
def emit_admin_message(topic_uid):
    global in_memory_admin_chat_messages
    output_buffer = list()

    if topic_uid in in_memory_admin_chat_messages.keys():
        if len(in_memory_admin_chat_messages[topic_uid]) > 0:
            print(f"New admin messages emited to - {current_user.login}")
            output_buffer = in_memory_admin_chat_messages[topic_uid].copy()

    return jsonify(
        {"status": "OK",
         "new_messages": output_buffer}
    )

@chat_with_admin.route('/chat_with_admin/select_channel', methods=['GET', 'POST'])
@login_required
@admin_required
def select_channel():
    global last_admin_dates

    chats = (
        db.session.execute(text('SELECT u.uid, cwa.topic_uid, u.login, COUNT(topic_uid) AS "message_count" '
                                'FROM user u LEFT JOIN chat_with_admin  cwa ON cwa.topic_uid = u.uid WHERE u.login != "admin" GROUP BY u.uid'))
    )

    # First update of BehaviorSubject
    if last_admin_dates is None:
        last_admin_dates = BehaviorSubject(one_time_fill_last_admin_date_of_chat_categories())
        incoming_messages_with_admin.subscribe(on_next=lambda sacm: update_latest_date_for_category_with_admin(sacm))
        print("Initalize last_admin_dates as BehaviorSubject")

    return render_template('chat_with_admin_channels_selection.html', chats=chats, now_z_date=datetime.now().isoformat() + "Z")

@chat_with_admin.route('/chat_with_admin/channel/last_messages', methods=['GET', "POST"])
@login_required
@admin_required
def last_admin_messages():
    global db
    global last_admin_dates
    output = {}

    if not last_admin_dates is None:
        for ccid, dat in last_admin_dates.value.items():
            output[str(ccid)] = dat.isoformat() + "Z"


    return jsonify(
        {"status": "OK",
         "last_messages": output}
    )