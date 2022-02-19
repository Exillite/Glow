from calendar import c
from lib2to3.pgen2 import token
from re import T
import os
from turtle import title
from flask import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import DATA
import sqlite3
import question
import random

import json

import smtplib  # Импортируем библиотеку по работе с SMTP

# Добавляем необходимые подклассы - MIME-типы
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект
from email.mime.text import MIMEText  # Текст/HTML

# from email.mime.image import MIMEImage  # Изображения
#HVoW%kA%3q*y
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///glow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['UPLOAD_FOLDER'] = 'C:\\Users\\Alexander\\Desktop\\low\\static\\img'

quests2st = []
quests2st.append(question.Qeston2Students('1', 'Нравится ли вам, как организован формат дистанционного обучения в вашей школе?', ['Да', 'Скорее да, чем нет', 'Скорее нет, чем да', 'Нет']))
quests2st.append(question.Qeston2Students('2', 'Какие ключевые факторы вы бы хотели поменять в дистанционной форме проведения занятий?', ['Меня все устраивает', 'Плохо проводятся онлайн занятия', 'Неструктурированное д/з', 'Неполноценно дается материал']))
quests2st.append(question.Qeston2Students('3', 'Обучайтесь ли вы в интернете?', ['Да', 'Скорее да, чем нет', 'Скорее нет, чем да', 'Нет']))
quests2st.append(question.Qeston2Students('4', 'Как вы считайте, образовательная платформа (например, Stepik, Moodle или GoogleClass) способствуют улучшению обучения в интернете?', ['Да', 'Скорее да, чем нет', 'Скорее нет, чем да', 'Нет']))
quests2st.append(question.Qeston2Students('5', 'Что для вас самое главное в образовательной платформе?', ['Наличие онлайн конференций с преподавателем', 'Качественная и быстрая проверка заданий', 'Красивый дизайн и удобный интерфейс', 'Наличие как веб сервиса, так и десктоп приложения', 'Возможность задать преподавателю вопрос в письменном виде']))
quests2st.append(question.Qeston2Students('6', 'Вы бы хотели, что бы дистанционный формат обучения в вашей школе проходил на подобной (Stepik, Moodle), оптимизированной для этого системе?', ['Да', 'Скорее да, чем нет', 'Скорее нет, чем да', 'Нет']))


quests2tch = []
quests2tch.append(question.Qeston2Teachers('1', 'Что бы вы хотели изменить в формате дистанционного обучения?'))
quests2tch.append(question.Qeston2Teachers('2', 'Как вы считайте, обр платформа улучшит дистанционное обучение?'))
quests2tch.append(question.Qeston2Teachers('3', 'Что для вас важно в образовательной платформе?'))
quests2tch  .append(question.Qeston2Teachers('4', 'Как вы думайте, наша платформа улучшит самостоятельное и дистанционное обучение школьников?'))


myip = "http://exillite.xyz/"


def connect_db():
    conn = sqlite3.connect("mydatabase.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


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
    name = db.Column(db.String(50))

    def __repr__(self):
        return f"<module {self.id}>"


class Blocks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer)
    type = db.Column(db.String(50))
    title = db.Column(db.String(50))
    text = db.Column(db.Text)
    one_answer = db.Column(db.Boolean)
    answers = db.Column(db.Text)
    path = db.Column(db.String(500))
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


@app.route("/adminka")
def adminka():
    db = get_db()
    cursor = db.cursor()
    sqlt = "SELECT count(*) FROM students_answers"
    cursor.execute(sqlt)
    col = int(cursor.fetchall()[0][0])
    return render_template('adminka.html', studentscol=col)

@app.route("/courses")
def courses():
    if request.cookies.get('user_token') is None:
        return redirect(url_for('login'))

    token = request.cookies.get('user_token')
    student_id = Users.query.filter_by(token=token).first().id
    
    courses_ids = User2Course.query.filter_by(user_id=student_id).all()
    crs = []
    for i in courses_ids:
        c = Courses.query.filter_by(id=i.course_id).first()
        
        ath = Users.query.filter_by(id=c.author_id).first()
        dic = {'id': c.id, 'name': c.name, 'description': c.description, 'author_id': c.author_id, 'auther_name': f'{ath.name} {ath.surname}'}
        crs.append(dic)

    return render_template('courses.html', courses=crs, nb=True, is_logined=True)

@app.route("/course/<id>")
def course(id):
    if request.cookies.get('user_token') is None:
        return redirect(url_for('login'))

    moduls = Moduls.query.filter_by(course_id=id).all()
    mdls = []
    for m in moduls:
        dic = {'id': m.id, 'name': m.name, 'course_id': m.course_id}
        mdls.append(dic)

    this_course = Courses.query.filter_by(id=id).first()
    course_name = this_course.name
    course_description = this_course.description
    
    return render_template('course.html', course_name=course_name, course_description=course_description, moduls=mdls, nb=True, is_logined=True)

@app.route("/questions", methods=["POST", "GET"])
def questions():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO students_answers
            VALUES ('{request.form['1']}', '{request.form['2']}', '{request.form['3']}', '{request.form['4']}', '{request.form['5']}', '{request.form['6']}')"""
        )
        db.commit()
        return redirect(url_for('snxpage'))

    return render_template('questions.html', questions=quests2st)

@app.route("/questionsforteachers", methods=["POST", "GET"])
def questions_teachers():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO teachers_answers
            VALUES ('{request.form['1']}', '{request.form['2']}', '{request.form['3']}', '{request.form['4']}')"""
        )
        db.commit()
        return redirect(url_for('snxpage'))


    return render_template('questions_teachers.html', questions=quests2tch)


@app.route("/snxpage")
def snxpage():
    print(request.cookies.get('user_token'))
    return render_template('snxpage.html')



@app.route("/teach", methods=['POST', 'GET'])
def teahc():
    if request.cookies.get('user_token') is None:
        return redirect(url_for('login'))

    token = request.cookies.get('user_token')
    if request.method == 'POST':
        name = request.form.get('name')  # запрос к данным формы
        description = request.form.get('description')
        
        a_id = Users.query.filter_by(token=token).first().id
        db.session.add(Courses(name=name, description=description, author_id=a_id, is_public=False))
        db.session.flush()
        db.session.commit()
    
    student_id = Users.query.filter_by(token=token).first().id
    courses = Courses.query.filter_by(author_id=student_id).all()
    crs = []
    for c in courses:
        ath = Users.query.filter_by(id=c.author_id).first()
        dic = {'id': c.id, 'name': c.name, 'description': c.description, 'author_id': c.author_id, 'auther_name': f'{ath.name} {ath.surname}'}
        crs.append(dic)

    return render_template('teachers_courses.html', curses=crs, nb=True, is_logined=True)

@app.route("/edit_course/<course_id>", methods=['GET', 'POST'])
def edit_course(course_id):
    if request.cookies.get('user_token') is None:
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form.get('name')  # запрос к данным формы
        token = request.cookies.get('user_token')
        
        db.session.add(Moduls(course_id=course_id, name=name))
        db.session.flush()
        db.session.commit()
        return redirect(f'/edit_course/{course_id}')

    moduls = Moduls.query.filter_by(course_id=course_id).all()
    mdls = []
    for m in moduls:
        dic = {'id': m.id, 'name': m.name, 'course_id': m.course_id}
        mdls.append(dic)

    course_code = 842859 - int(course_id)

    this_course = Courses.query.filter_by(id=course_id).first()
    course_name = this_course.name
    course_description = this_course.description

    return render_template('course_edit.html', course_name=course_name, course_description=course_description, moduls=mdls, course_code=course_code, nb=True, is_logined=True)

@app.route("/edit_course/<course_id>/<block_id>/<step_id>", methods=['GET', 'POST'])
def edit_block(course_id, block_id, step_id):
    if request.cookies.get('user_token') is None:
        return redirect(url_for('login'))
    
    blocks = Blocks.query.filter_by(module_id=block_id).all()
    stps = []
    for b in blocks:
        dic = {'id': b.id, 'is_ready': False}
        stps.append(dic)


    blk = Blocks.query.filter_by(id=step_id).first()
    if blk.type == 'theory':
        dt = {'type': blk.type, 'title': blk.title, 'text': blk.text}
    elif blk.type == 'short_ans':
        dt = {'type': blk.type, 'title': blk.title, 'text': blk.text}
    elif blk.type == 'long_ans':
        dt = {'type': blk.type, 'title': blk.title, 'text': blk.text}
    elif blk.type == 'task_with_answers':
        dt = {'type': blk.type, 'title': blk.title, 'text': blk.text, 'is_one_ans': blk.one_answer, 'answers': blk.answers.split('#')}
    elif blk.type == 'file':
        dt = {'type': blk.type, 'title': blk.title, 'text': blk.text, 'file_name': blk.path}
        
    return render_template('edit_block.html', steps=stps, dt=dt)


@app.route("/exercise")
def exercisepage():
    if request.cookies.get('user_token') is None:
        return redirect(url_for('login'))
    return render_template('exercise.html', nb=True, is_logined=True)

@app.route("/theory")
def theory():
    if request.cookies.get('user_token') is None:
        return redirect(url_for('login'))
    return render_template('theory_video.html', nb=True, is_logined=True)

@app.route("/newcourse", methods=["POST", "GET"])
def new_course():
    if request.cookies.get('user_token') is None:
        return redirect(url_for('login'))

    token = request.cookies.get('user_token')
    if request.method == 'POST':
        name = request.form.get('name')  # запрос к данным формы
        description = request.form.get('description')
        
        a_id = Users.query.filter_by(token=token).first().id
        db.session.add(Courses(name=name, description=description, author_id=a_id, is_public=False))
        db.session.flush()
        db.session.commit()
        return redirect(url_for('teahc'))

    return render_template('newcourse.html', nb=True, is_logined=True)

@app.route("/addcourse", methods=["POST", "GET"])
def add_course():
    if request.cookies.get('user_token') is None:
        return redirect(url_for('login'))

    token = request.cookies.get('user_token')
    student_id = Users.query.filter_by(token=token).first().id

    if request.method == 'POST':
        code = request.form.get('code')

        
        courses = Courses.query.filter_by(id=842859-int(code)).all()
        courses_test = User2Course.query.filter_by(course_id=842859-int(code), user_id=student_id).all()

        if len(courses) == 1 and len(courses_test) == 0:
            db.session.add(User2Course(user_id=student_id, course_id=842859-int(code)))
            db.session.flush()
            db.session.commit()
        return redirect(url_for('courses'))

    return render_template('addcourse.html', nb=True, is_logined=True)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    # Appending app path to upload folder path within app root folder
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    # Returning file from appended path
    return send_from_directory(directory=r"C:\Users\Alexander\Desktop\glow\static\img", path=filename)


@app.route('/api', methods=['GET', 'POST'])
def api():
    j = request.json

    if j['method'] == 'reg':
        try:
            if len(Users.query.filter_by(email=j['email']).all()) != 0:
                return 'ALR'
            pshash = generate_password_hash(j['password'])
            token = generate_password_hash(j['email'])
            u = Users(is_active=True, name=j['name'], surname=j['surname'], email=j['email'], password=pshash,
                      token=token)
            db.session.add(u)
            db.session.flush()
            db.session.commit()
            #testemail(j['email'], token)
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
                '''
                if j['is_active']:
                    if j['stay']:
                        pass
                    return 'id=' + u.token
                else:
                    return 'NOTACTIVE'
                '''
                return 'id=' + u.token
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
            db.session.add(Courses(name=j['name'], description=j['description'], author_id=a_id, is_public=False))
            db.session.flush()
            db.session.commit()

            r['status'] = 'OK'

        except Exception as e:
            print('!!>>>>' + str(e))
            db.session.rollback()
            r['status'] = 'ERROR'

        return json.dumps(r)

    elif j['method'] == 'make_step':
        r = {}
        try:
            b = Blocks(module_id=j['module_id'], type=j['type'])

            db.session.add(b)
            db.session.flush()
            db.session.commit()

            r['status'] = 'OK'

        except Exception as e:
            print('!!>>>>' + str(e))
            db.session.rollback()
            r['status'] = 'ERROR'

        return json.dumps(r)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
