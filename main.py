import random
import string
import sys


# Helper function to calculate fitness
def calculate_fitness(word, target):
    return sum(c1 == c2 for c1, c2 in zip(word, target))


# Function to mutate a word
def mutate(word, mutation_rate=0.01):
    new_word = ''.join(
        (char if random.random() > mutation_rate else random.choice(string.ascii_lowercase))
        for char in word
    )
    return new_word


# Function to perform crossover between two parents
def crossover(parent1, parent2):
    index = random.randint(0, len(parent1) - 1)
    child = parent1[:index] + parent2[index:]
    return child


# Main genetic algorithm function
def genetic_algorithm(target, population_size=100, mutation_rate=0.01, max_generations=1000):
    # Initialize population
    population = [''.join(random.choices(string.ascii_lowercase, k=len(target))) for _ in range(population_size)]
    generations = 0

    while generations < max_generations:
        # Evaluate fitness of each word
        fitness_scores = [(word, calculate_fitness(word, target)) for word in population]
        fitness_scores.sort(key=lambda x: x[1], reverse=True)

        # Yield the best word of the current generation
        best_word, best_score = fitness_scores[0]
        yield best_word, best_score, generations

        if best_score == len(target):
            break

        # Select the top half of the population
        top_half = fitness_scores[:population_size // 2]

        # Generate the next generation
        next_generation = []
        for _ in range(population_size):
            parent1 = random.choice(top_half)[0]
            parent2 = random.choice(top_half)[0]
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            next_generation.append(child)

        population = next_generation
        generations += 1


# Entry point of the script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python genetic_algorithm.py <target_word>")
        sys.exit(1)

    target_word = sys.argv[1]
    population_size = 200
    mutation_rate = 0.05
    max_generations = 1000

    gen = genetic_algorithm(target_word, population_size, mutation_rate, max_generations)

    for word, score, generation in gen:
        print(f"Generation {generation}: {word} (Score: {score})")
        if word == target_word:
            print(f"Target word '{target_word}' reached in {generation} generations!")
            break
