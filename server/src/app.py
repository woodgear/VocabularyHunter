from flask import *
from controler import *
import json
from flask_cors import CORS
from flask_gzip import Gzip

import time

import gzip

def create_app():
    app = Flask(__name__)
    CORS(app)
    Gzip(app)
    @app.route('/api/vh/hunter',methods=['POST'])
    def hunter():
        id = request.headers.get('id')
        body=request.data
        if request.headers["Content-Encoding"]== "gzip":
            body=gzip.decompress(body)
            body = json.loads(body)
        else:
            body =request.json()

        article = body["article"]
        
        print("hunter",id)
        unknow_words = Controller().find_unknow_words_by_article(id,article)
        return jsonify(words=unknow_words)

    @app.route('/api/vh/mark/know',methods=['POST'])
    def mark_know_word():
        id = request.headers.get('id')
        words = request.json["words"]
        Controller().mark_know_word(id,words)
        return ''

    @app.route('/api/vh/mark/unknow',methods=['POST'])
    def mark_unknow_word():
        id = request.headers.get('id')
        words = request.json["words"]
        Controller().mark_unknow_word(id,words)
        return ''


    @app.route('/api/vh/export/unknow',methods=['POST'])
    def export_unknow_word():
        id = request.headers.get('id')
        words = Controller().get_all_unknow_word(id)
        return jsonify(words=words)

    @app.route('/api/vh/export/know',methods=['POST'])
    def export_know_word():
        id = request.headers.get('id')
        words = Controller().get_all_know_word(id)
        return jsonify(words=words)

    @app.route('/api/vh/explain',methods=['POST'])
    def get_word_explain():
        start_time = time.time()
        id = request.headers.get('id')
        print("explain",id)

        body=request.data
        if request.headers["Content-Encoding"]== "gzip":
            body=gzip.decompress(body)
            body = json.loads(body)
        else:
            body =request.json()

        words = body["words"]
        res = Controller().describes(id,words)
        elapsed_time = time.time() - start_time
        print(f"explain {len(words)} elapsed_time {elapsed_time*1000}")
        return jsonify(util.to_json_serializable(res))
    
    return app