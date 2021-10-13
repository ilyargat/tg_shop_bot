from data.data_edit import dating
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from db.db import token
from config import PHONE
from json import load
start_buttons=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⚡️ Товары',callback_data='nalik')).add(InlineKeyboardButton(text='🎫 Аккаунт',callback_data='me'),InlineKeyboardButton(text='💸 Пополнить баланс',callback_data='money'))

def towars_buttons():
    towars = InlineKeyboardMarkup()
    with open('data/data.json','rb') as g:
        data = load(g)['towars']
    h=0
    while h<len(data):
        print(h,len(data))
        if h%2==0 and h!=len(data)-1:
            towars.add(InlineKeyboardButton(text=data[h]['text'],callback_data='get|'+data[h]['callback']),InlineKeyboardButton(text=data[h+1]['text'],callback_data='get|'+data[h+1]['callback']))
            h+=2
        else:
            towars.add(InlineKeyboardButton(text= data[h]['text'],callback_data='get|'+data[h]['callback']))
            h+=1
    towars.add(InlineKeyboardButton(text='👈 Вернуться в меню',callback_data='exit'))
    return towars

me_buttons=InlineKeyboardMarkup().add(InlineKeyboardButton(text='👈 Вернуться в меню',callback_data='exit'),InlineKeyboardButton(text='🔧 Настройки',callback_data='settings'))

def pay_but(_id,key=None):
    but = InlineKeyboardMarkup()
    tok_now = token(_id)
    def gen(commen,sum):
        return InlineKeyboardButton(text=f'{sum} ₽',url=f'https://qiwi.com/payment/form/99?amountInteger={sum}&amountFraction=0&currency=643&extra%5B%27comment%27%5D={commen}&extra%5B%27account%27%5D={PHONE}&blocked%5B0%5D=comment&blocked%5B1%5D=account')
    if key!=None:
        but.row(InlineKeyboardButton(text='👈 Вернуться в меню',callback_data='exit'),gen(tok_now,key))
    else:
        but.row(gen(tok_now,25),gen(tok_now,50)).row(gen(tok_now,100),gen(tok_now,200)).row(gen(tok_now,500)).add(InlineKeyboardButton(text='👈 Вернуться в меню',callback_data='exit'),InlineKeyboardButton(text='🆗 Я оплатил',callback_data='oplata_check'))
    return but



def buy_buttons(call,num):
    return InlineKeyboardMarkup().row(InlineKeyboardButton(text='⏪',callback_data='change|-5|'+call.split('|')[1]),InlineKeyboardButton(text='◀️',callback_data='change|-1|'+call.split('|')[1]),InlineKeyboardButton(text=str(num),callback_data='none'),InlineKeyboardButton(text='▶️',callback_data='change|+1|'+call.split('|')[1]),InlineKeyboardButton(text='⏩',callback_data='change|+5|'+call.split('|')[1])).add(InlineKeyboardButton(text='👈 Вернуться в меню',callback_data='exit'),InlineKeyboardButton(text='✅ Купить',callback_data='buy|'+call.split('|')[1]))

admin_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Создать товар',callback_data='creat'),InlineKeyboardButton('Добавить предметы в товар',callback_data='adder'),InlineKeyboardButton('Удалить товар',callback_data='deleter')).add(InlineKeyboardButton('Рассылка',callback_data='toall'),InlineKeyboardButton('Статистика',callback_data='stat'))
adm_exit = InlineKeyboardMarkup().add(InlineKeyboardButton('👈 Выйти в админ меню',callback_data='exit_adm'))


def tow_but():
    mark = InlineKeyboardMarkup()
    for i in dating().return_towar_list():
        ca = i['callback']
        mark.add(InlineKeyboardButton(text=i['text'],callback_data=f'edit|{ca}'))
    return mark.add(InlineKeyboardButton('👈 Выйти в админ меню',callback_data='exit_adm'))


