from nltk.corpus import stopwords
from nltk.stem import  SnowballStemmer
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import newsfilter


stemmer = SnowballStemmer(language='english')

def preProcess(sentence):
    words = []
    for word in sentence.split():
        #Take out all non letter characters
        #word = re.sub("[^a-zA-Z]+", "", word.lower())
        word = word.lower()
        if word not in stopwords.words('english') and word != "":
            newWord = stemmer.stem(word)
            words.append(newWord.replace("'", ""))

    return ' '.join(words)

def createTokenizer(word_index, vocab_size=10000, oov_tok="<OOV>"):

    tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
    tokenizer.word_index = word_index

    print(f"Word Index Size: {len(tokenizer.word_index)}")

    return tokenizer

def predict(headlines, tokenizer, model, max_length=35, trunc_type="post", padding_type="post",):
    for i in range(len(headlines)):
        headlines[i] = preProcess(headlines[i])
    
    sequences = tokenizer.texts_to_sequences(headlines)
    padded = pad_sequences(sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)
    
    return model.predict(padded)

while True:
    headlines = newsfilter.getNews()