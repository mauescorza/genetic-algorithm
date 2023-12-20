# Genetic Algorithm for N-Queens Problem

This Python script implements a genetic algorithm to solve the N-Queens problem, aiming to find a configuration of queens on an N x N chessboard where no two queens threaten each other. The genetic algorithm involves creating a population of individuals (each representing a possible solution), evolving them through selection, recombination, and mutation to improve fitness, and iteratively repeating this process until a solution is found or a predefined number of generations is reached.

## Implementation Details

The script defines two classes:

### `Individuo`

- Represents an individual solution with a chromosome of eight integers (representing the positions of queens on each row).
- Initializes with a random chromosome or a provided one.
- Implements mutation with a 20% probability of changing each gene.
- Calculates conflicts (threats) in the chromosome, considering vertical and diagonal positions.
- Calculates fitness based on the maximum number of conflicts.

### `Poblacion`

- Represents a population of individuals.
- Initializes with an empty population and the maximum number of conflicts set to 0.
- Creates a population of 50 random individuals.
- Finds the best individual based on fitness.
- Calculates the maximum number of conflicts in the population.
- Assigns fitness to each individual based on the maximum number of conflicts.
- Checks if there is at least one solution (individual with 0 conflicts) in the population.
- Implements selection using the roulette wheel method.

## Usage Instructions

1. Copy and paste the script into a Python environment.
2. Run the script.

The genetic algorithm will attempt to find a solution to the N-Queens problem. Adjust the `limite_generaciones` variable to set the maximum number of generations. The script outputs the best individual found during the process.

Feel free to experiment with different parameters and explore how the genetic algorithm evolves over generations to reach a solution.
