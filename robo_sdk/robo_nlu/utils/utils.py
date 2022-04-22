import yaml

def load_yaml_to_json(filepath:str) -> dict:
   
    def clean_pipes(entry):
        for key, value in entry.items():            
            if key == 'examples':
                entry[key] = [value.strip('- ') for value in value.split('\n') if value]

    with open(filepath, 'r') as stream:
        try:
            data_dict=yaml.safe_load(stream)
            for item in data_dict['nlu']:
                clean_pipes(item)
        except yaml.YAMLError as exc:
            print(exc)
        return data_dict

