import os

from flask import Flask, request
from handler.deployment_handler import DeploymentHandler
from util.yaml_parser import parse_yaml

app = Flask(__name__)
yaml = parse_yaml("config.yaml")
deployment_handler = DeploymentHandler(yaml)


@app.route('/request', methods=['GET'])
def request_handler():
    # Get Authorization header
    auth_header = request.headers.get('Authorization')

    # Check if Authorization header is present
    if auth_header is None:
        return 'Unauthorized', 401

    # Check if Authorization header is valid
    if auth_header != f'Bearer {"test"}':  # os.getenv("DEPLOYER_API_KEY")

        return 'Forbidden', 403

    # Get deployment id from query parameter
    deployment_id = request.args.get('deployment_id')

    return deployment_handler.runDeployment(deployment_id)


if __name__ != '__main__':
    application = app
else:
    debug = True
    app.run(debug=debug)
