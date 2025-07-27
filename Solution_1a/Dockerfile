# Use slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install OS dependencies for PyMuPDF and other common packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy all necessary files and folders from current dir (Solution_1a)
COPY requirements.txt ./
COPY process_pdfs.py ./
COPY pdf_outliner/ ./pdf_outliner/
COPY sample_dataset/ ./sample_dataset/
COPY tests/ ./tests/
COPY local_model/ ./local_model/

# Install pip and upgrade it
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the main script
CMD ["python", "process_pdfs.py"]
