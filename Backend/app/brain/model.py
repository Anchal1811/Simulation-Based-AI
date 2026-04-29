from dowhy import CausalModel

class CausalBrain:
    def __init__(self, data):
        self.model = CausalModel(
            data=data,
            treatment='Treatment',
            outcome='Recovery',
            common_causes=['Age']
        )

    def get_estimate(self):
        identified_estimand = self.model.identify_effect()
        estimate = self.model.estimate_effect(
            identified_estimand,
            method_name="backdoor.linear_regression"
        )
        return estimate.value