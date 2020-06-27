from flask import *
from elasticsearch import Elasticsearch

es = Elasticsearch()
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')  

@app.route('/search', methods=['GET'])
def search_songs():
    query  = request.args.get("q")
    from_  = request.args.get("from")
    
    body = {
        "from" : from_,
        "query": {
            "multi_match": {
                "query": query
            }
        }
    }

    res = es.search(index="songs", body=body)

    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)

