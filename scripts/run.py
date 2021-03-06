import argparse
import logging
import os
import sys
from collections import namedtuple
from copy import deepcopy
from pathlib import Path

from translate.pddl import Atom, NegatedAtom, Function

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

rover_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'pddl_files', 'rover')).absolute()
rover_domain_file_name = 'domain.pddl'
rover_problem_file_names = [f'pfile{x}.pddl' for x in range(2, 21)]
rover_info_file_names = [s.replace('.pddl', '.json') for s in rover_problem_file_names]
rover_exp = Exp(rover_dir, rover_domain_file_name, rover_problem_file_names, rover_info_file_names)

sailing_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'pddl_files', 'sailing')).absolute()
sailing_domain_file_name = 'domain.pddl'
sailing_problem_file_names = \
    ['prob_2_1_1229.pddl', 'prob_2_2_1229.pddl', 'prob_2_3_1229.pddl', 'prob_2_4_1229.pddl', 'prob_2_5_1229.pddl',
    'prob_3_1_1229.pddl', 'prob_3_2_1229.pddl', 'prob_3_3_1229.pddl', 'prob_3_4_1229.pddl', 'prob_3_5_1229.pddl',
    'prob_4_1_1229.pddl', 'prob_4_2_1229.pddl', 'prob_4_3_1229.pddl', 'prob_4_4_1229.pddl', 'prob_4_5_1229.pddl',
    'prob_5_1_1229.pddl', 'prob_5_2_1229.pddl', 'prob_5_3_1229.pddl', 'prob_5_4_1229.pddl', 'prob_5_5_1229.pddl']
sailing_info_file_names = [s.replace('.pddl', '.json') for s in sailing_problem_file_names]
sailing_exp = Exp(sailing_dir, sailing_domain_file_name, sailing_problem_file_names, sailing_info_file_names)

exp_dict = dict(depots=depots_exp, gripper=gripper_exp, rover=rover_exp, sailing=sailing_exp)


def main(domain_name, problem_nr, timeout, planner):

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
    res = solve_pddl(compiled_domain_file_path.absolute(),
                     compiled_prob_file_path.absolute(),
                     timeout, logger=logger.info, planner=planner)
    logger.info("exp_completed::True")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("domain_name", type=str, choices=exp_dict.keys())
    parser.add_argument("problem_nr", type=int, choices=list(range(1, 21)))
    parser.add_argument("-timeout", type=int, default=60*30)
    parser.add_argument("-planner", type=str, default='ff', choices=['fd', 'ff'])
    args = parser.parse_args()
    main(domain_name=args.domain_name,
         problem_nr=args.problem_nr,
         timeout=args.timeout,
         planner=args.planner)
