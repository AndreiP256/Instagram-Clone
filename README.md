### DESCRIERE APLICATIE "INSTAGRAM" - PRUSACOV ANDREI IONUT 313CD ###

# FRONTEND #
    - Frontend-ul se bazeaza pe templeate-uri Jinja2 + CSS + putin Bootstrap
    - In folderul de "templates" se fla cate o pagina penru fiecare parte majora a aplicatiei
    - Template-ul de baza ( numit "index" ) contine NavBar-ul si un footer simplist
    - Tot in folderul de frontedn se afla in "static" cateva imagini folosite pe site ce nu au legatura cu logica de stocare ( imaginea de la about, user icon )
    Paginile principale ale aplicatiei ( alaturi de rutele asociate sunt ):

        /about: Pagina statica ce contine o simpla descriere si o poza
        /error: Pagina pentru error404 not found
        /login: Pagina ce contine formularul pentru login
        /register: Pagina ce contine formularul de register
        /statistics: Pagina ce contine niste statistici ale aplcatie
        /profile: Pagina ce contine buton de logout + imaginile unui user cu optiune de delete
        /upload: Pagina cu formular de uppload pt poze
        /photos: Pagina cu toate pozele incarcate ( impartita pe categori )

    Particularitati de implementare:
        - in script.css s-a folosit un scrip ce creeaza un piechart pentru statistici
        - S-au folosit if-uri + caraterisiticile "current_user.is_authentificated" pentru a afisa dinamic anumite parti ale paginii ( Profile / upload )
        - S-au folosit formulare cu un <hidden> tag pentru trmiterea token-ului cfrs pentru securitate
        - S-a folosit un form cu categoriile pentru a returna din backend doar imaginile unei anumite categorii
        - S-au folosit array-uri de imagini si un for din jinja2 pentru afisarea imaginilor returnate pentru anumite categorii

# BCAKEND #
    Backend-ul ete impartit in 4 fisiere:
        1. forms.py: contine logica + validare formularelor de Login, Register, Logout si DeleteIamge
        2. models.py: contine modelele fiecarei entitati din baza de date: User si Image + relatia dintre ele
        3. views.py: Contine toate rutele si logica asociata acestora
        4. __init__.py: Contine logica ce initializeaza aplicatia

    Routele specifice backend ( excluzandu-le pe cele frontedn discutate deja )
        /images: ruta pentru upload-ul unei imagini
        /images/id: ruta pentru accesarea unei imagini specifice
        /images/id/delete: ruta pentru stergerea unei imagini
        /logout: delogheaza utilizatorul

    Rutele comune back-front:
        ( Toate rutele acestea au ca efect final render-template pentru paginile lor respective )
        / : ruta de baza care returneaza toate imaginile in functei de categorie 
        /login : Preia datele din formularul de pe front si incearca gasirea unui utlizator care sa se potriveasca cu acestea, in caz afirmativ in logheaza
        /register: Preia datele din formular, veririca exsitenta unui utiizator care coincide si in caz contrar il creeaza
        /upload: Preia imaginea numele si categoria din formualar si creeaza o imagine noua in baza de date apartinand utikiztorului curent logat
        /profile: Returneaza imaginile utilizatorilor curent
        /statistics: returneaza statisticile din backend pentru render

    Particularitati de implementare:
        - S-a folosit un LoginManager din flask pentru a vedea ce utilizator este logat, daca este logat si pentru a face validari de genu: imagine apartine user
        - S-a folosit werkzeug ( security ) pentru hash-uri de parole
        - S-a folosit token CSRF pentru a verifica autenticitatea request-urilor
    
    Init:
        - in init s-au initializat CSRF-ul, Login-manager-ul si baza de date cu SQLAlchemy
        - in functia de create app s-a intializat cheia secreta pentru tokens
        - in contextul aplicatiei s-a initializat utilizatorul curent folsoindu-se modelul pentru user

# DOCKER + DATABASE #
    In afara celor 2 foldere exista fisierele necesare rularii aplicatiei:
        - config: contine configurari similare cu __init__
        - createDB: scrip care creeaza baza de date daca aceasta nu exista deja
        - requirements: contine librariile de python necesare rularii
        - run: ruleaza efectiv aplicatia
        - DockerFile: se ocupa de docker
        - test.db: baza de date

    BAZA de DATE:
        - baza de date este una de tip sqlite3 ( baza de date relationala )
        - contine doar 2 tabele, una de user si una de imagini cu relatie one to many intre acestea

    DockerFile:
        - preia o imagine de pyhton
        - seteaza directorul de lucru ca fiind /app
        - adauga TOT continutul directorului actual in acesta
        - instaleaza dependentele necesare ( pip -install pe fisierul cu requirentments )
        - ruleaza createDB ( care va creea sau nu o baza de date in functiie de daca aceasta esista deja )
        - Deschide portul 5000
        - ruleaza run.py pentru a porti aplicatia

# LIBRARI FOLOSITE #
    1. Flask ( + flask_login, flask_wtf, flask_sqlalchemy)
    2. Sqlalchemy: pentru baza de date
    3. Werkzeug: penutr securitate
    4. WTForms: pentru trimiterea de date front-back prin formualre
    5. Jinja2: pneutr HTML-ul dinamic

# PROVOCARI INTAMPINATE #
    - Trimiterea tokenelor CSRF pentru securitate: s-a rezolvat cu <hidden> tag in forms
    - Login si Logout rute diferite sau comune: Eram obisnuit de la JavaScript + React sa am rute diferrite pentru logare front si logare backend, insa in aceasta implementare am reutis sa le pun in acelsai loc printr-un form
    - Configurarea aplicatiei ca sa initializeze baza de date / login-manager-ul: Am rezolvat incluzand initializarea si in config si in __init__ 

# RULARE #
    ( in the main folder of the app )
    docker build -t [name] .
    docker run [name]

# CONTURI #
    - Se pot creea conturi prin formularul de register
    - Cont default:
        email: test@gmail.com
        passw: Test123
