import string
from collections import Counter
from nltk import ngrams
from nltk.corpus import brown, words
from nltk.metrics.distance import edit_distance as distance


def preprocess_text(text, retain_punctuation=False):
    """
    Preprocesses the input text by removing punctuation, converting it to lowercase, and splitting it into words.
    
    Args:
        text (str): The input text to preprocess.
        retain_punctuation (bool): Flag indicating whether punctuation should be retained. Default is False.
        
    Returns:
        list: A list of preprocessed words.
    """
    translator = str.maketrans('', '', string.punctuation if not retain_punctuation else "")
    return text.translate(translator).lower().split()


def build_model():
    """
    Builds a language model using the Brown corpus and a frequency model using the NLTK words corpus.
    
    Returns:
        tuple: A tuple containing:
            - tokens (list): List of all tokens (words) in the Brown corpus in lowercase.
            - trigram_model (Counter): A Counter object representing the trigram model.
            - vocabulary (set): A set of unique words from the NLTK words corpus.
            - word_frequencies (Counter): A Counter object representing the word frequencies.
    """
    tokens = [word.lower() for word in brown.words()]
    trigram_model = Counter(ngrams(tokens, 3))
    vocabulary = set(words.words())
    word_frequencies = Counter(tokens)  # Lowercase tokens for consistency
    return tokens, trigram_model, vocabulary, word_frequencies


def calculate_bigram_prob(prev_word, next_word, suggestion, model):
    """
    Calculates the bigram probability of a word suggestion based on the previous and next words.
    
    Args:
        prev_word (str): The previous word in the sequence.
        next_word (str): The next word in the sequence.
        suggestion (str): The suggested word for correction.
        model (Counter): The trigram model that provides word co-occurrence data.
        
    Returns:
        float: The average bigram probability of the suggestion given the previous and next words.
    """
    prob_prev = model.get((prev_word, suggestion), 0) / max(sum(1 for bigram in model if bigram[0] == prev_word), 1)
    prob_next = model.get((suggestion, next_word), 0) / max(sum(1 for bigram in model if bigram[0] == suggestion), 1)
    return (prob_prev + prob_next) / 2


def generate_suggestions(word, vocabulary, word_frequencies):
    """
    Generates word suggestions based on the closest words in the vocabulary and their frequencies.
    
    Args:
        word (str): The word to correct.
        vocabulary (set): A set of words used to generate suggestions.
        word_frequencies (Counter): A Counter object representing word frequencies.
        
    Returns:
        list: A list of the top 5 word suggestions, sorted by edit distance and frequency.
    """
    suggestions = [
        (vocab_word, distance(word, vocab_word), word_frequencies.get(vocab_word, 0))
        for vocab_word in vocabulary
    ]
    suggestions = sorted(suggestions, key=lambda x: (x[1], -x[2]))
    return [suggestion[0] for suggestion in suggestions[:5]]


def correct_text(input_text, model, vocabulary, word_frequencies):
    """
    Corrects the input text by suggesting corrections for words not in the vocabulary and selecting the best suggestion 
    based on bigram probabilities.
    
    Args:
        input_text (str): The input text to correct.
        model (Counter): The trigram model that provides word co-occurrence data.
        vocabulary (set): A set of known words in the vocabulary.
        word_frequencies (Counter): A Counter object representing word frequencies.
        
    Returns:
        tuple: A tuple containing:
            - corrected_text (str): The corrected text with suggestions applied.
            - corrections (dict): A dictionary of words and their suggested corrections.
    """
    words = preprocess_text(input_text)
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

    corrected_text = ' '.join(corrected_words)

    corrected_text = corrected_text.capitalize() 

    if not corrected_text.endswith('.'):
        corrected_text += '.'

    return corrected_text, corrections
