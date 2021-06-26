import json
import os
import pickle
from os import path
from uuid import uuid4

from flask import Flask, render_template, request, url_for
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
def split_token(x):
    return x.split(' ')
clf = joblib.load('./models/svc_clf_pipeline.pkl')

# with open('./models/svc_clf_pipeline.pkl','rb') as f:
#     clf = pickle.load(f)
# with open('svc_clf_test_set_72_acc.pkl','rb') as f:
#     model = pickle.load(f)
# with open('tfid_vectorizer.pkl','rb') as f:
#     tfidfVectorizer = pickle.load(f)
with open('./models/similarity_matrix.pkl','rb') as f:
    similarity_matrix = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/classify',methods=['POST'])
def classify():
    try:
        print(request.json)
        data = request.get_json(force=True)

        res = clf.predict([data['text']])[0]

        return {
            'status':'success',
            'code': 200,
            'message': res
        }
    except Exception as e:
        return {
            'status':'fail',
            'code': 501,
            "message":e
        }

@app.route('/api/recommend',methods=['POST'])
def recommend():
    try:
        data = json.loads(request.data)
        res = clf.predict([data])[0]
        
        return {
            'status':'success',
            'code': 200,
            'message': res
        }
    except Exception as e:
        return {
            'status':'fail',
            'code': 501,
            "message":e
        }

if __name__ == '__main__':
    app.run(debug=True)