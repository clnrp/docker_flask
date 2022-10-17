from flask import Flask, render_template, request, url_for, flash, redirect, session
from flask_session import Session
import email
import psycopg2
import psycopg2.extras
from psycopg2.pool import SimpleConnectionPool
import sys

class PostgreSql:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(host="postgresql", user="flask", password="W78&@Tn5tit&", dbname="flaskdb")
        except psycopg2.Error as ex:
            print(str(ex), file=sys.stdout)

    def disconnect(self):
        try:
            self.conn.close()
        except psycopg2.Error as ex:
            print(str(ex), file=sys.stdout)

    def sqlExc(self, sql):
        result = ''
        try:
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            if isinstance(sql, list):
                for cmd in sql:
                    self.cur.execute(cmd)
                    self.conn.commit()
                result = self.cur.lastrowid
            else:
                self.cur.execute(sql)
                if sql.find('select') != -1:
                    result = self.cur.fetchall()
                else:
                    self.conn.commit()
                    result = self.cur.lastrowid
            self.conn.rollback()
        except psycopg2.Error as ex:
            raise Exception(str(ex))
        return result

class PostgreSqlPool:

    def __init__(self):
        self.conn = None
        self.conn_pool = None
        self.cur = None
        self.connect()

    def connect(self):
        try:
            self.conn_pool = SimpleConnectionPool(1, 10, dsn="dbname='flaskdb' user='flask' host='postgresql' password='W78&@Tn5tit&'")
        except psycopg2.Error as ex:
            print(str(ex), file=sys.stdout)

    def disconnect(self):
        try:
            self.conn.close()
        except psycopg2.Error as ex:
            print(str(ex), file=sys.stdout)

    def sqlExc(self, sql):
        result = ''
        try:
            self.conn = self.conn_pool.getconn()
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            if isinstance(sql, list):
                for cmd in sql:
                    self.cur.execute(cmd)
                self.conn.commit()
                result = self.cur.lastrowid
            else:
                self.cur.execute(sql)
                if sql.find('select') != -1:
                    result = self.cur.fetchall()
                else:
                    self.conn.commit()
                    result = self.cur.lastrowid
            self.conn.rollback()
        except psycopg2.Error as ex:
            raise Exception(str(ex))
        return result


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dc126a294c0b983a25521326cd212345845ce6768422e864'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

posts = [
    {
        'author': 'author 1',
        'title': 'title 1',
        'content': 'content 1',
        'date_posted': '2001'
    },
    {
        'author': 'author 2',
        'title': 'title 2',
        'content': 'content 2',
        'date_posted': '2002'
    }
]

messages = [{'message': 'message 1',
             'content': 'content 1'},
            {'message': 'message 2',
             'content': 'content 2'}
]

@app.route("/")
@app.route("/home")
def home():
    print("Home Page", file=sys.stdout)
    #return "<h1>Home Page</h1>"
    if not session.get("email"):
        return redirect("/login")
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    try:
        psql = PostgreSql()
        result = psql.sqlExc("select * from userdb")
        print(result, file=sys.stdout)
    except Exception as ex:
        print(str(ex), file=sys.stdout)
    return render_template('about.html', title='About')

@app.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not email:
            flash('Email is required!')
        elif not password:
            flash('Password is required!')
        else:
            messages.append({'email': email, 'password': password})
            print(str(messages), file=sys.stdout)
            session["email"] = request.form.get("email")
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/")

@app.route('/search/', methods=('GET', 'POST'))
def search_id():
    if request.method == 'POST':
        id = request.form['id']
        if not id:
            flash('ID is required!')
        else:
            try:
                result = {"result": "foi!"}
            except Exception as ex:
                result = {"result": str(ex)}
            return render_template('search.html', post=result)
    return render_template('search.html', post={"result": ""})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
