import streamlit as st
from src.utils import correct_text
from src.components import load_resources


# Initialize session state variables
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

if "corrections" not in st.session_state:
    st.session_state.corrections = {}

if "updated_text" not in st.session_state:
    st.session_state.updated_text = ""

# Load resources
trigram_model, vocabulary, word_frequencies = load_resources()

if trigram_model is None:
    st.stop()  # Stop the app execution if loading fails

# Streamlit App
st.title("Spellchecker")

# Input area
st.markdown("### Enter your sentence:")
input_text = st.text_area(
    "Type your sentence here:",
    value=st.session_state.input_text,
    height=100,
    placeholder="Enter a sentence to check spelling...",
)

if st.button("Correct Sentence"):
    if input_text.strip():
        try:
            # Correct the text and retrieve corrections
            corrected_text, corrections = correct_text(
                input_text, trigram_model, vocabulary, word_frequencies
            )

            # Save the corrections and input text in session state
            st.session_state.input_text = input_text
            st.session_state.corrections = corrections
            st.session_state.updated_text = input_text  # Start with the original text

        except Exception as e:
            st.error(f"Error correcting text: {e}")
    else:
        st.warning("Please enter some text to correct.")

# Highlight corrections
if st.session_state.corrections:
    corrections = st.session_state.corrections
    highlighted_text = st.session_state.input_text

    for original_word in corrections:
        highlighted_text = highlighted_text.replace(
        original_word, f"<span style='background-color: #EEA406'>{original_word}</span>")

    # Render the highlighted text
    st.markdown("### Words to correct:")
    st.markdown(highlighted_text, unsafe_allow_html=True)

    # Show corrections
    updated_text = st.session_state.updated_text

    for original_word, suggestions in corrections.items():
        dropdown_key = f"dropdown_{original_word}"
        selected_word = st.selectbox(
            f"Suggestions for '{original_word}':",
            [original_word] + suggestions,
            key=dropdown_key,
        )

        # Update the text with the selected word
        if selected_word != original_word:
            updated_text = updated_text.replace(original_word, selected_word, 1)

    # Save the updated text back to session state
    st.session_state.updated_text = updated_text.capitalize()  # Capitalize and add period

    # Display the updated corrected text
    st.markdown("### Updated Corrected Text:")
    st.code(st.session_state.updated_text + '.', language="text")

