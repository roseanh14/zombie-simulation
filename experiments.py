
import csv
from pathlib import Path
from model import ZombieModel


SCENARIOS = {
    "no_doctors": 0,
    "five_doctors": 5,
    "ten_doctors": 10
}

RUNS = 50
STEPS = 300


def main():
    output = Path("results")
    output.mkdir(exist_ok=True)

    finals = []
    histories = []

    for name, doctors in SCENARIOS.items():
        for run in range(RUNS):

            model = ZombieModel(
                people=100,
                zombies=10,
                doctors=doctors,
                width=20,
                height=20,
                seed=1000 + run
            )

            for _ in range(STEPS):
                model.step()

            last = model.history[-1]

            finals.append({
                "scenario": name,
                "run": run + 1,
                "doctors_initial": doctors,
                "people_final": last["people"],
                "zombies_final": last["zombies"],
                "infections": last["infections"],
                "healings": last["healings"]
            })

            for row in model.history:
                histories.append({
                    "scenario": name,
                    "run": run + 1,
                    **row
                })

        print(f"Finished: {name}")

    # Save final results
    with open(output / "final_results.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=finals[0].keys())
        writer.writeheader()
        writer.writerows(finals)

    # Save results from all steps
    with open(output / "all_histories.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=histories[0].keys())
        writer.writeheader()
        writer.writerows(histories)

    print("All experiments finished!")


if __name__ == "__main__":
    main()
