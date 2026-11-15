
import mesa


class Person(mesa.Agent):
    def __init__(self, model, x, y):
        super().__init__(model)
        self.x = x
        self.y = y
        self.active = True

    def step(self):
        # Find all zombies
        zombies = [a for a in self.model.agents if isinstance(a, Zombie)]

        if zombies:
            nearest = min(zombies, key=lambda z: self.model.distance(self, z))

            # Run away if a zombie is nearby
            if self.model.distance(self, nearest) <= 4:
                self.model.move_away(self, nearest)
                return

        self.model.move_randomly(self)


class Zombie(mesa.Agent):
    def __init__(self, model, x, y):
        super().__init__(model)
        self.x = x
        self.y = y
        self.active = True

    def step(self):
        # Find all people
        people = [a for a in self.model.agents if isinstance(a, Person)]

        if not people:
            self.model.move_randomly(self)
            return

        nearest = min(people, key=lambda p: self.model.distance(self, p))

        # Chase the nearest person
        if self.model.distance(self, nearest) <= 6:
            self.model.move_toward(self, nearest)
        else:
            self.model.move_randomly(self)

        # Infect a person in the same cell
        for person in people:
            if person.active and self.x == person.x and self.y == person.y:
                if self.random.random() < self.model.infection_chance:
                    person.active = False
                    x, y = person.x, person.y

                    person.remove()
                    Zombie(self.model, x, y)

                    self.model.infections += 1
                    break


class Doctor(mesa.Agent):
    def __init__(self, model, x, y):
        super().__init__(model)
        self.x = x
        self.y = y
        self.active = True

    def step(self):
        # Find all zombies
        zombies = [a for a in self.model.agents if isinstance(a, Zombie)]

        if not zombies:
            self.model.move_randomly(self)
            return

        nearest = min(zombies, key=lambda z: self.model.distance(self, z))

        # Move toward the nearest zombie
        if self.model.distance(self, nearest) <= 6:
            self.model.move_toward(self, nearest)
        else:
            self.model.move_randomly(self)

        # Heal a zombie in the same cell
        if nearest.active and self.x == nearest.x and self.y == nearest.y:
            if self.random.random() < self.model.healing_chance:
                nearest.active = False
                x, y = nearest.x, nearest.y

                nearest.remove()
                Person(self.model, x, y)

                self.model.healings += 1
