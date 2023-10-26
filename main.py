import telebot
import time

token = ''
bot = telebot.TeleBot(token)
stats = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id not in stats.keys():
        init_chat(message)
        bot.send_message(message.chat.id, "Бот активирован🎉\nДля просмотра доступных команд используйте /help")
    else:
        bot.send_message(message.chat.id, "Бот уже следит за вами😎")


@bot.message_handler(commands=["stats"])
def print_stats(message):
    if message.chat.id not in stats.keys():
        bot.send_message(message.chat.id, "Для начала запустите бота командой /start")
    else:
        messages_number = stats[message.chat.id]['messages_number']
        active_users = stats[message.chat.id]['active_users']
        photos = stats[message.chat.id]['photos_number']
        videos = stats[message.chat.id]['videos_number']
        stickers = stats[message.chat.id]['stickers_number']
        bot.send_message(message.chat.id, "📈Статистика чата:\n" +
                        f"🤳🏻Активных пользователей: {active_users}\n\n" +
                        f"✍🏻Всего сообщений: {messages_number}\n" +
                        f"📃Стикеры: {stickers}\n" +
                        f"🏞️Фото: {photos}\n" +
                        f"🎥Видео: {videos}")


@bot.message_handler(commands=["personalStats"])
def print_personal_stats(message):
    if message.from_user.id not in stats[message.chat.id]['users']:
        bot.send_message(message.chat.id, "Вы еще не написали ни одного сообщения🥲")
    else:
        messages_number = stats[message.chat.id]['users'][message.from_user.id]['messages_number']
        photos = stats[message.chat.id]['users'][message.from_user.id]['photos_number']
        videos = stats[message.chat.id]['users'][message.from_user.id]['videos_number']
        stickers = stats[message.chat.id]['users'][message.from_user.id]['stickers_number']
        name = stats[message.chat.id]['users'][message.from_user.id]['nickname']
        user_name = stats[message.chat.id]['users'][message.from_user.id]['username']
        bot.send_message(message.chat.id, f"📈Статистика пользователя {name}(@{user_name}):\n\n" +
                         f"✍🏻Всего сообщений: {messages_number}\n" +
                         f"📃Стикеры: {stickers}\n" +
                         f"🏞️Фото: {photos}\n" +
                         f"🎥Видео: {videos}")


@bot.message_handler(commands=["userOfTheWeek"])
def print_most_active_week_user(message):
    t = time.time()
    last_week = int(t - 604800)
    user_week_msg = {}
    for user in stats[message.chat.id]['users'].values():
        user_msg = user['messages_timestamps']
        week_msg = list(map(lambda x : x >= last_week, list(user_msg.keys())))
        user_week_msg[user['username']] = len(week_msg)

    if len(user_week_msg) > 0:
        max_value = sorted(user_week_msg.values(), reverse=True)[0]
        n_max = sorted(user_week_msg.values(), reverse=True).count(sorted(user_week_msg.values(), reverse=True)[0])
        users_max = []

        for user in user_week_msg.items():
            if user[1] == max_value:
                users_max.append(user)
        if n_max == 1:
            bot.send_message(message.chat.id, "🤯Самый активный пользователь этой недели:\n\n" +
                             f"@{users_max[0][0]}\n" +
                             f"Отправленных сообщений: {users_max[0][1]}")
        elif n_max > 1:
            bot.send_message(message.chat.id, "🤯Самыe активныe пользователи этой недели:\n\n" +
                             '\n'.join([f'@{name}\nОтправленных сообщений: {count}\n\n' for name, count in users_max]))
    else:
        bot.send_message(message.chat.id, "В чате за последнюю неделю не было сообщений🥵")


@bot.message_handler(commands=["userOfTheDay"])
def print_most_active_day_user(message):
    t = time.time()
    last_week = int(t - 86400)
    user_week_msg = {}
    for user in stats[message.chat.id]['users'].values():
        user_msg = user['messages_timestamps']
        week_msg = list(map(lambda x: x >= last_week, list(user_msg.keys())))
        user_week_msg[user['username']] = len(week_msg)

    if len(user_week_msg) > 0:
        max_value = sorted(user_week_msg.values(), reverse=True)[0]
        n_max = sorted(user_week_msg.values(), reverse=True).count(sorted(user_week_msg.values(), reverse=True)[0])
        users_max = []

        for user in user_week_msg.items():
            if user[1] == max_value:
                users_max.append(user)

        if n_max == 1:
            bot.send_message(message.chat.id, "🥳Самый активный пользователь сегодня:\n\n" +
                             f"@{users_max[0][0]}\n" +
                             f"Отправленных сообщений: {users_max[0][1]}")
        elif n_max > 1:
            bot.send_message(message.chat.id, "🥳Самыe активныe пользователи сегодня:\n\n" +
                             '\n'.join([f'@{name}\nОтправленных сообщений: {count}\n\n' for name, count in users_max]))
    else:
        bot.send_message(message.chat.id, "В чате за последний день не было сообщений🥵")


@bot.message_handler(commands=["stickersLover"])
def print_stickers_lover(message):
    user_stickers = {}
    for user in stats[message.chat.id]['users'].values():
        user_stickers[user['username']] = user['stickers_number']

    if len(user_stickers) > 0:
        max_value = sorted(user_stickers.values(), reverse=True)[0]
        n_max = sorted(user_stickers.values(), reverse=True).count(sorted(user_stickers.values(), reverse=True)[0])
        users_max = []

        for user in user_stickers.items():
            if user[1] == max_value:
                users_max.append(user)

        if n_max == 1:
            bot.send_message(message.chat.id, "🥳Любитель стикеров:\n\n" +
                             f"@{users_max[0][0]}\n" +
                             f"Количество отправленных стикеров: {users_max[0][1]}")
        elif n_max > 1:
            bot.send_message(message.chat.id, "🥳Любители стикеров:\n\n" +
                             '\n'.join([f'@{name}\nКоличество отправленных стикеров: {count}\n\n' for name, count in users_max]))
    else:
        bot.send_message(message.chat.id, "В чате еще не было отправлено ни одного стикера🥵")


@bot.message_handler(commands=["rating"])
def print_rating(message):
    user_msg = []
    for user in stats[message.chat.id]['users'].values():
        user_msg.append((user['messages_number'], user['username']))

    if len(user_msg) > 0:
        sorted_msg = sorted(user_msg, reverse=True)
        bot.send_message(message.chat.id, "✅Рейтинг пользователей:\n\n" +
                        '\n'.join([f'@{name}\nОтправленных сообщений: {count}\n\n' for count, name in user_msg]))
    else:
        bot.send_message(message.chat.id, "В чате еще не было сообщений🥵")


@bot.message_handler(commands=["help"])
def print_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n\n" +
                     "/start — запуск бота\n" +
                     "/stats — статистика чата\n" +
                     "/personalStats — персональная статистика\n" +
                     "/userOfTheWeek — самый активный пользователь недели\n" +
                     "/userOfTheDay — самый активный пользователь дня\n" +
                     "/stickersLover — любитель стикеров\n" +
                     "/rating — рейтинг пользователей по количеству сообщений")


@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'video', 'location', 'contact', 'sticker'])
def all_messages(message):
    if message.content_type == 'sticker':
        count_stickers(message)
        count_user_stickers(message)
    if message.content_type == 'photo':
        count_photos(message)
        count_user_photos(message)
    if message.content_type == 'video':
        count_videos(message)
        count_videos(message)

    if not message.from_user.is_bot:
        stats[message.chat.id]['messages_number'] += 1
        if message.from_user.id not in stats[message.chat.id]['users'].keys():
            stats[message.chat.id]['active_users'] += 1
            init_user(message)
    count_user_messages(message)


def count_stickers(message):
    stats[message.chat.id]['stickers_number'] += 1


def count_photos(message):
    stats[message.chat.id]['photos_number'] += 1


def count_videos(message):
    stats[message.chat.id]['videos_number'] += 1


def init_chat(message):
    stats[message.chat.id] = {
        'messages_number': 0,
        'active_users': 0,
        'stickers_number': 0,
        'photos_number': 0,
        'videos_number': 0,
        'users': {}
    }


def init_user(message):
    user_name = ''
    if message.from_user.first_name != None and message.from_user.last_name != None:
        user_name = message.from_user.first_name + message.from_user.last_name
    elif message.from_user.first_name != None and message.from_user.last_name == None:
        user_name = message.from_user.first_name
    elif message.from_user.first_name == None and message.from_user.last_name != None:
        user_name = message.from_user.last_name
    stats[message.chat.id]['users'][message.from_user.id] = {
        'nickname': user_name,
        'username': message.from_user.username,
        'messages_number': 0,
        'stickers_number': 0,
        'photos_number': 0,
        'videos_number': 0,
        'messages_timestamps': {}
    }


def count_user_stickers(message):
    stats[message.chat.id]['users'][message.from_user.id]['stickers_number'] += 1


def count_user_videos(message):
    stats[message.chat.id]['users'][message.from_user.id]['videos_number'] += 1


def count_user_photos(message):
    stats[message.chat.id]['users'][message.from_user.id]['photos_number'] += 1


def count_user_messages(message):
    stats[message.chat.id]['users'][message.from_user.id]['messages_number'] += 1
    stats[message.chat.id]['users'][message.from_user.id]['messages_timestamps'][message.date] = 1


if __name__ == "__main__":
    bot.infinity_polling()
