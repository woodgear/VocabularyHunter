from pydal import DAL, Field
import time as pytime
import os
DB_VERSION = 1


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
        self.db.define_table('word', Field('user_id'), Field(
            'word'), Field('word_type'), Field('time'))
        self.db.define_table('meta', Field('key'), Field('value'))
        self.db.meta.insert(key='db_version', value=DB_VERSION)
        self.db.commit()

    def init_corpus_table(self,db):
        """
初始化与语料相关的表 也许以后应当是横切的数据库
corpus_meta {
    id,                 # 自动生成主键之类的
    md5,            # corpus 应当是纯文字的感觉
    type,            # corpus类型 设计上有 article subtitle book 之类的
    struct,         # 存储来此corpus的结构 之后查询的时候 通过这个结构和倒排索引 拿到初始范围  {start:xx,end:xxx,type:"root",child:[{start:xx,end:xxx etc}]
    time, 
    source,        # 例如url之类的
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
        # 
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
    