# take in an mcdp system and create a matrix game from it

# import yaml
import re
import numpy as np

# Function to get the integer value at the specified index `x` from the right of '->'
def get_value_at_index(lines, x):
    values = []
    for line in lines:
        # Split the part after '->' by commas and strip extra spaces
        right_side_values = line.split('->')[1].split(',')
        right_side_values = [value.strip() for value in right_side_values]
        
        # Adjust negative index to count from the end of the list
        if x < 0:
            x = len(right_side_values) + x
        
        # Get the value at index `x` if it exists
        if 0 <= x < len(right_side_values):
            value = right_side_values[x]
            # Attempt to extract the integer part only
            try:
                # Use regex to find the first integer in the value string
                value = float(re.search(r'\d+\.\d+|\d+', value).group())
                values.append(value)
            except (ValueError, AttributeError):
                # If conversion fails, append None or handle it as needed
                values.append(None)
        else:
            values.append(None)  # Append None if the index is out of range
    return values

def get_all_values(lines, token='->'):
    all_values = []
    for line in lines:
        # Split the part after '->' by commas and strip extra spaces
        if token == '->':
            side_values = line.split('->')[1].split(',')
        elif token == '<-':
            side_values = line.split('<-')[0].split(',')
        side_values = [value.strip() for value in side_values]
        
        # Convert each value to a float if possible, otherwise append None
        converted_values = []
        for value in side_values:
            try:
                # Extract and convert to float
                float_value = float(re.search(r'\d+\.\d+|\d+', value).group())
                converted_values.append(float_value)
            except (ValueError, AttributeError):
                # Append None if the value cannot be converted
                converted_values.append(None)
        
        all_values.append(converted_values)
    return all_values

def main(players):

    outname = 'out/matrix_game.out'
    fileoutput = ''

    # parse a .mcdp file and extract the actions for each player
    values = {}
    implementations = {}
    raw_imps = {}
    for p in players:

        with open(f'{p}.mcdp', 'r') as f:
            # player_1 = yaml.safe_load(f)
            player = f.read()

        # print(player)
        imps = [line[4:] for line in player.splitlines() if re.search(r'\bi_\w+', line)]
        provides = [line[4:] for line in player.splitlines() if re.search(r'\bprovides\b', line)]
        requires = [line[4:] for line in player.splitlines() if re.search(r'\brequires\b', line)]
        # print(imps)

        # get the integer values
        # result = np.array(get_all_values(imps, '->'))
        prov_values = np.array(get_all_values(imps, '<-'))
        implementations[p] = {}
        implementations[p]['provides'] = {prov.split(' ')[-2]: prov_values[:, i] for i, prov in enumerate(provides)}
        req_values = np.array(get_all_values(imps, '->'))
        implementations[p]['requires'] = {req.split(' ')[-2]: req_values[:, i] for i, req in enumerate(requires)}
        values[p] = implementations[p]['requires']['invprofit']
        # [float(re.search(r'\d+\.\d+|\d+', term).group()) if re.search(r'\d+\.\d+|\d+', term) else None for term in provides]
        # implementations[p]['requires']

        raw_imps[p] = imps
    
    # print(values)
    # print(implementations)

    game = np.zeros((len(values['player_1']), len(values['player_2']), len(players)))
    
    # check for feasibility
    for i in range(len(values['player_1'])):
        for j in range(len(values['player_2'])):
            game[i, j, 0] = values['player_1'][i]
            game[i, j, 1] = values['player_2'][j]
            for req in implementations['player_1']['requires']:
                if req != 'invprofit' \
                    and implementations['player_1']['requires'][req][i] > implementations['player_2']['provides'][req][j]:
                        game[i, j, :] = np.ones(len(players)) * 10
                        break
            for prov in implementations['player_1']['provides']:
                if implementations['player_1']['provides'][prov][i] < 10:
                    game[i, j, :] = np.ones(len(players)) * 10
                    break

    # print(game[:, :, 0])
    # print(game[:, :, 1])

    # find the Nash equilibrium, needing to minimize. Brute force implementation for now
    for i in range(len(values['player_1'])):
        for j in range(len(values['player_2'])):
            # if i == np.argmin(game[:, j, 0]) and j == np.argmin(game[i, :, 1]):
            if i in np.where(game[:, j, 0] == game[:, j, 0].min())[0] \
                and j in np.where(game[i, :, 1] == game[i, :, 1].min())[0]:
                # print(f'Nash equilibrium: {i, j} \t Value: {game[i, j, :]}')
                # print('Player 1:', raw_imps['player_1'][i])
                # print('Player 2:', raw_imps['player_2'][j])
                # print(f'Nash equilibrium: {i, j}')
                fileoutput += f'{game[i, j, :]}\n'

    with open(outname, 'w') as f:
        f.write(fileoutput)

if __name__ == '__main__':
    players = ['player_1', 'player_2']
    main(players)