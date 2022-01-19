from translate import pddl
from translate import pddl_parser

domain = '/home/ronenn/projects/numeric-slv/pddl_files/depots/domain.pddl'
prob = '/home/ronenn/projects/numeric-slv/pddl_files/depots/pfile1.pddl'

task = pddl_parser.open_pddl(domain_filename=domain, task_filename=prob)
print('ok')