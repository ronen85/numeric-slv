import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import logging
import os
import sys
from collections import namedtuple
from pathlib import Path

from numeric_slv.main import Compilation
from numeric_slv.task_to_pddl import get_pddl_domain, get_pddl_prob
from numeric_slv.utils import solve_task, write_file, solve_pddl

Exp = namedtuple('Exp', 'dir_path, domain_file, problem_files, info_files')

depots_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'pddl_files', 'depots_multiagents')).absolute()
depots_domain_file_name = 'domain.pddl'
depots_problem_file_names = [f'pfile{x}.pddl' for x in range(1, 21)]
depots_info_file_names = [f'pfile{x}.json' for x in range(1, 21)]
depots_exp = Exp(depots_dir, depots_domain_file_name, depots_problem_file_names, depots_info_file_names)

gripper_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'pddl_files', 'multi_gripper')).absolute()
gripper_domain_file_name = 'domain.pddl'
gripper_problem_file_names = [f'prob0{x}.pddl' for x in range(1, 10)] + [f'prob{x}.pddl' for x in range(10, 21)]
gripper_info_file_names = [s.replace('.pddl', '.json') for s in gripper_problem_file_names]
gripper_exp = Exp(gripper_dir, gripper_domain_file_name, gripper_problem_file_names, gripper_info_file_names)

exp_dict = dict(depots=depots_exp, gripper=gripper_exp)


def main(domain_name, problem_nr, timeout):

    def get_logger():
        logger = logging.getLogger(f'exp_{domain_name}_{problem_nr}')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        fh = logging.FileHandler(str(problem_path).replace('.pddl', '.log'), 'w+')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(stdout_handler)
        return logger

    dir_path, domain_file, problem_files, info_files = exp_dict[domain_name]
    domain_path = dir_path / domain_file
    problem_path = dir_path / problem_files[problem_nr-1]
    info_path = dir_path / info_files[problem_nr-1]
    logger = get_logger()
    logger.info(f"domain::{domain_name} problem_nr::{problem_nr} timeout::{timeout}")
    logger.info("starting compilation...")
    compilation = Compilation(domain_path, problem_path, info_path, logger=logger.info)
    compiled_task = compilation.compiled_task
    logger.info("writing compiled files to disk...")
    compiled_domain_file_path = Path(str(problem_path).replace('.pddl', '_compiled_domain.pddl'))
    compiled_prob_file_path = Path(str(problem_path).replace('.pddl', '_compiled_problem.pddl'))
    write_file(get_pddl_domain(compiled_task), compiled_domain_file_path.absolute())
    write_file(get_pddl_prob(compiled_task), compiled_prob_file_path.absolute())
    logger.info("done.")
    # solve
    logger.info("solving compiled problem...")
    res = solve_pddl(compiled_domain_file_path.absolute(), compiled_prob_file_path.absolute(),
                     timeout, logger=logger.info)
    logger.info("exp_completed::True")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_name", type=str, choices=exp_dict.keys())
    parser.add_argument("problem_nr", type=int, choices=list(range(1, 21)))
    parser.add_argument("-timeout", type=int, default=60*30)
    args = parser.parse_args()
    main(args.domain_name, args.problem_nr, args.timeout)
