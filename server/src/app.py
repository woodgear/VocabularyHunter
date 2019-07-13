from flask import *
from controler import *
from dicthelper import DictHelper
import json

app = Flask(__name__)


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
    id = request.headers.get('id')
    words = request.json["words"]
    res = DictHelper().describes(words)
    return jsonify(util.to_json_serializable(res))
