FROM python:3.11-slim

# Set working directory
WORKDIR /spellchecker

# Copy requirements file if it exists, otherwise we'll install common packages
COPY . ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt; \

EXPOSE 8501

CMD ["streamlit", "run", "streamlit.py", "--server.port=?", "--server.address=0.0.0.0"]
