# Spellchecker

A modern, intelligent spellchecker application built with Python, Streamlit, and NLP techniques. This project provides an interactive web interface for correcting spelling errors in text using advanced language modeling and edit distance algorithms.

## Features

- **Interactive Web Interface**: User-friendly Streamlit-based web application
- **Intelligent Spell Correction**: Uses trigram language models and edit distance algorithms
- **Context-Aware Suggestions**: Considers surrounding words for better correction accuracy
- **Real-time Correction**: Instant feedback and suggestions as you type
- **Multiple Suggestion Options**: Provides up to 5 alternative word suggestions
- **Highlighted Corrections**: Visual highlighting of words that need correction
- **Docker Support**: Easy deployment with containerization

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.11
- **NLP Libraries**: NLTK, spaCy
- **Language Models**: Trigram models using Brown corpus
- **Text Processing**: Edit distance algorithms, word frequency analysis
- **Containerization**: Docker

### How to Use

1. **Enter Text**: Type or paste your text in the input area
2. **Check Spelling**: Click "Correct Sentence" to analyze your text
3. **Review Suggestions**: Words with spelling errors will be highlighted
4. **Select Corrections**: Choose from the dropdown suggestions for each highlighted word
5. **View Results**: See your corrected text with proper capitalization and punctuation

## Core Components

### Spellchecking Algorithm

The spellchecker uses a sophisticated approach combining:

1. **Edit Distance**: Levenshtein distance to find similar words
2. **Language Modeling**: Trigram models from the Brown corpus
3. **Frequency Analysis**: Word frequency data for ranking suggestions
4. **Context Awareness**: Bigram probabilities considering surrounding words

### Key Functions

- `correct_text()`: Main correction function
- `generate_suggestions()`: Creates word suggestions based on edit distance
- `calculate_bigram_prob()`: Computes context-aware probabilities
- `build_model()`: Constructs language models from corpora
