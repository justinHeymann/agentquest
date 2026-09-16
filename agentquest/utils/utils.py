import importlib.resources
import json
import os
import pprint
from pathlib import Path
from termcolor import colored

class Observation():
    def __init__(self, output:str, done:bool):
        self.output = output
        self.done = done
class Action():
    def __init__(self, action_value:str, **kwargs):
        self.action_value = action_value
        for key, value in kwargs.items():
            setattr(self, key, value)


def load_data(benchmark, category=None):
    # Load benchmarks games
    base_package_name  = __package__.split('.')[0]
    base_package_path = importlib.resources.files(base_package_name)
    data_path = base_package_path / f'data/{benchmark}/games.json'
    if not data_path.exists() and benchmark == 'autopenbench':
        benchmark_root = os.environ.get('AUTOPENBENCH')
        if benchmark_root:
            data_path = Path(benchmark_root).parent / 'data' / 'games.json'
    if not data_path.exists():
        raise FileNotFoundError(
            f'AutoPenBench data not found at {data_path}. '
            'Set AUTOPENBENCH to the benchmark directory, for example '
            'AUTOPENBENCH=/path/to/auto-pen-bench/benchmark.'
        )
    with open(data_path, 'r') as file:
        games = json.loads(file.read())
    try:
        categories = list(games.keys())
    except:
        return games

    if type(category)!=type(None):
        try:
            return games[category]
        except:
            raise ValueError(f'You must provide one category among {categories}')    
    else:
        raise ValueError(f'You must provide one category among {categories}')

def cpprint(data, color='white'):
    # Convert the data to a formatted string
    formatted_data = pprint.pformat(data)
    # Colorize the formatted string
    colored_data = colored(formatted_data\
                                .replace('\\n', '')
                                .replace('(', '')
                                .replace(')', '')
                                .replace("\'", ''), color)
    
    # Print the colored and formatted data
    print(colored_data)
