
from shutil import ExecError
from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, TextField, IntegerField
couch = Server("http://admin:admin@172.21.100.174:5984")
db = couch["staff"]
# db['123445'] = dict(name='vcute', age=25)
# db['34355'] = dict(name='hvcute', age=26)
view = ViewDefinition('filter', 'count_documents', '''function(doc) {
            emit(null, 1);
        }''', reduce_fun='_count')
res = view.sync(db) 
design_doc = view.get_doc(db)
print(design_doc)
class Person(Document):
    name = TextField()
    age = IntegerField()
    def __init__(self, name, age) -> None:
        super().__init__()
        self.name = name
        self.age = age
# person = Person("ttttt", "24")
# person.store(db)
# list_data = [{'name':'tai', 'age':21}, {'name':'tpai', 'age':18}]
try:
    db.update('list_data')
except Exception as err:
    print(err)
else:
    print("update success")
import random
name = 'ABCDEFGHKIJMNLPQSTUVRW'
b = [[x,y,z,t,w] for x,y,z,t,w in zip(name, name, name, name, name)]
# b = [''.join(i) for i in name]
print(b)
# a = [b + i + ',' for i in name]
# print(a)
# a += i for i in name
print(name[random.randrange(0, 22)] + name[random.randrange(0, 22)])
print(random.randrange(0, 22))
print(random.randrange(0, 22))
print(random.randrange(0, 22))
print(random.randrange(0, 22))  
print(random.randrange(0, 22))
print(random.randrange(0, 22))
# db.delete(db['06dac1926803d6682168038b2d01a3e1'])
# for row in db.view('tests/all'):
#     print(row)
# map_fun = '''function(doc) {
#         ...     if (name in doc)
#         ...         emit(doc.name, doc.age);
#         ... }'''
     
# for row in db.query(map_fun):
#         print(row.key, row.value)   
# mango = {
#     'selector': {
#         'name': 'vcute'
#     }
# }
# data = db.find(mango)

# for row in data:
#     row['name'] = 'vcutee'
#     print(row['_id'], row['_rev'], row['name'], row['age'])
#     db.update([row])
# for id in db:
#     print(db[id])
