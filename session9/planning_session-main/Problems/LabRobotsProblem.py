from Domains.Domain import Domain
from Model.Predicate import Predicate
from Model.State import State
from Problems.Problem import Problem


# class Tire(Problem):
#     def __init__(self, domain: Domain):
#         super().__init__(domain)

#         at_flat_axle = Predicate("At", [domain.flat, domain.axle])

#         at_spare_trunk = Predicate("At", [domain.spare, domain.trunk])

#         self.initial_state = State(
#             "",
#             [at_flat_axle, at_spare_trunk],
#         )

#         at_spare_axel = Predicate("At", [domain.spare, domain.axle])
#         at_flat_ground = Predicate("At", [domain.flat, domain.ground])

#         self.goal_state = State("", [at_spare_axel, at_flat_ground])

class LabRobotsProblem(Problem):
    def __init__(self, domain: Domain):
        super().__init__(domain)
        # is_sample_ready = Predicate("Ready", [sample])
        sample_on_table_and_ready = Predicate("Ready", [domain.Sample])
        is_chemical_available = Predicate("AvailableChemical", [domain.Chemical])


        self.initial_state = State(
            "",
            [sample_on_table_and_ready, is_chemical_available],
        )

        is_sample_scanned = Predicate("Scanned", [domain.Sample])
        is_sample_heated = Predicate("HeatedSample", [domain.Sample])
        is_sample_cooled = Predicate("CooledSample", [domain.Sample])
        is_chemicals_mixed = Predicate("ChemicalsMixed", [domain.Chemical])
        self.goal_state = State("", [is_sample_scanned, is_sample_heated, is_sample_cooled, is_chemicals_mixed])

        

