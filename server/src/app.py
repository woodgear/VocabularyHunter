from flask import *
from controler import *
import json
from flask_cors import CORS
from flask_gzip import Gzip

import time
import util
import gzip

def get_json_body(request):
        body = request.data
        if "Content-Encoding" in request.headers and request.headers["Content-Encoding"] == "gzip":
            body = gzip.decompress(body)
            body = json.loads(body)
        else:
            body = request.json
        return body


def create_app():
    app = Flask(__name__)
    CORS(app)
    Gzip(app)
    @app.route('/api/vh/hunter', methods=['POST'])
    def hunter():
        id = request.headers.get('id')

        article = get_json_body(request)["article"]

        print("hunter", id)
        unknow_words = Controller().find_unknow_words_by_article(id, article)
        return jsonify(words=unknow_words)

    @app.route('/api/vh/mark/know', methods=['POST'])
    def mark_know_word():
        id = request.headers.get('id')
        words = request.json["words"]
        Controller().mark_know_word(id, words)
        return ''

    @app.route('/api/vh/mark/unknow', methods=['POST'])
    def mark_unknow_word():
        id = request.headers.get('id')
        words = request.json["words"]
        Controller().mark_unknow_word(id, words)
        return ''

    @app.route('/api/vh/export/unknow', methods=['POST'])
    def export_unknow_word():
        id = request.headers.get('id')
        words = Controller().get_all_unknow_word(id)
        return jsonify(words=words)

    @app.route('/api/vh/export/know', methods=['POST'])
    def export_know_word():
        id = request.headers.get('id')
        words = Controller().get_all_know_word(id)
        return jsonify(words=words)

    @app.route('/api/vh/export/all', methods=['POST'])
    def export_all_word():
        print("export all")
        id = request.headers.get('id')
        know = Controller().get_all_know_word(id)
        unknow = Controller().get_all_unknow_word(id)
        return jsonify(util.to_json_serializable({"words": {"know":know, "unknow":unknow}}))

    @app.route('/api/vh/import/all', methods=['POST'])
    def import_all_word():
        print("import_all_word start")
        id = request.headers.get('id')
        words = get_json_body(request)["words"]
        know = words["know"]
        unknow = words["unknow"]
        Controller().mark_know_word(id,know)
        Controller().mark_unknow_word(id,unknow)
        print("import_all_word over")

        return jsonify(success=True)

    @app.route('/api/vh/explain', methods=['POST'])
    def get_word_explain():
        start_time = time.time()
        id = request.headers.get('id')
        print("explain", id)
        words = get_json_body(request)["words"]
        res = Controller().describes(id, words)
        elapsed_time = time.time() - start_time
        print(f"explain {len(words)} elapsed_time {elapsed_time*1000}")
        return jsonify(util.to_json_serializable(res))

    @app.route('/api/vh/corpus', methods=['POST'])
    def add_corpus():
        start_time = time.time()
        id = request.headers.get('id')
        print("add_corpus",id)
        words = get_json_body(request)
        res = Controller().save_article(id, words)
        elapsed_time = time.time() - start_time
        print(f"collection  elapsed_time {elapsed_time*1000}")
        return jsonify(success=True)

    return app
