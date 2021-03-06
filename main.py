from lstm import MyLSTM
from gensim.models import FastText
from keras.models import load_model
from keras.preprocessing import sequence
import numpy as np
import pickle
import utils

# Loading..
# ├ ⑴Toy dict.(pre-stored @toyData.py)
# ├ ⑵Word Embedding Model (pre-trained @wordEmbedding.py)
# └ ⑶LSTM model (pre-stored @lstm.py)

max_seq_len = 30
with open('dictionary/toyDict.pickle', 'rb') as handle:
    toy_dict = pickle.load(handle)
fastText = FastText.load('model/FastText.bin')
preLSTM = load_model('model/lstm.h5')
#---------------------------------------------------------#

LSTM = MyLSTM(toy_dict=toy_dict, embedding_model=fastText)
index_dict = LSTM.create_index_dict()
(X_train, Y_train, X_val, Y_val, X_test, Y_test, toy_test_dict) = LSTM.split_train_test()
X_test = sequence.pad_sequences(np.array(X_test), maxlen=max_seq_len)
#print(len(X_test[0][0])) # 300 (300D vec)
#print(len(X_test[0])) # 30 (padding size)

#＊-----------UPDATED on Dec. 22 2018 at 16:00-----------＊#

# Prediction Example #
X_new = X_test[:50]
Y_new = Y_test[:50]
Y_hat = list(preLSTM.predict_classes(X_new))
print("\nY_hat: {},\nY_new: {}\n".format(Y_hat, Y_new))

for i in range(len(Y_hat)):
    pl_no = toy_test_dict[i]
    pl_nm = utils.PL_basic_dict()[pl_no]
    predicted = index_dict[Y_hat[i]][1]
    prediction_res = (Y_hat[i] == Y_new[i])
    if prediction_res == True:
        print("\t✔ | {} ===> {}".format(pl_nm, predicted))
    else:
        print("\t✖ | {} ===> {} | ✪정답: {}".format(pl_nm, predicted,index_dict[Y_new[i]][1]))