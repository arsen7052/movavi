import datetime
import sqlite3
import random
import telebot

current_datetime = datetime.datetime.now()
sp = ""
sp += (
    str(current_datetime.day)
    + " "
    + str(current_datetime.month)
    + " "
    + str(current_datetime.year)
)
connection = sqlite3.connect("jelania.db")

cursor_object = connection.execute(
    """
    CREATE TABLE IF NOT EXISTS jelanis(
        order_id INTEGER PRIMARY KEY,
        chat_id INTEGER,
        jelania TEXT,
        data TEXT
    )
  """
)
a = (
    "В этом году ты точно будешь с друзьями на одной волне! А ещё - в одной WiFi-сети, когда вы вместе придете на занятия в школу Movavi.\n"
    "Активируем IT-интуицию: в наступающем году ты сможешь создать самый крутой проект на своем курсе!\n"
    "Подходящий год для великих дел! Даже самые сложные задачки не устоят перед твоим энтузиазмом ☀️\n"
    'У тебя появится особый "хакерский" навык — умение узнавать, кто съел последнее печенье, по одному взгляду на одногруппников. \n'
    "Предсказываем тебе урожай новых умений, крутых проектов — и много-много-много самых любимых печенек 🍪\n"
    "Будет много крутых каток с друзьями! Но не забывай иногда выпускать телефон из рук. Говорят, катать на лыжах тоже интересно. \n"
    "В этом году на занятиях в школе Movavi у тебя появится крутой друг, который будет понимать все-все-все твои шутки!\n"
    'Наши "да" в людях - быть похожим на тебя! Потому что ты очень-очень крутой :) Пусть этот год принесет тебе много радости! \n'
    "Босс айти - это про тебя. Да-да, не скромничай :) Желаем добиться еще больших высот в IT-мире, а мы тебе в этом поможем.\n"
    "Твои успехи в новом году заметят все друзья - и захотят заниматься с тобой в одной группе 🤩\n"
    "Звезды предсказывают, что в новом году ты справишься со всеми багами!\n"
    "Твой уровень креативности взлетит до небес! Жди лавину гениальных идей для собственных проектов, которые удивят всех преподавателей.\n"
    "В грядущем году ты освоишь новый IT-навык так же легко, как распаковываешь новогодние подарки!\n"
    "Счастливого Нового Года! Пусть в этом году тебя ждут мега-каникулы с любимыми друзьями. Не забывайте делать перерывы от экранов - на улице отличная погода! \n"
    "В новом году ты обретешь суперсилу: превращать скучные задачи в увлекательные челленджи! \n"
    "Прогнозируем: твои проекты взорвут интернет! Жди миллионы лайков и репостов. \n"
    "В этом году твои проекты будут настолько крутыми, что даже самые требовательные преподаватели Movavi будут ставить тебе самые высокие оценки!\n"
    "Ты научишься так быстро набирать код, что клавиатура будет звучать как музыка для ушей твоих одногруппников.\n"
    "В этом году ты станешь настоящим гуру в области кибербезопасности и будешь помогать друзьям защищать свои устройства от хакеров.\n"
    "Твои знания будут расти так быстро, что уже совсем скоро ты сможешь начать свой собственный стартап!"
)

TOKEN = "7385654525:AAEVcKf7OpEcWHPy5uloizg7DNwivUQlXtw"
bot = telebot.TeleBot(TOKEN)
connection.close()


@bot.message_handler(commands=["start"])
def handle_start(message):
    k = telebot.types.InlineKeyboardMarkup()
    btn_get_photo = telebot.types.InlineKeyboardButton(
        "Хочу пожелание", callback_data="0"
    )
    k.add(btn_get_photo)
    bot.send_message(
        message.chat.id,
        "Привет!\nС наступающим Новым годом 🎄🎅\nЗаходи в этот бот каждый день, чтобы получить новое IT-пожелание. ",
        reply_markup=k,
    )


@bot.callback_query_handler(func=lambda callback: True)
def handle_callback(callback):
    global a
    connection = sqlite3.connect("jelania.db")
    cursor_object = connection.execute(
        f"""
            SELECT jelania
            FROM jelanis
            WHERE chat_id = {callback.message.chat.id}
        """
    )
    # достаем все данные и перебираем список
    current_datetime = datetime.datetime.now()
    sp = ""
    sp += (
        str(current_datetime.day)
        + " "
        + str(current_datetime.month)
        + " "
        + str(current_datetime.year)
    )
    g = cursor_object.fetchall()
    connection.close()
    t = False
    if g == []:
        t = True
        g = a.split("\n")
        connection = sqlite3.connect("jelania.db")
        cursor_object = connection.execute(
            f"""
        INSERT INTO jelanis(chat_id, jelania, data) 
        VALUES ({callback.message.chat.id}, '{a}', '{sp}')
        """
        )
        connection.commit()
        connection.close()
    else:
        g = g[0][0].strip("\n").split("\n")
        print("******************", g)
    connection = sqlite3.connect("jelania.db")
    cursor_object = connection.execute(
        f"""
            SELECT data
            FROM jelanis
            WHERE chat_id = {callback.message.chat.id}
        """
    )
    sd = cursor_object.fetchall()[0][0]
    print(sd)
    if sp != sd or t:
        f = g[random.randint(0, len(g) - 1)]
        g.remove(f)
        s = "\n".join(g)
        print("#############", s)

        if len(s) == 0:
            s = a
        SQL_UPDATE_TABLE = f"""
        UPDATE jelanis
        SET jelania = '{s}', data = '{sp}'
        WHERE chat_id = {callback.message.chat.id}
        """
        connection.execute(SQL_UPDATE_TABLE)
        connection.commit()
        print(f)
        bot.send_message(callback.message.chat.id, f)
        connection.close()
    else:
        bot.send_message(
            callback.message.chat.id, "вы уже получили пожелание, возвращайтесь завтра"
        )


bot.polling(non_stop=True, interval=1)
