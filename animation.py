
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from agents import Person, Zombie, Doctor
from model import ZombieModel


# Simulation settings
STEPS = 300

model = ZombieModel(
    width=20,
    height=20,
    people=100,
    zombies=10,
    doctors=5,
    seed=42
)

fig, ax = plt.subplots(figsize=(7, 7))


def update(frame):
    # Run the next simulation step
    if frame > 0:
        model.step()

    ax.clear()

    # Draw all three agent types
    agent_types = [
        (Person, "blue", "People"),
        (Zombie, "red", "Zombies"),
        (Doctor, "green", "Doctors")
    ]

    for agent_type, color, label in agent_types:
        agents = [
            agent for agent in model.agents
            if isinstance(agent, agent_type)
        ]

        x = [agent.x for agent in agents]
        y = [agent.y for agent in agents]

        ax.scatter(x, y, c=color, label=label, s=35)

    people, zombies, doctors = model.counts()

    # Show current simulation information
    ax.set_title(
        f"Zombie Simulation - Step {frame}/{STEPS}\n"
        f"People: {people} | Zombies: {zombies} | Doctors: {doctors}"
    )

    ax.set_xlim(-0.5, model.width - 0.5)
    ax.set_ylim(-0.5, model.height - 0.5)

    ax.set_xticks(range(model.width))
    ax.set_yticks(range(model.height))

    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right")


# Create animation
animation = FuncAnimation(
    fig,
    update,
    frames=range(STEPS + 1),
    interval=100,
    repeat=False
)

plt.tight_layout()
plt.show()
