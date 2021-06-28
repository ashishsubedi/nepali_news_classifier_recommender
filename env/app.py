import json
import os
import pickle
from os import path
from uuid import uuid4

from flask import Flask, render_template, request, url_for
from flask_cors import CORS, cross_origin
import joblib
import pandas as pd

'''
POST /api/classify
{
 "text": <news text>
}
POST /api/recommend
{
 "id":id
}
GET /api/random-news

'''

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def split_token(x):
    return x.split(' ')


clf = joblib.load('./models/svc_clf_pipeline.pkl')
#clf = None

with open('./models/similarity_matrix.pkl', 'rb') as f:
    similarity_matrix = pickle.load(f)


DATA_DIR = os.path.abspath('../datasets/output/data_2.csv')
df = pd.read_csv(DATA_DIR, index_col=0)
df['id'] = df.index


def item(id):
    id = str(id)
    return {
        'text': df.loc[df['id'] == id]['text'].tolist()[0].split(' - ')[0],
        'class': df.loc[df['id'] == id]['class'].tolist()[0].split(' - ')[0]
    }


def recommender(item_id, num):

    recs = similarity_matrix[str(item_id)][:num]
    print(json.dumps(recs))
    return json.dumps(recs)


@app.route('/',methods=['GET'])
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/api/random-news',methods=['GET'])
@cross_origin()
def random_news():
    num = request.args.get('num') or 10
    samples = df.sample(n=int(num),replace=True)
    #print(samples)
    return {
        'status': 'success',
        'code': 200,
        'data': samples.to_json()
    }


@app.route('/api/classify', methods=['POST'])
@cross_origin()
def classify():
    try:
        data = request.get_json(force=True)

        res = clf.predict([data['text']])[0]

        return {
            'status': 'success',
            'code': 200,
            'message': res
        }
    except Exception as e:
        return {
            'status': 'fail',
            'code': 501,
            "message": e
        }


@app.route('/api/recommend', methods=['POST'])
@cross_origin()
def recommend():
    try:

        data = request.get_json(force=True)
        print(data)
        res = recommender(item_id=data['id'],num=data['num'])

        return {
            'status': 'success',
            'code': 200,
            'message': res
        }
    except Exception as e:
        return {
            'status': 'fail',
            'code': 501,
            "message": e
        }

if __name__ == '__main__':
    app.run(debug=True)
