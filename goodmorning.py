from blocks import mods
import yaml

with open("config.yml", "r") as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print("globals", config['globals'])

print("Blocks IN:")
for key, value in config['ins'].items():
    print(key)
    for step in value:
        mod, attr = list(step.items())[0]
        mods[mod](attr)

print("Blocks OUT:")
for key, value in config['outs'].items():
    print(key,value)




