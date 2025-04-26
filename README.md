
# Teaching and Learning Enhancement using Computer Vision and Generative AI

This Django-based project enhances the teaching and learning experience using Computer Vision for interaction and Generative AI for automatic quiz generation. It includes features for student-teacher interaction, quiz creation, notes, and more.

---

## 📹 Project Demonstration

[![Project Demonstration](https://img.youtube.com/vi/CEdwwNnpVpo/0.jpg)](https://www.youtube.com/watch?v=CEdwwNnpVpo)

---

## 🚀 Features

- ✍️ Handwriting in the air using Mediapipe and OpenCV.
- 🤖 AI-based quiz generation using Gemini (Google Generative AI).
- 🧪 Student quiz attempt and result tracking.
- 📝 Summary generation for videos**: Automatically generates summaries for videos.
- 🌐 Language translation: Translate text content to various languages for better accessibility.
- 📚 Teacher portal to create/manage quizzes and notes.
- ❓ Doubts section for student-teacher communication.
- 🧠 MongoDB + Djongo integration for efficient document storage.


---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/RagalahariAkula-42/Teaching-and-Learning-Enhancement-using-Computer-Vision-and-Generative-AI.git
cd Teaching-and-Learning-Enhancement-using-Computer-Vision-and-Generative-AI
```

### 2. (Optional) Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, install manually:

```bash
pip install django djongo pymongo djangorestframework google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

---

## ⚙️ Configuration

### 🔑 Add Google API Key for Gemini

- Open the file: `signup/quiz.py`
- Replace the placeholder with your **Google Gemini API Key**:

```python
GOOGLE_API_KEY = "your_google_gemini_api_key"
```

> This API key is used to generate quizzes automatically using Google's Generative AI (Gemini).

---

### 📁 Add Google Drive Storage `.json` File

- Place your **Google Cloud service account JSON** file in:

```bash
quizzz/quizzz/
```

> This file allows authentication for Google Drive operations like uploading or reading documents.

---

## 🧱 Database Setup

Make sure MongoDB is running locally or use MongoDB Atlas.

In `quizzz/settings.py`, update the database section:

```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'your_database_name',
    }
}
```

---

## 🧪 Running the Project

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # (Optional)
python manage.py runserver
```

Then open your browser and visit:  
🔗 **http://127.0.0.1:8000/**

---
