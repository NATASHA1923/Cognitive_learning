from flask import Flask, render_template, Response, redirect, stream_with_context,request,url_for,session
import cv2
import numpy as np
import os
from transformers import DetrImageProcessor, DetrForObjectDetection,pipeline
import PyPDF2
import re
from pymongo import MongoClient
import urllib.parse

app = Flask(__name__)
app.secret_key = 'abc'

mongodb_uri = mongodb_uri = "mongodb+srv://harshankishore004:"+urllib.parse.quote("harshan@1803") +"@cluster0.n4seoyw.mongodb.net/?retryWrites=true&w=majority"
database_name = 'credentials_db'
client = MongoClient(mongodb_uri)
db = client[database_name]
users_collection = db['users']

def answer_question(context, question):
    qa_pipeline = pipeline('question-answering', model='bert-large-uncased-whole-word-masking-finetuned-squad', tokenizer='bert-large-uncased-whole-word-masking-finetuned-squad')
    result = qa_pipeline(context=context, question=question)
    return result['answer']

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
@app.route('/')
def start():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_auth = request.form['nm']
        pwd_auth = request.form['pwd']
        user_data = users_collection.find_one({'email': user_auth})

        if user_data and str(user_data['password']) == pwd_auth:
            session['user'] = str(user_data['_id'])  
            return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route("/home", methods=['GET'])
def home():
    return render_template("index2.html")

@app.route("/snake", methods=['GET'])
def snake():
    return render_template("index3.html")

@app.route("/typing_game", methods=['GET'])
def typing_game():
    return render_template("index4.html")

def handle_finished_timer():
    timer_value = request.form.get('timerValue')
    # Process the timer value as needed (e.g., save it to a database)
    print("Received timer value:", timer_value)
    # You can return a response if needed
    return "Timer value received successfully!"




@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/answer', methods=['POST'])
def get_answer():
    user_question = request.form['question']
    answer = answer_question(cleaned_text, user_question)
    return render_template('chatbot.html', question=user_question, answer=answer)

@app.route('/finished', methods=['POST'])
def handle_finished_timer():
    timer_value = request.form.get('timerValue')
    # Process the timer value as needed (e.g., save it to a database)
    print("Received timer value:", timer_value)
    return "Timer value received successfully!"

if __name__ == '__main__':
    pdf_path = 'EEG.pdf'
    pdf_text = extract_text_from_pdf(pdf_path)
    cleaned_text = preprocess_text(pdf_text)
    app.run(host="0.0.0.0", port=5000, debug=True)
    
