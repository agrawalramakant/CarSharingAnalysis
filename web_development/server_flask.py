# import dataset
from flask import Flask, jsonify, request
import flask.ext.sqlalchemy
import flask.ext.restless

import select
try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

import sys
import paramiko

class ForwardServer (SocketServer.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

class Handler (SocketServer.BaseRequestHandler):

    def handle(self):
        try:
            chan = self.ssh_transport.open_channel('direct-tcpip',
                                                   (self.chain_host, self.chain_port),
                                                   self.request.getpeername())
        except Exception as e:
            print ('Incoming request to %s:%d failed: %s' % (self.chain_host,
                                                              self.chain_port,
                                                              repr(e)))
            return
        if chan is None:
            print ('Incoming request to %s:%d was rejected by the SSH server.' % (self.chain_host, self.chain_port))
            return

        print ('Connected!  Tunnel open %r -> %r -> %r' % (self.request.getpeername(),
                                                            chan.getpeername(), (self.chain_host, self.chain_port)))
        while True:
            r, w, x = select.select([self.request, chan], [], [])
            if self.request in r:
                data = self.request.recv(1024)
                if len(data) == 0:
                    break
                chan.send(data)
            if chan in r:
                data = chan.recv(1024)
                if len(data) == 0:
                    break
                self.request.send(data)
        peername = self.request.getpeername()
        chan.close()
        self.request.close()
        print ('Tunnel closed from %r' % (peername,))


def forward_tunnel(local_port, remote_host, remote_port, transport):
    # this is a little convoluted, but lets me configure things for the Handler
    # object.  (SocketServer doesn't give Handlers any way to access the outer
    # server normally.)
    class SubHander (Handler):
        chain_host = remote_host
        chain_port = remote_port
        ssh_transport = transport
    ForwardServer(('', local_port), SubHander).serve_forever()


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/connections.db'
db = flask.ext.sqlalchemy.SQLAlchemy(app)
#Fields

#Global Dict of Servers
servers = []
#Switch Dictionary
_dict = {}

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)
    host = db.Column(db.Unicode)
    username = db.Column(db.Unicode)
    password = db.Column(db.Unicode)
    isAccessKey = db.Column(db.Boolean)
    sshKeyFile = db.Column(db.Unicode)
    sshFilePass = db.Column(db.Unicode)
    localport = db.Column(db.Integer)
    isAlive = db.Column(db.Boolean)

db.create_all()

#DEmo Data
d = {'host': 'maidb.hack.celonis.de',
 'id': 2,
 'isAccessKey': True,
 'localport': 5432,
 'name': 'Celonis-DB-Server',
 'password': 'dasda',
 'sshFilePass': 'Soo4phie9i',
 'sshKeyFile': '~/Downloads/id_hacker',
 'username': 'hacker'}

def create_postprocessor(result=None, filters=None, sort=None, group_by=None, single=None, **kw):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())
    with open("Output.txt", "w") as text_file:
        text_file.write("Single: ", single)

# Create the Flask-Restless API manager.
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
postprocessors = {'GET_COLLECTION': [create_postprocessor]}
manager.create_api(Connection, methods=['GET', 'POST', 'DELETE'], postprocessors=postprocessors)

@app.route("/")
def index():
    return ("<h2> Ssh-Tunnel Baby !</h2> <h3>Hey, User</h3>")

@app.route("/help")
def help():
    return jsonify(ok = True)

@app.route("/ping")
def ping():
    return jsonify(ok = True)

# http://0.0.0.0:8080/create?host=students.iitmandi.ac.in&port=22
@app.route("/create", methods=['GET', 'POST'])
def create():
    host = request.args.get('host')
    hostPort = int(request.args.get('hostPort'))
    global _dict

    # Defaults

    # Create unique ID

    # Create Object

    # Add to database
    # return ID

@app.route("/start", methods=['GET', 'POST'])
def start():
    switchNo = int(request.args.get('switch'))
    status = request.args.get('status')
    global _dict

@app.route("/stop", methods=['GET', 'POST'])
def stop():
    switchNo = int(request.args.get('switch'))
    status = request.args.get('status')
    global _dict

# http://0.0.0.0:8080/check?switch=2
@app.route("/list", methods=['GET', 'POST'])
def list():
    global _dict
    # status = request.args.get('status')
    switchNo = int(request.args.get('switch'))
    ret = {switchNo : _dict[str(switchNo)]}
    return jsonify(ret)

# http://0.0.0.0:8080/check?switch=2
@app.route("/check", methods=['GET', 'POST'])
def check():
    global _dict
    # status = request.args.get('status')
    switchNo = int(request.args.get('switch'))
    ret = {switchNo : _dict[str(switchNo)]}
    return jsonify(ret)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8080)