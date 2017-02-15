from mongoengine import *

connect('jike')

class People(Document):
    name = StringField(required=True)
    age = IntField(required=True)
    sex = StringField(required=True)
    salary = IntField()
meiji = People('jane', 25, 'female', 9999999)
meiji.save()
meiji.age = 21
meiji.save()
meiji.delete()