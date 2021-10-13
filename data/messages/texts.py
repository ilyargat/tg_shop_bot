from db.db import get_balance
from data.data_edit import dating

def start_text(message):
    return f'<b>✋ Привет <a href="t.me/{message.from_user.username}">{message.from_user.first_name}</a>!\n\nТебя приветствует KILLER_SHOP</b>'

towars_text = '<b>🔑  Выберите интересующий товар</b>'


def me_text(message):
    balik = get_balance(message.from_user.id)
    return f'<b>👤 Мой аккаунт\n\n🆔 : <code>{message.from_user.id}</code>\n💳 Баланс: <code>{balik}</code></b>'

pay_text = '<strong>Платежная система: </strong><code>🥝 QIWI</code>\n\n<i>Выберите сумму на которую хотите совершить пополнение</i>'
def admin_text(mote):
    return f'<b>📌 Вас приветсвует админ  панель killer_shop\n\nВаши права: <code>{mote}</code></b>'
