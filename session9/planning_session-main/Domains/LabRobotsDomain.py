from Domains.Domain import Domain
from Model.Action import Action
from Model.Entity import Entity
from Model.Predicate import Predicate


class LabRobotsDomain(Domain):
    def __init__(self):
        super().__init__("Lab Domain")
        self.RobotA = Entity("A", "Robot")
        self.RobotB = Entity("B", "Robot")
        self.Sample = Entity("Sample1", "Sample")
        self.Chemical = Entity("Chemicals", "Chemical")

        self.entities.append(self.RobotA)
        self.entities.append(self.RobotB)
        self.entities.append(self.Sample)
        self.entities.append(self.Chemical)
        # self.entities.append(self.trunk)

    @Domain.schema
    def Scan_Sample_Start(self, robot, sample):
        if not (robot.name == "A"  and sample.type == "Sample"):
            return None
        is_sample_ready = Predicate("Ready", [sample])
        is_sample_scanned = Predicate("Scanned", [sample])
        is_scan_started = Predicate("ScanStarted", [sample])

        action_name = f"Scan Started"

        return Action(
            action_name,
            [is_sample_ready],
            [is_sample_scanned, is_scan_started],
            [is_scan_started],
            [],
        )

    @Domain.schema
    def Scan_Sample_End(self, robot, sample):
        if not (robot.name == "A" and sample.type == "Sample"):
            return None
        is_scan_started = Predicate("ScanStarted", [sample])
        is_sample_scanned = Predicate("Scanned", [sample])
        is_sample_ready = Predicate("Ready", [sample])
        action_name = f"Scan Ended"

        return Action(
            action_name,
            [is_scan_started],
            [],
            [is_sample_scanned],
            [is_scan_started],
        )


    @Domain.schema
    def Heat_Sample_Start(self, robot, sample):
        if not (robot.name == "A" and sample.type == "Sample"):
            return None
        
        is_sample_scanned = Predicate("Scanned", [sample])
        is_heat_started = Predicate("StartedHeat", [sample])
        is_sample_heated = Predicate("HeatedSample", [sample])
        is_sample_cooled = Predicate("CooledSample", [sample])

        action_name = f"Heat Started"

        return Action(
            action_name,
            [is_sample_scanned], 
            [is_heat_started, is_sample_cooled, is_sample_heated], 
            [is_heat_started], 
            []
        )


    @Domain.schema
    def Heat_Sample_End(self, robot, sample):
        if not (robot.name == "A" and sample.type == "Sample"):
            return None
        
        is_heat_started = Predicate("StartedHeat", [sample])
        is_heat_finished = Predicate("FinishedHeat", [sample])
        is_sample_heated = Predicate("HeatedSample", [sample])
        
        action_name = f"Heat Ended"

    
        return Action(
            action_name,
            [is_heat_started],
            [],
            [is_heat_finished, is_sample_heated],
            [is_heat_started],
        )

    @Domain.schema
    def Cool_Sample_Start(self, robot, sample):
        if not (robot.name == "B" and sample.type == "Sample"):
            return None
        
        is_heat_finished = Predicate("FinishedHeat", [sample])
        is_sample_heated = Predicate("HeatedSample", [sample])
        is_cool_started = Predicate("CoolStarted", [sample])
        
        action_name = f"Cool Started"
        return Action(
            action_name,
            [is_heat_finished, is_sample_heated],
            [is_cool_started],
            [is_cool_started],
            []
        )
    @Domain.schema
    def Cool_Sample_End(self, robot, sample):
        if not (robot.name == "B" and sample.type == "Sample"):
            return None
        is_cool_started = Predicate("CoolStarted", [sample])
        is_sample_cooled = Predicate("CooledSample", [sample])

        action_name = f"Cool Finished"
        return Action(
            action_name,
            [is_cool_started],
            [],
            [is_sample_cooled],
            [is_cool_started]
        )
    
    @Domain.schema
    def Mix_Chemicals_Start(self, robot, chemical):
        if not (robot.name == "B" and chemical.type == "Chemical"):
            return None
        is_chemical_available = Predicate("AvailableChemical", [chemical])
        is_mix_started = Predicate("MixStarted", [chemical])
        is_mix_ended = Predicate("MixEnded", [chemical])

        action_name = "Mix Started"

        return Action(
            action_name,
            [is_chemical_available],           # فقط مواد موجود باشن
            [is_mix_started, is_mix_ended],    # هنوز نه شروع شده نه تموم
            [is_mix_started],                  # MixStarted رو اضافه کن
            []                                 # چیزی حذف نکن
        )
    @Domain.schema
    def Mix_Chemicals_End(self, robot, chemical):
        if not (robot.name == "B" and chemical.type == "Chemical"):
            return None
        is_mix_started = Predicate("MixStarted", [chemical])
        is_chemicals_mixed = Predicate("ChemicalsMixed", [chemical])
        is_mix_ended = Predicate("MixEnded", [chemical])
        action_name = f"Mix Ended"

        return Action(
            action_name, 
            [is_mix_started],
            [],
            [is_chemicals_mixed, is_mix_ended], 
            [is_mix_started]
        )
#  @Domain.schema
#     def remove_action(self, obj, loc):
#         if not (obj.type == "Tire" and loc.type == "Location"):
#             return None
#         at_loc = Predicate("At", [obj, loc])
#         at_action_name = f"Remove({obj.name},{loc.name})"
#         at_ground = Predicate("At", [obj, self.ground])

#         return Action(
#             at_action_name,
#             [at_loc],
#             [],
#             [at_ground],
#             [at_loc],
#         )

#     @Domain.schema
#     def PutOn_action(self, t):
#         if t.type != "Tire":
#             return None
#         at_t = Predicate("At", [t, self.ground])
#         at_axle = Predicate("At", [self.flat, self.axle])
#         at_spare = Predicate("At", [self.spare, self.axle])
#         at_action_name = f"PutOn({t.name},{self.axle.name})"

#         at_t_axle = Predicate("At", [t, self.axle])

#         return Action(
#             at_action_name,
#             [at_t],
#             [at_axle, at_spare],
#             [at_t_axle],
#             [at_t],
#         )