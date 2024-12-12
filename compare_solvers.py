import os
import re
import subprocess
import random

def random_generate_strategies(headers, ranges, num_imps):
    '''
    headers: dictionary of provides and requires for each player, {player: {provides: [val1, val2, ...], requires: [val1, val2, ...]}}
    num_imps: list of number of implementations for each player, [num1, num2, ...]
    '''
    assert len(num_imps) == len(headers.keys()), 'Number of implementations must match number of players'
    strategies = {}
    for j, p in enumerate(headers.keys()):
        strategies[p] = {
            'provides': [],
            'requires': []
        }
        # for req in headers[p]['requires']:
        for _ in range(num_imps[j]):
            strategies[p]['requires'].append([random.randint(ranges[p]['requires'][i][0], ranges[p]['requires'][i][1]) for i in range(len(headers[p]['requires']))])
            strategies[p]['provides'].append([random.randint(ranges[p]['provides'][i][0], ranges[p]['provides'][i][1]) for i in range(len(headers[p]['provides']))])
    
    return strategies

def generate_player(headers, strategies):
    '''
    headers: dictionary of provides and requires for each player, {player: {provides: [val1, val2, ...], requires: [val1, val2, ...]}}
    strategies: dict of players, and values on requires and provides side 
        {player: {requires: [[val1, val2, ...],[val1, val2, ...]], provides: [[val1, val2, ...],[val1, val2, ...]]}}

    '''
    files = {}
    for p in strategies.keys():

        file = 'catalogue{ \n'

        postscripts = {'provides': [], 'requires': []}
        for prov in headers[p]['provides']:
            file += f'    provides    {prov}\n'
            postscripts['provides'].append(re.sub(r'[\[\]]', '', prov.split(' ')[-1]))
        for req in headers[p]['requires']:
            file += f'    requires    {req}\n'
            postscripts['requires'].append(re.sub(r'[\[\]]', '', req.split(' ')[-1]))

        file += '\n'

        reqs = strategies[p]['requires']
        provs = strategies[p]['provides']
        for i, (req, prov) in enumerate(zip(reqs, provs)):
            prov_line = ', '.join([f"{value} {ps}" for value, ps in zip(prov, postscripts['provides'])])
            req_line = ', '.join([f"{value} {ps}" for value, ps in zip(req, postscripts['requires'])])
            file += f'    {prov_line} <- i_{i} -> {req_line}\n'

        file += '}\n'
        files[p] = file
    
    return files

def run_mcdp(output, error):

    if error[0] is not None:
        print("Error:", error)
        return 1

    # outf = output.split('\n')[-2].split(' ')[-1]
    outf = output
    with open(outf, 'r') as f:
        output = f.read()

    match = re.search(r'\{([^}]*)\}', output.split('\n')[-2]).group(1)
    tuples = [tuple(map(float, item.split(','))) for item in re.findall(r'⟨([^⟩]*)⟩', match)]
    return tuples
    # numbers = re.findall(r"Decimal\('([\d\.]+)'\)", output.split('\n')[-3])
    # numbers = [float(num) for num in numbers]

def main(seed = 0):
    
    headers = {
        'player_1': {
            'provides': ['lift [N]'],
            'requires': ['torque [Nm]', 'partcost [USD]', 'invprofit [USD]']
        },   
        'player_2' : {
            'provides': ['torque [Nm]', 'partcost [USD]',],
            'requires': ['power [W]', 'invprofit [USD]']
        }     
    }

    ranges = {
        'player_1': {
            'provides': [(5, 15)],
            'requires': [(5, 15), (3, 8), (3, 9)]
        },
        'player_2': {
            'provides': [(5, 15), (3, 8)],
            'requires': [(5, 15), (3, 9)]
        }
    }
    
    random.seed(seed)
    strategies = random_generate_strategies(headers, ranges, [2, 3])
    # strategies = {
    #     'player_1': {
    #         'provides': [[10], [11]],
    #         'requires': [[10, 10, 4], [11, 12, 3]]
    #     },
    #     'player_2': {
    #         'provides': [[10, 10], [12, 12]],
    #         'requires': [[10, 4], [11, 5.2]]
    #     }
    # }

    files = generate_player(headers, strategies)
    for p in files.keys():
        with open(f'{p}.mcdp', 'w') as f:
            f.write(files[p])
    
    # print('Files generated')

    # Run mcdp
    # First, start the docker container and then run the second command inside it
    # commands = ['''
    #     docker run -it --rm \
    #     -v "$(pwd):$(pwd)" -w "$(pwd)" \
    #     zupermind/mcdp:2024 bash -c "mcdp-solve-query system_all"
    #     ''',
    #     '''
    #     docker run -it --rm \
    #     -v "$(pwd):$(pwd)" -w "$(pwd)" \
    #     zupermind/mcdp:2024 bash -c "mcdp-solve-query system_profit"
    #     '''
    # ]
    # pwd = '/Users/victorqin/Documents/MIT_G4_2024-25/1.S980\ Category\ Theory/game_theoretic.mcdplib/'
    commands = [
        [ 'docker', 'run', '-it', '--rm', '-v', f'{os.getcwd()}:{os.getcwd()}', '-w', f'{os.getcwd()}', 
         'zupermind/mcdp:2024', 'bash', '-c', 'mcdp-solve-query system_all --out out/output_all'],# '--out', 'out/output_all'],
        [ 'docker', 'run', '-it', '--rm', '-v', f'{os.getcwd()}:{os.getcwd()}', '-w', f'{os.getcwd()}', 
         'zupermind/mcdp:2024', 'bash', '-c', 'mcdp-solve-query system_profit --out out/output_profit'],# '--out', 'out/output_profit']
    ]

    # Execute the command
    # result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    read_from = ['out/output_all/output.yaml', 'out/output_profit/output.yaml']
    mcdp_results = []
    # output = {i: '' for i in range(len(commands))}
    processes = [subprocess.Popen(command, shell=False, stderr=subprocess.PIPE, text=True) for command in commands]
    for i, process in enumerate(processes):
        error = process.communicate()
        out = run_mcdp(read_from[i], error)
        mcdp_results.append(out)

    # for line in mcdp_results:
    #     print(str(line))

    # run Nash Equilibrium
    command = ['python', 'matrix_game.py']  
    process = subprocess.Popen(command, shell=False, stderr=subprocess.PIPE, text=True)
    error = process.communicate()
    # Step 1: Split the string by lines and remove empty lines
    with open('out/matrix_game.out', 'r') as f:
        output = f.read()
    lines = output.strip().split('\n')

    result = []
    for line in lines:
        numbers = line.strip('[]').split()
        result.append(tuple(float(num) for num in numbers))
    # print(str(result))
    # prune nonfeasible entries
    result = [r for r in result if r != (10.0, 10.0)]

    if len(mcdp_results[1]) >= 1:
        if len(result) > 1:
            for res in mcdp_results[1]:
                assert res in result
            for res in result:
                assert res in mcdp_results[1]
        else:
            assert mcdp_results[1] == result, 'Results do not match'
    else:
        print('empty')
        assert result == []

    return mcdp_results, result

if __name__ == '__main__':
    for k in range(0, 100):
        print(k)
        mcdp, matrix = main(k)
        print(mcdp[1])
        print(matrix)