from peewee import *
from uuid import uuid4
db = SqliteDatabase('db/users.sqlite')

class Users(Model):
    id = PrimaryKeyField()
    balance = IntegerField(default=0)
    noficate=BooleanField(default=True)
    photo= BooleanField(default=True)

    class Meta:
        database=db

class Pay(Model):
    id=PrimaryKeyField()
    token=TextField()

    class Meta:
        database=db
    


with db:
    db.create_tables([Users,Pay])


def start_press(_id):
    with db:
        if Users.select(1).where(Users.id == _id).exists() == False:
            Users.create(id=_id)

def get_balance(_id):
    with db:
        return Users.get(Users.id==_id).balance

def buy(_id,sum):
    with db:
        bali = Users.get(Users.id==_id).balance
        if bali >= sum:
            Users.update(balance=bali-sum).where(Users.id == _id).execute()
            return True
        else:
            return False

def give_balance(_id,sum):
    with db:
        bali = Users.get(Users.id==_id).balance
        Users.update(balance=bali+sum).where(Users.id == _id).execute()

def token(_id):
    with db:
        if Pay.select(1).where(Pay.id==_id).exists() == False:
            gen_token =uuid4()
            Pay.create(id=_id,token=gen_token)
            return gen_token
        else:
            return Pay.get(Pay.id==_id).token

def del_token(tok):
    with db:
        if Pay.select(1).where(Pay.token==tok).exist():
            _id = Pay.get(Pay.token==tok).id
            Pay.delete().where(Pay.token==tok).execute()
            return _id

def sta():
    with db:
        return len(Users.select(Users.id))


async def send(all,mark):
    with db:
        f=0
        for user in Users.select(Users.id):
            try:
                await all.copy_to(user.id,reply_markup=mark)
                f+=1
            except:
                Users.delete().where(Users.id==user.id).execute()
        return f


#give_balance(1783366130,100)