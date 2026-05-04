import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()




def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    y = [i for i in text if i.isalnum()]
    stop_words = set(stopwords.words('english'))
    y = [i for i in y if i not in stop_words and i not in string.punctuation]
    y = [ps.stem(i) for i in y]
    return " ".join(y)


try:
    vector = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model or vectorizer file not found. Please ensure 'model.pkl' and 'vectorizer.pkl' are available.")
    st.stop()

# Streamlit app layout
st.title("Email Spam Classifier")
input_sms = st.text_area("Enter the message")

if st.button('Predict'):

   
    if input_sms.strip() == "":  
        st.warning("Please enter a message for classification.")
    else:
      
        transformed_sms = transform_text(input_sms)
        
        
        vector_input = vector.transform([transformed_sms])
        
    
        result = model.predict(vector_input)[0]
        
        # 4. Display result
        if result == 1:
            st.header("Spam")
        else:
            st.header("Not Spam")
