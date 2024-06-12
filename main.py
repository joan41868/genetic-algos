import random
import sys
from calc_ent import calculate_entropy

def calculate_fitness(word, target):
    return sum(c1.lower() == c2 for c1, c2 in zip(word, target))


def mutate(word, mutation_rate=0.01):
    word = list(word)
    for i in range(len(word)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(word) - 1)
            word[i], word[j] = word[j], word[i]
    return ''.join(word)


def crossover(parent1, parent2):
    half = len(parent1) // 2
    child = parent1[:half]
    used_chars = set(char.lower() for char in child)
    for char in parent2:
        if char.lower() not in used_chars:
            child += char
            used_chars.add(char.lower())
    return child


# Main genetic algorithm function
def genetic_algorithm(target, population_size=100, mutation_rate=0.01, max_generations=1000):
    unique_chars = list(set(target))
    available_chars = unique_chars + [char.upper() for char in unique_chars]

    # Ensure initial population contains valid permutations
    population = []
    for _ in range(population_size):
        while True:
            individual = ''.join(random.sample(available_chars, len(target)))
            if len(set(char.lower() for char in individual)) == len(target):  # Ensure no repeating characters
                population.append(individual)
                break

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

        top_half = fitness_scores[:population_size // 2]

        # Generate the next generation
        next_generation = []
        while len(next_generation) < population_size:
            parent1 = random.choice(top_half)[0]
            parent2 = random.choice(top_half)[0]
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            if len(set(char.lower() for char in child)) == len(target):  # Ensure no repeating characters
                next_generation.append(child)

        population = next_generation
        generations += 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python genetic_algorithm.py <target_word>")
        sys.exit(1)

    target_word = sys.argv[1].lower()
    population_size = 50
    mutation_rate = 1
    max_generations = 2000

    gen = genetic_algorithm(target_word, population_size, mutation_rate, max_generations)
    words = []
    scores = []
    for word, score, generation in gen:
        # print(f"Generation {generation}: {word} (Score: {score})")
        print(f"{word} (Score: {score})")
        words.append(word)
        scores.append(score)
    entropy = calculate_entropy(words)
    print(f"Wcount {len(words)} Unique {len(set(words))}")
    print(f"Entropy of generation {entropy}")
    print(f"{entropy} -> gen {max_generations}; pop {population_size}; mut {mutation_rate}")