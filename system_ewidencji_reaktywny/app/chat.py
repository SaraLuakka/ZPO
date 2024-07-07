import os
from dataclasses import dataclass
from datetime import datetime, timedelta

from flask import Blueprint, render_template, redirect, url_for
from flask import request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm

from rx.subject import Subject, BehaviorSubject
# Reactive Extensions for Python
# subject - mostu, zapisuje na nowe dane, jak i emisję własnych danych; źródłem informacji, jak i ich odbiorcami.
# behavior - otrzymywali aktualne dane, bez konieczności czekania na kolejne emitowane wartości
from rx import operators as ops
#ops - przekształcanie strumieni danych
from rx.scheduler import ThreadPoolScheduler
#asynchroniczne wykonywanie operacji w oddzielnym wątk
from sqlalchemy import desc, func
from sqlalchemy.exc import IntegrityError
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired

from app import db
from app.auth import admin_required
from app.helpers import flash_bootstrap_success, flash_bootstrap_danger
from app.models import ChatCategory, Chat, User


@dataclass
class SingleChatMessage:
    # wiadomość z czata
    chat_category_name: str
    uid: int
    message: str
    ccid: int = None #  identyfikator grupy czatu
    login: str = None #  identyfikator logowania użytkownika
    entry_id: int = None #  identyfikator wpisu
    commited_date: datetime = None


def update_in_memory_chat_messages(scm):
    #koperty i daty do nich
    global in_memory_chat_messages
    global db

    if scm.chat_category_name not in in_memory_chat_messages.keys():
        in_memory_chat_messages[scm.chat_category_name] = list()
        # dla podanej nazwy kategorii czatu (scm.chat_category_name) nie istnieje jeszcze żadna lista komunikatów.
        # jeśli nie, tworzy nową pustą listę dla tej kategorii.

    in_memory_chat_messages[scm.chat_category_name].append([scm.login, scm.message, scm.entry_id, scm.commited_date])
    # dodaje nowy komunikat do listy komunikatów dla konkretnej kategorii czatu.
    # komunikat obejmują login użytkownika, treść komunikatu, identyfikator wpisu oraz datę i godzinę zatwierdzenia


    filtered_messages = []
    one_minute_ago = datetime.now().utcnow() - timedelta(minutes=1)
    # filtrowanie komunikatów starszych niż minutę


    for msg in in_memory_chat_messages[scm.chat_category_name]:
        if msg[3] >= one_minute_ago:
            filtered_messages.append(msg)
    # młodsze niż minuta i je doklejamy
    # przechodzi przez wszystkie komunikaty w liście dla konkretnej kategorii czatu i dodaje te,
    # które zostały zatwierdzone w ciągu ostatniej minuty, do listy filtered_messages.

    in_memory_chat_messages[scm.chat_category_name] = filtered_messages
    #dopisujemy do in memory chat... do tej kat młodsze niż minutę
    # aktualizuje listę komunikatów dla konkretnej kategorii czatu, zastępując oryginalną listę nową listą filtered_messages,
    # która zawiera tylko komunikaty z ostatniej minuty

def insert_new_chat(scm: SingleChatMessage):
    # dodawania nowych komunikatów czatu do bazy danych i do listy komunikatów czatu przechowywanych w pamięci
    global db

    try:
        # Database section
        new_chat = Chat(ccid=scm.ccid, uid=scm.uid, message=scm.message) #tworzony jest nowy obiekt new_chat klasy Chat, który jest inicjalizowany wartościami przekazanymi z scm
        db.session.add(new_chat)# obiekt ten jest dodawany do sesji db.session i zatwierdzany przez commit
        db.session.commit()

        scm.entry_id = new_chat.entry_id
        scm.commited_date = new_chat.date
        # te pola są dodwane do scm z bazy
        # aktualizowane są wartości entry_id i commited_date w obiekcie scm, który reprezentuje nowy komunikat czatu.

        # In memory section
        update_in_memory_chat_messages(scm)
        #wywołuje funkcję update_in_memory_chat_messages i  przekazując do niej aktualizowany obiekt scm.
        # Dodanie nowego komunikatu do listy komunikatów czatu przechowywanych w pamięci
        # oraz za usunięcie komunikatów, które zostały zatwierdzone więcej niż minutę temu.

        print("Dodano wpis chatu")
    except Exception as e:
        # Rollback the transaction in case of error
        db.session.rollback()
        print(f"Błąd dodawania wpisu chatu: {e}")
        # jeśli wystąpi błąd, transakcja jest cofana (rollback), co oznacza,
        # że wszelkie zmiany dokonane w bazie danych w ramach tej transakcji są anulowane


def determine_chat_category_name_name(scm: SingleChatMessage):
    #przeznaczona do ustalania identyfikatora grupy czatu
    #ustalenia identyfikatora grupy czatu dla danego komunikatu czatu na podstawie jego nazwy kategorii czatu.
    #Jeśli taka kategoria istnieje w bazie danych, jej identyfikator jest przypisywany do komunikatu;
    # w przeciwnym razie funkcja zgłasza błąd.
    global db
    category_instance = db.session.query(ChatCategory).filter_by(chat_category_name=scm.chat_category_name).first()
    # zapytanie do bazy danych, aby znaleźć pierwszy (lub żaden) obiekt ChatCategory,
    # który ma tę samą nazwę kategorii czatu (chat_category_name) co przekazany komunikat czatu (scm).
    # Metoda filter_by jest używana do ograniczenia wyników zapytania do tych,
    # które pasują do określonego kryterium
    # first() zwraca pierwszy wynik z tej listy.

    if category_instance:
        scm.ccid = category_instance.ccid
    else:
        raise ValueError(f"No category found with name: {scm.chat_category_name}")

    # znaleziono kategorię czatu o podanej nazwie, to identyfikator grupy czatu (ccid) z tej kategorii jest przypisywany
    # do komunikatu czatu (scm).

    return scm
    # zwraca zmodyfikowany obiekt scm, który teraz zawiera przypisany identyfikator grupy czatu (ccid).
    # scm +1 pole


def convert_uid_to_login(scm: SingleChatMessage):
    #przyjmuje obiekt SingleChatMessage jako argument i próbuje znaleźć użytkownika w bazie danych (db)
    # na podstawie unikalnego identyfikatora użytkownika (uid).
    global db

    user = db.session.query(User).get(scm.uid)
    if user:
        scm.login = user.login
    return scm
    #użytkownik zostanie znaleziony, funkcja przypisuje jego login do pola login w obiekcie scm.
    # Na koniec funkcja zwraca zmodyfikowany obiekt scm.

in_memory_chat_messages = dict() #przechowujący komunikaty czatu w pamięci
incoming_messages = Subject()
thread_scheduler = ThreadPoolScheduler(os.cpu_count())

incoming_messages.pipe(
    #pipe to metoda, która przekierowuje dane z incoming_messages przez serię operacji przetwarzania
    ops.map(lambda scm: determine_chat_category_name_name(scm)),
    #przetwarza każdy komunikat czatu, ustalając jego identyfikator grupy czatu (ccid)
    ops.map(lambda scm: convert_uid_to_login(scm)),
    #przetwarza każdy komunikat czatu, przekształcając unikalny identyfikator użytkownika (uid) na login (login).
).subscribe(on_next=insert_new_chat, scheduler=thread_scheduler)
# subskrybuje przepływ danych, wywołując funkcję insert_new_chat dla każdego komunikatu po przetworzeniu go
# przez operacje mapowania.
# dodanie przetworzonych komunikatów do bazy danych

# definiuje proces przetwarzania nowych komunikatów czatu, który obejmuje ustalenie identyfikatora grupy czatu,
# przekształcenie unikalnego identyfikatora użytkownika na login, a następnie dodanie komunikatu do bazy danych

# RXPy function
def one_time_fill_last_date_of_chat_categories():
    #bierze daty z bazy danych z każdej kategorii,
    #te daty są do koperty
    #

    global db
    output = {} #pusty słownik output, który będzie używany do przechowywania wyników


    all_categories = db.session.query(ChatCategory).all()
    #funkcja pyta baze danych o wszystkie kategorie czatu



    for category in all_categories:
        #iteruje przez każdą kategorię w all_categories

        latest_chat_date = db.session.query(func.max(Chat.date)).filter(Chat.ccid == ChatCategory.ccid).scalar()
        #funkcja wykonuje kolejne zapytanie do bazy danych, aby znaleźć najnowszą datę wiadomości (latest_chat_date)
        #w tej kategorii; Robi to, porównując daty wszystkich wiadomości w kategorii i wybierając najnowszą.

        #func.max(Chat.date) to funkcja, która zwraca najnowszą datę (date) z tabeli Chat.
        #filter(Chat.ccid == ChatCategory.ccid) - ogranicza wyniki zapytania tylko do wiadomości należących do aktualnie przetwarzanej kategorie
        #scalar() zwraca pierwszy wynik zapytania; jest  to z najnowszą datą wiadomości.

        # Decyzja, jaką datę użyć
        if latest_chat_date:

            date_obj = latest_chat_date
        # jeśli latest_chat_date jest znana (tzn. w kategorii są wiadomości), to ta data jest używana bez zmian.
        else:
            date_obj = datetime(1970, 1, 1)
            # jeśli latest_chat_date nie jest znana (tzn. w kategorii nie ma wiadomości), to jako domyślną datę używana
            # jest data 1 stycznia 1970 roku

        output[category.ccid] = date_obj
        # dla każdej kategorie dodawana jest najnowsza data wiadomości
        # do słownika output, gdzie kluczem jest identyfikator kategorie (category.ccid), a wartością jest data (date_obj).

    return output
    #funkcja zwraca słownik output, który zawiera najnowsze daty wiadomości dla wszystkich kategorii czatu


def update_latest_date_for_category(scm: SingleChatMessage):
    #funkcję aktualizującą najnowszą datę dla konkretnej kategorii czatu oraz inicjalizację i konfigurację modułu czatu
    last_dates_new = last_dates.value.copy()
    #last_dates jest obiektem BehaviorSubject,
    #last_dates.value.copy() tworzy kopię bieżącego stanu last_dates, który jest słownikiem przechowującym najnowsze daty
    # dla różnych kategorii czatu.
    last_dates_new[scm.ccid] = scm.commited_date
    #aktualizuje najnowszą datę dla kategorii czatu, do której należy komunikat (scm.ccid), na datę,
    # kiedy komunikat został zatwierdzony (scm.commited_date)


    last_dates.on_next(last_dates_new)
    #aktualizuje stan last_dates, emitując nowy słownik z aktualizowaną datą.

# Initalized on first entry to @chat.route('/chat/select_channel', methods=['GET', 'POST'])
last_dates = None

# last_dates jest zmienną, która początkowo jest ustawiona na None.
# Ma ona służyć jako miejsce przechowywania najnowszych dat dla kategorii czatu.
# W momencie, gdy pierwszy komunikat czatu jest przetwarzany, last_dates zostanie zainicjalizowane
# jako obiekt BehaviorSubject.


# Flask functions
chat = Blueprint('chat', __name__)


@chat.route('/chat/select_channel', methods=['GET', 'POST']) #definuje drogę do url dla blueprint
@login_required #zapewnia, że dostęp do trasy jest możliwy tylko po zalogowaniu się
def select_channel():
    #pozwala użytkownikowi wybrać kategorię czatu, do której chce się przyłączyć
    global last_dates # używana do przechowywania najnowszych dat dla kategorii czatu
    chats = ChatCategory.query.order_by(desc(ChatCategory.ccid)).all()
    # pobiera wszystkie kategorie czatu z bazy danych, sortując je w porządku malejącym według ich identyfikatorów (ccid)


    if last_dates is None:
        #czy last_dates jest None (co oznacza, że nie zostało jeszcze zainicjalizowane)

#Na początek sprawdzamy, czy last_dates już istnieje i jest gotowe do użycia. Jeśli nie, to robimy coś, co go uruchamia.
#Jeśli last_dates nie było jeszcze gotowe, to teraz go uruchamiamy. Robimy to, używając funkcji one_time_fill_last_date_of_chat_categories(), która sprawdza, jakie są najnowsze daty wiadomości w każdej kategorii czatu, i wypełnia last_dates tymi datami.
# Teraz, kiedy last_dates jest gotowe, zaczynamy śledzić nowe wiadomości, które przychodzą. Każdorazowo, gdy dostaniemy nową wiadomość, automatycznie aktualizujemy najnowszą datę dla odpowiedniej kategorii czatu, używając funkcji update_latest_date_for_category(scm).
#Na końcu, pokazujemy użytkownikowi listę kategorii czatu, które są dostępne.


        last_dates = BehaviorSubject(one_time_fill_last_date_of_chat_categories())

        incoming_messages.subscribe(on_next=lambda scm: update_latest_date_for_category(scm))
        print("Initalize last_dates as BehaviorSubject")

    return render_template('chat_channels_selection.html', chats=chats)

#tworzy stronę, która pozwala użytkownikom na wybór kategorie czatu, do której chcą się przyłączyć.
# Używa globalnej zmiennej last_dates do śledzenia najnowszych dat dla kategorii czatu oraz
# subskrypcji nowych komunikatów czatu, aby aktualizować te daty w czasie rzeczywistym.

@chat.route('/chat/channel/<chat_category_name>') #parametr trasy, który będzie dynamicznie pasował do nazwy kategorii czatu, którą użytkownik chce zobaczyć
@login_required
def chat_channel(chat_category_name):
    # czat dla wybranej kategorii
    global incoming_messages
    global in_memory_chat_messages
    global db
    #przechowywania nowych wiadomości czatu, historii wiadomości w pamięci podręcznej i sesji bazy danych

    ccid = -1

    category_instance = db.session.query(ChatCategory).filter_by(chat_category_name=chat_category_name).first()
    if category_instance:
        ccid = category_instance.ccid

        # Sprawdza, czy istnieje kategoria czatu o podanej nazwie (chat_category_name).
        # Jeśli tak, to pobiera jej identyfikator (ccid).



    chats_query = db.session.query(Chat.message, User.login, Chat.entry_id).join(
        ChatCategory, Chat.ccid == ChatCategory.ccid
    ).join(
        User, Chat.uid == User.uid
    ).filter(
        ChatCategory.chat_category_name == chat_category_name
    ).order_by(
        Chat.date.asc()
    )
    #zapytanie do bazy danych, aby pobrać wszystkie wiadomości (message), loginy użytkowników (User.login)
    # i identyfikatory wprowadzeń (entry_id) dla konkretnej kategorii czatu.
    # Zapytanie to łączy tabele Chat, ChatCategory i User na podstawie wspólnych kluczy,
    # filtruje wyniki według nazwy kategorii czatu i sortuje je według daty w porządku rosnącym.

    initial_messages = chats_query.all()

    return render_template('chat_channel_show.html', chat_category_name=chat_category_name, initial_messages=initial_messages)
    #zwraca rendered szablon HTML chat_channel_show.html, przekazując mu nazwę kategorii czatu i listę początkowych wiadomości

@chat.route('/chat/channel/<chat_category_name>/new_message', methods=['POST'])
@login_required
#wysyłanie nowych wiadomości do konkretnej kategorii czatu.
def new_message(chat_category_name):
    message = request.form.get('message')
    incoming_messages.on_next(SingleChatMessage(chat_category_name, current_user.uid, message))
    # dodaje nową wiadomość do kolekcji
    return jsonify({"status": "OK", "message": "Your message was successfully submitted."})


@chat.route('/chat/channel/<chat_category_name>/emit', methods=['GET', "POST"])
@login_required
def emit_message(chat_category_name):
    # emitowanie nowych wiadomości do użytkowników, czy jest coś nowego
    global in_memory_chat_messages
    output_buffer = list()

    if chat_category_name in in_memory_chat_messages.keys():
        if len(in_memory_chat_messages[chat_category_name]) > 0:
            print(f"New messages emited to - {current_user.login}")
            output_buffer = in_memory_chat_messages[chat_category_name].copy()
    # Sprawdzamy, czy dla danej kategorii czatu mamy jakieś wiadomości w in_memory_chat_messages.
    # Jeśli tak, to kopiuje je do output_buffer.

    return jsonify(
        {"status": "OK",
         "new_messages": output_buffer}
    )


@chat.route('/chat/channel/last_messages', methods=['GET', "POST"]) #pobranie najnowszych dat wiadomości dla wszystkich kategorii czatu
@login_required
def last_messages():
    # do kopert
    global db
    output = {}

    if not last_dates is None:
        for ccid, dat in last_dates.value.items():
            output[ccid] = dat.isoformat() + "Z"
    # Sprawdzamy, czy last_dates nie jest None (co oznacza, że zostało zainicjalizowane).
    # Jeśli tak, to iterujemy przez wszystkie kategorie czatu i pobieramy ich najnowsze daty,
    # przekształcając je na format ISO i dodając "Z" na końcu (oznacza to, że daty są w strefie czasowej UTC).

    return jsonify(
        {"status": "OK",
         "last_messages": output}
    )

class ChatCategoryForm(FlaskForm):
   chat_category_name = StringField('Nazwa kanału tematycznego', validators=[DataRequired()])
   submit = SubmitField('Dodaj kanał tematyczny')
# Służy do walidacji danych wejściowych użytkownika przed ich zapisaniem w bazie danych.
# Walidator DataRequired() zapewnia, że pole to musi być wypełnione.
# submit to przycisk "Dodaj kanał tematyczny", który po naciśnięciu wywoła walidację formularza.

@chat.route('/chat_category_add', methods=['GET', 'POST'])
@login_required
@admin_required
# pozwala administratorowi na dodanie nowej kategorii czatu. GET - do wyświetlenia formularza, POST - do przesłania danych formularza
#form = ChatCategoryForm() tworzy instancję formularza ChatCategoryForm
#Jeśli formularz jest poprawnie wypełniony i przesłany, próbujemy utworzyć nową kategorię czatu z nazwą z formularza,
# dodać ją do sesji bazy danych i zatwierdzić transakcję.
# niezależnie od wyniku, użytkownika przekierowujemy z powrotem do strony dodawania kategorii czatu.
def chat_category_add():
    form = ChatCategoryForm()

    if form.validate_on_submit():
        try:
            chat_category = ChatCategory(chat_category_name=form.chat_category_name.data)
            db.session.add(chat_category)
            db.session.commit()

            flash_bootstrap_success("Dodano kanał tematyczny")
        except IntegrityError as e:
            db.session.rollback()
            flash_bootstrap_danger(e)
        except Exception as e:
            flash_bootstrap_danger(e)
        finally:
            return redirect(url_for('chat.chat_category_add'))

    return render_template('chat_category_add.html', form=form)