import json
from sklearn.model_selection import train_test_split
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from model import makeModel
import helper
import nlpaug.augmenter.word as naw
import torch

with open("./data/training_data.json", 'r') as f:
    datastore = json.load(f)

headlines = []
labels = []

for item in datastore:
    headlines.append(item['title'])
    labels.append(item['good_news'])

# split the data 80/20
training_headlines, testing_headlines, training_labels, testing_labels = train_test_split(headlines, labels, train_size=0.8)

#limiting character length and vocab size
vocab_size = 10000
max_length = 25
embedding_dim = 10
trunc_type='post'
padding_type='post'
oov_tok = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)

# training tokenizer
tokenizer.fit_on_texts(headlines)
word_index = tokenizer.word_index



TOPK=20 #default=100
ACT = 'insert' #"substitute"
training_headlines_aug=[] 

# with open(r'data/augmented_training_data.txt', 'w', encoding="utf-8") as fp:

#     for i in range(len(training_headlines)):
#         aug = naw.ContextualWordEmbsAug(
#             model_path='bert-base-uncased', action="insert")
#         fp.write(str(aug.augment(training_headlines[i])) + "\n")
#         print(str(i) + " out of " + str(len(training_headlines)))

#print("------------------------------------------------------------------------------")
#print("Augmented Text:")
#print(training_headlines_aug[0:10])

with open('data/augmented_training_data.txt', 'r', encoding='UTF-8') as file:
    for line in file:
        training_headlines_aug.append(line)
    
file.close()
#print(training_headlines_aug[0])

# adding padding 
training_sequences = tokenizer.texts_to_sequences(training_headlines_aug)
training_padded = pad_sequences(training_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

testing_sequences = tokenizer.texts_to_sequences(testing_headlines)
testing_padded = pad_sequences(testing_sequences, maxlen=max_length, padding=padding_type, truncating=trunc_type)

training_labels = np.array(training_labels)
testing_labels = np.array(testing_labels)


model = makeModel(vocab_size, embedding_dim, max_length)


history = model.fit(training_padded, training_labels, batch_size=8,epochs=40, validation_data=(testing_padded, testing_labels), callbacks=[])

#helper.plot_lr(history)
helper.plot_loss_curves(history)