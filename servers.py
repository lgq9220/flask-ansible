from flask import Blueprint
from flask import request
from flask import send_from_directory
import tool_db,tool_excel
import json,os,time
servers = Blueprint("servers", __name__)

@servers.route('/index')
def index():
    return "Servers!"

@servers.route('/mutidelete', methods=['get', 'post'])
def mutidelete():
    info = request.get_data()
    info = json.loads(info)
    for oneid in info:
        sql = 'delete from servers where id = %s'
        tool_db.updateByParameters(sql, (oneid, ))
    return "Success!"

@servers.route('/delete_by_id')
def delete_by_id():
    id = int( request.args.get('id') )
    sql = 'delete from servers where id = %s'
    tool_db.updateByParameters( sql, (id, ) )
    return "Servers!"

@servers.route('/insert_from_excel', methods=['get', 'post'])
def insert_from_excel():
    f = request.files.get('servers')
    ramname = int(time.time() * 1000)
    f.save('/tmp/{0}'.format( ramname ))
    tool_excel.insertFromExcel( '/tmp/{0}'.format( ramname ) )
    return "Success!"

@servers.route('/getexcel')
def getexcel():
    curdir = os.path.dirname(os.path.realpath(__file__))
    return send_from_directory( curdir + "/static/", "servers.xlsx", as_attachment=True )

@servers.route('/update', methods=['get', 'post'])
def update():
    info = request.get_data()
    info = json.loads(info)
    sql = 'replace into servers (id,name,ip, port, user) VALUES(%s, %s, %s, %s, %s);'
    params = (info['id'], info['name'], info['ip'], info['port'], info['user'])
    tool_db.updateByParameters( sql, params )
    return "Success"

@servers.route('/insert', methods=['get', 'post'])
def insert():
    info = request.get_data()
    info = json.loads(info)
    sql = 'replace into servers (name,ip, port, user) VALUES(%s, %s, %s, %s);'
    params = ( info['name'], info['ip'], info['port'], info['user'])
    tool_db.updateByParameters( sql, params )
    return "Success"

@servers.route('/get_by_id')
def get_by_id():
    id = int( request.args.get('id'))
    sql = "select * from servers where id = %s"
    result = tool_db.selectByParameters( sql, params=(id, ) )
    return json.dumps( result )

@servers.route('/getall')
def getall():
    sql = "select * from servers;"
    result = tool_db.selectByParameters( sql )
    return json.dumps( result )

@servers.route('/get_by_page', methods = ['get', 'post'])
def get_by_page():
    info = request.get_data()
    info = json.loads(info)
    pagenow = info['pagenow']
    pagesize = info['pagesize']
    search = info['search']
    search = "%{0}%".format(search)
    sql = 'select * from servers where name like %s or ip like %s limit %s,%s'
    params = ( search, search, (pagenow-1)*pagesize, pagesize )
    result = tool_db.selectByParameters( sql, params=params )
    return json.dumps( result )