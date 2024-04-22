from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import pickle
import numpy as np
import nltk
import random
import json

app = Flask(__name__)

nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer

# Load the preprocessed data
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))
model = load_model("chatbot_model.h5")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents outside of the if __name__ == '__main__': block
intents = json.loads(open('intents.json').read())

def clean_up_sentence(sentence):
    # Tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # Lemmatize each word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # Tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # Bag of words
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence):
    # Filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # Sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def get_response(ints, intents):
    tag = ints[0]['intent']
    list_of_intents = intents['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

@app.route('/')
def launch():
    return render_template('launch.html')

@app.route('/index')
def index():
    return render_template('index.html')

settings = {
    'font-color': '#000000',  # Default font color (black)
    'font-size': '16px',      # Default font size (medium)
    'background-color': '#ffffff',  # Default background color (white)
    'font-family': 'Arial, sans-serif'  # Default font family
}

@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    if request.method == 'POST':
        # Update settings with form data
        settings['font-color'] = request.form['font-color']
        settings['font-size'] = request.form['font-size']
        settings['background-color'] = request.form['background-color']
        settings['font-family'] = request.form['font-family']

    return render_template('settings.html', settings=settings)

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.form['msg']
    res = chatbot_response(msg)
    return jsonify({'response': res})

def chatbot_response(msg):
    ints = predict_class(msg)
    res = get_response(ints, intents)
    return res

if __name__ == '__main__':
    app.run(debug=True)
