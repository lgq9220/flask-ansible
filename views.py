from flask import Blueprint
from flask import render_template
views = Blueprint("views", __name__)

@views.route('/test')
def test():
    return render_template("test.html")

@views.route('/servers')
def servers():
    return render_template("servers.html")

@views.route('/deploy')
def deploy():
    return render_template("deploy.html")

@views.route('/playbook')
def playbook():
    return render_template("playbook.html")