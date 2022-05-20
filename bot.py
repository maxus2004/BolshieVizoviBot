import urllib.request
import time
import telebot
import threading

bot = telebot.TeleBot("---КЛЮЧ ДОСТУПА---")

chats = []

def get_news():

    page = urllib.request.urlopen('https://konkurs.sochisirius.ru/news').read().decode('utf-8')

    startI = page.find('<p class="card__title">')
    endI = page.find('</p>',startI)
    
    return page[startI+len('<p class="card__title">'):endI]

def send_message_to_all(text):
    for chat_id in chats:
        print('sending message:',text, 'to:', chat_id)
        bot.send_message(chat_id, text)


@bot.message_handler(commands=["start"])
def start(m, res=False):
    if m.chat.id in chats:
        print('alredy in chat: ', m.chat.id)
        bot.send_message(m.chat.id, 'Бот уже был запущен в этом чате')
        return
    chats.append(m.chat.id)
    print('added chat: ', m.chat.id)
    bot.send_message(m.chat.id, 'Бот запущен, вам будет отправленно сообщение когда появится новая новость на сайте')

def check_loop(): 
    while True:
        if(get_news() != 'Опубликованы результаты первого тура заключительного этапа'):
            print("резы!!!!")
            send_message_to_all('РЕЗУЛЬТАТЫЫЫЫ!!!!!! https://konkurs.sochisirius.ru/news')
            send_message_to_all('РЕЗУЛЬТАТЫЫЫЫ!!!!!! https://konkurs.sochisirius.ru/news')
            send_message_to_all('РЕЗУЛЬТАТЫЫЫЫ!!!!!! https://konkurs.sochisirius.ru/news')
            break
        else:
            print("пока резов нет")
        time.sleep(10)

def user_input_loop(): 
    while True:
        str = input()
        if(str == '/message'):
            str2 = input()
            send_message_to_all(str2)
        if(str == '/printchats'):
            print(chats)

def main():

    threading1 = threading.Thread(target=user_input_loop)
    threading1.daemon = True
    threading1.start()

    threading2 = threading.Thread(target=check_loop)
    threading2.daemon = True
    threading2.start()

    print('bot started')

    bot.polling(none_stop=True, interval=0)
   

main()
