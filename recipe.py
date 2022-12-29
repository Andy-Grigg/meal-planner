class Ingredient:
    def __init__(self, amount, unit, name):
        self.amount = amount
        self.unit = unit
        self.name = name

        if not self.name:
            raise ValueError("Ingredient must have a name.")

        if self.unit and not self.amount:
            raise ValueError("Unit can only be specified with a amount.")

    def __repr__(self):
        if self.unit:
            return f"{self.name} ({self.amount} {self.unit})"
        elif self.amount:
            return f"{self.name} ({self.amount})"
        else:
            return self.name
