# We need to import request to access the details of the POST request
from flask import Flask, request
from flask.ext.restful import abort
import json
from keystoneclient.auth.identity import v2
from keystoneclient import session
from novaclient import client as nova_client

# Openstack credentials
OPENSTACK_USERNAME = "admin" 
OPENSTACK_PASSWORD = "password"
OPENSTACK_PROJECT_NAME = "admin" 
OPENSTACK_AUTH_URL = "http://10.0.0.1:5000"

# Configure auth and nova client
args = \
    {'AuthServerUrl': OPENSTACK_AUTH_URL,
     'OpenstackPassword': OPENSTACK_PASSWORD,
     'OpenstackTenant': OPENSTACK_PROJECT_NAME,
     'OpenstackUsername': OPENSTACK_USERNAME}
auth_url=args['AuthServerUrl']
username=args['OpenstackUsername']
password=args['OpenstackPassword']
tenant_name=args['OpenstackTenant']
NOVA_CLIENT_VERSION = '2'
nova = nova_client.Client(NOVA_CLIENT_VERSION,
                          username,
                          password,
                          tenant_name,
                          auth_url)

# Functions for migration
def get_instances(host):
    instances = \
        nova.servers.list(search_opts={'all_tenants': 1, 'host': host})
    return [instance.id for instance in instances]

def migrate_all_instances(host):
    instances = get_instances(host)
    for instance in instances:
        nova.servers.live_migrate(
            instance, None, False, False)

# Initialize the Flask application
app = Flask(__name__)

@app.route('/', methods=['POST'])
def app_message_post():
    message = "No action"
    try:
        if request.headers['Content-Type'] != 'application/json':
            return json.dumps({'result': message})
        data = request.json
        status = data['status']
        spec = data['spec']
        if spec['eventRuleId'] == '1f28c2dc-2669-11e7-b224-0242ac130005':
            host = status['entityId']
            meta = status['metaData']
            migrate_all_instances(host)
            message = \
                "Migrate all instances from Host {}".format(host)
        return json.dumps({'result': message})
    except Exception as e:
        abort(400, message="Hit an issue when processing message: {}"
                           .format(e))

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("7070")
    )
