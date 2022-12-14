"""File to train our model"""
import nltk #pylint: disable=W
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
stopword_list = stopwords.words('english')


def preprocess_text(input_text):
    """Function to Pre-process our dataset"""
    global stopword_list #pylint:disable= W C

    preprocessed_text = []
    lemmatizer = WordNetLemmatizer()
    tokenized_sentence = word_tokenize(input_text)
    for i, _ in enumerate(tokenized_sentence):
        tokenized_sentence[i] = tokenized_sentence[i].lower()
        if tokenized_sentence[i].isalpha() and tokenized_sentence[i] not in stopword_list:
            tokenized_sentence[i] = lemmatizer.lemmatize(tokenized_sentence[i])
            preprocessed_text.append(tokenized_sentence[i])
    output_text = ""
    for word in preprocessed_text:
        output_text = output_text + word + " "
    output_text.strip()
    #print(output_text)
    return output_text

def train_model():
    """Function to train Logistic Regression model"""
    train = pd.read_csv("fixed_final_dataset.csv", header=None, dtype=str)
    train = train.dropna()

    train.columns=["comment", "category"]
    train["processed"] = [preprocess_text(str(x)) for x in train["comment"]]

    bag_of_words = CountVectorizer(
        tokenizer=word_tokenize,
        stop_words=stopword_list,
        ngram_range=(1, 1)
    )

    train_split, test_split = train_test_split(train, test_size=0.2, random_state=0)

    train_text = bag_of_words.fit_transform(train_split.processed.astype(str))
    test_text = bag_of_words.transform(test_split.processed.astype(str))

    train_label = train_split["category"]
    test_label = test_split["category"]

    model = RandomForestClassifier()
    model.fit(train_text, train_label)

    predictions = model.predict(test_text)
    print("Accuracy: ", accuracy_score(test_label, predictions) * 100)

train_model()


