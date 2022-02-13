import os
import subprocess
from pathlib import Path
from .config import FD_PATH

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