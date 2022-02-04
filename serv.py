from flask import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import DATA

import json

import smtplib  # Импортируем библиотеку по работе с SMTP

# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML

# from email.mime.image import MIMEImage  # Изображения

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///glow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

myip = "http://127.0.0.1:5000"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=False)
    is_teacher = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(800), nullable=False)

    def __repr__(self):
        return f"<users {self.id}>"


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    author_id = db.Column(db.String(300))
    is_public = db.Column(db.Boolean)

    def __repr__(self):
        return f"<course {self.id}>"


class Moduls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer)
    number = db.Column(db.Integer)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"<module {self.id}>"


class Blocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer)
    number = db.Column(db.Integer)
    type = db.Column(db.String(50))
    text = db.Column(db.Text)
    condition = db.Column(db.Text)
    answer_type = db.Column(db.String(50))
    one_answer = db.Column(db.Boolean)
    answers = db.Column(db.String(1000))
    example_in = db.Column(db.String(250))
    example_out = db.Column(db.String(250))

    def __repr__(self):
        return f"<block {self.id}>"


class User2Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)


def testemail(email, tok):
    addr_from = "noreply@exillite.xyz"  # Адресат
    addr_to = email  # Получатель
    password = DATA.EMAIL_PASSWORD  # Пароль (я знаю, что это хардкод)
    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = addr_from  # Адресат
    msg['To'] = addr_to  # Получатель
    msg['Subject'] = 'Тема сообщения'  # Тема сообщения

    html = """
<html>
<head>
<style type="text/css">
body{
background: #C4DFE6;
}
   .a {
    width: 690px;
    border-radius: 5px;
    background: #66A5AD;
    box-shadow: 0 0 20px 9px #07575B; 
margin-left: auto;
    margin-right: auto;
   }
   .btn{
position: relative;
left: 50%;
transform: translate(-50%, 0);
height: 80px;
font-size:18px;
    width: 200px;
border-radius: 5px;
background-color: #C4DFE6;

   }
  </style>
</head>
  <body>
    <div class="a">
       <font size="5" color="black" face="sans-serif">Спасибо за регистрацию на образовательной системе <b>Glow</b>.<br>
Чтобы проолжить регистрацию нажмите на ссылку ниже.
</font>
    </div>
<br>
<a class="btn" href=""" + f"{myip}/con/{tok}" + """>Потвердить e-mail</a>
  </body>
</html>
"""
    msg.attach(MIMEText(html, 'html', 'utf-8'))  # Добавляем в сообщение HTML-фрагмент

    server = smtplib.SMTP('mail.exillite.xyz', 587)  # Создаем объект SMTP
    server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
    server.starttls()  # Начинаем шифрованный обмен по TLS
    server.login(addr_from, password)  # Получаем доступ
    server.send_message(msg)  # Отправляем сообщение
    server.quit()


@app.errorhandler(404)
def error_page(error):
    return render_template('404.html', nb=True)


@app.route("/login")
def login():
    return render_template('login.html', title='Log In')


@app.route("/alreg")
def alreg():
    return render_template('alreg.html')


@app.route("/al")
def alert():
    return render_template('testcoockies.html', nb=True, is_logined=True)


@app.route("/con/<tok>")
def con(tok):
    f = Users.query.filter_by(token=tok).first()
    f.is_active = True
    db.session.commit()
    return render_template('alreg.html', emconf=True)


@app.route("/cr")
def cr():
    db.create_all()
    return 'OK'


@app.route("/courses")
def courses():
    return render_template('courses.html', nb=True)

@app.route("/course/<id>")
def course(id):
    return render_template('course.html', nb=True)


@app.route('/api', methods=['GET', 'POST'])
def api():
    j = request.json

    if j['method'] == 'reg':
        try:
            if len(Users.query.filter_by(email=j['email']).all()) != 0:
                return 'ALR'
            pshash = generate_password_hash(j['password'])
            token = generate_password_hash(j['email'])
            u = Users(is_active=False, name=j['name'], surname=j['surname'], email=j['email'], password=pshash,
                      token=token)
            db.session.add(u)
            db.session.flush()
            db.session.commit()
            testemail(j['email'], token)
            return 'OK'
        except Exception as e:
            print('!!>>>>' + str(e))
            db.session.rollback()
            return 'ERROR'

    elif j['method'] == 'login':
        try:
            if len(Users.query.filter_by(email=j['email']).all()) == 0:
                return 'NO'
            u = Users.query.filter_by(email=j['email']).first()

            if check_password_hash(u.password, j['password']):
                if j['is_active']:
                    if j['stay']:
                        pass
                    return 'id=' + u.token
                else:
                    return 'NOTACTIVE'
            else:
                return 'PAS'


        except Exception as e:
            print('!!>>>>' + str(e))
            db.session.rollback()
            return 'ERROR'


    elif j['method'] == 'get_courses':
        r = {}
        try:
            student_id = Users.query.filter_by(token=j['token']).first().id
            r['token'] = j['token']
            courses_ids = User2Course.query.filter_by(user_id=student_id).all()
            crs = []
            for i in courses_ids:
                c = Courses.query.filter_by(id=i.id).first()
                dic = {'id': c.id, 'name': c.name, 'description': c.description, 'author_id': c.author_id}
                crs.append(dic)
            r['count'] = len(crs)
            r['courses'] = crs
            r['status'] = 'OK'

        except Exception as e:
            print('!!>>>>' + str(e))
            db.session.rollback()
            r['status'] = 'ERROR'

        return json.dumps(r)

    elif j['method'] == 'get_modules':
        r = {}
        try:
            mdls = Moduls.query.filter_by(course_id=j['course_id']).all()
            md = []

            for m in mdls:
                dic = {'id': m.id, 'number': m.number, 'name': m.name}
                md.append(dic)

            r['count'] = len(md)
            r['maduls'] = md
            r['status'] = 'OK'

        except Exception as e:
            print('!!>>>>' + str(e))
            db.session.rollback()
            r['status'] = 'ERROR'

        return json.dumps(r)

    elif j['method'] == 'get_blocks':
        r = {}
        try:
            blocks = Blocks.query.filter_by(module_id=j['module_id']).all()
            bl = []

            for b in blocks:
                dic = {'id': b.id, 'number': b.number, 'type': b.type}

                if b.type == 'tutorial':
                    dic['text'] = b.text
                elif b.type == 'task':
                    dic['condition'] = b.condition
                    dic['answer_type'] = b.answer_type
                elif b.type == 'task_with_answers':
                    dic['condition'] = b.condition
                    dic['one_answer'] = b.one_answer
                    dic['answers'] = b.answers
                elif b.type == 'code_task':
                    dic['condition'] = b.condition
                    dic['example_in'] = b.example_in
                    dic['example_out'] = b.example_out

                bl.append(dic)

            r['count'] = len(bl)
            r['blocks'] = bl

            r['status'] = 'OK'

        except Exception as e:
            print('!!>>>>' + str(e))
            db.session.rollback()
            r['status'] = 'ERROR'

        return json.dumps(r)


    elif j['method'] == 'get_my_courses':
        r = {}
        try:
            student_id = Users.query.filter_by(token=j['token']).first().id
            r['token'] = j['token']
            courses_ids = User2Course.query.filter_by(author_id=student_id).all()
            crs = []
            for i in courses_ids:
                c = Courses.query.filter_by(id=i.id).first()
                dic = {'id': c.id, 'name': c.name, 'description': c.description, 'author_id': c.author_id}
                crs.append(dic)
            r['count'] = len(crs)
            r['courses'] = crs
            r['status'] = 'OK'

        except Exception as e:
            print('!!>>>>' + str(e))
            db.session.rollback()
            r['status'] = 'ERROR'

        return json.dumps(r)

    elif j['method'] == 'add_course':
        r = {}
        try:
            a_id = Users.query.filter_by(token=j['token']).first().id
            с = Courses(name=j['name'], description=j['description'], author_id=a_id, is_public=j['is_public'])

            r['status'] = 'OK'

        except Exception as e:
            print('!!>>>>' + str(e))
            db.session.rollback()
            r['status'] = 'ERROR'

        return json.dumps(r)


app.run(debug=True)
