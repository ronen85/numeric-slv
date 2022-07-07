import os
import re
import string
import subprocess
import time
import uuid
from subprocess import Popen, PIPE
from threading import Timer
import shlex
from pathlib import Path
from .config import FD_PATH
from .task_to_pddl import get_pddl_domain, get_pddl_prob


def read_file(file_path):
    if isinstance(file_path, str):
        file_path = Path(file_path)
    assert file_path.is_file(), f'expected a file in {file_path}'
    with open(str(file_path), 'r') as f:
        res = f.read()
    return res


def write_file(str_to_write, file_path, rewrite=True):
    assert isinstance(str_to_write, str), f'expected str, got: {str_to_write}'
    assert isinstance(file_path, str) or isinstance(file_path, Path), f'expected str/Path, got: {file_path}'
    if isinstance(file_path, str):
        file_path = Path(file_path)
    if file_path.is_file():
        if rewrite:
            file_path.unlink()
        else:
            print("file exists!")
            return
    with open(str(file_path.absolute()), 'w') as f:
        f.write(str_to_write)
    return


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


def get_tmp_dir_path():
    return Path(os.path.abspath(os.path.join(os.path.dirname(__file__), '../tmp')))


def solve_task(task, timeout=10., logger=None):
    tmp_dir_path = get_tmp_dir_path()
    rand_key = str(uuid.uuid4())[:6]
    domain_file_name = '_'.join([rand_key, task.domain_name + '.pddl'])
    prob_file_name = '_'.join([rand_key, task.task_name + '.pddl'])
    domain_file_path = tmp_dir_path / domain_file_name
    prob_file_path = tmp_dir_path / prob_file_name
    # write files to path
    write_file(get_pddl_domain(task), domain_file_path.absolute())
    write_file(get_pddl_prob(task), prob_file_path.absolute())
    # solve
    res = solve_pddl(domain_file_path.absolute(), prob_file_path.absolute(), timeout, logger=logger)
    # delete files
    domain_file_path.unlink(missing_ok=True)
    prob_file_path.unlink(missing_ok=True)
    return res


def solve_pddl(domain, problem, timeout=10., logger=None):
    """
    input:
    domain, problem: path to domain and problem pddl files
    return the output of the planner
    """
    if logger==None:
        logger = print
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
    sol_time = ''
    try:
        begin = time.time()
        subprocess.call(f'timeout {int(timeout+1)} ' + cmd, timeout=timeout, shell=True, )
        sol_time = round(time.time() - begin, 3)
        logger(f"solving_time::{sol_time}")
    except subprocess.TimeoutExpired:
        is_timeout = True
        logger(f"solving_time::timeout")
    # parse result
    info = dict(solved=False, plan=[], reached_timeout=is_timeout, sol_time=sol_time)
    if output_path.is_file():
        logger(f"output_file::{output_path.name}")
        if not is_timeout:
            output = read_file(output_path)
            if 'Solution found.' in output:
                info['solved'] = True
                logger(f"solution_found::True")
                assert sas_plan_path.is_file(), f'expected a plan file in {sas_plan_path}'
                sas_plan = read_file(sas_plan_path)
                plan = [s.strip('()').strip() for s in sas_plan.split('\n')]
                plan = list(filter(lambda x: bool(x), map(lambda x: x.index(';') if ';' in x else x, plan)))
                info['plan'] = plan
                logger(f"plan::{','.join(plan)}")
            else:
                logger(f"solution_found::False")
    else:
        logger(f"output_file::not_found")
    return info
