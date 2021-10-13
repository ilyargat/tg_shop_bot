from json import load,dump
from random import choice

class dating:
    def __init__(self) -> None:
        with open('data/data.json',encoding='utf-8')as g:
            self.data=load(g)
    
    def search(self,call,use,key=None):
        for tovar in self.data['towars']:
            if call == tovar['callback']:
                if key:
                    return tovar[key]
                else:
                    name = tovar['text']
                    price = use*tovar['price']
                    num = len(tovar['items'])
                    return f'<b>📝 {name}\n\n💵 Цена: {price} ₽\n📦 В наличии: {num}\n\nВы берете {use} товар(-ов)</b>'
    
    def save(self):
        with open('data/data.json','w') as j:
            j.seek(0)       
            dump(self.data, j, indent=4)
    
    def buy(self,call,use):
        f=''
        for tovar in self.data['towars']:
            if call == tovar['callback']:
                if len(tovar['items'])<use:
                    return False
                for i in range(use):
                    ine=choice(tovar['items'])
                    f=f+ine+'\n'
                    tovar['items'].remove(ine)
        self.save()
        return f'<b>👑 Спасибо за покупку вот ваш товар\n\n{f}</b>'

    def creat(self,text,callback,price,items):
        default = {'text':text,'callback':callback,'price':price,'items':items}
        self.data['towars'].append(default)
        self.save()
    
    def update(self,text,item,what_update=['text','callback','items','price'],all=False):
        for updater in self.data['towars']:
            if updater['callback']==text:
                if what_update =='items':
                    if all==True:
                        updater[what_update]=[item]
                    else:
                        updater[what_update].append(item)
                else:
                    updater[what_update]=item

        self.save()
    def remov(self,text):
        for item in self.data['towars']:
            if item['text']==text:
                self.data['towars'].remove(item)

        self.save()

    def read_admin(self,_id):
        for admins in self.data['admins']:
            if str(_id) in admins.keys():
                return admins[str(_id)]
    
    def return_towar_list(self):
        return self.data['towars']
    
    def promote(self,_id,prava):
        for admins in self.data['admins']:
            if _id not in admins:
                self.data['admins'].append({_id:prava})
            else:
                admins[str(_id)]=prava
        self.save()

    def demote(self,_id):
        for  admin in self.data['admins']:
            if str(_id) in admin.keys():
                self.data['admins'].remove(admin)
            
        self.save()

