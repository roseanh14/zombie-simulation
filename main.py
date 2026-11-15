
import csv
from pathlib import Path
import matplotlib.pyplot as plt

from agents import Person, Zombie, Doctor
from model import ZombieModel


def draw_map(model, filename):
    plt.figure(figsize=(6, 6))

    types = [
        (Person, "blue", "People"),
        (Zombie, "red", "Zombies"),
        (Doctor, "green", "Doctors")
    ]

    for kind, color, label in types:
        agents = [a for a in model.agents if isinstance(a, kind)]

        plt.scatter(
            [a.x for a in agents],
            [a.y for a in agents],
            c=color,
            label=label
        )

    plt.xlim(-0.5, model.width - 0.5)
    plt.ylim(-0.5, model.height - 0.5)
    plt.grid()
    plt.legend()
    plt.title("Zombie Simulation")

    plt.savefig(filename)
    plt.close()


def main():
    output = Path("results")
    output.mkdir(exist_ok=True)

    model = ZombieModel(
        people=100,
        zombies=10,
        doctors=5,
        seed=42
    )

    draw_map(model, output / "map_start.png")

    # Run 300 simulation steps
    for _ in range(300):
        model.step()

    draw_map(model, output / "map_end.png")

    # Save simulation history
    with open(output / "demo_history.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=model.history[0].keys())
        writer.writeheader()
        writer.writerows(model.history)

    # Plot population changes
    for name in ["people", "zombies", "doctors"]:
        plt.plot(
            [row["step"] for row in model.history],
            [row[name] for row in model.history],
            label=name
        )

    plt.xlabel("Simulation Step")
    plt.ylabel("Number of Agents")
    plt.legend()
    plt.grid()

    plt.savefig(output / "demo_population.png")
    plt.close()

    print("Simulation finished!")
    print("Results saved in the results folder.")


if __name__ == "__main__":
    main()
