from itertools import product

arg1_list = ['depots', 'gripper']
arg2_list = list(range(1,21))
arguments = list(product(arg1_list, arg2_list))
cmd_list = [f'python run.py {a} {b}\n' for a,b in arguments]
test_file = 'test.sh'
with open(test_file, 'w') as f:
    f.writelines(cmd_list)
