import json
import os
from functools import wraps
from itertools import product
from random import shuffle


def check_output_dir(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists('./output'):
            os.mkdir('./output')
        return func(*args, **kwargs)
    return wrapper


@check_output_dir
def generate_type(info: list[dict]):
    with open('./output/condition_datatype.py', 'w', encoding='utf-8') as file:
        file.write('import unreal\n\n\n')
        file.write('@unreal.ustruct()\n')
        file.write('class ConditionStruct(unreal.StructBase):\n')
        for item in info:
            file.write(f'\t{item["name"]}=unreal.uproperty({item["type"]})\n')


def get_trial_vars(info: list[dict], config: dict) -> list[dict]:
    if config['use_session']:
        return [var for index, var in enumerate(info) if index != config['session_var'] and index != config['block_var']]
    if config['use_block']:
        return [var for index, var in enumerate(info) if index != config['block_var']]
    return info


@check_output_dir
def generate_json(info: list[dict], config: dict):
    full_conditions = {}
    session_items_count = len(info[config['session_var']]['levels']) if config['use_session'] else 1
    block_items_count = len(info[config['block_var']]['levels']) if config['use_block'] else 1

    trial_vars = get_trial_vars(info, config)

    # Get Count
    full_conditions['session_count'] = session_items_count
    full_conditions['block_count'] = block_items_count

    # Randomize the condition according to the config
    if(config["randomize"]):
        if config["random_session"]:
            shuffle(info[config['session_var']]['levels'])
        if config["random_block"]:
            shuffle(info[config['block_var']]['levels'])

    # Initialize the dictionary
    for session in range(session_items_count):
        full_conditions[str(session)] = {}
        for block in range(block_items_count):
            full_conditions[str(session)][str(block)] = []

    # Generate the conditions
    for session in range(session_items_count):
        for block in range(block_items_count):
            full_conditions[str(session)][str(block)] = {}
            trials = []
            for item in product(*(var['levels'] for var in trial_vars)):
                trial_dict = {var['name']: value for var, value in zip(trial_vars, item)}
                if config['use_session']:
                    trial_dict[info[config['session_var']]['name']] = info[config['session_var']]['levels'][session]
                if config['use_block']:
                    trial_dict[info[config['block_var']]['name']] = info[config['block_var']]['levels'][block]
                trials.append(trial_dict)

            trials *= config['trial_rep']
            if config['randomize'] and config['random_trial']:
                shuffle(trials)
            full_conditions[str(session)][str(block)] = trials

    conditions_json_str = json.dumps(full_conditions, indent=2, ensure_ascii=False)

    with open('./output/full_conditions.json', 'w', encoding='utf-8') as file:
        file.write(conditions_json_str)
