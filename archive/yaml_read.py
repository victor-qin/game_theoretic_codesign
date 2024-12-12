import yaml

with open('player_1.mcdp', 'r') as f:
    player_1 = yaml.safe_load(f)

print('here')
print(player_1)