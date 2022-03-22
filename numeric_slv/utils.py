import os
import re
import string
import subprocess
from subprocess import Popen, PIPE
from threading import Timer
import shlex
from pathlib import Path
from .config import FD_PATH

def read_file(file_path):
    if isinstance(file_path, str):
        file_path = Path(file_path)
    assert file_path.is_file(), f'expected a file in {file_path}'
    with open(str(file_path), 'r') as f:
        res = f.read()
    return res

def solve_pddl(domain_path, problem_path):
    executable = Path(FD_PATH) / 'src/translate/translate.py'
    domain_path, problem_path = Path(domain_path), Path(problem_path)
    # sanity check
    assert executable.is_file(), f'{executable} should be a file'
    assert domain_path.is_file(), f'{domain_path} should be a file'
    assert problem_path.is_file(), f'{problem_path} should be a file'
    # compiling a command
    print()


def get_sas_translation(domain, problem):
    executable = Path(FD_PATH) / 'src/translate/translate.py'
    domain, problem = Path(domain), Path(problem)
    # sanity check
    assert executable.is_file(), f'{executable} should be a file'
    assert domain.is_file(), f'{domain} should be a file'
    assert problem.is_file(), f'{problem} should be a file'
    # compiling a command
    res = subprocess.run(['python2.7', str(executable), str(domain), str(problem)], capture_output=True)
    assert 'Done!' in str(res.stdout, encoding='utf-8'), 'Translation process should have output "Done!"'
    # return sas file as list
    sas_file = Path(os.getcwd()) / 'output.sas'
    assert sas_file.is_file(), f'{sas_file} should be a file'
    with sas_file.open('r') as f:
        sas_as_list = [l for l in f]
    return sas_as_list


def replace_punctuation(s, replace=' '):
    """
    replaces punctuation (/*-+...) with 'replace'
    """
    chars = re.escape(string.punctuation)
    return re.sub(r'[' + chars + ']', replace, s)


def solve_pddl(domain, problem, timeout=10.):
    """
    input:
    domain, problem: path to domain and problem pddl files
    return the output of the planner
    """
    executable = Path(FD_PATH) / 'fast-downward.py'
    domain, problem = Path(domain), Path(problem)
    # sanity check
    assert executable.is_file(), f'{executable} should be a file'
    assert domain.is_file(), f'{domain} should be a file'
    assert problem.is_file(), f'{problem} should be a file'
    output_path = problem.parent / problem.name.replace('.pddl', '.output')
    output_path.unlink(missing_ok=True)
    sas_plan_path = problem.parent / problem.name.replace('.pddl', '.sas_plan')
    sas_plan_path.unlink(missing_ok=True)
    # compiling a command
    cmd = f'/usr/bin/python {str(executable)} --build=release64  --plan-file={str(sas_plan_path)} {str(domain)} {str(problem)} --search "astar(blind)" > {str(output_path)}'
    # running planner
    is_timeout = False
    try:
        subprocess.call(cmd, timeout=5, shell=True)
    except subprocess.TimeoutExpired:
        is_timeout = True
        print('timeout!')
    # parse result
    info = dict(solved=False, plan=[], reached_timeout=is_timeout)
    if (not is_timeout) and (output_path.is_file()):
        output = read_file(output_path)
        if 'Solution found.' in output:
            info['solved'] = True
            assert sas_plan_path.is_file(), f'expected a plan file in {sas_plan_path}'
            sas_plan = read_file(sas_plan_path)
            info['plan'] = sas_plan
    return info
