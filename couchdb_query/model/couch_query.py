
from httplib2 import Http
from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, TextField, BooleanField, IntegerField, DateField
from couchdb.http import HTTPError, ResourceNotFound
from datetime import date, datetime, time
import sys
from json import dumps
import pandas as pd
# adding Folder_2 to the system path
# sys.path.insert(0, '/home/vietph/workspace/couchdb_crud/couchdb_query/doc')
sys.path.insert(0, '/home/vietph/workspace/couchdb_crud/couchdb_query')
sys.path.insert(0, '/home/vietph/workspace/couchdb_crud/couchdb_query/doc')
from staff import Staff
from helper import func_info
from helper import json_serial

class CouchQuery:
    def __init__(self, db):
        self.db = db
        self.list_view = []
        
    def create_view(self, design_name, view_name, map_func, reduce_func=None):
        """ Create a view for this database 
            A view include a design_name, view_name, map_function and reduce_function
        """
        view = ViewDefinition(design_name, view_name, map_fun=map_func, reduce_fun=reduce_func)
        view.sync(self.db) 
        doc_view = view.get_doc(self.db)
        if(doc_view['views'].get(view_name) != None):
            self.list_view.append({'db_name':self.db.name, 'design_name':design_name,
                               'view_name':view_name, 'map_function':map_func, 'reduce_function':reduce_func})
        return doc_view
    
    def insert_doc(self, doc, **kwargs):
        """ Insert a document """
        try: 
            if(doc != None):
                if(isinstance(doc, dict) == False):
                    f_info = func_info()
                    print('Error: ', f_info[0], f_info[1], f_info[2], " wrong data type: doc is dict type instead of ", type(doc)) 
                    return False
                return self.db.save(doc)
            else:
                return self.db.save(kwargs)
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
    
    def insert_docs(self, list_doc, batch_size = 128):
        """ Insert a list of documents """
        number_iter = len(list_doc) // 128
        for i in range(number_iter):
            try:
                self.db.update(list_doc[i*batch_size:(i+1)*batch_size])
            except TypeError as err:
                f_info = func_info()
                print('TypeError: ', f_info[0], f_info[1], f_info[2], err)
                return False
        try:
            self.db.update(list_doc[number_iter*batch_size:])
        except TypeError as err:
            f_info = func_info()
            print('TypeError: ', f_info[0], f_info[1], f_info[2], err)
            return False
        return True

    def update_doc(self, doc):
        """ Update a document """
        try:
            if(isinstance(doc, dict) == False):
                f_info = func_info()
                print('[Error]: ', f_info[0], f_info[1], f_info[2], ' wrong data type: doc is dict type instead of ', type(doc)) 
                return False
            return self.db.update([doc])
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
            return []
        except TypeError as err:
            f_info = func_info()
            print('TypeError: ', f_info[0], f_info[1], f_info[2], err)
            return []

    def update_docs(self, docs):
        """ Update a list of documents """
        if(isinstance(docs, list) == False):
            f_info = func_info()
            print('Error: ', f_info[0], f_info[1], f_info[2], ' wrong data type: doc is dict type instead of ', type(doc)) 
            return []
        try:
            return self.db.update(docs)
        except HTTPError as err:
            f_info = func_info()
            print('HTTPError: ', f_info[0], f_info[1], f_info[2], err)
            return []
        except TypeError as err:
            f_info = func_info()
            print('TypeError: ', f_info[0], f_info[1], f_info[2], err)
            return []
            
    def mango_query(self, query=None, selector=None, fields=None, sort=None, limit=None, skip=None, execution_stats=None, use_index=None):
        """Search by mango query. Return list of documents
            Components of a mango query
            - fields, sort, limit, skip, execution_stats are optinal properties
            {
                "selector": {
                    "status": { "$eq": "draft" }
                },
                "fields": ["_id", "_rev", "title", "content", "date", "author"],
                "sort": [],
                "limit": 10,
                "skip": 0,
                "execution_stats": true
            }
        """
        if(query == None and selector == None):
            return []
        if(query == None):
            query = {}
            query['selector'] = selector
            if(fields != None):
                query['fields'] = fields
            if(sort != None):
                query['sort'] = sort
            if(limit != None):
                query['limit'] = limit
            if(skip != None):
                query['skip'] = skip
            if(execution_stats != None):
                query['execution_stats'] = execution_stats
            if(use_index != None):
                query['use_index'] = use_index
        data = self.db.find(query)
        list_res = [doc for doc in data]
        return list_res
    
    def mango_query_explain(self, query=None, selector=None, fields=None, sort=None, limit=None, skip=None, execution_stats=None, use_index=None):
        """Explain mango query. Return list of documents"""
        if(query == None and selector == None):
            return {}
        if(query == None):
            query = {}
            query['selector'] = selector
            if(fields != None):
                query['fields'] = fields
            if(sort != None):
                query['sort'] = sort
            if(limit != None):
                query['limit'] = limit
            if(skip != None):
                query['skip'] = skip
            if(execution_stats != None):
                query['execution_stats'] = execution_stats
            if(use_index != None):
                query['use_index'] = use_index
        return self.db.explain(query)
    
    def view_query(self, design_name, view_name, wrapper=None, include_docs=False, **options):
        """There are many options include
            key,
            keys,
            startkey,
            endkey,
            group_level,
            limit,
            skip,
            descending,
            sort """
        data = self.db.view(design_name+'/'+view_name, wrapper=wrapper, include_docs=include_docs, **options)
        if(include_docs):
            return [{'key':dat['key'], 'value':dat['value'], 'doc':dat['doc']} for dat in data]
        else:
            return [{'key':dat['key'], 'value':dat['value']} for dat in data]
        
    def delete_doc(self, doc):
        try:
            self.db.delete(doc)
        except KeyError as err:
            f_info = func_info()
            print('KeyError: ', f_info[0], f_info[1], f_info[2], err)
        except ValueError as err:
            f_info = func_info()
            print('ValueError: ', f_info[0], f_info[1], f_info[2], err)
            
    def delete_docs(self, docs):
        if(isinstance(docs, list) == False):
            f_info = func_info()
            print('Error: ', f_info[0], f_info[1], f_info[2], " wrong data type: doc is dict type instead of ", type(doc)) 
            return False
        for doc in docs:
            try:
                self.db.delete(doc)
            except KeyError as err:
                f_info = func_info()
                print('KeyError: ', f_info[0], f_info[1], f_info[2], err)
            except ValueError as err:
                f_info = func_info()
                print('ValueError: ', f_info[0], f_info[1], f_info[2], err)
            
    def delete_doc_by_id(self, id):
        try:
            del self.db[id]
        except ResourceNotFound as err:
            f_info = func_info()
            print('Error: ', f_info[0], f_info[1], f_info[2], 'ResourceNotFound')
            
    def delete_docs_by_id(self, ids):
        if(isinstance(ids, list) == False):
            f_info = func_info()
            print('Error: ', f_info[0], f_info[1], f_info[2], " wrong data type: doc is dict type instead of ", type(doc)) 
            return False
        for id in ids:
            try:
                del self.db[id]
            except ResourceNotFound as err:
                f_info = func_info()
                print('Error ', f_info[0], f_info[1], f_info[2], 'ResourceNotFound')
            
    def purge_docs(self, docs):
        if(isinstance(docs, list) == False):
            f_info = func_info()
            print('Error: ', f_info[0], f_info[1], f_info[2], " wrong data type: doc is dict type instead of ", type(doc)) 
            return False
        try:
            self.db.purge(docs)
        except TypeError as err:
            f_info = func_info()
            print('TypeError: ', f_info[0], f_info[1], f_info[2], err)
    
class StaffModel(CouchQuery):
    def __init__(self, db):
        super().__init__(db)

        
import random 
if __name__ == '__main__': 
    couch = Server("http://admin:admin@172.21.100.174:5984")
    # couch = Server("http://admin:admin@localhost:5984")
    try:
        db = couch.create('staff')
    except HTTPError as err:
        print(err)
        db = couch['staff']

    
    data_demo = {'staff_code': 277457, 'full_name': 'NPTttaii', 'mail_code': 'tainp', 
    'cellphone': ['097881888', '098881888'], 'unit': 'TQDT', 'department': 'DK',
    'date_of_birth': json_serial(date(1998, 10, 2)), 
    'sex': 'male', 'title': 'system programing', 
    'note': 'pro', 'should_roll_up': True, 'active': True}
    staff_model = StaffModel(db)
    # res = staff_model.update_doc(data_demo)
    # print(res)
    doc_view = staff_model.create_view('filter', 'by_staff_code', '''function(doc) {
            emit(doc.staff_code, {name:doc.full_name, note:doc.note});
        }''')
    # print(doc_view)

    # kwarg = {'include_docs':True, 'startkey':100000, 'endkey':100010}
    view_data = staff_model.view_query('filter','count_documents', wrapper=None)
    # print(view_data[0])

    selector = {'staff_code': {'$gt': 100000, '$lt':250000}}
    query = {'selector':selector, 'limit':3000}
    # staff_model.delete(data_demo)
    data = staff_model.mango_query(selector={'staff_code':277457})
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        print(row["cellphone"][1])
    # staff_model.purge_docs(data)
    # for doc in data:
    #     staff_model.delete(doc)
        # print(doc['_id'], doc['staff_code'])
        # db.purge([doc])
        
    # print(staff_model.mango_query_explain(query))
    
# name = 'ABCDEFGHKIJMNLPQSTUVRW'
# list_doc = []
# batch_size = 128
# for code in range(300000, 306000):
#     full_name = name[random.randrange(0, 22)] + name[random.randrange(0, 22)] +\
#                 name[random.randrange(0, 22)] + name[random.randrange(0, 22)] +\
#                     name[random.randrange(0, 22)]
#     mail_code = full_name + '@vtx'
#     list_doc.append({'staff_code': code, 'full_name': full_name, 
#                      'mail_code': mail_code, 'cellphone': ['098'+str(code), '097'+str(code), '096'+str(code)], 
#                      'unit': 'TQDT', 'department': 'DK', 'date_of_birth':'02-10-1998', 
#                      'sex': 'male', 'title': 'system programing', 'note': 'pro', 
#                      'should_roll_up': True, 'active': True})
#     if(len(list_doc) == batch_size):
#         print(len(list_doc))
#         staff_model.insert_many(list_doc)
#         list_doc.clear()
