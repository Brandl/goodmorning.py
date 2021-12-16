import blocks
import yaml
from pathlib import Path

# Check for config.yml and (TODO: optional) secrets.yml

files = [Path("config.yml"), Path("secrets.yml")]
globals_dict = {}
configs = []

for config_file in files:
    if config_file.is_file():
        with open(config_file, "r") as stream:
            config_str = stream.read()
            configs.append(config_str)
            try:
                tmp = yaml.safe_load(config_str)
                globals_dict.update(tmp['globals'])
            except yaml.YAMLError as exc:
                print(exc)
    else:
        print(config_file, "missing")
        exit()

try:
    # quick and dirty replace $global vars TODO: Clean
    # TODO: calling save_load 4x, for what could be done in 3x
    tmp = yaml.safe_load(configs[0])
    for key,value in globals_dict.items():
        print(key, value)
        configs[0] = configs[0].replace("$"+key, value)
    config = yaml.safe_load(configs[0])
except yaml.YAMLError as exc:
    print(exc)

segments = ['ins', 'outs']
result_block = []

for key, value in config['ins'].items():
    result_flow = {}
    for step in value:
        block, attr = list(step.items())[0]
        if attr is None:
            attr = dict()
        result = blocks.blocks[block](**attr, flow=result_flow)
        result_flow.update({'prev': result, block: result})
    result_block.append(result_flow['prev'])

for key, value in config['outs'].items():
    for step in value:
        block, attr = list(step.items())[0]
        if attr is None:
            attr = dict()
        result = blocks.blocks[block](**attr, flow={'text':'\n'.join(result_block)})

