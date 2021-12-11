import blocks
import yaml

with open("config.yml", "r") as stream:
    try:
        # quick and dirty replace $global vars TODO: Clean
        yml = stream.read()
        tmp = yaml.safe_load(yml)
        for key,value in tmp['globals'].items():
            yml = yml.replace("$"+key, value)
        config = yaml.safe_load(yml)
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

