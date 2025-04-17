import os
from io import BytesIO
import pdfplumber
import docx
import zipfile
from fpdf import FPDF
import google.generativeai as genai

# Set up Google API key for Gemini


def extract_text_from_file(uploaded_file):
    """
    Extracts text from an uploaded file by reading its content.
    Supports PDF, DOCX, and TXT formats.

    Args:
        uploaded_file (File): The uploaded file object.

    Returns:
        str: The extracted text or an error message if unsupported or unreadable.
    """
    try:
        # Read the first few bytes to identify the format
        file_data = uploaded_file.read()
        uploaded_file.seek(0)  # Reset the file pointer for subsequent reading

        # Check if it's a PDF (starts with "%PDF")
        if file_data[:4] == b'%PDF':
            with pdfplumber.open(BytesIO(file_data)) as pdf:
                text = ''.join([page.extract_text() or '' for page in pdf.pages])  # Handle empty pages
            return text.strip()

        # Check if it's a DOCX file (ZIP archive with specific files)
        elif uploaded_file.name.endswith('.docx'):
            doc = docx.Document(BytesIO(file_data))
            text = '\n'.join([para.text for para in doc.paragraphs])
            return text.strip()

        # Assume plain text if no markers for other formats
        else:
            try:
                return file_data.decode('utf-8').strip()
            except UnicodeDecodeError:
                return "Unable to decode the file as plain text."

    except Exception as e:
        return f"Error reading file: {e}"

# Function to generate MCQs using Google's Gemini AI model
def Question_mcqs_generator(input_text, num_questions):
    prompt = f"""
    You are an AI assistant helping the user generate multiple-choice questions (MCQs) based on the following text:
    '{input_text}'
    Please generate {num_questions} MCQs from the text. Each question should have:
    - A clear question
    - Four answer options (labeled A, B, C, D)
    - The correct answer clearly indicated
    Format:
    ## MCQ
    Question: [question]
    A) [option A]
    B) [option B]
    C) [option C]
    D) [option D]
    Correct Answer: [correct option]
    """
    response = model.generate_content(prompt).text.strip()
    return response
