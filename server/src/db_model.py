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
    def __del__(self):
        self.db.close()
        pass  

    def _init_db(self):
        print("init_db")
        try:
            sqlite_uri = f'sqlite://{self.db_name}.sqlite'
            print(sqlite_uri,self.folder_path)
            self.db = DAL(sqlite_uri, folder=self.folder_path)
            self.db.define_table('word', Field('user_id'),Field('word'),Field('word_type'),Field('time'))
            self.db.define_table('meta', Field('key'),Field('value'))
            self.db.meta.insert(key='db_version',value=DB_VERSION)
            self.db.commit()
        except Exception as Err:
            print("err",Err)

        print("init_db over")
        pass
    def get_all_unknow_word_by_id(self,id):
        """
        Args:
            id: string user id
        Returns:
            [string]
        """
        return [item.word for item in self.db((self.db.word.user_id==id) & (self.db.word.word_type=="unknow")).select(self.db.word.ALL)]
    def get_all_know_word_by_id(self,id):
        """
        Args:
            id: string user id
        Returns:
            [string]
        """
        return [item.word for item in self.db((self.db.word.user_id==id) & (self.db.word.word_type=="know")).select(self.db.word.ALL)]
        pass
    def mark_know_word_by_id(self,id,words):
        """
        Args:
            id: string user id
            words: [string]
        """
        for word in words:
            self.db.word.update_or_insert(
            (self.db.word.word == word) & (self.db.word.user_id == id) ,
            word=word,
            user_id=id,
            word_type="know",
            time=pytime.asctime(pytime.gmtime()))        
        self.db.commit()
        pass

    def mark_unknow_word_by_id(self,id,words):
        """
        Args:
            id: string user id
            words: [string]
        """
        for word in words:
            self.db.word.update_or_insert(
            (self.db.word.word == word) & (self.db.word.user_id == id) ,
            word=word,
            user_id=id,
            word_type="unknow",
            time=pytime.asctime(pytime.gmtime()))
        self.db.commit()
        pass        