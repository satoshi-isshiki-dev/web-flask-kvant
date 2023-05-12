from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode
import sqlite3

# инициализация бота и диспетчера
bot = Bot(token='5906782322:AAF1ojh7Mi6OVKgh6-tuh7JNUJkCTQotcNA')
dp = Dispatcher(bot)

# обработка команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я ещё один чат-бот, нажми на /help чтобы посмотреть что я умею.")

# обработка команды /help
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("Вот небольшой список команд которые я умею выпполнять на данный момент\n /start - показать приветсвенное сообщение\n /news - показать последние новости сайта\n /contacts - показать конакты\n /schedule - показать расписание занятий педагога\n")

# Обработчик команды /news
@dp.message_handler(commands=['news'])
async def news_command(message: types.Message):
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('instance/news.db')
    cursor = conn.cursor()

    # Выборка последних 3 новостей из базы данных
    cursor.execute("SELECT * FROM news ORDER BY id DESC LIMIT 3")
    news = cursor.fetchall()

    # Если новости есть, отправляем их в чат
    if news:
        await message.answer("Последние новости на сайте:")
        for n in news:
            await message.answer(f"<b>{n[1]}</b>\n{n[2]}", parse_mode=ParseMode.HTML)
    else:
        await message.answer("Новостей пока нет")

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

# обработка команды /contacts
@dp.message_handler(commands=['contacts'])
async def contacts_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Телефон", callback_data="1234567890"))
    keyboard.add(types.InlineKeyboardButton(text="Email", callback_data="igarett@yandex.ru"))
    keyboard.add(types.InlineKeyboardButton(text="Telegram", url="t.me/igarett"))
    await message.reply("Контактная информация:", reply_markup=keyboard)

# обработка команды /schedule
@dp.message_handler(commands=['schedule'])
async def schedule_command(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Понедельник", callback_data="schedule_monday"))
    keyboard.add(types.InlineKeyboardButton(text="Вторник", callback_data="schedule_tuesday"))
    keyboard.add(types.InlineKeyboardButton(text="Среда", callback_data="schedule_wednesday"))
    keyboard.add(types.InlineKeyboardButton(text="Четверг", callback_data="schedule_thursday"))
    keyboard.add(types.InlineKeyboardButton(text="Пятница", callback_data="schedule_friday"))
    await message.reply("Расписание работы групп педагога:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == '1234567890')
async def process_callback_phone(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_contact(callback_query.from_user.id, phone_number='+1234567890', first_name='Роман', last_name='Сергиенко')

@dp.callback_query_handler(lambda c: c.data == 'igarett@yandex.ru')
async def process_callback_email(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Напишите мне на почту igarett@yandex.ru')

# обработка нажатия кнопки в расписании
@dp.callback_query_handler(lambda c: c.data.startswith('schedule_'))
async def process_callback_schedule(callback_query: types.CallbackQuery):
    day = callback_query.data.split('_')[1]
    if day == 'monday':
        text = 'Расписание на понедельник:\n\n1. Мобильная разработка - целый день\n2. Анализ данных - с 14:00 до 17:00\n3. Английский язык - с 17:00 до 18:30'
    elif day == 'tuesday':
        text = 'Расписание на вторник:\n\n1. Анализ данных - с 10:00 до 13:00\n2. Мобильная разработка - с 14:00 до 17:00\n3. Английский язык - с 17:00 до 18:30'
    elif day == 'wednesday':
        text = 'Расписание на среду:\n\n1. Английский язык - с 10:00 до 11:30\n2. Мобильная разработка - с 14:00 до 17:00\n3. Анализ данных - с 17:00 до 20:00'
    elif day == 'thursday':
        text = 'Расписание на четверг:\n\n1. Анализ данных - с 10:00 до 13:00\n2. Мобильная разработка - с 14:00 до 17:00\n3. Английский язык - с 17:00 до 18:30'
    elif day == 'friday':
        text = 'Расписание на пятницу:\n\n1. Мобильная разработка - целый день\n2. Анализ данных - с 14:00 до 17:00\n3. Английский язык - с 17:00 до 18:30'
    else:
        text = 'Расписание на этот день пока не определено'
    await bot.send_message(callback_query.from_user.id, text)
    await bot.answer_callback_query(callback_query.id)

# обработка текстовых сообщений
@dp.message_handler(content_types=['text'])
async def echo_message(message: types.Message):
    await message.reply(message.text)

# запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)