from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from shijiange import shijiange
from views import views
from servers import servers
from auth import auth
from deploy import deploy
from playbook import playbook
import datetime

app = Flask(__name__)
app.config['SECRET_KEY']='mypwd'
app.permanent_session_lifetime = datetime.timedelta(minutes=1440)
app.register_blueprint(shijiange, url_prefix="/shijiange")
app.register_blueprint(views, url_prefix="/views")
app.register_blueprint(servers, url_prefix="/servers")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(deploy, url_prefix="/deploy")
app.register_blueprint(playbook, url_prefix="/playbook")

@app.before_request
def before_request():
    if request.path == "/static/login.html" or request.path == "/auth/login" or request.path.endswith(".js") or request.path.endswith(".css"):
        pass
    else:
        username = session.get('username')
        if not username:
            return redirect('/static/login.html')

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
