from aiogram import Bot
from aiogram.dispatcher import Dispatcher,FSMContext
from aiogram.utils import executor
from aiogram.types import Message,CallbackQuery, message
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db.db import send, start_press,buy,give_balance,sta
from startup.noficate import Noficate
from config import TOKEN,CREATOR,PHOTO_ID
from data.messages.texts import *
from data.messages.buttons import *
from data.data_edit import dating
from data.states.states import State_t
from db.qiwi import get

storage = MemoryStorage()
bot = Bot(token=TOKEN,parse_mode='html')
dp = Dispatcher(bot,storage=storage)


@dp.message_handler(state=State_t.add_towar)
async def adder(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('<b>Отменнено</b>')
    else:
        async with state.proxy() as data:
            dating().update(data['calls'],message.text,what_update='items')
            await state.finish()
        await message.reply('<b>Успешно</b>')


@dp.message_handler(state=State_t.all)
async def adder(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('<b>Отменнено</b>')
        return
    else:
        await state.finish()
        num = await send(message,InlineKeyboardMarkup().add(InlineKeyboardButton(text='❌ Удалить',callback_data='del_mess')))
        await message.reply(f'<b>Успешно отправлено: <code>{num}</code></b>')



@dp.callback_query_handler(lambda c: c.data == 'me')
async def account(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(me_text(call),reply_markup=me_buttons)
    

@dp.callback_query_handler(lambda c: c.data == 'oplata_check')
async def to_menu(call: CallbackQuery):
    g = get(call.from_user.id)
    if g!=None:
        await call.message.answer(f'<b>✅ Спасибо за пополнение вам начислено {g} rub</b>',parse_mode='html')
    else:
        await call.answer('❌ Платеж не найден')



@dp.callback_query_handler(lambda c: c.data == 'exit')
async def to_menu(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(start_text(call),reply_markup=start_buttons)


@dp.callback_query_handler(lambda c: c.data == 'money')
async def to_me(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(pay_text,reply_markup=pay_but(call.from_user.id))


@dp.callback_query_handler(lambda c: c.data == 'del_mess')
async def dela(call: CallbackQuery):
    await call.message.delete()



@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'edit')
async def to_add(call: CallbackQuery,state: FSMContext):
    async with state.proxy() as data:
        data['calls']=call.data.replace('edit|','')
    await call.answer()
    await call.message.edit_text('<b>Введи товар или напиши <code>Отмена</code></b>')
    await State_t.add_towar.set()


@dp.callback_query_handler(lambda c: c.data == 'adder')
async def adds(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text('<b>Выберите куда добавить товар</b>',reply_markup=tow_but())
    


@dp.callback_query_handler(lambda c: c.data == 'toall')
async def s(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text('<b>🔫 Введи сообщение для рассылки или напиши <code>Отмена</code></b>')
    await State_t.all.set()



@dp.callback_query_handler(lambda c: c.data == 'stat')
async def stat(call: CallbackQuery):
    await call.answer()
    us = sta()
    await call.message.edit_text(f'<b>🗒 Пользователей: {us}</b>',reply_markup=adm_exit)


@dp.callback_query_handler(lambda c: c.data == 'nalik')
async def towars(call: CallbackQuery,state: FSMContext):
    async with state.proxy() as data:
        data['number']=1
    await call.answer()
    await call.message.edit_caption(towars_text,reply_markup=towars_buttons())
    

@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'get')
async def get_(call: CallbackQuery,state: FSMContext):
    num=1
    async with state.proxy() as data:
        if 'number' not in data:
            data['number']=num
        else:
            num = data['number']

    await call.message.edit_caption(dating().search(call.data.split('|')[1],data['number']),reply_markup=buy_buttons(call.data,num))


@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'buy')
async def buu(call: CallbackQuery,state:FSMContext):
    async with state.proxy() as data:
        rubs = dating().search(call.data.split('|')[1],data['number'],key='price')*data['number']
    if buy(call.from_user.id,rubs)==True:
        dco = dating().buy(call.data.split('|')[1],data['number'])
        if dco == False:
            give_balance(call.from_user.id,rubs)
            await call.answer('В данный момент товара нет')
        else:
            await call.answer()
            await call.message.answer(dco)
    else:
        await call.answer('❌ Пожалуйста пополните баланс')
    await to_menu(call)
    
@dp.callback_query_handler(lambda c: c.data == 'exit_adm')
async def exit_adm(call: CallbackQuery):
    prava = dating().read_admin(call.message.from_user.id)
    await call.message.edit_text(admin_text(prava),reply_markup=admin_markup)

@dp.callback_query_handler(lambda c: c.data.split('|')[0] == 'change')
async def change(call: CallbackQuery,state: FSMContext):
    da = call.data.split('|')
    ca = da[2]
    if da[1][:1]=='+':
        async with state.proxy() as data:
            if data['number']>50 or data['number']+int(da[1][1:])>50:
                await call.answer('Больше 50 нельзя!')
            else:
                data['number']+=int(da[1][1:])
    else:
        async with state.proxy() as data:
            if data['number']-int(da[1][1:])<1:
                await call.answer('Меньше 1 купить нельзя!')
            else:
                data['number']-=int(da[1][1:])
    async with state.proxy() as data:
        await call.message.edit_caption(dating().search(call.data.split('|')[2],data['number']),reply_markup=buy_buttons(f'none|{ca}',data['number']))

        
@dp.message_handler(commands=['admin'])
async def adm(message: Message):
    prava = dating().read_admin(str(message.from_user.id))
    if prava != None:
        await message.answer(admin_text(prava),reply_markup=admin_markup)





@dp.callback_query_handler()
async def els(call: CallbackQuery):
    await call.answer('В разработке')


@dp.message_handler(commands=['add_money'])
async def start(message: Message):
    arq = message.get_args().split()
    
    if message.from_user.id == CREATOR:
        try:
            give_balance(int(arq[0]),int(arq[1]))
            await message.reply('<b>succesfull</b>',parse_mode='html')
        except Exception as f:
            await message.reply(f'<b>error\n\n{f}</b>',parse_mode='html')
    else:
        pass
    

@dp.message_handler(commands=['promote'])
async def promote(message: Message):
    if dating().read_admin(message.from_user.id ) != None:
        g=message.get_args().split()
        print(g)
        dating().promote(g[0],g[1])
        await message.answer('<b>Повышен!</b>')


@dp.message_handler(commands=['demote'])
async def demote(message: Message):
    if dating().read_admin(message.from_user.id ) != None:
        dating().demote(message.get_args().split()[0])
        await message.answer('<b>Понижен!</b>')


@dp.message_handler(commands=['start'])
async def start(message: Message):
    start_press(message.from_user.id)
    try:
        await bot.delete_message(message.chat.id,message.message_id-1)
    except:
        pass
    await bot.send_photo(message.chat.id,PHOTO_ID,caption=start_text(message),reply_markup=start_buttons)


if __name__ == '__main__':
    print('Для добавления товара редактируем data/data.json добавлю в следуещем обновлении остальное')
    sender = Noficate(bot,CREATOR)
    executor.start_polling(dp,on_startup=sender.strike,on_shutdown=sender.off_strike)