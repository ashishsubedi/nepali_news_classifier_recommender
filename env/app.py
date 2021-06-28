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

similarity_matrix = joblib.load('./models/similarity_matrix.joblib')
# with open('./models/similarity_matrix.pkl', 'rb') as f:
#     similarity_matrix = pickle.load(f)


DATA_DIR = os.path.abspath('./datasets/output/data_2.csv')
df = pd.read_csv(DATA_DIR, index_col=0)
df['id'] = df.index


# def item(id):
#     id = str(id)
#     print(df.loc[int(id)]['text'])
#     return {
#         'text': df.loc[int(id)]['text'],
#         'class': df.loc[int(id)]['class']
#         }


def recommender(item_id, num):

    recs = similarity_matrix[int(item_id)][:num]
    # print(df.loc[int(item_id)]['text'])
    # recs = list(map(lambda s,id,cat: (s,df.loc[int(id)]['text'],cat),recs))
    res = [(s,df.loc[int(_id)]['text'],cat) for s,_id,cat in recs]
    return json.dumps(res)


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
