
# Zombie Simulation

Agent-Based Simulation Project using Python and Mesa.

## 1. Project Description

This project implements a simple agent-based zombie simulation
using the Mesa library in Python.

The simulation models the interaction between three types of agents:

- Person: A human who moves around and tries to escape zombies.
- Zombie: An infected agent who chases and infects people.
- Doctor: An agent who searches for zombies and attempts to heal them.

The main goal is to investigate how the number of doctors affects
the spread of infection and the number of surviving people.

## 2. Simulation Model

The simulation takes place on a two-dimensional grid.

Default parameters:

- Grid size: 20 x 20
- Initial people: 100
- Initial zombies: 10
- Initial doctors: depends on the scenario
- Infection probability: 0.3
- Healing probability: 0.6
- Simulation duration: 300 steps
- Number of replications: 50 per scenario

Multiple agents can occupy the same grid cell.

Agents can move in four directions:
up, down, left, and right.

Movement outside the grid boundaries is not allowed.

## 3. Agent Behavior

### Person

- Moves randomly when there are no nearby zombies.
- Runs away from the nearest zombie within distance 4.
- Can become infected when sharing a cell with a zombie.

### Zombie

- Searches for the nearest person.
- Chases people within distance 6.
- Otherwise moves randomly.
- Infects a person in the same cell with probability 0.3.

### Doctor

- Searches for the nearest zombie.
- Moves toward zombies within distance 6.
- Otherwise moves randomly.
- Heals a zombie in the same cell with probability 0.6.
- A healed zombie becomes a person again.

## 4. Project Structure

```text
zombie_simulation/
├── main.py
├── agents.py
├── model.py
├── experiments.py
├── analysis.py
├── requirements.txt
├── README.md
└── results/
```

File descriptions:

- main.py: Runs a single simulation and creates visualizations.
- agents.py: Defines the three types of agents.
- model.py: Implements the simulation environment.
- experiments.py: Runs repeated simulations.
- analysis.py: Calculates statistics and creates graphs.
- requirements.txt: Lists required Python libraries.
- results/: Contains generated CSV files and images.

## 5. Installation

Python and pip must be installed.

Install the required libraries:

```bash
python -m pip install -r requirements.txt
```

## 6. Running the Simulation

Run a single simulation:

```bash
python main.py
```

Run all experiments:

```bash
python experiments.py
```

Generate statistical results:

```bash
python analysis.py
```

The experiments must be completed before running analysis.py.

## 7. Experimental Scenarios

Three scenarios are evaluated:

| Scenario | People | Zombies | Doctors |
|----------|--------|---------|---------|
| A | 100 | 10 | 0 |
| B | 100 | 10 | 5 |
| C | 100 | 10 | 10 |

All scenarios use the same grid size and infection rules.

Each scenario is repeated 50 times.

Each simulation runs for 300 steps.

In total, 150 simulation runs are performed.

Each replication uses a random seed to generate reproducible results.

## 8. Collected Data

The following values are recorded:

- Number of people
- Number of zombies
- Number of doctors
- Number of infections
- Number of healings
- Number of simulation steps

## 9. Statistical Analysis

The experiments are evaluated using:

- Mean final number of people
- Approximate 95% confidence intervals
- Population development over time
- Convergence of cumulative means across replications

The confidence interval is calculated using:

CI = mean +/- 1.96 * standard_deviation / sqrt(n)

where n is the number of replications.

The confidence interval provides an approximate estimate
of the uncertainty of the mean result.

## 10. Experimental Results

The following results were obtained from 50 replications
of each scenario.

| Scenario | Mean Final People | 95% CI Lower | 95% CI Upper |
|----------|-------------------|--------------|--------------|
| A: 0 doctors | 0.00 | 0.00 | 0.00 |
| B: 5 doctors | 8.02 | 0.80 | 15.24 |
| C: 10 doctors | 97.34 | 87.74 | 106.94 |

### Scenario A: No Doctors

All 50 replications ended with no surviving people.

The infection spread to the entire population.

### Scenario B: Five Doctors

The average final number of people was 8.02.

In 3 out of 50 replications, the infection was completely
eliminated.

The doctors slowed the spread of infection but were
not sufficient to stop it consistently.

### Scenario C: Ten Doctors

The average final number of people was 97.34.

In 44 out of 50 replications, the infection was completely
eliminated.

This scenario achieved the best results.

## 11. Convergence Analysis

The convergence graph shows how the cumulative mean
changes as the number of replications increases.

In the scenario without doctors, the cumulative mean
remained stable at zero.

In the scenarios with five and ten doctors, the
cumulative means changed when individual replications
produced different outcomes.

The results suggest that 50 replications are useful
for comparing the scenarios, but additional replications
could improve the precision of the estimates.

## 12. Generated Results

The application creates the following files:

- map_start.png: Initial agent positions.
- map_end.png: Final agent positions.
- demo_population.png: Population development in one run.
- demo_history.csv: Data from one simulation.
- final_results.csv: Final results of all replications.
- all_histories.csv: Population data for each step.
- summary.csv: Mean values and confidence intervals.
- population_by_step.png: Average number of people over time.
- convergence.png: Convergence of cumulative means.

## 13. Conclusion

The experiments demonstrate that the number of doctors
has a significant influence on the simulation outcomes
under the selected model parameters.

Without doctors, all people became infected in every run.

With five doctors, the infection was eliminated in
6% of replications.

With ten doctors, the infection was eliminated in
88% of replications.

The results show that increasing the number of doctors
can substantially reduce the spread of infection and
improve population survival.

## 14. Technologies

- Python
- Mesa
- Matplotlib
- CSV
- Python Statistics Library

## 15. References

Mesa Documentation:
https://mesa.readthedocs.io/stable/

Repast Java Getting Started:
https://repast.github.io/docs/RepastJavaGettingStarted.pdf

This project is an independent simplified implementation
of a zombie agent-based model using Python and Mesa.
