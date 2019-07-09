from pydal import DAL, Field
import time as pytime
DB_VERSION = 1

class DbModel:
    """the abstract layer of vh.

    make the caller need not to care about what and how to storage/fetch data

    Attributes:
        db: string the data base name,just to idenity.
    
    """
    def __init__(self,db_name="vh",folder_path="db_storage"):
        self.db_name=db_name
        self.folder_path=folder_path
        self._init_db()
        pass
    def _init_db(self):
        sqlite_uri = f'sqlite://{self.db_name}.sqlite'
        self.db = DAL(sqlite_uri, folder=self.folder_path)
        self.db.define_table('know', Field('user_id'),Field('word'),Field('time'))
        self.db.define_table('unknow', Field('user_id'),Field('word'),Field('time'))
        self.db.define_table('meta', Field('key'),Field('value'))
        self.db.meta.insert(key='db_version',value=DB_VERSION)
        self.db.commit()
        pass
    def __del__(self):
        self.db.close()
        pass  
    def get_all_unknow_word_by_id(self,id):
        """
        Args:
            id: string user id
        Returns:
            [string]
        """
        return [item.word for item in self.db(self.db.unknow.user_id==id).select(self.db.unknow.ALL)]
        pass
    def get_all_know_word_by_id(self,id):
        """
        Args:
            id: string user id
        Returns:
            [string]
        """
        return [item.word for item in self.db(self.db.know.user_id==id).select(self.db.know.ALL)]
        pass
    def insert_know_word_by_id(self,id,words):
        """
        Args:
            id: string user id
            words: [string]
        """
        for word in words:
            self.db.know.insert(user_id=id,word=word,time=pytime.asctime(pytime.gmtime()))
        self.db.commit()
        pass

    def insert_unknow_word_by_id(self,id,words):
        """
        Args:
            id: string user id
            words: [string]
        """
        for word in words:
            self.db.unknow.insert(user_id=id,word=word,time=pytime.asctime(pytime.gmtime()))
        self.db.commit()
        pass

    def replace_know_word_by_id(self,id,words):
        """
        Args:
            id: string user id
            words: [string]
        """
        self.db.know.truncate()
        self.db.commit()
        self.insert_know_word_by_id(id,words)
        pass

    def replace_unknow_word_by_id(self,id,words):
        """
        Args:
            id: string user id
            words: [string]
        """
        self.db.unknow.truncate()
        self.db.commit()
        self.insert_unknow_word_by_id(id,words)
        pass
