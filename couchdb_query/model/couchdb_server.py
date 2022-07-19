from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.http import HTTPError, ResourceNotFound, Unauthorized
from datetime import date, datetime
import sys, os
dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(dir, '..')))
from helper import func_info

DEFAULT_HOST = 'http://localhost:5984/'
DEFAULT_PORT = 5984
class CouchDBServer:
    stats= dict()
    version = str()
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, username=None, password=None):
        if(username == None and password == None):
            self.url = 'http://' + host + ':' + str(port)
            self.server = Server(self.url)
        else:
            if(isinstance(password, str) == False):
                password = str(password)
            self.url = 'http://' + username + ':' + password + '@' + host + ':' + str(port)
            self.server = Server(self.url)
            
        try:
            self.version = self.server.version()
            self.stats['status'] = 'Ok'
            self.stats['url'] = self.url
        except OSError as err:
            f_info = func_info()
            print('OSError: ', f_info[0], f_info[1], f_info[2], err)
            self.stats['error'] = {'OSError':err, 'url':self.url}
        except Unauthorized as err:
            f_info = func_info()
            print('UnauthorizedError: ', f_info[0], f_info[1], f_info[2], err)
            self.stats['error'] = {'Unauthorized':err, 'url':self.url}
            
    def status(self):
        return self.stats
    
    def version(self):
        return self.version
    
    def create_db(self, name):
        if(isinstance(name, str) == False):
            print('name field must be str instead of ', type(name))
            return None
        try:
            return self.server.create(name)
        except HTTPError as err:
            print('datebase ',name, 'is existed: ', err)
            return self.server[name]
        
    def db_by_name(self, name):
        if(isinstance(name, str) == False):
            print('name field must be str instead of ', type(name))
            return None
        try:
            return self.server[name]
        except ResourceNotFound as err:
            print('datebase ',name, 'is not found: ', err)
            return None
        
    def delete_db(self, name):
        if(isinstance(name, str) == False):
            print('name field must be str instead of ', type(name))
            return None
        try:
            del self.server[name]
        except ResourceNotFound as err:
            print('datebase ',name, 'is not found: ', err)
            
            