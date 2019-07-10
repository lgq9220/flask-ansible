from flask import Blueprint, request
import json, tool_db, subprocess, threading, time

deploy = Blueprint("deploy", __name__)


@deploy.route('/insert', methods=['get', 'post'])
def insert():
    info = request.get_data()
    info = json.loads(info)
    # name, hosts_path, hosts_pattern, module, args, forks
    sql = 'replace into deploy (name,hosts_path, hosts_pattern, module, args, forks) VALUES(%s, %s, %s, %s, %s, %s);'
    params = ( info['name'], info['hosts_path'], info['hosts_pattern'], info['module'], info['args'], info['forks'])
    tool_db.updateByParameters( sql, params )
    return "Success"

@deploy.route('/delete_by_id')
def delete_by_id():
    id = int( request.args.get('id') )
    sql = 'delete from deploy where id = %s'
    tool_db.updateByParameters( sql, (id, ) )
    return "Servers!"

@deploy.route('/get_by_page', methods=['get', 'post'])
def get_by_page():
    info = request.get_data()
    info = json.loads(info)
    pagenow = info['pagenow']
    pagesize = info['pagesize']
    search = info['search']
    search = "%{0}%".format(search)
    sql = 'select * from deploy where name like %s limit %s,%s'
    params = (search, (pagenow - 1) * pagesize, pagesize)
    result = tool_db.selectByParameters(sql, params=params)
    return json.dumps(result)


@deploy.route('/get_by_id')
def get_by_id():
    id = int(request.args.get('id'))
    sql = "select * from deploy where id = %s"
    result = tool_db.selectByParameters(sql, params=(id,))
    return json.dumps(result)


def shellRun(command):
    (status, output) = subprocess.getstatusoutput(command)
    return (status, output)


@deploy.route('/deploy_by_id')
def deploy_by_id():
    id = int(request.args.get('id'))
    sql = "select * from deploy where id = %s"
    result = tool_db.selectByParameters(sql, params=(id,))[0]
    tmpnumber = int(time.time() * 1000)
    # name, hosts_path, hosts_pattern, module, args, forks
    runcommand = """ /usr/local/python/bin/ansible -i {0} {1} -m {2} -a '{3}' -f {4} """.format(
        result['hosts_path'],
        result['hosts_pattern'],
        result['module'],
        result['args'],
        result['forks']
    )
    command = """ /usr/local/python/bin/ansible -i {0} {1} -m {2} -a '{3}' -f {4} >static/logs/{5} 2>&1; printf '\n\t\t\t' >>static/logs/{6} """.format(
        result['hosts_path'],
        result['hosts_pattern'],
        result['module'],
        result['args'],
        result['forks'], tmpnumber, tmpnumber
    )
    t1 = threading.Thread(target=shellRun, args=(command,))
    t1.start()
    return json.dumps({"command": runcommand, "logpath": tmpnumber})


@deploy.route('/update', methods=['get', 'post'])
def update():
    info = request.get_data()
    info = json.loads(info)
    # name, hosts_path, hosts_pattern, module, args, forks
    sql = 'replace into deploy (id,name,hosts_path, hosts_pattern, module, args, forks) VALUES(%s, %s, %s, %s, %s, %s, %s);'
    params = (
        info['id'], info['name'], info['hosts_path'], info['hosts_pattern'], info['module'], info['args'],
        info['forks'])
    tool_db.updateByParameters(sql, params)
    return "Success"
