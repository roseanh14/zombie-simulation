
import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


def confidence_interval(values):
    mean = statistics.mean(values)

    if len(values) < 2:
        return mean, mean, mean

    margin = 1.96 * statistics.stdev(values) / math.sqrt(len(values))

    return mean, mean - margin, mean + margin


def main():
    output = Path("results")

    with open(output / "final_results.csv", newline="") as file:
        results = list(csv.DictReader(file))

    with open(output / "all_histories.csv", newline="") as file:
        histories = list(csv.DictReader(file))

    groups = defaultdict(list)

    for row in results:
        groups[row["scenario"]].append(int(row["people_final"]))

    # Calculate the mean and confidence interval
    with open(output / "summary.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "scenario",
            "runs",
            "mean_people",
            "ci95_low",
            "ci95_high"
        ])

        for name, values in groups.items():
            mean, low, high = confidence_interval(values)

            writer.writerow([
                name,
                len(values),
                round(mean, 2),
                round(low, 2),
                round(high, 2)
            ])

            print(f"{name}: mean = {mean:.2f}, CI = [{low:.2f}, {high:.2f}]")

    # Calculate average population at each step
    by_step = defaultdict(list)

    for row in histories:
        key = (row["scenario"], int(row["step"]))
        by_step[key].append(int(row["people"]))

    for name in groups:
        steps = sorted(
            step for scenario, step in by_step
            if scenario == name
        )

        means = [
            statistics.mean(by_step[(name, step)])
            for step in steps
        ]

        plt.plot(steps, means, label=name)

    plt.xlabel("Simulation Step")
    plt.ylabel("Mean Number of People")
    plt.legend()
    plt.grid()

    plt.savefig(output / "population_by_step.png")
    plt.close()

    # Check convergence across replications
    for name, values in groups.items():
        means = []

        for n in range(1, len(values) + 1):
            means.append(statistics.mean(values[:n]))

        plt.plot(range(1, len(values) + 1), means, label=name)

    plt.xlabel("Number of Replications")
    plt.ylabel("Cumulative Mean")
    plt.legend()
    plt.grid()

    plt.savefig(output / "convergence.png")
    plt.close()

    print("Analysis finished!")


if __name__ == "__main__":
    main()
