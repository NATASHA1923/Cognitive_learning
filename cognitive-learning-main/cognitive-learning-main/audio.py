from gtts import gTTS
import os
import PyPDF2

# Open the PDF file in binary mode
with open('EEG.pdf', 'rb') as file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(file)
    
# Extract the text from the PDF file
text = ''
for page in pdf_reader.pages:
    text += page.extract_text()

# Convert the text to speech using gTTS
language = 'en'
speech = gTTS(text=text, lang=language, slow=False)

# Save the converted audio in an MP3 file named 'voice.mp3'
speech.save("voice.mp3")

# Play the audio file
os.system("mpg321 voice.mp3")