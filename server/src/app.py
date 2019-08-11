from flask import *
from controler import *
import json
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

@app.route('/hunter',methods=['POST'])
def hunter():
    id = request.headers.get('id')
    article = request.json["article"]
    unknow_words = Controller().find_unknow_words_by_article(id,article)
    return jsonify(words=unknow_words)

@app.route('/mark/know',methods=['POST'])
def mark_know_word():
    id = request.headers.get('id')
    words = request.json["words"]
    Controller().mark_know_word(id,words)
    return ''

@app.route('/mark/unknow',methods=['POST'])
def mark_unknow_word():
    id = request.headers.get('id')
    words = request.json["words"]
    Controller().mark_unknow_word(id,words)
    return ''


@app.route('/export/unknow',methods=['POST'])
def export_unknow_word():
    id = request.headers.get('id')
    words = Controller().get_all_unknow_word(id)
    return jsonify(words=words)

@app.route('/export/know',methods=['POST'])
def export_know_word():
    id = request.headers.get('id')
    words = Controller().get_all_know_word(id)
    return jsonify(words=words)

@app.route('/explain',methods=['POST'])
def get_word_explain():
    start_time = time.time()
    id = request.headers.get('id')
    words = request.json["words"]
    res = Controller().describes(id,words)
    elapsed_time = time.time() - start_time
    print(f"explain {len(words)} elapsed_time {elapsed_time*1000}")
    return jsonify(util.to_json_serializable(res))
