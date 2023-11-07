from pymongo import MongoClient
import csv
import csv
import os
import json
import requests
import time

import tensorflow as tf
import numpy as np
import pandas as pd
from nltk.tokenize import TweetTokenizer


tk = TweetTokenizer()

MODEL_PATH = '././train/model_output/caption_to_category'
connection_string = ''
db_name = 'clarus-ai-core'
database_data_file_name = 'data1.csv'
prediction_csv_file_name = 'categorization.1.csv'
is_art_thresholds = 0.61


def connect_to_db():
    client = MongoClient(connection_string)
    db = client[db_name]
    artists = db.artists
    return artists


def create_artist_dict(artists):
    artist_dict = {}

    for a in artists.find():
        artist_dict[a['instagram']['handle']] = ''
        if a.get('instagram', {}).get('media', {}).get('all', 'NA') != 'NA':
            for c in a['instagram']['media']['all']:
                if c['caption'] is not None:
                    artist_dict[a['instagram']['handle']] += c['caption']
    return artist_dict


def create_csv_file(artist_dict):
    with open(database_data_file_name, 'w') as csvfile:
        fieldnames = ['Handle', 'Caption']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in artist_dict:
            if artist_dict[data] != '':
                print(data)
                writer.writerow({'Handle': data, 'Caption': artist_dict[data].replace('#', '')})


def database_data_to_csv():
    artists = connect_to_db()
    artist_dict = create_artist_dict(artists)
    create_csv_file(artist_dict)




def setup_model():

    model = tf.keras.models.load_model(MODEL_PATH+'/model_v002 (71.5)')

    return model


def setup_tokenizer():
    with open(MODEL_PATH+"/tokenizer.json") as f:
        data = json.load(f)
        tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(data)
        return tokenizer


def setup_label_dict(file_name):
    filepath = os.path.abspath(os.path.join(os.getcwd(),
                                            "data/url_to_category/downloads/IAB/" + file_name))
    with open(filepath) as f:
        full_label_dict = json.load(f)
    return full_label_dict


def words_len(words):
    if len(words) >= 300:
        return words

    return words_len(words + words)


def get_words(text, numwords=300):
    words = tk.tokenize(text)
    if len(words) == 0:
        return []
    words = words_len(words)[0:numwords]

    return words


def categories(predictions):
    full_label_dict = setup_label_dict('iab.json')
    artist_label_dict = setup_label_dict('art.json')


    results = []
    art_result = []

    i = 0
    for k, v in full_label_dict.items():
        results.append({
            'Label': v,
            'Prediction': predictions[0][i]
        })
        if k in artist_label_dict:
            art_result.append({
                'Label': v,
                'Prediction': predictions[0][i]
            })
        i += 1


    pred_df = pd.DataFrame(data=results)
    pred_art_df = pd.DataFrame(data=art_result)


    pd.options.display.float_format = "{:,.2f}".format
    return pred_df.sort_values(by='Prediction', ascending=False), pred_art_df


def predict_category(text, model, tok):
    words = get_words(text)
    if len(words) == 0:
        return []

    wordss = [" ".join(words)]
    test_text = tok.texts_to_sequences(wordss)
    test_text = tf.keras.preprocessing.sequence.pad_sequences(
        test_text, maxlen=300)

    predictions = model(test_text)
    tf.keras.backend.clear_session()

    return categories(predictions)


def create_lable(art_sum):
    if art_sum > is_art_thresholds:
        return 'True'
    else:
        return 'False'


def create_prediction_csv(model, tok):
    count = 0
    with open(database_data_file_name, newline='') as incsv:
        with open(prediction_csv_file_name, mode='w') as outcsv:
            reader = csv.reader(incsv)
            fieldnames = ['Handle', 'Label', 'Prediction', 'Is artist']
            writer = csv.DictWriter(outcsv, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                count += 1
                if count == 1:
                    continue
                handle = row[0]
                text = row[1]
                prediction, art_pred = predict_category(text, model, tok)
                prediction = prediction.head(3)
                art_sum = sum([float(p) for p in art_pred['Prediction']])
                is_artist = create_lable(art_sum)

                writer.writerow({'Handle': handle, 'Label': [l for l in prediction['Label']],
                                 'Prediction': ["%.3f" % float(p) for p in prediction['Prediction']],
                                 'Is artist': is_artist})


def predict_from_url_csv(create_csv = False):
    if create_csv:
       database_data_to_csv()

    model = setup_model()
    tok = setup_tokenizer()
    create_prediction_csv(model, tok)


def main():
    predict_from_url_csv(())


if __name__ == "__main__":
    main()
