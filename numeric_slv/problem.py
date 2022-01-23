from translate import pddl_parser

from numeric_slv import utils



class SocialPlanningProblem:

    def __init__(self, domain_filename, prob_filename):
        self.domain_filename, self.prob_filename = domain_filename, prob_filename
        self.task = pddl_parser.open_pddl(domain_filename, prob_filename)
        self.sas_translation_list = utils.get_sas_translation(domain_filename, prob_filename)
        self.domain_name = self.task.domain_name
        self.problem_name = self.task.task_name
        self.predicates = self.get_grounded_predicates_from_sas_list(self.sas_translation_list)
        self.variables = None
        self.init = None
        self.num_init = None
        self.actions = None
        self.goal = None
        self.num_goal = None

    def get_grounded_predicates_from_sas_list(self, sas_list):
        ll = [l.strip() for l in sas_list if l.startswith('Atom')]
        names = [l.replace('Atom ', '').split('(')[0] for l in ll]
        preds = []
        return preds





class Predicate:
    def __init__(self, name, arguments):
        self.name = name  # str
        self.arguments = arguments  # list of TypedObject

    def __str__(self):
        return f"Predicate: {self.name} ({', '.join(map(str, self.arguments))})"


class Function:
    def __init__(self, name, arguments):
        self.name = name  # str
        self.arguments = arguments  # list of TypedObject

    def __str__(self):
        return f"Function: {self.name} ({', '.join(map(str, self.arguments))})"


class NumericInitialState:
    pass


class Action:
    pass


class PropositionalGoal:
    pass


class NumericGoal:
    pass
