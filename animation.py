
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.path import Path

from agents import Person, Zombie, Doctor
from model import ZombieModel


STEPS = 300

model = ZombieModel(
    width=20,
    height=20,
    people=100,
    zombies=10,
    doctors=5,
    seed=42
)

fig, ax = plt.subplots(figsize=(9, 8))


def make_person_marker():
    # Create a simple stick figure
    points = []
    codes = []

    def line(start, end):
        points.extend([start, end])
        codes.extend([Path.MOVETO, Path.LINETO])

    # Head
    for i in range(13):
        angle = 2 * math.pi * i / 12
        point = (
            0.15 * math.cos(angle),
            0.65 + 0.15 * math.sin(angle)
        )

        if i == 0:
            points.append(point)
            codes.append(Path.MOVETO)
        else:
            points.append(point)
            codes.append(Path.LINETO)

    # Body, arms and legs
    line((0, 0.5), (0, -0.3))
    line((0, 0.2), (-0.35, -0.05))
    line((0, 0.2), (0.35, -0.05))
    line((0, -0.3), (-0.3, -0.8))
    line((0, -0.3), (0.3, -0.8))

    return Path(points, codes)


person_marker = make_person_marker()


def update(frame):
    if frame > 0:
        model.step()

    ax.clear()

    agent_types = [
        (Person, "black", "People"),
        (Zombie, "firebrick", "Zombies"),
        (Doctor, "forestgreen", "Doctors")
    ]

    for agent_type, color, label in agent_types:
        agents = [
            agent for agent in model.agents
            if isinstance(agent, agent_type)
        ]

        x = [agent.x for agent in agents]
        y = [agent.y for agent in agents]

        ax.scatter(
            x, y,
            color=color,
            marker=person_marker,
            s=160,
            label=label,
            zorder=3
        )

    # Draw arrows from zombies toward nearby people
    people = [
        a for a in model.agents
        if isinstance(a, Person)
    ]

    zombies = [
        a for a in model.agents
        if isinstance(a, Zombie)
    ]

    for zombie in zombies[:30]:
        if not people:
            break

        nearest = min(
            people,
            key=lambda p: model.distance(zombie, p)
        )

        if model.distance(zombie, nearest) <= 6:
            ax.annotate(
                "",
                xy=(nearest.x, nearest.y),
                xytext=(zombie.x, zombie.y),
                arrowprops={
                    "arrowstyle": "->",
                    "color": "firebrick",
                    "alpha": 0.5,
                    "lw": 0.8
                },
                zorder=2
            )

    people_count, zombie_count, doctor_count = model.counts()

    ax.set_title(
        f"Zombie Simulation - Step {frame}/{STEPS}\n"
        f"People: {people_count} | "
        f"Zombies: {zombie_count} | "
        f"Doctors: {doctor_count}",
        fontsize=13
    )

    ax.set_xlim(-0.5, 19.5)
    ax.set_ylim(-0.5, 19.5)

    ax.set_xticks(range(20))
    ax.set_yticks(range(20))
    ax.set_aspect("equal")

    ax.grid(alpha=0.2)
    ax.legend(loc="upper right")


animation = FuncAnimation(
    fig,
    update,
    frames=range(STEPS + 1),
    interval=150,
    repeat=False,
    cache_frame_data=False
)

plt.tight_layout()
plt.show()
