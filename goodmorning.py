import blocks
import yaml

with open("config.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print("globals", config['globals'])

segments = ['ins', 'outs']
result_block = []

for key, value in config['ins'].items():
    result_flow = {}
    for step in value:
        block, attr = list(step.items())[0]
        result = blocks.blocks[block](**attr, flow=result_flow)
        result_flow.update({'prev': result, block: result})
    result_block.append(result_flow['prev'])

for key, value in config['outs'].items():
    for step in value:
        block, attr = list(step.items())[0]
        result = blocks.blocks[block](**attr, flow={'text':'\n'.join(result_block)})

