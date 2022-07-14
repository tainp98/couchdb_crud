
from couchdb import Server
from couchdb.design import ViewDefinition
from couchdb.mapping import Document, TextField, IntegerField
couch = Server("http://admin:admin@172.21.100.174:5984")
db = couch["db_test"]
# db['123445'] = dict(name='vcute', age=25)
# db['34355'] = dict(name='hvcute', age=26)
view = ViewDefinition('tests', 'all', '''function(doc) {
            if('name' in doc)
                emit(doc.name, doc.age);
        }''')
res = view.sync(db) 
design_doc = view.get_doc(db)

class Person(Document):
    name = TextField()
    age = IntegerField()
    def __init__(self, name, age) -> None:
        super().__init__()
        self.name = name
        self.age = age
person = Person("hvnn", "28")
# person.store(db)
db.delete(db['06dac1926803d6682168038b2d01a3e1'])
for row in db.view('tests/all'):
    print(row)
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
#     print(row)
# for id in db:
#     print(db[id])
