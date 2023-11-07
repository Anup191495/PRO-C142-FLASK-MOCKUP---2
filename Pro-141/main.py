from flask import Flask, jsonify
from demographic_filtering import output
from content_filtering import get_recommendation
from storage import all_articles, liked_articles, not_liked_articles
from content_filtering import cosine_sim
import csv

all_articles = []
with open('articles.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)
    all_articles = data[1:]

liked_articles = []
not_liked_articles = []
did_not_read = []

app = Flask(__name__)

@app.route('/get_articles')
def get_articles():
    if all_articles:
        article = all_articles[0]
        return jsonify({
            "data": article,
            "status": "success"
        })
    else:
        return jsonify({"status": "no more articles"})

@app.route("/liked_articles", methods=["POST"])
def mark_liked_articles():
    if all_articles:
        article = all_articles[0]
        all_articles.pop(0)
        liked_articles.append(article)
        return jsonify({
            "status": "success"
        })
    else:
        return jsonify({"status": "no more articles"})

@app.route("/not_liked_articles", methods=["POST"])
def mark_not_liked_articles():
    if all_articles:
        article = all_articles[0]
        all_articles.pop(0)
        not_liked_articles.append(article)
        return jsonify({
            "status": "success"
        })
    else:
        return jsonify({"status": "no more articles"})

@app.route("/did_not_read", methods=["POST"])
def mark_did_not_read():
    if all_articles:
        article = all_articles[0]
        all_articles.pop(0)
        did_not_read.append(article)
        return jsonify({
            "status": "success"
        })
    else:
        return jsonify({"status": "no more articles"})
    
@app.route('/popular_articles', methods=['GET'])
def popular_articles():
    popular_articles_list = output.to_dict(orient='records')
    return jsonify({'popular_articles': popular_articles_list})

@app.route('/recommended_articles/<int:contentId>', methods=['GET'])
def recommended_articles(contentId):
    recommendations = get_recommendation(contentId, cosine_sim)  # Use the imported cosine_sim
    return jsonify({'recommended_articles': recommendations})

if __name__ == "__main__":
    app.run()

