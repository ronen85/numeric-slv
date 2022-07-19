import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from numeric_slv.main import get_automatic_goal_affiliation
from translate import pddl_parser

rover_path = Path(os.path.abspath('..')) / 'pddl_files' / 'rover'
domain_path = str((rover_path / 'domain.pddl').absolute())
prob_list = [str(p.absolute()) for p in rover_path.glob('pfile*pddl')]
prob_list.sort()
json_file_names = [p.replace('.pddl', '.json') for p in prob_list]
for p_path, j_path in zip(prob_list, json_file_names):
    t = pddl_parser.open_pddl(domain_path, p_path)
    goal_affiliation = get_automatic_goal_affiliation(t)
    info_dict = {"waitfor": [],
                 "num_waitfor": [],
                 "goal_affiliation": goal_affiliation}
    json_object = json.dumps(info_dict)
    with open(j_path, "w") as outfile:
        outfile.write(json_object)
    print()