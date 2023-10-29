from generator import generate_type, generate_json


def get_variable_num() -> int:
    num = input('Enter the number of dependent variables: ')
    try:
        num = int(num)
    except ValueError:
        print('Invalid input')
        exit()
    assert 0 < num <= 5, 'Out of range'
    return num


def get_single_info(current: int) -> dict:
    current_info = {'name': input(f'Enter the name of variable {current + 1}: ')}
    type_index = input(f'Enter the type of variable {current + 1} (1: int, 2: float, 3: str): ')
    assert type_index in ['1', '2', '3'], 'Invalid input'
    match type_index:
        case '1':
            current_info['type'] = 'int'
            converter = int
        case '2':
            current_info['type'] = 'float'
            converter = float
        case '3':
            current_info['type'] = 'str'
            converter = str
        case _:
            print('Invalid input')
            exit()
    levels = input(f'Enter the number of levels of variable {current + 1}: ')
    try:
        levels = int(levels)
    except ValueError:
        print('Invalid input')
        exit()
    assert levels > 0, 'Out of range'
    levels_info = []
    for level in range(levels):
        levels_info.append(converter(input(f'Enter the value of level {level + 1}: ')))
    current_info['levels'] = levels_info
    print()
    return current_info


def get_variable_info(total_num: int) -> list[dict]:
    info = []
    for current_num in range(total_num):
        info.append(get_single_info(current_num))
    return info


def get_runtime_config(var_list) -> dict:
    choices = [f"{index}:{item['name']} " for index, item in enumerate(var_list)]

    config = {'use_session': input('Use session? (y/n): ') == 'y'}
    if config['use_session']:
        config['session_var'] = int(input(f'Enter the INDEX of session variable: {choices}'))
        assert config['session_var'] < len(var_list), 'Out of range'
        config['use_block'] = True
    else:
        config['use_block'] = input('Use block? (y/n): ') == 'y'

    if config['use_block']:
        config['block_var'] = int(input(f'Enter the INDEX of block variable: {choices}'))
        if config['use_session']:
            assert config['block_var'] != config['session_var'], 'Duplicate variable'

    config['randomize'] = input('Randomize Now? (y/n): ') == 'y'

    if config['randomize']:
        if config['use_session']:
            config['random_session'] = input('Randomize session? (y/n): ') == 'y'
        if config['use_block']:
            config['random_block'] = input('Randomize block? (y/n): ') == 'y'
        if config['use_session'] or config['use_block']:
            config['random_trial'] = input('Randomize trial? (y/n): ') == 'y'
        else:
            config['random_trial'] = True

    config['trial_rep'] = int(input('Enter the number of trial repetitions: '))

    return config


if __name__ == '__main__':
    num_of_variables = get_variable_num()

    variable_info = get_variable_info(num_of_variables)
    runtime_config = get_runtime_config(variable_info)

    generate_type(variable_info)
    generate_json(variable_info, runtime_config)

    print("Done!")
