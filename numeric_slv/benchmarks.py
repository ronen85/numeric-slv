import os
from os.path import join as opj
from pathlib import Path

pddl_files_dir = Path(opj(os.path.dirname(__file__), '..', 'pddl_files'))

multi_gripper_0_dir = pddl_files_dir / 'multi_gripper/adapted_0'
multi_gripper_0_domain = multi_gripper_0_dir / 'domain.pddl'
multi_gripper_0_problems = [multi_gripper_0_dir / f'prob01.pddl']
multi_gripper_0_jsons = [multi_gripper_0_dir / p.name.replace('.pddl', '.json') for p in multi_gripper_0_problems]

lunch_0_dir = pddl_files_dir / 'lunch/lunch_0'
lunch_0_domain = lunch_0_dir / 'domain.pddl'
lunch_0_problems = [lunch_0_dir / f'prob01.pddl']
lunch_0_jsons = [lunch_0_dir / p.name.replace('.pddl', '.json') for p in lunch_0_problems]

domain_dict = dict(lunch_0=lunch_0_domain, multi_gripper_0=multi_gripper_0_domain)
problem_list_dict = dict(lunch_0=lunch_0_problems, multi_gripper_0=multi_gripper_0_problems)
json_list_dict = dict(lunch_0=lunch_0_jsons, multi_gripper_0=multi_gripper_0_jsons)
