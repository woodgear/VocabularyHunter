from pydal import DAL, Field
import time as pytime
import datetime
import os
import json
DB_VERSION = 2


class DbModel:
    """the abstract layer of vh.

    make the caller need not to care about what and how to storage/fetch data

    Attributes:
        db: string the data base name,just to idenity.

    """

    def __init__(self, db_name="vh", folder_path="db_storage"):
        self.db_name = db_name
        self.folder_path = folder_path
        self._init_db()
        pass

    def __del__(self):
        if hasattr(self, "db"):
            self.db.close()
        pass

    def _init_db(self):
        sqlite_uri = f'sqlite://{self.db_name}.sqlite'
        self.db = DAL(sqlite_uri, folder=self.folder_path)
        # TODO  pydal会自动自动创建id字段为自增主键 user-id 是不是多余了
        self.db.define_table('word', Field('user_id'), Field(
            'word'), Field('word_type'), Field('time'))
        self.db.define_table('meta', Field('key'), Field('value'))

        self.db.meta.insert(key='db_version', value=DB_VERSION)
        self.db.commit()

        self.init_corpus_table(self.db)

    def _db(self):
        return self.db

    def get_all_unknow_word_by_id(self, id):
        """
        Args:
            id: string user id
        Returns:
            [string]
        """
        return [item.word for item in self.db((self.db.word.user_id == id) & (self.db.word.word_type == "unknow")).select(self.db.word.ALL)]

    def get_all_know_word_by_id(self, id):
        """
        Args:
            id: string user id
        Returns:
            [string]
        """
        return [item.word for item in self.db((self.db.word.user_id == id) & (self.db.word.word_type == "know")).select(self.db.word.ALL)]
        pass

    def mark_know_word_by_id(self, id, words):
        """
        Args:
            id: string user id
            words: [string]
        """
        for word in words:
            self.db.word.update_or_insert(
                (self.db.word.word == word) & (self.db.word.user_id == id),
                word=word,
                user_id=id,
                word_type="know",
                time=pytime.asctime(pytime.gmtime()))
        self.db.commit()
        pass

    def mark_unknow_word_by_id(self, id, words):
        """
        Args:
            id: string user id
            words: [string]
        """
        for word in words:
            self.db.word.update_or_insert(
                (self.db.word.word == word) & (self.db.word.user_id == id),
                word=word,
                user_id=id,
                word_type="unknow",
                time=pytime.asctime(pytime.gmtime()))
        self.db.commit()
        pass

    def init_corpus_table(self, db):
        """
初始化与语料相关的表 也许以后应当是横切的数据库
corpus_meta {
    id,                 # 自动生成主键之类的
    md5,            # corpus 应当是纯文字的感觉
    type,            # corpus类型 设计上有 article subtitle book 之类的
    struct,         # 存储来此corpus的结构 之后查询的时候 通过这个结构和倒排索引 拿到初始范围  {start:xx,end:xxx,type:"root",child:[{start:xx,end:xxx etc}]
    time, 
    source,        # 例如url之类的
    name,
}
corpus {
    id,
    content,
}

user_corpus {
    user_id,
    corpus_id
}

word_invert_index {
    word,
    lemma,
    corpus_id
    position, # left-right
}
        """
        db.define_table("corpus_meta",
                        Field("id", type="id"),
                        Field("md5", type="string", length=255),
                        Field("type", type="string", length=255),
                        Field("struct", type="string", length=10240),  # 应该够了
                        Field("time", 'datetime'),
                        Field("source", type="string", length=1024),
                        Field("name", type="string", length=1024),
                        )
        db.define_table("corpus",
                        Field("corpus_id", type='reference corpus_meta'),
                        Field("content", type="text", length=1024*1024),
                        )

        db.define_table("user_corpus",
                        Field("user_id", type="string"),
                        Field("corpus_id", type="reference corpus_meta")
                        )
        db.define_table("word_invert_index",
                        Field("word", type="string"),
                        Field("lemma", type="string"),
                        Field("corpus_id", type="reference corpus_meta"),
                        Field("span", type="string"),
                        )
        pass

    def has_article(self, article):
        record = self.db(self.db.corpus_meta.md5 ==
                         article["md5"]).select().first()
        return record != None
        pass

    def find_aritcle_meta(self, id):
        record = self.db.corpus_meta(id)
        if record is None:
            return None
        return record.as_dict()

    def find_aritcle(self, id, span):
        data = self.db(self.db.corpus.corpus_id == id).select(
            self.db.corpus.content[span[0]:span[1]]).first()
        raw = list(data._extra.as_dict().values())[0]
        return raw

    def save_aritcle(self, aritcle):
        raw_aritcle = aritcle["aritcle"]
        corpus_meta_data = {"name": aritcle["name"], "source": aritcle["source"], "type": aritcle["type"],
                            "time": aritcle["time"], "struct": aritcle["struct"], "md5": aritcle["md5"]}
        cropus_id = self.db.corpus_meta.insert(**corpus_meta_data)
        self.db.corpus.insert(corpus_id=cropus_id, content=raw_aritcle)
        self.db.commit()

        return cropus_id
        pass

    def save_word_invert_index(self, corpus_id, words):
        def map_word(corpus_id, word):
            word["corpus_id"] = corpus_id
            word["span"] = json.dumps(word["span"])
            return word
        words = [map_word(corpus_id, w) for w in words]
        self.db.word_invert_index.bulk_insert(words)
        self.db.commit()

        pass

    def connect_user_and_corpus(self, user_id, corpus_id):
        self.db.user_corpus.insert(
            **{"user_id": user_id, "corpus_id": corpus_id})
        self.db.commit()
        pass

    def find_word_invert_index(self, user_id, lemma):
        words = self.db(
            (self.db.user_corpus.user_id == user_id)
            & (self.db.word_invert_index.corpus_id == self.db.user_corpus.corpus_id)
            & (self.db.word_invert_index.lemma == lemma)
        ).select(self.db.word_invert_index.ALL)
        for w in words:
            w = w.as_dict()
            del w["id"]
            w["span"] = json.loads(w["span"])
            yield w
        pass
