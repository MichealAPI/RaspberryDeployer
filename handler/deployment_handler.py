import os
import subprocess
from entity.deployment import Deployment


def run_command(command, cwd=None):
    """Runs a shell command and returns the output."""
    process = subprocess.Popen(command, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout.decode(), stderr.decode()


def load_deployments(parsed_yaml: dict) -> dict:
    """Loads deployment configurations from YAML."""
    deployments = {}
    for deployment_name, deployment in parsed_yaml.get('deployments', {}).items():
        deployments[deployment['id']] = Deployment(
            deployment['remote'],
            deployment['local_path'],
            deployment['id'],
            deployment['branch'],
            deployment['version_control'],
            deployment.get('run-scripts', [])  # Load post-deployment scripts
        )
    return deployments


def load_scripts(parsed_yaml: dict) -> list:
    """Loads version control scripts from YAML."""
    scripts = []
    for vc, script_data in parsed_yaml.get('scripts', {}).items():
        scripts.append({"vc": vc, "scripts": script_data})
    return scripts


class DeploymentHandler:
    __deployments: dict = {}
    __scripts: dict = {}

    def __init__(self, parsed_yaml: dict):
        self.__deployments = load_deployments(parsed_yaml)
        self.__scripts = load_scripts(parsed_yaml)

    @property
    def deployments(self) -> dict:
        return self.__deployments

    @property
    def scripts(self) -> dict:
        return self.__scripts

    def runDeployment(self, deployment_id: str):
        """Handles deployment process."""
        print(f"Running deployment for {deployment_id}")
        deployment = self.__deployments.get(deployment_id)

        if deployment is None:
            return f"Deployment with id {deployment_id} not found", 404

        deployment_vc = deployment.version_control
        deployment_scripts = self.__get_vc(deployment_vc)

        if not deployment_scripts:
            return f"Script for {deployment_vc} not found", 404

        # Clone if folder doesn't exist, otherwise pull
        if not os.path.exists(deployment.local_path):
            for command in deployment_scripts['clone']:
                returncode, stdout, stderr = run_command(
                    command.format(remote=deployment.remote, local_path=deployment.local_path, branch=deployment.branch)
                )
                print(stdout, stderr)
        else:
            for command in deployment_scripts['pull']:
                returncode, stdout, stderr = run_command(
                    command.format(remote=deployment.remote, local_path=deployment.local_path, branch=deployment.branch),
                    cwd=deployment.local_path
                )
                print(stdout, stderr)

        # **Run post-deployment scripts**
        self.run_post_scripts(deployment)

        return f"Deployment for {deployment_id} ran successfully", 200

    def run_post_scripts(self, deployment: Deployment):
        """Runs additional scripts after deployment."""
        for command in deployment.run_scripts:
            print(f"Executing: {command.format(local_path=deployment.local_path)}")
            returncode, stdout, stderr = run_command(command.format(local_path=deployment.local_path), cwd=deployment.local_path)
            print(stdout, stderr)

    def __get_vc(self, vc: str) -> dict:
        """Fetches version control scripts."""
        for script in self.__scripts:
            if script['vc'] == vc:
                return script['scripts']
        return {}
