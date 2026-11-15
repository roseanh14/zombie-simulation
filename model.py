
import mesa
from agents import Person, Zombie, Doctor


class ZombieModel(mesa.Model):
    def __init__(self, width=20, height=20, people=100, zombies=10,
                 doctors=0, infection_chance=0.3, healing_chance=0.6,
                 seed=None):

        super().__init__(seed=seed)

        if width < 2 or height < 2:
            raise ValueError("Map must be at least 2 x 2")

        self.width = width
        self.height = height
        self.infection_chance = infection_chance
        self.healing_chance = healing_chance

        self.infections = 0
        self.healings = 0
        self.history = []

        # Create people
        for _ in range(people):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            Person(self, x, y)

        # Create zombies
        for _ in range(zombies):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            Zombie(self, x, y)

        # Create doctors
        for _ in range(doctors):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            Doctor(self, x, y)

        self.record(0)

    def distance(self, first, second):
        return abs(first.x - second.x) + abs(first.y - second.y)

    def options(self, agent):
        choices = []

        # Possible movements: up, down, right, left
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x = agent.x + dx
            y = agent.y + dy

            # Prevent movement outside the map
            if 0 <= x < self.width and 0 <= y < self.height:
                choices.append((x, y))

        return choices

    def move_randomly(self, agent):
        agent.x, agent.y = self.random.choice(self.options(agent))

    def move_toward(self, agent, target):
        choices = self.options(agent)

        best = min(
            abs(x - target.x) + abs(y - target.y)
            for x, y in choices
        )

        choices = [
            (x, y) for x, y in choices
            if abs(x - target.x) + abs(y - target.y) == best
        ]

        agent.x, agent.y = self.random.choice(choices)

    def move_away(self, agent, target):
        choices = self.options(agent)

        best = max(
            abs(x - target.x) + abs(y - target.y)
            for x, y in choices
        )

        choices = [
            (x, y) for x, y in choices
            if abs(x - target.x) + abs(y - target.y) == best
        ]

        agent.x, agent.y = self.random.choice(choices)

    def counts(self):
        agents = list(self.agents)

        people = sum(isinstance(a, Person) for a in agents)
        zombies = sum(isinstance(a, Zombie) for a in agents)
        doctors = sum(isinstance(a, Doctor) for a in agents)

        return people, zombies, doctors

    def record(self, step):
        people, zombies, doctors = self.counts()

        self.history.append({
            "step": step,
            "people": people,
            "zombies": zombies,
            "doctors": doctors,
            "infections": self.infections,
            "healings": self.healings
        })

    def step(self):
        # Execute agents in random order
        agents = list(self.agents)
        self.random.shuffle(agents)

        for agent in agents:
            if agent.active:
                agent.step()

        self.record(len(self.history))
