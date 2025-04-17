import whisper
import io
import ffmpeg
from pydub import AudioSegment
from transformers import pipeline

def extract_audio(file_path):
    """Extract audio from video/audio file without saving to disk."""
    try:
        # Process Video Files
        if file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv')):
            audio_buffer = io.BytesIO()
            process = (
                ffmpeg
                .input(file_path)
                .output('pipe:', format='wav', acodec='pcm_s16le', ar='16000')
                .run(capture_stdout=True, capture_stderr=True)
            )
            audio_buffer.write(process[0])
            audio_buffer.seek(0)

        # Process Audio Files
        elif file_path.lower().endswith(('.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a')):
            audio = AudioSegment.from_file(file_path)
            audio_buffer = io.BytesIO()
            audio.export(audio_buffer, format="wav")
            audio_buffer.seek(0)
        
        else:
            raise ValueError("Unsupported file format.")
        
        return audio_buffer
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None

def transcribe_audio(audio_buffer):
    """Transcribes audio using Whisper."""
    if not audio_buffer:
        return "Error: Could not process audio."
    
    model = whisper.load_model("base")  # You can change this to "small", "medium", or "large"
    result = model.transcribe(audio_buffer)

    return result["text"]

def summarize_text(text):
    """Summarize transcribed text using Hugging Face transformers."""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    
    return summary[0]["summary_text"]

def video_summary_pipeline(file_path):
    """Extracts audio, transcribes speech, and summarizes it."""
    print("Extracting audio...")
    audio_buffer = extract_audio(file_path)
    
    print("Transcribing audio...")
    transcribed_text = transcribe_audio(audio_buffer)
    
    print("Summarizing text...")
    summary = summarize_text(transcribed_text)

    return summary
