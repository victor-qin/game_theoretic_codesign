import os
import yaml
import re
import subprocess

# Solve for the Cournot game without cooperation; get the Nash equilibrium


    # commands = [
    #     [ 'docker', 'run', '-it', '--rm', '-v', f'{os.getcwd()}:{os.getcwd()}', '-w', f'{os.getcwd()}',
    #      'zupermind/mcdp:2024', 'bash', '-c', 'mcdp-solve-query system_all --out out/output_all'],# '--out', 'out/output_all'],
    #     [ 'docker', 'run', '-it', '--rm', '-v', f'{os.getcwd()}:{os.getcwd()}', '-w', f'{os.getcwd()}',
    #      'zupermind/mcdp:2024', 'bash', '-c', 'mcdp-solve-query system_profit --out out/output_profit'],# '--out', 'out/output_profit']
    # ]

    # # Execute the command
    # # result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # read_from = ['out/output_all/output.yaml', 'out/output_profit/output.yaml']
    # mcdp_results = []

def read_mcdp(output, error):

    if error[0] is not None:
        print("Error:", error)
        return 1

    # outf = output.split('\n')[-2].split(' ')[-1]
    outf = output
    with open(outf, 'r') as f:
        output = yaml.safe_load(f)

    # match = re.search(r'\{([^}]*)\}', output.split("\n")[-2]).group(1)
    # lines = re.split(r'\n|\\n', output)
    # match = re.search(r'\{([^}]*)\}', lines[-2]).group(1)
    tuples = [tuple(map(float, item.split(','))) for item in re.findall(r'⟨([^⟩]*)⟩', output['pessimistic']['pretty'])]
    return tuples

def solve_queries(filenames):
    '''
    Solve z1 and then z1 + x1 games - this finds the x1 that is optimal for the z1 game
    Arguments:
        filenames: list of filenames to solve
    Returns:
        mcdp_results: list of tuples with the results
    '''
    commands = []
    read_from = []
    for filename in filenames:
        command = ['docker', 'run', '-it', '--rm', '-v', f'{os.getcwd()}:{os.getcwd()}', '-w', f'{os.getcwd()}',
                   'zupermind/mcdp:2024', 'bash', '-c', f'mcdp-solve-query --optimistic 150 --pessimistic 150 {filename} --out out/{filename}']
        commands.append(command)
        read_from.append(f'out/{filename}/output.yaml')

    processes = [subprocess.Popen(command, shell=False, stderr=subprocess.PIPE, text=True) for command in commands]
    mcdp_results = []
    for i, process in enumerate(processes):
        error = process.communicate()
        out = read_mcdp(read_from[i], error)
        mcdp_results.append(out)

    return mcdp_results

def main():

    # step size:
    alpha = 0.6

    # Change the working directory to the folder (cournot_operations)
    current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Changed working directory to: {current_dir}")
    query_suffix = '.mcdp_query.yaml'
    query_filename = 'test_v2'
    z1_filename = 'test_v2_z1'
    z2_filename = 'test_v2_z2'
    z1_x1_filename = 'test_v2_z1_x1'
    z2_x2_filename = 'test_v2_z2_x2'
    # commands = [
    #     [ 'docker', 'run', '-it', '--rm', '-v', f'{os.getcwd()}:{os.getcwd()}', '-w', f'{os.getcwd()}',
    #      'zupermind/mcdp:2024', 'bash', '-c', f'mcdp-solve-query {z1_filename} --out out/output_all'],# '--out', 'out/output_all'],
    #     [ 'docker', 'run', '-it', '--rm', '-v', f'{os.getcwd()}:{os.getcwd()}', '-w', f'{os.getcwd()}',
    #      'zupermind/mcdp:2024', 'bash', '-c', f'mcdp-solve-query {z1_x1_filename} --out out/output_profit'],# '--out', 'out/output_profit']
    # ]

    # Load the model
    with open('test_v2.mcdp', 'r') as f:
        model = f.read()

    x1_old = float(re.search(r'[0-9]*\.[0-9]+',re.search(r'c1 = [0-9]*\.[0-9]+ dimensionless', model).group(0)).group(0))
    x2_old = float(re.search(r'[0-9]*\.[0-9]+',re.search(r'c2 = [0-9]*\.[0-9]+ dimensionless', model).group(0)).group(0))

    # make sure model has x1 and x2 set to 0
    model = model.replace(f'c1 = {x1_old}', f'c1 = 0.0').replace(f'c2 = {x2_old}', f'c2 = 0.0')
    x1_old = 0.0
    x2_old = 0.0

    # Load the original YAML file
    with open(query_filename + query_suffix, 'r') as f:
        config = yaml.safe_load(f)

    error = 1.0
    count = 0
    while error > 0.01 and count < 10:

        '''x1 side'''
        with open('test_v2.mcdp', 'w') as f:
            f.write(model.replace(f'c1 = 0.0', f'c1 = 0.0').replace(f'c2 = 0.0', f'c2 = {x2_old}'))

        # solve for the z1 game
        config['query']['optimize_for'] = ['z1']
        with open(z1_filename + query_suffix, 'w') as f:
            yaml.dump(config, f)

        # solve for the x1 and z1 game,
        config['query']['optimize_for'] = ['z1', 'x1']
        with open(z1_x1_filename + query_suffix, 'w') as f:
            yaml.dump(config, f)

        output = solve_queries([z1_filename, z1_x1_filename])

        # get the x1 value for the best z1
        assert len(output[0]) <= 1, \
            ValueError("More than one solution found for z1")
        z1 = output[0][0][0]
        x1 = [i[1] for i in output[1] if i[0] == z1]
        assert len(x1) <= 1, \
            ValueError("More than one solution found for x1")
        x1 = x1[0]


        # force x1 to be at the value found - c1
        # with open('test_v2.mcdp', 'w') as f:
        #     f.write(model.replace(f'c1 = 0.0', f'c1 = {x1}'))
        x1_error = abs(x1 - x1_old)
        x1_old = x1_old + alpha * (x1 - x1_old)
        print('x1', x1, 'z1', z1, 'x1_old', x1_old)

        '''x2 side'''
        with open('test_v2.mcdp', 'w') as f:
            # f.write(model.replace(f'c2 = {x2_old}', f'c2 = 0.0'))
            f.write(model.replace(f'c1 = 0.0', f'c1 = {x1_old}').replace(f'c2 = 0.0', f'c2 = 0.0'))

        # solve for the z1 game
        config['query']['optimize_for'] = ['z2']
        with open(z2_filename + query_suffix, 'w') as f:
            yaml.dump(config, f)

        # solve for the x1 and z1 game,
        config['query']['optimize_for'] = ['z2', 'x2']
        with open(z2_x2_filename + query_suffix, 'w') as f:
            yaml.dump(config, f)

        output = solve_queries([z2_filename, z2_x2_filename])

        # get the x1 value for the best z1
        assert len(output[0]) <= 1, \
            ValueError("More than one solution found for z1")
        z2 = output[0][0][0]
        x2 = [i[1] for i in output[1] if i[0] == z2]
        assert len(x2) <= 1, \
            ValueError("More than one solution found for x1")
        x2 = x2[0]


        # force x1 to be at the value found - c1
        # with open('test_v2.mcdp', 'w') as f:
        #     f.write(model.replace(f'c2 = 0.0', f'c2 = {x2}'))
        x2_error = abs(x2 - x2_old)
        x2_old = x2_old + alpha * (x2 - x2_old)
        print('x2', x2, 'z2', z2, 'x2_old', x2_old)

        error = max(x1_error, x2_error)
        print(f'Error: {error}')
        count += 1

    print(f'Final x1: {x1}, x2: {x2}, z1: {z1}, z2: {z2}, x1_old: {x1_old}, x2_old: {x2_old}, count: {count}')

if __name__ == '__main__':
    main()