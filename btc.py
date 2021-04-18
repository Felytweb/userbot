from telethon import TelegramClient, events, sync
import re
import config as cfg
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
api_id = cfg.api_id
api_hash = cfg.api_hash
regex = r"BTC_CHANGE_BOT\?start="
idchat = cfg.idchat
client = TelegramClient('session', api_id, api_hash)
username = cfg.username
print('Enabled Ловлер чеков? [Yes]')

@client.on(events.NewMessage([159405177, idchat], blacklist_chats=True))
async def normal_handler(event):
    user_mess = event.message.to_dict()['message']
    m_from = event.message.to_dict()
    if re.search(r'BTC_CHANGE_BOT\?start=', user_mess):
        m = re.search(r'c_\S+', user_mess)
        sex = m.group(0)
        if re.search(r' ', user_mess):
            n = re.search(r' \S+', user_mess)
            reg = re.compile('[^a-zA-Z0-9_]')
            genius = (reg.sub('', m.group(0)))
            genius2 = (reg.sub('', n.group(0)))
            await client.send_message('BTC_CHANGE_BOT', '/start ' + genius + genius2)
            await client.send_message(idchat, '🧹 Чек был `очищен` от русских символов и пробелов: ' + genius + genius2)
        elif len(sex) > 35:
            reg = re.compile('[^a-zA-Z0-9_]')
            genius = (reg.sub('', m.group(0)))
            await client.send_message('BTC_CHANGE_BOT', '/start ' + genius)
            await client.send_message(idchat, '🧹 Чек был `очищен` от русских символов и прочего: ' + genius)
        elif len(m.group(0)) == 34 or len(m.group(0)) == 35:
            await client.send_message('BTC_CHANGE_BOT', '/start ' + m.group(0))
        else:
            await client.send_message('BTC_CHANGE_BOT', '/start ' + m.group(0))


@client.on(events.NewMessage(chats='BTC_CHANGE_BOT'))
async def withdraw(event):
    if "Кошелек BTC" in event.raw_text:
        balance = event.raw_text.replace('\n', ' ').split('Баланс:')[-1].split()[0]
        if balance == '0':
            return
        else:
            await client(GetBotCallbackAnswerRequest(
                event.to_id,
                event.id,
                data=event.reply_markup.rows[1].buttons[0].data
            ))
    elif 'Вы можете создать чек' in event.raw_text:
        await client(GetBotCallbackAnswerRequest(
            event.to_id,
            event.id,
            data=event.reply_markup.rows[0].buttons[0].data
        ))
    elif event.raw_text == "Выберите валюту":
        await client(GetBotCallbackAnswerRequest(
            event.to_id,
            event.id,
            data=event.reply_markup.rows[0].buttons[0].data
        ))
    elif 'На какую сумму BTC выписать чек? ' in event.raw_text:
        balance = event.raw_text.split('Доступно:')[-1].split()[0]
        await client.send_message('BTC_CHANGE_BOT', balance)
    elif 'BTC_CHANGE_BOT?start=' in event.raw_text:
        check = event.raw_text.split('https://')[-1].split()[0]
        await client.send_message(username, check)


@client.on(events.NewMessage(chats='BTC_CHANGE_BOT'))
async def btc_handler(event):
    user_mess = event.message.to_dict()['message']
    print(user_mess)
    if re.search(r'Вы получили', user_mess):
        k = re.search(r'Вы получили \S+', user_mess)
        v = re.search(r' BTC \S+', user_mess)
        await client.send_message(idchat,'**✅ Активирован чек: ** ' + k.group(0) + v.group(0) + ') РУБ')
        await event.respond('💼 Кошелек')
    elif re.search(r'Упс', user_mess):
        await client.send_message(idchat,'**🗑️ Пойман недействительный чек.** __[Мусор]__ ')
    elif re.search(r'Баланс', user_mess):
        j = re.search(r'Баланс: \S+', user_mess)
        h = re.search(r'Примерно: \S+', user_mess)
        await client.send_message(idchat, '' + j.group(0) + '** BTC**' + '\n' + h.group(0) + '** RUB**')
    elif re.search(r'обналичил чек', user_mess):
        o = re.search(r'на \S+', user_mess)
        await client.send_message(idchat, '💸 Вывод произошёл **успешно**. Сумма: ' + o.group(0) + ' **BTC**')


@client.on(events.NewMessage(chats=idchat))
async def logger(event):
    user_mess = event.message.to_dict()['message']
    if re.search(r'/help', user_mess):
        await client.send_message(idchat, '📕 Доступные команды:' + '\n-- /balance' + '\n -- /')
    elif re.search(r'/balance', user_mess):
        await client.send_message('BTC_CHANGE_BOT', '💼 Кошелек')


client.start()
client.run_until_disconnected()
print('Выключение\n3...\n2...\n1...\n  ')