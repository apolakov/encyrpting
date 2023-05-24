import random

# English letter frequencies
letter_frequencies = {
    'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 13.0, 'f': 2.2, 'g': 2.0, 'h': 6.1, 'i': 7.0,
    'j': 0.2, 'k': 0.8, 'l': 4.0, 'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9, 'q': 0.1, 'r': 6.0,
    's': 6.3, 't': 9.1, 'u': 2.8, 'v': 1.0, 'w': 2.4, 'x': 0.2, 'y': 2.0, 'z': 0.1, ' ': 19.2
}

# English bigram frequencies
bigram_frequencies = {
    'th': 2.71, 'he': 2.33, 'in': 2.03, 'er': 1.78, 'an': 1.61, 're': 1.41, 'nd': 1.38, 'at': 1.33,
    'on': 1.33, 'nt': 1.17, 'ha': 1.13, 'es': 1.11, 'st': 1.09, 'en': 1.09, 'ed': 1.07, 'to': 1.07,
    'it': 1.06, 'ou': 1.05, 'ea': 1.00, 'hi': 0.99, 'is': 0.96, 'or': 0.96, 'ti': 0.94, 'as': 0.94,
    'te': 0.91, 'et': 0.91, 'ng': 0.89, 'of': 0.88, 'al': 0.88, 'de': 0.87, 'se': 0.87, 'le': 0.83,
    'sa': 0.82, 'si': 0.79, 'ar': 0.78, 've': 0.77, 'ra': 0.76, 'ld': 0.76, 'ur': 0.75
}

# Function to decrypt the text using a given key
def decrypt_text(text, key):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            decrypted_text += key[char]
        else:
            decrypted_text += char
    return decrypted_text

# Function to calculate the fitness score of a decryption key
def calculate_fitness(text, key):
    decrypted_text = decrypt_text(text, key)
    word_list = decrypted_text.split()
    word_count = 0
    for word in word_list:
        if word.lower() in english_words:
            word_count += 1

    bigram_counts = {bigram: 0 for bigram in bigram_frequencies}
    total_bigrams = 0
    for i in range(len(decrypted_text) - 1):
        bigram = decrypted_text[i:i+2]
        if bigram in bigram_frequencies:
            bigram_counts[bigram] += 1
            total_bigrams += 1

    fitness = word_count
    for bigram in bigram_frequencies:
        expected_frequency = bigram_frequencies[bigram] / 100
        actual_frequency = bigram_counts[bigram] / total_bigrams
        fitness += abs(expected_frequency - actual_frequency)

    return fitness

# Function to generate a random decryption key
def generate_key():
    alphabet = list(letter_frequencies.keys())
    random.shuffle(alphabet)
    return {alphabet[i]: chr(ord('a') + i) for i in range(27)}

# Function to perform mutation on a decryption key
def mutate_key(key):
    new_key = key.copy()
    char1, char2 = random.sample(list(new_key.keys()), 2)
    new_key[char1], new_key[char2] = new_key[char2], new_key[char1]
    return new_key

# Function to perform the genetic algorithm for decryption
def genetic_decrypt(ciphertext, iterations=1000, population_size=100, elite_size=10):
    population = [generate_key() for _ in range(population_size)]
    best_key = None
    best_fitness = 0

    for _ in range(iterations):
        # Evaluate fitness for each key
        fitness_scores = [calculate_fitness(ciphertext, key) for key in population]

        # Find the elite individuals
        elite_indices = sorted(range(len(fitness_scores)), key=lambda i: fitness_scores[i], reverse=True)[:elite_size]
        elite_population = [population[i] for i in elite_indices]

        # Check if a better solution is found
        max_fitness = max(fitness_scores)
        if max_fitness > best_fitness:
            best_fitness = max_fitness
            best_key = population[fitness_scores.index(max_fitness)]

        # Generate new population
        population = elite_population
        while len(population) < population_size:
            parent = random.choice(elite_population)
            offspring = mutate_key(parent)
            population.append(offspring)

    return decrypt_text(ciphertext, best_key)

# Load English word dictionary
with open('dictionary.txt', 'r') as file:
    english_words = set(file.read().split())

# Example usage
with open('encrypted_text.txt', 'r') as file:
    ciphertext = file.read()
plaintext = genetic_decrypt(ciphertext)
print("Ciphertext:", ciphertext)
print("Plaintext:", plaintext)