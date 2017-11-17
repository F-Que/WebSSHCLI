from app import app
from app.forms import ConnectToHost
from flask import render_template
from flask.globals import request
from run_ws import HOST,WS_PORT


@app.route('/', methods=['GET'])
def connect_to_host():
    form = ConnectToHost()
    return render_template('connect_to_host.html', form = form)


@app.route('/terminal',  methods=['POST'])
def terminal():
    form = ConnectToHost()
    data = {}
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        data['ws_server'] = '{}:{}'.format(HOST, WS_PORT)
        return render_template('terminal.html', msg=data)
    return 'Validate err'

