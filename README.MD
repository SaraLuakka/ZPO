# SEOP


### Instalacja
```
# Python 3.11
python -m pip install virtualenv
python -m venv venv
venv\Scripts\activate.bat
python -m pip install -r requirements.txt

```

### MySQL
```
'mysql+pymysql://system_ewidencji:to_jest_system_ewidencji@localhost/system_ewidencji?charset=utf8mb4'

Link do instalacji: https://downloads.mysql.com/archives/get/p/23/file/mysql-8.1.0-winx64.msi

Login: system_ewidencji
Haslo: to_jest_system_ewidencji
Host: localhost
DB: system_ewidencji

```

### Uruchamianie
```
cmd.exe
venv\Scripts\activate.bat
python run.py
(Pierwsze uruchomienie utworzy puste tabele w bazie danych)
(Utworz uzytkownika admin:admin, ale rola "admin" trzeba ustawić samodzielnie) 
W przegladarce: http://127.0.0.1:5000
```