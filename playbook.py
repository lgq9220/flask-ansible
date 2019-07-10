from flask import Blueprint, request
import json, tool_db, subprocess, threading, time

playbook = Blueprint("playbook", __name__)

@playbook.route('/delete_by_id')
def delete_by_id():
    id = int( request.args.get('id') )
    sql = 'delete from playbook where id = %s'
    tool_db.updateByParameters( sql, (id, ) )
    return "Servers!"

@playbook.route('/get_by_page', methods=['get', 'post'])
def get_by_page():
    info = request.get_data()
    info = json.loads(info)
    pagenow = info['pagenow']
    pagesize = info['pagesize']
    search = info['search']
    search = "%{0}%".format(search)
    sql = 'select * from playbook where name like %s limit %s,%s'
    params = (search, (pagenow - 1) * pagesize, pagesize)
    result = tool_db.selectByParameters(sql, params=params)
    return json.dumps(result)


def shellRun(command):
    (status, output) = subprocess.getstatusoutput(command)
    return (status, output)

@playbook.route('/insert', methods=['get', 'post'])
def insert():
    info = request.get_data()
    info = json.loads(info)
    sql = 'replace into playbook (name,hosts_path, playbook_path, forks) VALUES(%s, %s, %s, %s);'
    params = ( info['name'], info['hosts_path'], info['playbook_path'], info['forks'])
    tool_db.updateByParameters( sql, params )
    return "Success"

@playbook.route('/deploy_by_id')
def deploy_by_id():
    id = int(request.args.get('id'))
    sql = "select * from playbook where id = %s"
    result = tool_db.selectByParameters(sql, params=(id,))[0]
    tmpnumber = int(time.time() * 1000)
    # name, hosts_path, playbook_path, forks
    displaycommand = """ /usr/local/python/bin/ansible-playbook  -i {0} {1} -f {2} """.format(
        result['hosts_path'],
        result['playbook_path'],
        result['forks']
    )
    command = """ /usr/local/python/bin/ansible-playbook  -i {0} {1} -f {2} >static/logs/{3} 2>&1; printf '\n\t\t\t' >>static/logs/{4} """.format(
        result['hosts_path'],
        result['playbook_path'],
        result['forks'], tmpnumber, tmpnumber
        )
    t1 = threading.Thread(target=shellRun, args=(command,))
    t1.start()
    return json.dumps({"command": displaycommand, "logpath": tmpnumber})


@playbook.route('/get_by_id')
def get_by_id():
    id = int(request.args.get('id'))
    sql = "select * from playbook where id = %s"
    result = tool_db.selectByParameters(sql, params=(id,))
    return json.dumps(result)


@playbook.route('/update', methods=['get', 'post'])
def update():
    info = request.get_data()
    info = json.loads(info)
    # name, hosts_path, playbook_path, forks
    sql = 'replace into playbook (id,name,hosts_path, playbook_path, forks) VALUES(%s, %s, %s, %s, %s);'
    params = (info['id'], info['name'], info['hosts_path'], info['playbook_path'], info['forks'])
    tool_db.updateByParameters(sql, params)
    return "Success"
