#todo: Find somewhere better than models to put this

class AlarmSpecification:

    def __init__(self, expected_value=None, variance=None):
        self._rules = set()
        
        if (expected_value is not None) and (variance is not None):
            self.add_rule(
                ((lambda x: x < expected_value - variance),
                 "below expected value"))
            self.add_rule(
                ((lambda x: x > expected_value + variance),
                 "above expected value"))
        
    @property
    def rules(self):
        """
        get the rules governing this specification
        """
        return self._rules

    def add_rule(self, rule):
        """
        add to this alarm specifications rule set
        """
        assert (hasattr(rule[0], '__call__')),\
            "rule must be callable"

        assert (isinstance(rule[1], str)),\
            "must include failure string"
        self.rules.add(rule)

    def satisfied_by(self, reading):
        """
        return whether the given reading evaluates to true for all rules in 
        this specification's ruleset.
        """
        ret = True
        for rule in self.rules:
            ret = ret and rule[0](reading)

        return ret
    
