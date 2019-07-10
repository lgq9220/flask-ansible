from flask import Blueprint
from flask import request
from flask import session
from flask import redirect
import tool_db,tool_pass
from flask import make_response
auth = Blueprint("auth", __name__)
''
@auth.route('/login', methods = ['get', 'post'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    password = tool_pass.md5encrypt(password)
    sql = "select * from user where username = %s and password = %s"
    result = tool_db.selectByParameters(sql, (username, password))
    if result:
        session['username'] = username
        return redirect('/views/servers')
    else:
        return redirect("/static/login.html")

@auth.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/static/login.html')