from data_preprocess import data_preprocess
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from sklearn.model_selection import train_test_split
from decision_tree_scratch import DecisionTree
import numpy as np
import pickle
import argparse
from data_preprocess_util import dataArrange

def train():
    x = data_preprocess()
    x.to_csv('Dataset.csv')

    y_actual = x.index
    x.reset_index(inplace= True, drop = True)
    encode = LabelEncoder()

    y = encode.fit_transform(y_actual)
    def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    X_train, X_test, y_train, y_test = train_test_split(x,y, test_size = .2, train_size = .8)
    X_train_val = X_train.values
    X_test_val =X_test.values
    clf = DecisionTree()
    clf.fit(X_train_val,y_train)

    y_pred = clf.predict(X_test_val)
    acc = accuracy(y_test, y_pred)

    print ("Accuracy:", acc)


    with open('model','wb') as model_file:
        pickle.dump(clf,model_file)

    with open('encode_model','wb') as model_file:
        pickle.dump(encode,model_file)

def prediction(X_raw):
    sympfile = open('symp_model','rb')
    symp_list = pickle.load(sympfile)

    infile = open('model','rb')
    clf = pickle.load(infile)

    encode_file = open('encode_model','rb')
    encode = pickle.load(encode_file)

    X = dataArrange(symp_list , X_raw)
    X = [X]

    pred = (clf.predict(X))
    pred = encode.inverse_transform(pred)
    print(pred[0])

    infile.close
    sympfile.close
    encode_file.close

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('function' , help='(train) - to train a model (predict) - to predict the disease')
    parser.add_argument('--symptoms' ,nargs='+', help='List of symptopms', default="")

    args = parser.parse_args()
    if (args.function == 'train'):
        train()
    elif (args.function == 'predict'):
        if (args.symptoms == ""):
            print("Please input symptoms")
        else:
            prediction(args.symptoms)
    else :
        print("Invalid Inputs, try typing (del.py -h) for help") 