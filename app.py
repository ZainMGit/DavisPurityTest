from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# 👇 Replace with your actual MongoDB URI!
mongo_uri = "mongodb+srv://zain:davispuritytest@davispuritytest.xdnj7kj.mongodb.net/?retryWrites=true&w=majority&appName=DavisPurityTest"

from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://zain:davispuritytest@davispuritytest.xdnj7kj.mongodb.net/?retryWrites=true&w=majority&appName=DavisPurityTest",  # replace this with your actual Mongo URI
    tls=True,
    tlsCAFile="C:/Program Files/SSL/cacert.pem"
)

db = client.purityDB
scores = db.scores

@app.route('/submit-score', methods=['POST'])
def submit_score():
    data = request.get_json()
    score = data.get('score')
    print("✅ Score received from frontend:", score)

    if score is None:
        return jsonify({'error': 'Score required'}), 400

    scores.insert_one({'score': score})
    print("✅ Score inserted into Mongo")

    agg = scores.aggregate([
        { "$group": {
            "_id": None,
            "avg": { "$avg": "$score" },
            "count": { "$sum": 1 }
        }}
    ])
    result = next(agg, {'avg': 0, 'count': 0})
    print("📊 Aggregation:", result)

    return jsonify({
        'averageScore': round(result['avg'], 2),
        'totalUsers': result['count']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
