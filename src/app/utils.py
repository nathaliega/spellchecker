import string
from collections import Counter
from nltk import ngrams
from nltk.corpus import brown, words
from nltk.metrics.distance import edit_distance as distance


def preprocess_text(text, retain_punctuation=False):
    translator = str.maketrans('', '', string.punctuation if not retain_punctuation else "")
    return text.translate(translator).lower().split()


def build_model():
    tokens = [word.lower() for word in brown.words()]
    trigram_model = Counter(ngrams(tokens, 3))
    vocabulary = set(words.words())
    word_frequencies = Counter(tokens)  # Lowercase tokens for consistency
    return tokens, trigram_model, vocabulary, word_frequencies


def calculate_bigram_prob(prev_word, next_word, suggestion, model):
    prob_prev = model.get((prev_word, suggestion), 0) / max(sum(1 for bigram in model if bigram[0] == prev_word), 1)
    prob_next = model.get((suggestion, next_word), 0) / max(sum(1 for bigram in model if bigram[0] == suggestion), 1)
    return (prob_prev + prob_next) / 2


def generate_suggestions(word, vocabulary, word_frequencies):
    suggestions = [
        (vocab_word, distance(word, vocab_word), word_frequencies.get(vocab_word, 0))
        for vocab_word in vocabulary
    ]
    suggestions = sorted(suggestions, key=lambda x: (x[1], -x[2]))
    return [suggestion[0] for suggestion in suggestions[:5]]


def correct_text(input_text, model, vocabulary, word_frequencies):
    words =     (input_text)
    corrected_words = []
    corrections = {}
    prev_word = None

    for i, word in enumerate(words):
        if word not in vocabulary:
            suggestions = generate_suggestions(word, vocabulary, word_frequencies)
            corrections[word] = suggestions

            next_word = words[i + 1] if i + 1 < len(words) else None
            best_suggestion = suggestions[0]
            best_prob = 0

            for suggestion in suggestions:
                prob = calculate_bigram_prob(prev_word, next_word, suggestion, model)
                if prob > best_prob:
                    best_prob = prob
                    best_suggestion = suggestion

            corrected_words.append(best_suggestion)
            prev_word = best_suggestion
        else:
            corrected_words.append(word)
            prev_word = word

    return ' '.join(corrected_words), corrections
