from src.utils import build_model
import streamlit as st

def load_resources():
    """
    Load necessary resources for the spell checker.

    Returns:
        tuple: A tuple containing:
            - trigram_model (Counter): A Counter of trigrams (3-grams) from the Brown corpus.
            - vocabulary (set): A set of valid words from the NLTK words corpus.
            - word_frequencies (Counter): A Counter of word frequencies from the Brown corpus.
    """
    try:
        _, trigram_model, vocabulary, word_frequencies = build_model()
        return trigram_model, vocabulary, word_frequencies
    except Exception as e:
        st.error(f"Error loading resources: {e}")
        return None, None, None


