import logging
import sqlite3
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

import pymorphy3
morph = pymorphy3.MorphAnalyzer()


from .settings import INDEX_DATABASE
from .settings import APPLICATION_DIR

from .convert import Converter

logging.basicConfig(level=logging.INFO, filename=os.path.join(APPLICATION_DIR, 'indexing.log'), filemode="w")


class IndexDB:
    def __init__(self):
        self.con = sqlite3.connect(INDEX_DATABASE, check_same_thread=False)
        self.con.text_factory = lambda data: str(data, encoding="utf-8", errors='ignore')
        
        create_table_query = 'CREATE TABLE IF NOT EXISTS words (storage TEXT, filename TEXT NOT NULL, original_filename TEXT NOT NULL, word TEXT NOT NULL, count INTEGER NOT NULL, filesize INTEGER NOT NULL)'
        self.con.cursor().execute(create_table_query)
        self.con.commit()


    def __del__(self):
        self.con.close()
        
    
    def close(self):
        self.con.close()


    def set_storage(self, storage):
        self.storage = storage
        

    def get_word_count(self, filename, word):
        result = self.con.cursor().execute('SELECT * FROM words WHERE storage=? AND filename=? AND word=?', (self.storage, filename, word)).fetchone()
        
        if result == None:
            return 0
        
        return int(result[4])
        

    def inc_word(self, filename, original_filename, word, count, filesize):
        current_word_count = self.get_word_count(filename, word)
        
        if current_word_count == 0:
            self.con.cursor().execute('INSERT INTO words (storage, filename, original_filename, word, count, filesize) VALUES(?,?,?,?,?,?)', (self.storage, filename, original_filename, word, count, filesize))
        else:
            self.con.cursor().execute('UPDATE words SET count=? WHERE storage=? AND filename=? AND word=?', (current_word_count + count, self.storage, filename, word))
        
        self.con.commit()
        

    def get_files_with_word(self, word):
        return self.con.cursor().execute('SELECT * FROM words WHERE word=?', (word, )).fetchall()
        

class Indexing:
    def __init__(self):
        self.db = IndexDB()
    
    
    def __del__(self):
        self.db.close()
        
        
    def close(self):
        self.db.close()


    def set_storage(self, storage):
        self.storage = storage
        self.db.storage = storage
        
    
    def index_file(self, file_name, original_file_name):
        text = Converter.convert(file_name)
        word_counts = {}

        for word in text.split(' '):
            word = word.strip(',:.;\"\'!@#$%^&*()[]{}<>?»«-_')
            word = word.lower()
            
            word = word_modifier(word)
            
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
                
        for word in word_counts:
            self.db.inc_word(os.path.basename(file_name), original_file_name, word, word_counts[word], os.path.getsize(file_name))

    
    def get(self, query):
        words = query.split(' ')
        
        words_result = []

        for word in words:
            words_result.append(self.db.get_files_with_word(word_modifier(word)))

        words_result_copy = words_result.copy()
        original_list = words_result.copy()
        def get_file_ids(sublist):
            return set(item[1] for item in sublist)
        file_id_sets = [get_file_ids(sublist) for sublist in original_list]
        common_file_ids = set.intersection(*file_id_sets)
        filtered_list = [
            [item for item in sublist if item[1] in common_file_ids]
            for sublist in original_list
        ]
        for sublist in filtered_list:
            print(sublist)
        words_result = filtered_list.copy()   
    
        original_names = {}
        filesizes = {}
        files = {}
        logging.info(words)
        
        for word in words_result:
            for row in word:
                original_names[row[1]] = row[2]
                filesizes[row[1]] = row[5]
                
                if row[1] in files:
                    files[row[1]] += row[4]
                else:
                    files[row[1]] = row[4]
        
        result = dict(sorted(files.items(), key=lambda item: item[1], reverse=True))
        r = []
        for filename in result:
            r.append([filename.rsplit('.', 1)[0], result[filename], original_names[filename], round(filesizes[filename] / 1024, 1), filename.rsplit('.', 1)[1]])
        logging.info(r)
        
        words_result = words_result_copy.copy()
        original_names = {}
        filesizes = {}
        files = {}
        logging.info(words)
        
        for word in words_result:
            for row in word:
                original_names[row[1]] = row[2]
                filesizes[row[1]] = row[5]
                
                if row[1] in files:
                    files[row[1]] += row[4]
                else:
                    files[row[1]] = row[4]
        
        result = dict(sorted(files.items(), key=lambda item: item[1], reverse=True))
        r = []
        for filename in result:
            r.append([filename.rsplit('.', 1)[0], result[filename], original_names[filename], round(filesizes[filename] / 1024, 1), filename.rsplit('.', 1)[1]])
        logging.info(r)
        
        no_duplicates_list = []
        for item in r:
            if item not in no_duplicates_list:
                no_duplicates_list.append(item)
                
        return no_duplicates_list


def word_modifier(word):
    parsed_word = morph.parse(word)[0]
    normalized_word = parsed_word.normal_form
    return normalized_word


# def word_modifier(word): # функция модификации слова, применяется как при индексации файла так и при поиске
#     # Список возможных русских окончаний
#     endings = ['а', 'я', 'и', 'ы', 'е', 'о', 'ё', 'ю', 'э', 'ь', 'ъ', 'й']
    
#     # Проверяем, заканчивается ли слово одним из окончаний
#     for ending in endings:
#         if word.endswith(ending):
#             # Если слово заканчивается окончанием, удаляем его
#             return word[:-len(ending)]

#     return word