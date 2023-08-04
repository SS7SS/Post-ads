import os
from telebot import *
from telebot.types import InlineKeyboardMarkup as Mk ,InlineKeyboardButton as btn


Token = os.environ.get("tokens")
id = os.environ.get("dev")
id_channel = os.environ.get("chid")
bot = TeleBot(Token)
ch = bot.get_chat(id_channel)
link = Mk().add(btn(text=f'{ch.title}',url=f't.me/{ch.username}'))



@bot.message_handler(commands=['start'])
def start(msg):
 if msg.chat.type == 'private' :
   link = Mk().add(btn(text=f'{ch.title}',url=f't.me/{ch.username}')) 
   bot.send_message(msg.chat.id,f'''
*• اهلا في بوت نشر الاعلانات🫦. 
- ارسل اعلانك وسيتم نشره بالقناة 👇🏻 📢.*''',
   parse_mode='Markdown',reply_markup=link)

@bot.message_handler(content_types=['text'])
def text(msg):
 global id
 if msg.chat.type == 'private':
  id = msg.chat.id 
  open(f'{id}.txt','w').write(msg.text)
  bot.send_message(msg.chat.id,'تم ارسال اعلانك الى المالك ليتم الموافقه على نشره♡..')
  key = Mk()
  key.add(btn(text='• صاحب الاعلان •',url=f'tg://user?id={id}'))
  key.add(btn(text='• قبول •',callback_data='ok'),
  btn(text='• رفض •',callback_data='no'))
  bot.send_message(id,f'- الاعلان : {msg.text} .',reply_markup=key)
@bot.callback_query_handler(func=lambda message:True)
def types(call):
    if call.data == 'ok':
        join = Mk().add(btn(text='• لنشر اعلانك •', url=f't.me/{bot.get_me().username}'))
        txt = open(f'{id}.txt', 'r').read()
        key = join.add(btn(text='• صاحب الاعلان •', url=f'tg://user?id={id}'))
        bot.send_message(ch.id, f'- الاعلان : {txt} .', reply_markup=key)
        bot.send_message(id,'تم نشر اعلانك بالقناة 👇🏻.',reply_markup=link)
        os.remove(f'{id}.txt')
        bot.delete_message(id,call.message.message_id)
    if call.data == 'no':
     os.remove(f'{id}.txt')
     bot.delete_message(id,call.message.message_id)
     bot.send_message(id,'- تم رفض اعلانك.\n- !')

bot.infinity_polling()
