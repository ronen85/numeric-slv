import json
import os
from pathlib import Path

from numeric_slv.main import get_automatic_goal_affiliation
from translate import pddl_parser

sailing_dir = Path(os.path.join(os.path.dirname(__file__), '..', 'pddl_files', 'sailing')).absolute()
sailing_domain_file_name = 'domain.pddl'
sailing_problem_file_names = \
    ['prob_2_1_1229.pddl', 'prob_2_2_1229.pddl', 'prob_2_3_1229.pddl', 'prob_2_4_1229.pddl', 'prob_2_5_1229.pddl',
     'prob_3_1_1229.pddl', 'prob_3_2_1229.pddl', 'prob_3_3_1229.pddl', 'prob_3_4_1229.pddl', 'prob_3_5_1229.pddl',
     'prob_4_1_1229.pddl', 'prob_4_2_1229.pddl', 'prob_4_3_1229.pddl', 'prob_4_4_1229.pddl', 'prob_4_5_1229.pddl',
     'prob_5_1_1229.pddl', 'prob_5_2_1229.pddl', 'prob_5_3_1229.pddl', 'prob_5_4_1229.pddl', 'prob_5_5_1229.pddl']


for p_name in sailing_problem_file_names:
    p_path, domain_path  = str(sailing_dir / p_name), str(sailing_dir / sailing_domain_file_name)
    t = pddl_parser.open_pddl(domain_path, p_path)
    goal_affiliation = get_automatic_goal_affiliation(t)
    info_dict = {"waitfor": [],
                 "num_waitfor": [],
                 "goal_affiliation": goal_affiliation}
    json_object = json.dumps(info_dict)
    j_path = p_path.replace('.pddl', '.json')
    with open(j_path, "w") as outfile:
        outfile.write(json_object)
    print()
print()