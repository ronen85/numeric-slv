import numeric_slv

domain = '/home/ronenn/projects/numeric-slv/pddl_files/depots/domain.pddl'
prob = '/home/ronenn/projects/numeric-slv/pddl_files/depots/pfile1.pddl'

# task = pddl_parser.open_pddl(domain_filename=domain, task_filename=prob)
spp = numeric_slv.SocialPlanningProblem(domain, prob)


print('ok')