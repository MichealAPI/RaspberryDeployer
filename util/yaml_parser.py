import yaml as yaml


def parse_yaml(file_path) -> dict:
    with open(file_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)