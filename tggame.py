import json
import re
import sqlite3
import telebot
import random
import time
import sys
import os
import datetime
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
import telebot.custom_filters
import smtplib
from email.message import EmailMessage
# Полностью заменяем импорт типов
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# WebAppInfo здесь не импортируем, чтобы не было ошибки
from telebot import types
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)


TOKEN = "8316070421:AAEm__-8bKWSteqNtYJNR8zkUMOFqyuF4Dg"
CREATOR_ID = 5633124867
GMAIL = "azaryanedmond8@gmail.com"
APP_PASSWORD = "abakmlfnojtkmaha"
WEB_APP_URL = "https://shssmensn.github.io/forminiappbott/"

class RegistrationStates(StatesGroup):
    email = State()
    code = State()
# 
chess_games = {}
warnings = {}
war_players = {}
xo_games = {}
blackjack_games = {}
blackjack_rooms = {}
royal_games = {}
royal_lives = {}
user_drom_data = {}

ROYAL_ITEMS = [
    "🍎",
    "🍋",
    "🍇",
    "🍓",
    "🍊",
    "💎"
]
ROYAL_SHOP = {
    "bomb": 500,
    "shuffle": 1000,
    "life": 1500
}
cards_deck = [
    ("🂡", 11),
    ("🂢", 2),
    ("🂣", 3),
    ("🂤", 4),
    ("🂥", 5),
    ("🂦", 6),
    ("🂧", 7),
    ("🂨", 8),
    ("🂩", 9),
    ("🂪", 10),
    ("🂫", 10),
    ("🂭", 10),
    ("🂮", 10),

    ("🂱", 11),
    ("🂲", 2),
    ("🂳", 3),
    ("🂴", 4),
    ("🂵", 5),
    ("🂶", 6),
    ("🂷", 7),
    ("🂸", 8),
    ("🂹", 9),
    ("🂺", 10),
    ("🂻", 10),
    ("🂽", 10),
    ("🂾", 10),

    ("🃁", 11),
    ("🃂", 2),
    ("🃃", 3),
    ("🃄", 4),
    ("🃅", 5),
    ("🃆", 6),
    ("🃇", 7),
    ("🃈", 8),
    ("🃉", 9),
    ("🃊", 10),
    ("🃋", 10),
    ("🃍", 10),
    ("🃎", 10),

    ("🃑", 11),
    ("🃒", 2),
    ("🃓", 3),
    ("🃔", 4),
    ("🃕", 5),
    ("🃖", 6),
    ("🃗", 7),
    ("🃘", 8),
    ("🃙", 9),
    ("🃚", 10),
    ("🃛", 10),
    ("🃝", 10),
    ("🃞", 10),
]

cars_shop = [
    ("Porsche Cayenne Turbo S", 295, 2500000),
    ("Porsche 911 Turbo S", 330, 3500000),
    ("Porsche 718 Cayman", 275, 1800000),
    ("Porsche 718 Boxster", 275, 1700000),
    ("Porsche 911 Carrera 4S", 308, 2900000),
    ("Porsche Panamera Turbo S", 315, 3200000),
    ("Porsche Macan", 272, 1500000),
    ("Porsche Taycan Turbo S", 260, 4000000),
    ("Porsche 911 GT3 RS", 296, 5000000),
    ("Porsche 718 Cayman GT4 RS", 315, 4200000),
    ("Porsche 718 Spyder", 300, 2400000)
]

bad_words = [
    "хуй",
    "хyй",
    "xуй",
    "хуйня",
    "пизда",
    "ебал",
    "ебать",
    "нахуй",
    "долбаеб",
    "долбоеб",
    "сука",
    "блять",
    "бля",
    "fuck"
]
def normalize_text(text):

    text = text.lower()

    replaces = {
        "x": "х",
        "y": "у",
        "a": "а",
        "e": "е",
        "o": "о",
        "p": "р",
        "k": "к",
        "c": "с",
        "b": "в",
        "m": "м",
    }

    for eng, rus in replaces.items():
        text = text.replace(eng, rus)

    text = text.replace(" ", "")

    return text
storage = StateMemoryStorage()

bot = telebot.TeleBot(
    TOKEN,
    state_storage=storage
)
# Убедись, что этот код стоит ПОСЛЕ создания бота (bot = telebot.TeleBot(...))


from telebot import types

@bot.message_handler(commands=['drom'])
def drom_command(message):

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "🚗 Открыть Дром",
            web_app=types.WebAppInfo(
                "https://shssmensn.github.io/forminiappbott/"
            )
        )
    )

    bot.send_message(
        message.chat.id,
        "🚗 Открыть Дром",
        reply_markup=markup
    )
# База данных


def init_db():

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # USERS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT DEFAULT 'Игрок',
        role TEXT DEFAULT 'Игрок',
        balance INTEGER DEFAULT 100,
        last_work INTEGER DEFAULT 0,
        title TEXT DEFAULT 'Игрок',
        email TEXT,
        nickname TEXT DEFAULT '',
        expiry_date TEXT DEFAULT '',
        fuel INTEGER DEFAULT 100,
        last_fuel INTEGER DEFAULT 0
    )
""")

    # GROUPS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        chat_id TEXT PRIMARY KEY,
        chat_title TEXT
    )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS clans (
    clan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    clan_name TEXT UNIQUE,
    owner_id TEXT,
    balance INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1,
    points INTEGER DEFAULT 0
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS clan_invites (
    user_id TEXT PRIMARY KEY,
    clan_id INTEGER
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS royal_records (
    user_id INTEGER PRIMARY KEY,
    record INTEGER DEFAULT 0
)
""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS clan_members (
    user_id TEXT PRIMARY KEY,
    clan_id INTEGER,
    role TEXT DEFAULT 'Участник'
)
""")

    # CARS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id TEXT DEFAULT NULL,
        car_name TEXT,
        speed INTEGER,
        price INTEGER
    )
    """)

    # SHOP CARS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars_shop (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_name TEXT,
        speed INTEGER,
        price INTEGER
    )
    """)

    # USER CARS
    cursor.execute("""
CREATE TABLE IF NOT EXISTS user_cars (
    user_id TEXT,
    car_name TEXT,
    speed INTEGER,
    turbo INTEGER DEFAULT 0,
    engine INTEGER DEFAULT 0,
    tires INTEGER DEFAULT 0,
    stars INTEGER DEFAULT 1,
    blueprints INTEGER DEFAULT 0,
    active INTEGER DEFAULT 0
)
""")
   
    cursor.execute("""
CREATE TABLE IF NOT EXISTS cases (
    user_id TEXT PRIMARY KEY,
    case_count INTEGER DEFAULT 0
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS offers (
    id INTEGER PRIMARY KEY,
    item TEXT,
    amount INTEGER,
    price INTEGER,
    expire INTEGER
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS family_storage (
    clan_id INTEGER,
    item TEXT,
    amount INTEGER DEFAULT 0,
    PRIMARY KEY(clan_id, item)
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS royal_boosters (
    user_id INTEGER PRIMARY KEY,
    bombs INTEGER DEFAULT 0,
    shuffles INTEGER DEFAULT 0,
    lives INTEGER DEFAULT 0
)
""")

    cursor.execute("""
CREATE TABLE IF NOT EXISTS family_wars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attacker INTEGER,
    defender INTEGER,
    winner INTEGER,
    war_time INTEGER
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS drom_ads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seller_id INTEGER,
    seller_name TEXT,
    car_name TEXT,
    speed INTEGER,
    turbo INTEGER,
    engine INTEGER,
    tires INTEGER,
    stars INTEGER,
    price INTEGER,
    created_at INTEGER,
    expires_at INTEGER
)
""")

    # WARNS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warns (
        user_id TEXT PRIMARY KEY,
        warns INTEGER DEFAULT 0
    )
    """)

    # NFTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nfts (
        nft_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id TEXT,
        nft_name TEXT,
        rarity TEXT,
        price INTEGER
    )
    """)

    # PROMOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS promos (
        code TEXT PRIMARY KEY,
        reward INTEGER,
        max_uses INTEGER,
        uses INTEGER DEFAULT 0
    )
    """)

    # PROMO ACTIVATIONS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS promo_activations (
        user_id TEXT,
        promo_code TEXT,
        activated_at INTEGER,
        PRIMARY KEY(user_id, promo_code)
    )
    """)

    # AUCTION
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auction (
        id INTEGER PRIMARY KEY,
        item_name TEXT,
        current_bid INTEGER DEFAULT 0,
        highest_bidder INTEGER DEFAULT NULL,
        end_time INTEGER
    )
    """)

    # BUSINESSES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS businesses (
        id INTEGER PRIMARY KEY,
        name TEXT,
        owner_id INTEGER DEFAULT NULL,
        price INTEGER,
        profit INTEGER
    )
    """)

    # NFT ITEMS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS nft_items (
        nft_id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_id TEXT,
        item_name TEXT,
        rarity TEXT,
        price INTEGER DEFAULT 0,
        for_sale INTEGER DEFAULT 0
    )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS race_season (
    id INTEGER PRIMARY KEY,
    end_time INTEGER
)
""")
     
    cursor.execute("""
CREATE TABLE IF NOT EXISTS active_wars (
    clan1 INTEGER,
    clan2 INTEGER,
    hp1 INTEGER DEFAULT 5000,
    hp2 INTEGER DEFAULT 5000,
    active INTEGER DEFAULT 1
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS territories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    owner_clan INTEGER DEFAULT NULL,
    income INTEGER
)
""")

    cursor.execute("SELECT COUNT(*) FROM territories")

    if cursor.fetchone()[0] == 0:

         cursor.executemany(
        "INSERT INTO territories (name, owner_clan, income) VALUES (?, ?, ?)",
        [
            ("Центр города", None, 5000),
            ("Порт", None, 8000),
            ("Промзона", None, 12000),
            ("Аэропорт", None, 20000),
            ("Элитный район", None, 35000)
        ]
    )

    cursor.execute("""
CREATE TABLE IF NOT EXISTS race_rating (
    user_id TEXT PRIMARY KEY,
    wins INTEGER DEFAULT 0
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS blueprint_shop (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_name TEXT,
    amount INTEGER,
    price INTEGER
)
""")

    # ДОБАВЛЯЕМ МАШИНЫ В МАГАЗИН
    cursor.execute("SELECT COUNT(*) FROM cars_shop")

    if cursor.fetchone()[0] == 0:

        cars_shop = [
    ("Porsche Cayenne Turbo S", 295, 2500000),
    ("Porsche 911 Turbo S", 330, 3500000),
    ("Porsche 718 Cayman", 275, 1800000),
    ("Porsche 718 Boxster", 275, 1700000),
    ("Porsche 911 Carrera 4S", 308, 2900000),
    ("Porsche Panamera Turbo S", 315, 3200000),
    ("Porsche Macan", 272, 1500000),
    ("Porsche Taycan Turbo S", 260, 4000000),
    ("Porsche 911 GT3 RS", 296, 5000000),
    ("Porsche 718 Cayman GT4 RS", 315, 4200000),
    ("Porsche 718 Spyder", 300, 2400000)
]

        cursor.executemany(
    "INSERT INTO cars_shop (car_name, speed, price) VALUES (?, ?, ?)",
    cars_shop
)

    # ДОБАВЛЯЕМ БИЗНЕСЫ
    cursor.execute("SELECT COUNT(*) FROM businesses")

    if cursor.fetchone()[0] == 0:

        businesses_list = [
            ("Шахта", 50000, 1000),
            ("Завод", 150000, 3500),
            ("Нефтевышка", 500000, 12000),
            ("Авиакомпания", 1000000, 30000),
        ]

        cursor.executemany(
            "INSERT INTO businesses (name, price, profit) VALUES (?, ?, ?)",
            businesses_list
        )
    cursor.execute("SELECT COUNT(*) FROM race_season")

    if cursor.fetchone()[0] == 0:

        season_end = int(time.time()) + 172800

        cursor.execute("""
        INSERT INTO race_season (id, end_time)
        VALUES (1, ?)
        """, (season_end,))
    

    # ALTER TABLE
    try:
        cursor.execute("""
        ALTER TABLE nft_items
        ADD COLUMN for_sale INTEGER DEFAULT 0
        """)
    except:
        pass

    try:
        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN email TEXT
        """)
    except:
        pass

    try:
        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN nickname TEXT DEFAULT ''
        """)
    except:
        pass

    try:
        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN expiry_date TEXT DEFAULT ''
        """)
    except:
        pass
    try:
        cursor.execute("""
        ALTER TABLE user_cars
        ADD COLUMN turbo INTEGER DEFAULT 0
        """)
    except:
        pass

    try:
        cursor.execute("""
        ALTER TABLE user_cars
        ADD COLUMN engine INTEGER DEFAULT 0
        """)
    except:
        pass

    try:
        cursor.execute("""
        ALTER TABLE user_cars
        ADD COLUMN tires INTEGER DEFAULT 0
        """)
    except:
        pass

    try:
        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN fuel INTEGER DEFAULT 100
        """)
    except:
        pass
    try:
        cursor.execute("""
        ALTER TABLE user_cars
        ADD COLUMN stars INTEGER DEFAULT 1
        """)
    except:
        pass
    try:
        cursor.execute("""
    ALTER TABLE businesses
    ADD COLUMN expiry_date TEXT DEFAULT ''
    """)
    except:
         pass

    try:
        cursor.execute("""
        ALTER TABLE user_cars
        ADD COLUMN blueprints INTEGER DEFAULT 0
        """)
    except:
        pass
    try:
        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN last_fuel INTEGER DEFAULT 0
        """)
    except:
        pass
    try:
        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN fuel INTEGER DEFAULT 100
        """)
    except:
        pass

    try:
        cursor.execute("""
        ALTER TABLE users
        ADD COLUMN last_fuel INTEGER DEFAULT 0
        """)
    except:
        pass
    try:
        cursor.execute("""
    ALTER TABLE user_cars
    ADD COLUMN active INTEGER DEFAULT 0
    """)
    except:
        pass

    conn.commit()
    conn.close()


def send_email(to_email, code):

    msg = EmailMessage()

    msg["Subject"] = "Verification Code"
    msg["From"] = GMAIL
    msg["To"] = to_email

    msg.set_content(
        f"Ваш код подтверждения: {code}"
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            GMAIL,
            APP_PASSWORD
        )

        smtp.send_message(msg)



def check_and_register_user(user_id, current_name):
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (str(user_id),))
    if cursor.fetchone() is None:
        cursor.execute(
            "INSERT INTO users (user_id, username, role, balance, last_work) VALUES (?, ?, ?, ?, ?)",
            (str(user_id), current_name, "Игрок", 100, 0),
        )
    else:
        cursor.execute(
            "UPDATE users SET username = ? WHERE user_id = ?",
            (current_name, str(user_id)),
        )
    conn.commit()
    conn.close()
def add_booster(user_id, booster, amount=1):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO royal_boosters(user_id)
    VALUES(?)
    """, (user_id,))

    cursor.execute(
        f"UPDATE royal_boosters SET {booster} = {booster} + ? WHERE user_id=?",
        (amount, user_id)
    )

    conn.commit()
    conn.close()
def init_db():
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user_cars (user_id TEXT, car_name TEXT)")
    conn.commit()
    conn.close()

init_db() # Вызывай
def save_royal_record(user_id, score):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT record FROM royal_records WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    if row is None:

        cursor.execute(
            "INSERT INTO royal_records (user_id, record) VALUES (?, ?)",
            (user_id, score)
        )

    elif score > row[0]:

        cursor.execute(
            "UPDATE royal_records SET record=? WHERE user_id=?",
            (score, user_id)
        )

    conn.commit()
    conn.close()
def get_user_display_name(user):

    try:
        conn = sqlite3.connect("game_database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nickname FROM users WHERE user_id = ?",
            (str(user.id),)
        )

        data = cursor.fetchone()

        conn.close()

        if data and data[0] and data[0].strip() != "":
            return f"<b>{data[0]}</b>"

    except:
        pass

    if user.username:
        return f"@{user.username}"

    return user.first_name
def init_db():
    # Проверяем, существует ли файл базы данных
    if not os.path.exists("game_database.db"):
        print("База данных не найдена, создаю новую...")
    
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    # Создаем таблицу, если её не существует
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_cars (
            user_id TEXT,
            car_name TEXT
        )
    """)
    conn.commit()
    conn.close()
def get_xo_markup(board):
    # ПРИНУДИТЕЛЬНАЯ ПРОВЕРКА:
    print(f"DEBUG: Текущий массив доски: {board}") 
    
    markup = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for i in range(9):
        # Если в ячейке не пробел и не цифра, принудительно ставим пробел
        # Это защитит нас от 'X', если оно там вдруг оказалось
        text = str(i) if board[i] == " " or board[i] == "" else board[i]
        
        # Если текст это не число и не X/O, то это баг, ставим пустую кнопку
        if text not in [str(x) for x in range(9)] and text not in ["❌", "⭕"]:
            text = " "
            
        buttons.append(InlineKeyboardButton(text, callback_data=f"xo_{i}"))
    markup.add(*buttons)
    return markup

def restore_lives():

    while True:

        time.sleep(1800)

        for user_id in royal_lives:

            if royal_lives[user_id] < 5:
                royal_lives[user_id] += 1

threading.Thread(
    target=restore_lives,
    daemon=True
).start()

def check_winner(board):
    lines = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in lines:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    return "Draw" if " " not in board else None
def get_balance(user_id):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (str(user_id),)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return 0
def remove_balance(user_id, amount):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET balance = balance - ? WHERE user_id=?",
        (amount, str(user_id))
    )

    conn.commit()
    conn.close() 
def log_group_activity(message):
    if message.chat.type in ["group", "supergroup"]:
        conn = sqlite3.connect("game_database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO groups (chat_id, chat_title) VALUES (?, ?)",
            (str(message.chat.id), message.chat.title),
        )
        conn.commit()
        conn.close()
def refresh_blueprint_shop():

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM blueprint_shop")

    cars_shop = [
    ("Porsche Cayenne Turbo S", 295, 2500000),
    ("Porsche 911 Turbo S", 330, 3500000),
    ("Porsche 718 Cayman", 275, 1800000),
    ("Porsche 718 Boxster", 275, 1700000),
    ("Porsche 911 Carrera 4S", 308, 2900000),
    ("Porsche Panamera Turbo S", 315, 3200000),
    ("Porsche Macan", 272, 1500000),
    ("Porsche Taycan Turbo S", 260, 4000000),
    ("Porsche 911 GT3 RS", 296, 5000000),
    ("Porsche 718 Cayman GT4 RS", 315, 4200000),
    ("Porsche 718 Spyder", 300, 2400000)
]

    offers = random.sample(cars_shop, 3)

    for car in offers:
        cursor.execute(
            """
            INSERT INTO blueprint_shop
            (car_name, amount, price)
            VALUES (?, ?, ?)
            """,
            car
        )

    conn.commit()
    conn.close()
# Пример того, как бот может сохранить машину в базу:
def save_car_to_db(user_id, car_name):
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_cars (user_id, car_name) VALUES (?, ?)", (user_id, car_name))
    conn.commit()
    conn.close()
       
def check_blueprint_refresh():

    if not os.path.exists("bp_time.txt"):

        refresh_blueprint_shop()

        with open("bp_time.txt", "w") as f:
            f.write(str(int(time.time())))

        return

    with open("bp_time.txt", "r") as f:
        last = int(f.read())

    if int(time.time()) - last >= 18000:

        refresh_blueprint_shop()

        with open("bp_time.txt", "w") as f:
            f.write(str(int(time.time())))

def is_user_admin(user_id):
    if int(user_id) == CREATOR_ID:
        return True
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE user_id = ?", (str(user_id),))
    data = cursor.fetchone()
    conn.close()
    if data and data[0].strip().lower() in [
        "админ",
        "модератор",
        "admin",
        "moderator",
        "разработчик",
    ]:
        return True
    return False
def get_car(car_name):
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars_shop WHERE car_name = ?", (car_name,))
    data = cursor.fetchone()
    conn.close()
    return data
    
def update_fuel(user_id):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT fuel, last_fuel
    FROM users
    WHERE user_id = ?
    """, (str(user_id),))

    data = cursor.fetchone()
    if data is None:
         conn.close()
         return

    fuel = data[0]
    last_fuel = data[1]

    now = int(time.time())

    passed = now - last_fuel

    add_fuel = passed // 120

    if add_fuel > 0:

        fuel += add_fuel * 2

        if fuel > 100:
            fuel = 100

        cursor.execute("""
        UPDATE users
        SET fuel = ?, last_fuel = ?
        WHERE user_id = ?
        """, (
            fuel,
            now,
            str(user_id)
        ))

        conn.commit()

    conn.close()
@bot.message_handler(commands=["start"])
def start_command(message):
    log_group_activity(message)
    user_id = message.from_user.id
    display_name = get_user_display_name(message.from_user)
    check_and_register_user(user_id, display_name)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT role, balance FROM users WHERE user_id = ?", (str(user_id),))
    role, balance = cursor.fetchone()
    conn.close()

    text = (
        f"🎮 Добро пожаловать в игру, {message.from_user.first_name}!\n\n"
        f"Ваш профиль загружен.\n"
        f"👑 Титул/Роль: {role}\n"
        f"💰 Баланс: {balance} монет.\n\n"
        f"📋 Список доступных команд:\n"
        f"💼 /work — Пойти работать\n"
        f"🎰 /casino ставка — Играть в казино\n"
        f"🎡 /roulette ставка цвет  Рулетка\n"
        f"🪙/coin [ставка] [орел/решка]\n"
        f"🏆 /forbes — Список самых богатых\n"
        f"⚔️ /duel @username ставка — Вызвать на дуэль (ответом на сообщение)\n"
        f"✅ /accept — Принять вызов на дуэль\n"
        f"🎟️ /promo код — Активировать промокод\n"
        f"🛒 /titles — Магазин покупных титулов\n"
        f"🔍 /myid — Узнать свой ID для бота"
        f"👑 /admins — Список администрации\n"
        f"🏢 /allbiz — Посмотреть список всех бизнесов\n"
        f"💼 /mybiz — Мои владения\n"
        f"💰 /collect — Собрать прибыль с бизнесов\n"
        f"📢 /check_auction — Статус аукциона\n"
        f"🔨 /bid [сумма] — Сделать ставку\n"
        f"💳 /paybiz [название] — Продлить бизнес на 24ч\n"
        f"ℹ️ /help — Показать эту справку\n"
    )
    bot.reply_to(message, text, parse_mode='HTML')


@bot.message_handler(commands=["help"])
def help_command(message):
    help_text = (
        "📜 **Список команд бота:**\n\n"
        "🎮 *Игры:*\n/work, /casino, /roulette, /case, /duel, /accept\n\n"
        "👤 *Профиль:*\n/profile, /myid, /whoami,  /forbes\n\n"
        "👑 *Админка:*\n/admins"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")


@bot.message_handler(commands=["work"])
def work_command(message):
    log_group_activity(message)
    user_id = message.from_user.id
    display_name = get_user_display_name(message.from_user)
    check_and_register_user(user_id, display_name)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT last_work, balance FROM users WHERE user_id = ?", (str(user_id),)
    )
    last_work, balance = cursor.fetchone()

    current_time = int(time.time())
    # Время кулдауна: 100 секунд
    cooldown = 100

    if current_time - last_work < cooldown:
        remaining_time = cooldown - (current_time - last_work)
        bot.reply_to(
            message, f"⏳ Вы слишком устали. Отдохните еще {remaining_time} секунд."
        )
        conn.close()
        return

    earned = random.randint(50, 250)
    new_balance = balance + earned

    cursor.execute(
        "UPDATE users SET balance = ?, last_work = ?, username = ? WHERE user_id = ?",
        (new_balance, current_time, display_name, str(user_id)),
    )
    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"💼 Вы отлично поработали! Заработано: {earned} монет.\n💰 Ваш новый баланс: {new_balance} монет.",
    )


@bot.message_handler(commands=["casino"])
def casino_command(message):
    log_group_activity(message)
    user_id = message.from_user.id
    display_name = get_user_display_name(message.from_user)
    check_and_register_user(user_id, display_name)

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Использование: /casino [ставка] или /casino allbalance")
        return

#    try:
 #       bet = int(args[1])
  #  except ValueError:
   #     bot.reply_to(message, "⚠️ Ставка должна быть числом!")
    #    return

#    if bet <= 0:
 #       bot.reply_to(message, "⚠️ Ставка должна быть больше 0!")
  #      return

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (str(user_id),))
    row = cursor.fetchone()
    balance = row[0] if row else 0
    conn.close() 
 
   # Логика для allbalance
    if args[1].lower() == "allbalance":
        bet = balance
    else:
        try:
            bet = int(args[1])
        except ValueError:
            bot.reply_to(message, "⚠️ Ставка должна быть числом!")
            conn.close()
            return

    if bet <= 0:
        bot.reply_to(message, "⚠️ Ставка должна быть больше 0!")
        conn.close()
        return
   
    if bet > balance:
        bot.reply_to(message, "❌ Недостаточно средств!")
        conn.close()
        return

    if random.choice([True, False]):
        new_balance = balance + bet
        bot.reply_to(
            message,
            f"🎰 Вы выиграли! 🎉 Слот показал победу. Вы получили {bet} монет.\n💰 Баланс: {new_balance}",
        )
    else:
        new_balance = balance - bet
        try:
            bot.restrict_chat_member(
                message.chat.id,
                user_id,
                until_date=int(time.time()) + 600,
                can_send_messages=False,
            )
            markup = InlineKeyboardMarkup()
            markup.add(
                InlineKeyboardButton(
                    "🔊 Размутить (Админ)", callback_data=f"unmute_{user_id}"
                )
            )
            bot.reply_to(
                message,
                f"🎰 Вы проиграли! 😔 Удача не на вашей стороне. Потеряно {bet} монет и выдан МУТ на 10 минут!\n💰 Баланс: {new_balance}",
                reply_markup=markup,
            )
        except BaseException:
            bot.reply_to(
                message,
                f"🎰 Вы проиграли! 😔 Удача не на вашей стороне. Потеряно {bet} монет.\n💰 Баланс: {new_balance} (Вы админ, мут не выдан)",
            )

    cursor.execute(
        "UPDATE users SET balance = ?, username = ? WHERE user_id = ?",
        (new_balance, display_name, str(user_id)),
    )
    conn.commit()
    conn.close()
@bot.message_handler(commands=['addcar'])
def test_add_car(message):
    user_id = str(message.from_user.id)
    car_name = "Тестовая Лада"
    
    # Сохраняем в базу
    save_car_to_db(user_id, car_name)
    
    bot.reply_to(message, f"Машина '{car_name}' добавлена в твой гараж! Теперь проверь API.")
        
@bot.message_handler(commands=["tablet"])
def tablet(message):

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "🚘 Дром",
            callback_data="tablet_drom"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "🏁 Гонки",
            callback_data="tablet_race"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "👥 Кланы",
            callback_data="tablet_clan"
        )
    )

    bot.send_message(
        message.chat.id,
        "📱 Планшет",
        reply_markup=markup
    )
@bot.callback_query_handler(
    func=lambda call:
    call.data == "tablet_drom"
)
def drom_menu(call):

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "📢 Подать объявление",
            callback_data="drom_sell"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "🔍 Поиск авто",
            callback_data="drom_search"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "🏪 Все объявления",
            callback_data="drom_all"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "📋 Мои объявления",
            callback_data="drom_my"
        )
    )

    bot.edit_message_text(
        "🚘 Дром",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )
# 1. Команда /drom для группы


# 2. Обработка данных из Web App
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(web_app_message):
    try:
        data = json.loads(web_app_message.web_app_data.data)
        if data.get('action') == 'add_car':
            bot.send_message(web_app_message.chat.id, f"✅ Объявление получено!\n"
                                                      f"Машина: {data.get('name')}\n"
                                                      f"Цена: {data.get('price')} $")
    except Exception as e:
        bot.send_message(web_app_message.chat.id, f"Ошибка обработки данных: {e}")


                         
@bot.callback_query_handler(
    func=lambda call: call.data == "drom_all"
)
def drom_all(call):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, car_name, price
    FROM drom_ads
    ORDER BY id DESC
    LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:

        bot.edit_message_text(
            "🚘 Авторынок\n\nОбъявлений пока нет.",
            call.message.chat.id,
            call.message.message_id
        )
        return

    text = "🚘 Авторынок\n\n"

    for ad in rows:

        text += (
            f"#{ad[0]} | {ad[1]}\n"
            f"💰 {ad[2]:,}$\n\n"
        )

    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id
    )
@bot.message_handler(commands=['testweb'])
def testweb(message):

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "TEST WEBAPP",
            web_app=types.WebAppInfo(
                "https://shssmensn.github.io/forminiappbott/"
            )
        )
    )

    bot.send_message(
        message.chat.id,
        "Тест",
        reply_markup=markup
    )
@bot.callback_query_handler(
    func=lambda call: call.data == "drom_sell"
)
def drom_sell(call):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT  car_name
    FROM user_cars
    WHERE user_id = ?
    """, (call.from_user.id,))

    cars = cursor.fetchall()

    conn.close()

    if not cars:
        bot.answer_callback_query(
            call.id,
            "У вас нет машин"
        )
        return

    markup = types.InlineKeyboardMarkup()

    for car in cars:

        markup.add(
            types.InlineKeyboardButton(
                f"🚗 {car[0]}",
                callback_data=f"drom_car_{car[0]}"
            )
        )

    bot.edit_message_text(
        "📢 Выберите автомобиль:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("drom_car_")
)
def drom_select_car(call):

    car_name = call.data.replace("drom_car_", "")

    

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "1 день - 5000$",
            callback_data=f"drom_day_1_{car_name}"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "2 дня - 10000$",
            callback_data=f"drom_day_2_{car_name}"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "3 дня - 15000$",
            callback_data=f"drom_day_3_{car_name}"
        )
    )

    bot.edit_message_text(
    f"🚗 Выбрана: {car_name}\n\n⏳ Выберите срок объявления:",
    call.message.chat.id,
    call.message.message_id,
    reply_markup=markup
)

@bot.message_handler(func=lambda message: str(message.from_user.id) in user_drom_data)
def drom_set_price(message):

    user_id = str(message.from_user.id)

    data = user_drom_data.get(user_id)

    if not data:
        return

    if not message.text.isdigit():

        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(
                "❌ Отмена",
                callback_data="drom_cancel"
            )
        )

        bot.send_message(
            message.chat.id,
            "💰 Введите цену только числом (например: 100000)",
            reply_markup=markup
        )

        return

    price = int(message.text)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT speed, turbo, engine, tires, stars
    FROM user_cars
    WHERE user_id = ? AND car_name = ?
    """, (
        user_id,
        data["car_name"]
    ))

    car = cursor.fetchone()

    if not car:
        conn.close()

        bot.send_message(
            message.chat.id,
            "❌ Машина не найдена"
        )

        return

    cursor.execute("""
    INSERT INTO drom_ads
    (
        seller_id,
        seller_name,
        car_name,
        speed,
        turbo,
        engine,
        tires,
        stars,
        price,
        created_at,
        expires_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        message.from_user.id,
        message.from_user.first_name,
        data["car_name"],
        car[0],
        car[1],
        car[2],
        car[3],
        car[4],
        price,
        int(time.time()),
        int(time.time()) + data["days"] * 86400
    ))

    conn.commit()
    conn.close()

    del user_drom_data[user_id]

    bot.send_message(
        message.chat.id,
        f"✅ Объявление выставлено!\n\n"
        f"🚗 Авто: {data['car_name']}\n"
        f"💰 Цена: {price:,}$\n"
        f"⏳ Срок: {data['days']} дн."
    )
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("drom_day_")
)
def drom_day(call):

    data = call.data.split("_")

    days = int(data[2])

    car_name = "_".join(data[3:])

    user_id = str(call.from_user.id)

    if user_id not in user_drom_data:
        user_drom_data[user_id] = {}

    user_drom_data[user_id]["car_name"] = car_name
    user_drom_data[user_id]["days"] = days

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "❌ Отмена",
            callback_data="drom_cancel"
        )
    )

    bot.send_message(
        call.message.chat.id,
        "💰 Введите цену объявления (например: 100000)",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda call: call.data == "drom_cancel")
def drom_cancel(call):

    user_id = str(call.from_user.id)

    if user_id in user_drom_data:
        del user_drom_data[user_id]

    bot.edit_message_text(
        "❌ Подача объявления отменена",
        call.message.chat.id,
        call.message.message_id
    )
@bot.message_handler(commands=["chess"])
def chess(message):

    chat_id = message.chat.id

    if chat_id in chess_games:

        bot.reply_to(
            message,
            "❌ Игра уже создана."
        )

        return

    board = [
        ["♜","♞","♝","♛","♚","♝","♞","♜"],
        ["♟","♟","♟","♟","♟","♟","♟","♟"],
        [" "," "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "," "],
        [" "," "," "," "," "," "," "," "],
        ["♙","♙","♙","♙","♙","♙","♙","♙"],
        ["♖","♘","♗","♕","♔","♗","♘","♖"]
    ]

    chess_games[chat_id] = {
        "board": board,
        "selected": None,
        "turn": "white",
        "white_player": message.from_user.id,
        "black_player": None,
        "last_move": time.time()
    }

    bot.reply_to(
        message,
        "♟ Шахматная игра создана!\n\n"
        "⚫ Второй игрок:\n"
        "/joinchess"
    )


@bot.message_handler(commands=["joinchess"])
def join_chess(message):

    chat_id = message.chat.id

    if chat_id not in chess_games:

        bot.reply_to(
            message,
            "❌ Игра не создана."
        )

        return

    game = chess_games[chat_id]

    if game["black_player"] is not None:

        bot.reply_to(
            message,
            "❌ Игрок уже подключён."
        )

        return

    if message.from_user.id == game["white_player"]:
        return

    game["black_player"] = message.from_user.id

    bot.reply_to(
        message,
        "✅ Второй игрок подключился!\n"
        "♟ Игра начинается."
    )

    send_chess_board(chat_id)


def send_chess_board(chat_id):

    game = chess_games[chat_id]
    board = game["board"]

    markup = InlineKeyboardMarkup(row_width=8)

    for y in range(8):

        row = []

        for x in range(8):

            piece = board[y][x]

            if piece == " ":
                piece = "⬜" if (x + y) % 2 == 0 else "⬛"

            row.append(
                InlineKeyboardButton(
                    text=piece,
                    callback_data=f"chess_{x}_{y}"
                )
            )

        markup.row(*row)

    turn_text = (
        "⚪ Белых"
        if game["turn"] == "white"
        else "⚫ Чёрных"
    )

    bot.send_message(
        chat_id,
        f"♟ Шахматы\n"
        f"Ход: {turn_text}",
        reply_markup=markup
    )


def is_white(piece):

    return piece in [
        "♔","♕","♖",
        "♗","♘","♙"
    ]


def is_black(piece):

    return piece in [
        "♚","♛","♜",
        "♝","♞","♟"
    ]


def same_color(piece1, piece2):

    if piece1 == " " or piece2 == " ":
        return False

    return (
        (is_white(piece1) and is_white(piece2))
        or
        (is_black(piece1) and is_black(piece2))
    )


def is_valid_move(board, sx, sy, x, y):

    piece = board[sy][sx]

    if piece == " ":
        return False

    dx = x - sx
    dy = y - sy

    # Белая пешка
    if piece == "♙":

        if dx == 0 and dy == -1 and board[y][x] == " ":
            return True

        if sy == 6 and dx == 0 and dy == -2:

            if (
                board[5][sx] == " "
                and
                board[4][sx] == " "
            ):
                return True

        if (
            abs(dx) == 1
            and
            dy == -1
            and
            board[y][x] != " "
        ):
            return True

        return False

    # Чёрная пешка
    if piece == "♟":

        if dx == 0 and dy == 1 and board[y][x] == " ":
            return True

        if sy == 1 and dx == 0 and dy == 2:

            if (
                board[2][sx] == " "
                and
                board[3][sx] == " "
            ):
                return True

        if (
            abs(dx) == 1
            and
            dy == 1
            and
            board[y][x] != " "
        ):
            return True

        return False

    # Ладья
    if piece in ["♖", "♜"]:
        return dx == 0 or dy == 0

    # Слон
    if piece in ["♗", "♝"]:
        return abs(dx) == abs(dy)

    # Конь
    if piece in ["♘", "♞"]:
        return (abs(dx), abs(dy)) in [
            (1, 2),
            (2, 1)
        ]

    # Ферзь
    if piece in ["♕", "♛"]:

        return (
            dx == 0
            or
            dy == 0
            or
            abs(dx) == abs(dy)
        )

    # Король
    if piece in ["♔", "♚"]:

        return (
            abs(dx) <= 1
            and
            abs(dy) <= 1
        )

    return False


@bot.callback_query_handler(func=lambda call: call.data.startswith("chess_"))
def chess_click(call):

    chat_id = call.message.chat.id

    if chat_id not in chess_games:
        return

    game = chess_games[chat_id]
    board = game["board"]

    x = int(call.data.split("_")[1])
    y = int(call.data.split("_")[2])

    user_id = call.from_user.id

    # Ждём второго игрока
    if game["black_player"] is None:

        bot.answer_callback_query(
            call.id,
            "⏳ Ждём второго игрока"
        )

        return

    # Проверка очереди хода
    if game["turn"] == "white":

        if user_id != game["white_player"]:

            bot.answer_callback_query(
                call.id,
                "❌ Сейчас ход белых"
            )

            return

    else:

        if user_id != game["black_player"]:

            bot.answer_callback_query(
                call.id,
                "❌ Сейчас ход чёрных"
            )

            return

    # Таймер
    if time.time() - game["last_move"] > 120:

        loser = (
            "⚪ Белые"
            if game["turn"] == "white"
            else "⚫ Чёрные"
        )

        winner = (
            "⚫ Чёрные"
            if game["turn"] == "white"
            else "⚪ Белые"
        )

        bot.send_message(
            chat_id,
            f"⏰ Время вышло!\n\n"
            f"{loser} проиграли.\n"
            f"🏆 Победили: {winner}"
        )

        del chess_games[chat_id]

        return

    piece = board[y][x]

    # Выбор фигуры
    if game["selected"] is None:

        if piece == " ":
            return

        if game["turn"] == "white" and not is_white(piece):
            return

        if game["turn"] == "black" and not is_black(piece):
            return

        game["selected"] = (x, y)

        bot.answer_callback_query(
            call.id,
            f"Выбрана {piece}"
        )

        return

    sx, sy = game["selected"]

    selected_piece = board[sy][sx]
    target_piece = board[y][x]

    # Своя фигура
    if same_color(selected_piece, target_piece):

        game["selected"] = None

        bot.answer_callback_query(
            call.id,
            "❌ Своя фигура"
        )

        return

    # Проверка хода
    if not is_valid_move(board, sx, sy, x, y):

        game["selected"] = None

        bot.answer_callback_query(
            call.id,
            "❌ Неверный ход"
        )

        return

    # ШАХ И МАТ
    if target_piece in ["♔", "♚"]:

        reward = 5000

        winner_id = user_id

        loser_id = (
            game["black_player"]
            if winner_id == game["white_player"]
            else game["white_player"]
        )

        conn = sqlite3.connect("game_database.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET balance = balance + ?
            WHERE user_id = ?
            """,
            (reward, str(winner_id))
        )

        cursor.execute(
            """
            UPDATE users
            SET balance = balance - 2500
            WHERE user_id = ?
            """,
            (str(loser_id),)
        )

        conn.commit()
        conn.close()

        board[y][x] = selected_piece
        board[sy][sx] = " "

        bot.edit_message_text(
            f"♛ ШАХ И МАТ!\n\n"
            f"🏆 Победитель: {call.from_user.first_name}\n"
            f"💰 +5000$",
            chat_id,
            call.message.message_id
        )

        del chess_games[chat_id]

        return

    # ДВИГАЕМ ФИГУРУ
    board[y][x] = selected_piece
    board[sy][sx] = " "

    # Проверка шаха
    enemy_king = (
        "♚"
        if game["turn"] == "white"
        else "♔"
    )

    check = False

    for yy in range(8):

        for xx in range(8):

            piece = board[yy][xx]

            if piece == " ":
                continue

            if game["turn"] == "white":

                if not is_white(piece):
                    continue

            else:

                if not is_black(piece):
                    continue

            for ky in range(8):

                for kx in range(8):

                    if board[ky][kx] == enemy_king:

                        if is_valid_move(
                            board,
                            xx,
                            yy,
                            kx,
                            ky
                        ):

                            check = True

    # Смена хода
    game["turn"] = (
        "black"
        if game["turn"] == "white"
        else "white"
    )

    game["selected"] = None
    game["last_move"] = time.time()

    markup = InlineKeyboardMarkup(row_width=8)

    for yy in range(8):

        row = []

        for xx in range(8):

            piece = board[yy][xx]

            if piece == " ":
                piece = "⬜" if (xx + yy) % 2 == 0 else "⬛"

            row.append(
                InlineKeyboardButton(
                    text=piece,
                    callback_data=f"chess_{xx}_{yy}"
                )
            )

        markup.row(*row)

    bot.edit_message_text(
        f"♟ Шахматы\n"
        f"Ход: {'⚪ Белых' if game['turn'] == 'white' else '⚫ Чёрных'}",
        chat_id,
        call.message.message_id,
        reply_markup=markup
    )

    if check:

        bot.send_message(
            chat_id,
            "♟ ШАХ!"
        )

    bot.answer_callback_query(
        call.id,
        f"✅ Ход выполнён. Ход {'⚫ чёрных' if game['turn'] == 'black' else '⚪ белых'}"
    )
def find_matches(board):

    matches = set()

    # Горизонталь
    for y in range(8):

        count = 1

        for x in range(1, 8):

            if board[y][x] == board[y][x - 1]:
                count += 1
            else:

                if count >= 3:

                    for i in range(count):
                        matches.add((x - 1 - i, y))

                count = 1

        if count >= 3:

            for i in range(count):
                matches.add((7 - i, y))

    # Вертикаль
    for x in range(8):

        count = 1

        for y in range(1, 8):

            if board[y][x] == board[y - 1][x]:
                count += 1
            else:

                if count >= 3:

                    for i in range(count):
                        matches.add((x, y - 1 - i))

                count = 1

        if count >= 3:

            for i in range(count):
                matches.add((x, 7 - i))

    return matches
def remove_matches(board, matches):

    for x, y in matches:
        board[y][x] = None
def drop_items(board):

    for x in range(8):

        column = []

        for y in range(8):

            if board[y][x] is not None:
                column.append(board[y][x])

        while len(column) < 8:
            column.insert(0, random.choice(ROYAL_ITEMS))

        for y in range(8):
            board[y][x] = column[y]
def create_royal_markup(game):

    markup = InlineKeyboardMarkup(row_width=8)

    board = game["board"]

    for y in range(8):

        row = []

        for x in range(8):

            item = board[y][x]

            if game["selected"] == (x, y):
                item = "🔵"

            row.append(
                InlineKeyboardButton(
                    text=item,
                    callback_data=f"royal_{x}_{y}"
                )
            )

        markup.row(*row)

    return markup
def send_royal_board(chat_id):

    game = royal_games[chat_id]
    board = game["board"]

    markup = InlineKeyboardMarkup(row_width=8)

    for y in range(8):

        row = []

        for x in range(8):

            item = board[y][x]

            if game["selected"] == (x, y):
                item = "🔵"

            row.append(
                InlineKeyboardButton(
                    text=item,
                    callback_data=f"royal_{x}_{y}"
                )
            )

        markup.row(*row)

    msg = bot.send_message(
        chat_id,
        f"👑 Royal Match\n⭐ Очки: {game['score']}\n🔄 Ходы: {game['moves']}",
        reply_markup=create_royal_markup(game)
    )
    royal_games[chat_id]["message_id"] = msg.message_id
    
@bot.message_handler(commands=["royal"])
def royal_start(message):

    user_id = message.from_user.id

    if user_id not in royal_lives:
        royal_lives[user_id] = 5

    if royal_lives[user_id] <= 0:
        bot.reply_to(
            message,
            f"❤️ Жизни закончились!\nОсталось: {royal_lives[user_id]}"
        )
        return

    board = []

    for y in range(8):

        row = []

        for x in range(8):
            row.append(random.choice(ROYAL_ITEMS))

        board.append(row)

    royal_games[message.chat.id] = {
        "board": board,
        "selected": None,
        "moves": 25,
        "score": 0,
        "lives": 5
    }

    send_royal_board(message.chat.id)
       
@bot.callback_query_handler(
    func=lambda call: call.data.startswith("royal_")
)
def royal_click(call):

    chat_id = call.message.chat.id

    if chat_id not in royal_games:
        return

    game = royal_games[chat_id]

    x = int(call.data.split("_")[1])
    y = int(call.data.split("_")[2])

    # Выбор первой клетки
    if game["selected"] is None:

        game["selected"] = (x, y)

        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=call.message.message_id,
            reply_markup=create_royal_markup(game)
        )

        bot.answer_callback_query(
            call.id,
            "Выберите вторую клетку"
        )

        return

    sx, sy = game["selected"]

    # Отмена выбора
    if (sx, sy) == (x, y):

        game["selected"] = None

        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=call.message.message_id,
            reply_markup=create_royal_markup(game)
        )

        return

    # Если нажали на бомбу
    if game["board"][y][x] == "💣":

        removed = 0

        for yy in range(max(0, y - 1), min(8, y + 2)):
            for xx in range(max(0, x - 1), min(8, x + 2)):
                game["board"][yy][xx] = None
                removed += 1

        drop_items(game["board"])

        game["score"] += removed * 10
        game["moves"] -= 1
        game["selected"] = None

        if game["moves"] <= 0:

             user_id = call.from_user.id

             if user_id not in royal_lives:
                  royal_lives[user_id] = 5

             if game["score"] < 1000:

                  royal_lives[user_id] -= 1

                  bot.edit_message_text(
                      f"💔 Вы проиграли!\n"
                      f"⭐ Очки: {game['score']}\n"
                      f"❤️ Осталось жизней: {royal_lives[user_id]}",
                      chat_id,
                      call.message.message_id
                  )

             else:

                  bot.edit_message_text(
                      f"🏆 Победа!\n"
                      f"⭐ Очки: {game['score']}\n"
                      f"❤️ Жизни: {royal_lives[user_id]}",
                      chat_id,
                      call.message.message_id
                  )

             user_id = call.from_user.id
             save_royal_record(user_id, game["score"])

             del royal_games[chat_id]
             return

        bot.edit_message_text(
            f"👑 Royal Match\n"
            f"⭐ Очки: {game['score']}\n"
            f"🔄 Ходы: {game['moves']}",
            chat_id,
            call.message.message_id,
            reply_markup=create_royal_markup(game)
        )

        bot.answer_callback_query(
            call.id,
            f"💣 Взрыв! +{removed * 10} очков"
        )

        return

    # Только соседние клетки
    if abs(sx - x) + abs(sy - y) != 1:

        game["selected"] = None

        bot.answer_callback_query(
            call.id,
            "❌ Можно менять только соседние клетки"
        )

        return

    board = game["board"]

    # Меняем местами
    board[sy][sx], board[y][x] = (
        board[y][x],
        board[sy][sx]
    )

    matches = find_matches(board)

    # Нет комбинации
    if not matches:

        game["moves"] -= 1

        board[sy][sx], board[y][x] = (
            board[y][x],
            board[sy][sx]
        )

        game["selected"] = None

        if game["moves"] <= 0:

            user_id = call.from_user.id

            if game["score"] < 1000:

                royal_lives[user_id] -= 1

                bot.edit_message_text(
                    f"💔 Вы проиграли!\n"
                    f"⭐ Очки: {game['score']}\n"
                    f"❤️ Осталось жизней: {royal_lives[user_id]}",
                    chat_id,
                    call.message.message_id
                )

            else:

                bot.edit_message_text(
                    f"🏆 Победа!\n"
                    f"⭐ Очки: {game['score']}\n"
                    f"❤️ Жизни: {royal_lives[user_id]}",
                    chat_id,
                    call.message.message_id
 )

            user_id = call.from_user.id
            save_royal_record(user_id, game["score"])

            del royal_games[chat_id]
            return
            

        bot.edit_message_text(
            f"👑 Royal Match\n"
            f"⭐ Очки: {game['score']}\n"
            f"🔄 Ходы: {game['moves']}",
            chat_id,
            call.message.message_id,
            reply_markup=create_royal_markup(game)
        )

        bot.answer_callback_query(
            call.id,
            "❌ Комбинации нет, ход потрачен"
        )

        return

    # Очки
    game["score"] += len(matches) * 10

    # Бомба за большую комбинацию
    if len(matches) >= 5:
        board[y][x] = "💣"

    remove_matches(board, matches)

    drop_items(board)

    # Каскады
    game["score"] += process_cascade(game)

    # Снимаем ход
    game["moves"] -= 1

    game["selected"] = None

    # Конец игры
    if game["moves"] <= 0:

        user_id = call.from_user.id

        if game["score"] < 1000:

            royal_lives[user_id] -= 1

            bot.edit_message_text(
                f"💔 Вы проиграли!\n"
                f"⭐ Очки: {game['score']}\n"
                f"❤️ Осталось жизней: {royal_lives[user_id]}",
                chat_id,
                call.message.message_id
            )

        else:

            bot.edit_message_text(
                f"🏆 Победа!\n"
                f"⭐ Очки: {game['score']}\n"
                f"❤️ Жизни: {royal_lives[user_id]}",
                chat_id,
                call.message.message_id
)

            user_id = call.from_user.id
            save_royal_record(user_id, game["score"])

            del royal_games[chat_id]
            return
        

    # Обновляем поле
    bot.edit_message_text(
        f"👑 Royal Match\n"
        f"⭐ Очки: {game['score']}\n"
        f"🔄 Ходы: {game['moves']}",
        chat_id,
        call.message.message_id,
        reply_markup=create_royal_markup(game)
    )

    bot.answer_callback_query(
        call.id,
        f"+{len(matches) * 10} очков"
    )


def create_bomb(board, x, y):

    board[y][x] = "💣"


def process_cascade(game):

    total_score = 0

    while True:

        matches = find_matches(game["board"])

        if not matches:
            break

        total_score += len(matches) * 10

        remove_matches(
            game["board"],
            matches
        )

        drop_items(
            game["board"]
        )

    return total_score


def explode_bomb(board, x, y):

    destroyed = 0

    for yy in range(max(0, y - 1), min(len(board), y + 2)):
        for xx in range(max(0, x - 1), min(len(board[0]), x + 2)):

            board[yy][xx] = random.choice(ROYAL_ITEMS)
            destroyed += 1

    return destroyed
@bot.message_handler(commands=["buybomb"])
def buy_bomb(message):

    user_id = message.from_user.id

    if get_balance(user_id) < 500:
        bot.reply_to(message, "❌ Недостаточно денег")
        return

    remove_balance(user_id, 500)
    add_booster(user_id, "bombs", 1)

    bot.reply_to(message, "💣 Бомба куплена")
@bot.message_handler(commands=["buyshuffle"])
def buy_shuffle(message):

    user_id = message.from_user.id

    if get_balance(user_id) < 1000:
        bot.reply_to(message, "❌ Недостаточно денег")
        return

    remove_balance(user_id, 1000)
    add_booster(user_id, "shuffles", 1)

    bot.reply_to(message, "🔄 Перемешивание куплено")
@bot.message_handler(commands=["buylife"])
def buy_life(message):

    user_id = message.from_user.id

    if get_balance(user_id) < 1500:
        bot.reply_to(message, "❌ Недостаточно денег")
        return

    remove_balance(user_id, 1500)

    royal_lives[user_id] = royal_lives.get(user_id, 5) + 1

    bot.reply_to(
        message,
        f"❤️ Жизнь куплена\nТеперь жизней: {royal_lives[user_id]}"
    )
@bot.message_handler(commands=["royalshop"])
def royal_shop(message):

    bot.reply_to(
        message,
        "🛒 Магазин Royal\n\n"
        "/buybomb — 💣 Бомба (500$)\n"
        "/buyshuffle — 🔄 Перемешать поле (1000$)\n"
        "/buylife — ❤️ Доп. жизнь (1500$)"
    )
@bot.message_handler(commands=["royalboosters"])
def royal_boosters_cmd(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT bombs, shuffles, lives
    FROM royal_boosters
    WHERE user_id=?
    """, (message.from_user.id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        bombs, shuffles, lives = row
    else:
        bombs, shuffles, lives = 0, 0, 0

    bot.reply_to(
        message,
        f"🎒 Ваши бустеры:\n\n"
        f"💣 Бомбы: {bombs}\n"
        f"🔄 Перемешивания: {shuffles}\n"
        f"❤️ Жизни: {lives}"
    )
@bot.message_handler(commands=["uselife"])
def use_life(message):

    user_id = message.from_user.id

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT lives FROM royal_boosters WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    if not row or row[0] <= 0:
        conn.close()
        bot.reply_to(message, "❌ У вас нет дополнительных жизней")
        return

    cursor.execute(
        "UPDATE royal_boosters SET lives = lives - 1 WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    if user_id not in royal_lives:
        royal_lives[user_id] = 5

    royal_lives[user_id] += 1

    bot.reply_to(
        message,
        f"❤️ Использована жизнь\nТеперь жизней: {royal_lives[user_id]}"
    )
@bot.message_handler(commands=["useshuffle"])
def use_shuffle(message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in royal_games:
        bot.reply_to(message, "❌ Игра не запущена")
        return

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT shuffles FROM royal_boosters WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    if not row or row[0] <= 0:
        conn.close()
        bot.reply_to(message, "❌ Нет перемешиваний")
        return

    cursor.execute(
        "UPDATE royal_boosters SET shuffles = shuffles - 1 WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    game = royal_games[chat_id]

    for y in range(8):
        for x in range(8):
            game["board"][y][x] = random.choice(ROYAL_ITEMS)

    bot.send_message(chat_id, "🔄 Поле перемешано")
@bot.message_handler(commands=["usebomb"])
def use_bomb(message):

    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in royal_games:
        bot.reply_to(message, "❌ Игра не запущена")
        return

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT bombs FROM royal_boosters WHERE user_id=?",
        (user_id,)
    )

    row = cursor.fetchone()

    if not row or row[0] <= 0:
        conn.close()
        bot.reply_to(message, "❌ У вас нет бомб")
        return

    cursor.execute(
        "UPDATE royal_boosters SET bombs = bombs - 1 WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    game = royal_games[chat_id]

    x = random.randint(0, 7)
    y = random.randint(0, 7)

    removed = 0

    for yy in range(max(0, y - 1), min(8, y + 2)):
        for xx in range(max(0, x - 1), min(8, x + 2)):
            game["board"][yy][xx] = None
            removed += 1

    drop_items(game["board"])

    game["score"] += removed * 10

    bot.edit_message_text(
        f"👑 Royal Match\n"
        f"⭐ Очки: {game['score']}\n"
        f"🔄 Ходы: {game['moves']}",
        chat_id,
        game["message_id"],
        reply_markup=create_royal_markup(game)
    )

    bot.send_message(
        chat_id,
        f"💣 Бомба взорвалась!\n+{removed * 10} очков"
    )
@bot.message_handler(commands=["createclan"])
def create_clan(message):

    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        bot.reply_to(message, "❌ /createclan Название")
        return

    clan_name = args[1]
    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT clan_id FROM clan_members WHERE user_id=?",
        (user_id,)
    )

    if cursor.fetchone():
        bot.reply_to(message, "❌ Вы уже состоите в клане.")
        conn.close()
        return

    cursor.execute("""
    INSERT INTO clans
    (clan_name, owner_id)
    VALUES (?, ?)
    """, (clan_name, user_id))

    clan_id = cursor.lastrowid

    cursor.execute("""
    INSERT INTO clan_members
    (user_id, clan_id, role)
    VALUES (?, ?, ?)
    """, (user_id, clan_id, "Лидер"))

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"🏆 Клан {clan_name} создан!"
    )
@bot.message_handler(commands=["royalrecord"])
def royal_record(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT record FROM royal_records WHERE user_id=?",
        (message.from_user.id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        record = row[0]
    else:
        record = 0

    bot.reply_to(
        message,
        f"🏆 Ваш рекорд: {record} очков"
    )
@bot.message_handler(commands=["royaltop"])
def royal_top(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, record
        FROM royal_records
        ORDER BY record DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        bot.reply_to(message, "❌ Рекордов пока нет")
        return

    text = "🏆 ТОП 10 игроков Royal Match\n\n"

    for i, (user_id, record) in enumerate(rows, start=1):

        try:
            user = bot.get_chat(user_id)
            name = user.first_name
        except:
            name = f"ID {user_id}"

        text += f"{i}. {name} — {record}⭐\n"

    bot.send_message(message.chat.id, text)
@bot.message_handler(commands=["clan"])
def clan_info(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT clan_id, role
    FROM clan_members
    WHERE user_id = ?
    """, (user_id,))

    member = cursor.fetchone()

    if not member:
        bot.reply_to(message, "❌ Вы не состоите в клане.")
        conn.close()
        return

    clan_id = member[0]

    cursor.execute("""
    SELECT clan_name, level, points, balance
    FROM clans
    WHERE clan_id = ?
    """, (clan_id,))

    clan = cursor.fetchone()

    cursor.execute("""
    SELECT COUNT(*)
    FROM clan_members
    WHERE clan_id = ?
    """, (clan_id,))

    members_count = cursor.fetchone()[0]

    conn.close()

    bot.reply_to(
        message,
        f"🏆 Клан: {clan[0]}\n"
        f"⭐ Уровень: {clan[1]}\n"
        f"🏁 Очки: {clan[2]}\n"
        f"💰 Банк: {clan[3]}$\n"
        f"👥 Участников: {members_count}"
    )
@bot.message_handler(commands=["clantop"])
def clan_top(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT clan_name, points
    FROM clans
    ORDER BY points DESC
    LIMIT 10
    """)

    clans = cursor.fetchall()

    text = "🏆 ТОП КЛАНОВ\n\n"

    place = 1

    for clan in clans:

        text += (
            f"{place}. {clan[0]}\n"
            f"⭐ Очки: {clan[1]}\n\n"
        )

        place += 1

    conn.close()

    bot.reply_to(message, text)
@bot.message_handler(commands=["territories"])
def territories_command(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, owner_clan, income
    FROM territories
    """)

    data = cursor.fetchall()

    text = "🌍 Территории\n\n"

    for t in data:

        text += (
            f"🏠 {t[0]}\n"
            f"💰 Доход: {t[2]}$\n"
            f"👑 Владелец: {t[1]}\n\n"
        )

    conn.close()

    bot.reply_to(message, text)
@bot.message_handler(commands=["capture"])
def capture_command(message):

    args = message.text.split()

    if len(args) < 2:
        return

    territory_id = int(args[1])

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT clan_id
    FROM clan_members
    WHERE user_id = ?
    """, (user_id,))

    clan = cursor.fetchone()

    if not clan:
        bot.reply_to(message, "❌ Вы не состоите в семье.")
        conn.close()
        return

    clan_id = clan[0]

    attack_power = random.randint(100, 1000)

    if attack_power >= 500:

        cursor.execute("""
        UPDATE territories
        SET owner_clan = ?
        WHERE id = ?
        """, (
            clan_id,
            territory_id
        ))

        conn.commit()

        bot.reply_to(
            message,
            "🏆 Территория успешно захвачена!"
        )

    else:

        bot.reply_to(
            message,
            "❌ Захват провалился."
        )

    conn.close()
@bot.message_handler(commands=["invite"])
def invite_to_clan(message):

    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на игрока.")
        return

    inviter = str(message.from_user.id)
    target = str(message.reply_to_message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT clan_id FROM clans WHERE owner_id = ?",
        (inviter,)
    )

    clan = cursor.fetchone()

    if not clan:
        bot.reply_to(message, "❌ Вы не лидер клана.")
        conn.close()
        return

    clan_id = clan[0]

    cursor.execute(
        "INSERT OR REPLACE INTO clan_invites (user_id, clan_id) VALUES (?, ?)",
        (target, clan_id)
    )

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        "✅ Игрок приглашён в клан.\nИспользуйте /acceptclan"
    )
@bot.message_handler(commands=["acceptclan"])
def accept_clan(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT clan_id FROM clan_invites WHERE user_id = ?",
        (user_id,)
    )

    invite = cursor.fetchone()

    if not invite:
        bot.reply_to(message, "❌ Приглашений нет.")
        conn.close()
        return

    clan_id = invite[0]

    cursor.execute(
        "INSERT OR REPLACE INTO clan_members (user_id, clan_id, role) VALUES (?, ?, ?)",
        (user_id, clan_id, "Участник")
    )

    cursor.execute(
        "DELETE FROM clan_invites WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    bot.reply_to(message, "✅ Вы вступили в клан.")
@bot.message_handler(commands=["leaveclan"])
def leave_clan(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM clan_members WHERE user_id = ?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    bot.reply_to(message, "✅ Вы покинули клан.")
@bot.message_handler(commands=["kick"])
def kick_member(message):

    if not message.reply_to_message:
        bot.reply_to(message, "❌ Ответьте на игрока.")
        return

    owner_id = str(message.from_user.id)
    target_id = str(message.reply_to_message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT clan_id FROM clans WHERE owner_id = ?",
        (owner_id,)
    )

    clan = cursor.fetchone()

    if not clan:
        bot.reply_to(message, "❌ Вы не лидер клана.")
        conn.close()
        return

    clan_id = clan[0]

    cursor.execute(
        "SELECT clan_id FROM clan_members WHERE user_id = ?",
        (target_id,)
    )

    member = cursor.fetchone()

    if not member or member[0] != clan_id:
        bot.reply_to(message, "❌ Игрок не состоит в вашем клане.")
        conn.close()
        return

    cursor.execute(
        "DELETE FROM clan_members WHERE user_id = ?",
        (target_id,)
    )

    conn.commit()
    conn.close()

    bot.reply_to(message, "✅ Игрок исключён из клана.")
@bot.message_handler(commands=["famstorage"])
def famstorage(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT clan_id FROM clan_members WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchone()

    if not data:
        bot.reply_to(message, "❌ Вы не состоите в семье.")
        conn.close()
        return

    clan_id = data[0]

    cursor.execute(
        "SELECT item, amount FROM family_storage WHERE clan_id=?",
        (clan_id,)
    )

    items = cursor.fetchall()

    text = "🏠 Семейный склад\n\n"

    if not items:
        text += "Пусто."

    for item, amount in items:
        text += f"🔫 {item}: {amount}\n"

    conn.close()

    bot.reply_to(message, text)
@bot.message_handler(commands=["famdepositweapon"])
def famdepositweapon(message):

    args = message.text.split()

    if len(args) < 3:
        bot.reply_to(
            message,
            "/famdepositweapon АК47 5"
        )
        return

    item = args[1]
    amount = int(args[2])

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT clan_id FROM clan_members WHERE user_id=?",
        (user_id,)
    )

    clan = cursor.fetchone()

    if not clan:
        bot.reply_to(message, "❌ Вы не в семье.")
        conn.close()
        return

    clan_id = clan[0]

    cursor.execute("""
    INSERT OR IGNORE INTO family_storage
    (clan_id,item,amount)
    VALUES(?,?,0)
    """, (clan_id, item))

    cursor.execute("""
    UPDATE family_storage
    SET amount = amount + ?
    WHERE clan_id=? AND item=?
    """, (amount, clan_id, item))

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"✅ На склад добавлено {amount} {item}"
    )
@bot.message_handler(commands=["famtakeweapon"])
def famtakeweapon(message):

    args = message.text.split()

    if len(args) < 3:
        bot.reply_to(
            message,
            "/famtakeweapon АК47 1"
        )
        return

    item = args[1]
    amount = int(args[2])

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT clan_id FROM clan_members WHERE user_id=?",
        (user_id,)
    )

    clan = cursor.fetchone()

    if not clan:
        bot.reply_to(message, "❌ Вы не в семье.")
        conn.close()
        return

    clan_id = clan[0]

    cursor.execute("""
    SELECT amount
    FROM family_storage
    WHERE clan_id=? AND item=?
    """, (clan_id, item))

    data = cursor.fetchone()

    if not data or data[0] < amount:
        bot.reply_to(message, "❌ Недостаточно оружия.")
        conn.close()
        return

    cursor.execute("""
    UPDATE family_storage
    SET amount = amount - ?
    WHERE clan_id=? AND item=?
    """, (amount, clan_id, item))

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"✅ Вы взяли {amount} {item}"
    )
@bot.message_handler(commands=["famwar"])
def famwar(message):

    args = message.text.split()

    if len(args) < 2:
        bot.reply_to(message, "/famwar ID")
        return

    enemy = int(args[1])

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT clan_id FROM clan_members WHERE user_id=?",
        (user_id,)
    )

    clan = cursor.fetchone()

    if not clan:
        conn.close()
        return

    my_clan = clan[0]

    cursor.execute(
        "DELETE FROM active_wars"
    )

    cursor.execute("""
    INSERT INTO active_wars
    (clan1, clan2, hp1, hp2)
    VALUES (?, ?, 5000, 5000)
    """, (my_clan, enemy))

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        "⚔️ Война началась!\n\n"
        "Участники пишут /joinwar"
    )
@bot.message_handler(commands=["joinwar"])
def joinwar(message):

    uid = message.from_user.id

    war_players[uid] = True

    bot.reply_to(
        message,
        "🔫 Вы присоединились к войне."
    )
@bot.message_handler(commands=["shoot"])
def shoot(message):

    uid = message.from_user.id

    if uid not in war_players:
        bot.reply_to(message, "❌ Используйте /joinwar")
        return

    damage = random.randint(100, 500)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT clan1, clan2, hp1, hp2
    FROM active_wars
    LIMIT 1
    """)

    war = cursor.fetchone()

    if not war:
        conn.close()
        bot.reply_to(message, "❌ Активной войны нет.")
        return

    clan1, clan2, hp1, hp2 = war

    cursor.execute(
        "SELECT clan_id FROM clan_members WHERE user_id=?",
        (str(uid),)
    )

    data = cursor.fetchone()

    if not data:
        conn.close()
        bot.reply_to(message, "❌ Вы не состоите в семье.")
        return

    my_clan = data[0]

    if my_clan == clan1:

        hp2 -= damage

        cursor.execute("""
        UPDATE active_wars
        SET hp2=?
        """, (hp2,))

    elif my_clan == clan2:

        hp1 -= damage

        cursor.execute("""
        UPDATE active_wars
        SET hp1=?
        """, (hp1,))

    else:

        conn.close()
        bot.reply_to(message, "❌ Ваша семья не участвует в войне.")
        return

    conn.commit()

    if hp1 <= 0:

        cursor.execute(
            "SELECT clan_name FROM clans WHERE clan_id=?",
            (clan2,)
        )

        winner_name = cursor.fetchone()[0]

        bot.send_message(
            message.chat.id,
            f"🏆 Победила семья: {winner_name}!"
        )

        cursor.execute("DELETE FROM active_wars")

        conn.commit()
        conn.close()
        return

    elif hp2 <= 0:

        cursor.execute(
            "SELECT clan_name FROM clans WHERE clan_id=?",
            (clan1,)
        )

        winner_name = cursor.fetchone()[0]

        bot.send_message(
            message.chat.id,
            f"🏆 Победила семья: {winner_name}!"
        )

        cursor.execute("DELETE FROM active_wars")

        conn.commit()
        conn.close()
        return

    conn.close()

    bot.reply_to(
        message,
        f"🔫 Вы нанесли {damage} урона!\n\n"
        f"🥷 Семья #{clan1}: {hp1} HP\n"
        f"🥷 Семья #{clan2}: {hp2} HP"
    )
# --- Обработчик команды /xo ---
@bot.message_handler(commands=["xo"])
def start_xo(message):
    chat_id = message.chat.id
    
    
    if chat_id in xo_games:
        del xo_games[chat_id]
        
    # 2. Создаем абсолютно новый, гарантированно пустой список
    # Мы используем цикл, чтобы создать 9 независимых элементов " "
    new_board = []
    for _ in range(9):
        new_board.append(" ")
    
    # 3. Записываем чистые данные
    xo_games[chat_id] = {
        "board": new_board, 
        "turn": "❌", 
        "player1": message.from_user.id, 
        "player2": None
    }
    
    bot.send_message(chat_id, "🎮 Игра создана! Ожидается второй игрок.\nВторой участник должен написать /join_xo")


# --- Обработчик команды /join_xo ---
@bot.message_handler(commands=["join_xo"])
def join_xo(message):
    chat_id = message.chat.id
    if chat_id in xo_games and xo_games[chat_id]["player2"] is None:
        if message.from_user.id == xo_games[chat_id]["player1"]:
            bot.reply_to(message, "❌ Вы не можете играть сами с собой!")
            return
        
        xo_games[chat_id]["player2"] = message.from_user.id
        bot.send_message(chat_id, "✅ Второй игрок найден! Игру начинает ❌ (Первый игрок).", 
                         reply_markup=get_xo_markup(xo_games[chat_id]["board"]))
    else:
        bot.reply_to(message, "❌ Нет активных игр для присоединения или место занято.")
def handle_xo_click(call):

    print("XO CLICK:", call.data)

    chat_id = call.message.chat.id
# --- ЕДИНСТВЕННЫЙ обработчик кликов ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("xo_"))
def handle_xo_click(call):
    chat_id = call.message.chat.id
    if chat_id not in xo_games: 
        return
    
    game = xo_games[chat_id]
    
    # Проверка, что оба игрока в сборе
    if game["player2"] is None:
        bot.answer_callback_query(call.id, "Ждем второго игрока!")
        return

    # Проверка хода
    current_player_id = game["player1"] if game["turn"] == "❌" else game["player2"]
    if call.from_user.id != current_player_id:
        bot.answer_callback_query(call.id, "Сейчас не ваш ход!")
        return

    # Логика хода
    cell = int(call.data.split("_")[1])
    if game["board"][cell] == " ":
        game["board"][cell] = game["turn"]
        winner = check_winner(game["board"])
        
        if winner:
            result = f"🎉 Победил игрок: {winner}!" if winner != "Draw" else "🤝 Ничья!"
            bot.edit_message_text(result, chat_id, call.message.message_id, reply_markup=None)
            del xo_games[chat_id]
        else:
            game["turn"] = "⭕" if game["turn"] == "❌" else "❌"
            bot.edit_message_text(f"Ход: {game['turn']}", chat_id, call.message.message_id, reply_markup=get_xo_markup(game["board"]))
    else:
        bot.answer_callback_query(call.id, "Клетка занята!")
     
@bot.callback_query_handler(func=lambda call: call.data.startswith("unmute_"))
def handle_unmute(call):
    if not is_user_admin(call.from_user.id):
        bot.answer_callback_query(
            call.id, "❌ Вы не Администратор бота!", show_alert=True
        )
        return
    t_uid = int(call.data.split("_")[1])
    try:
        bot.restrict_chat_member(
            call.message.chat.id,
            t_uid,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
        )
        bot.edit_message_text(
           f"🔊 Админ {call.from_user.first_name} снял мут с игрока!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None,
        )
    except BaseException:
        bot.answer_callback_query(
            call.id, "❌ Ошибка размута. Проверьте права бота в чате.", show_alert=True
        )
@bot.message_handler(commands=["ban"])
def ban_user(message):

    if message.from_user.id != CREATOR_ID:
        return

    # Бан ответом
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        try:

            bot.ban_chat_member(
                message.chat.id,
                target.id
            )

            bot.reply_to(
                message,
                f"🔨 @{target.username} забанен."
            )

        except Exception as e:

            bot.reply_to(
                message,
                f"❌ Ошибка:\n{e}"
            )

        return

    # Бан по username
    args = message.text.split()

    if len(args) < 2:

        bot.reply_to(
            message,
            "❌ Использование:\n/ban @username"
        )

        return

    username = args[1].replace("@", "")

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE username LIKE ?
        """,
        (f"%{username}%",)
    )

    data = cursor.fetchone()

    conn.close()

    if not data:

        bot.reply_to(
            message,
            "❌ Пользователь не найден."
        )

        return

    target_id = int(data[0])

    try:

        bot.ban_chat_member(
            message.chat.id,
            target_id
        )

        bot.reply_to(
            message,
            f"🔨 @{username} забанен."
        )

    except Exception as e:

        bot.reply_to(
            message,
            f"❌ Ошибка:\n{e}"
        )
        
@bot.message_handler(commands=["unban"])
def unban_user(message):

    if message.from_user.id != CREATOR_ID:
        return

    # Разбан ответом
    if message.reply_to_message:

        target = message.reply_to_message.from_user

        try:

            bot.unban_chat_member(
                message.chat.id,
                target.id
            )

            bot.reply_to(
                message,
                f"✅ @{target.username} разбанен."
            )

        except Exception as e:

            bot.reply_to(
                message,
                f"❌ Ошибка:\n{e}"
            )

        return

    # Разбан по username
    args = message.text.split()

    if len(args) < 2:

        bot.reply_to(
            message,
            "❌ Использование:\n/unban @username"
        )

        return

    username = args[1].replace("@", "")

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE username LIKE ?
        """,
        (f"%{username}%",)
    )

    data = cursor.fetchone()

    conn.close()

    if not data:

        bot.reply_to(
            message,
            "❌ Пользователь не найден."
        )

        return

    target_id = int(data[0])

    try:

        bot.unban_chat_member(
            message.chat.id,
            target_id
        )

        bot.reply_to(
            message,
            f"✅ @{username} разбанен."
        )

    except Exception as e:

        bot.reply_to(
            message,
            f"❌ Ошибка:\n{e}"
        )

@bot.message_handler(commands=["reg"])
def reg(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email FROM users WHERE user_id = ?",
        (user_id,)
    )

    data = cursor.fetchone()

    conn.close()

    if data and data[0]:
        bot.reply_to(
            message,
            "✅ Вы уже зарегистрированы."
        )
        return

    bot.set_state(
        message.from_user.id,
        RegistrationStates.email,
        message.chat.id
    )

    bot.reply_to(
        message,
        "📧 Введите ваш email:"
    )
@bot.message_handler(state=RegistrationStates.email)
def get_email(message):

    email = message.text.strip()

    code = random.randint(1000, 9999)

    with bot.retrieve_data(
        message.from_user.id,
        message.chat.id
    ) as data:

        data["email"] = email
        data["code"] = str(code)

    try:

        send_email(email, code)

        bot.set_state(
            message.from_user.id,
            RegistrationStates.code,
            message.chat.id
        )

        bot.reply_to(
            message,
            "📨 Код отправлен на почту. Введите код:"
        )

    except Exception as e:

        bot.reply_to(
            message,
            f"❌ Ошибка:\n{e}"
        )
@bot.message_handler(state=RegistrationStates.code)
def check_code(message):

    entered_code = message.text.strip()

    with bot.retrieve_data(
        message.from_user.id,
        message.chat.id
    ) as data:

        real_code = data["code"]
        email = data["email"]

    if entered_code == real_code:

        conn = sqlite3.connect("game_database.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET email = ? WHERE user_id = ?",
            (
                email,
                str(message.from_user.id)
            )
        )

        conn.commit()
        conn.close()

        bot.reply_to(
            message,
            "✅ Регистрация завершена!"
        )

        bot.delete_state(
            message.from_user.id,
            message.chat.id
        )

    else:

        bot.reply_to(
            message,
            "❌ Неверный код."
        )
@bot.message_handler(commands=['setnick'])
def setnick_command(message):

    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        bot.reply_to(
            message,
            "⚠️ Использование:\n/setnick ваш_ник"
        )
        return

    nickname = args[1]

    if len(nickname) > 20:
        bot.reply_to(message, "❌ Ник слишком длинный.")
        return

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET nickname = ?
        WHERE user_id = ?
        """,
        (nickname, user_id)
    )

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"✅ Новый ник установлен:\n👤 <b>{nickname}</b>",
        parse_mode='HTML'
    )
@bot.message_handler(commands=['profile'])
def profile_command(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT nickname, balance, role
        FROM users
        WHERE user_id = ?
        """,
        (user_id,)
    )

    data = cursor.fetchone()

    conn.close()

    if not data:
        bot.reply_to(message, "❌ Профиль не найден.")
        return

    nickname, balance, role = data

    if not nickname:
        if message.from_user.username:
            nickname = f"@{message.from_user.username}"
        else:
            nickname = message.from_user.first_name

    text = (
        f"👤 Ник:<b>{nickname}</b>\n"
        f"👑 Роль: {role}\n"
        f"💰 Баланс: {balance}"
    )

    bot.reply_to(message, text, parse_mode='HTML')
@bot.message_handler(commands=["forbes"])
def forbes_command(message):
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, username, role, balance FROM users ORDER BY balance DESC LIMIT 10"
    )
    top_users = cursor.fetchall()
    conn.close()

    if not top_users:
        bot.reply_to(message, "🏆 Список богачей пуст.")
        return

    text = "🏆 Список самых богатых игроков (Forbes):\n\n"
    for index, user in enumerate(top_users):
        u_id, u_name, u_role, u_balance = user
        display = u_name if u_name != "Игрок" else f"ID {u_id}"
        text += f"{index +
                   1}. Игрок: {display} | Роль: {u_role} | Баланс: {u_balance} монет\n"
    bot.reply_to(message, text, parse_mode='HTML')

@bot.message_handler(commands=["createcar"])
def create_car(message):

    if message.from_user.id != CREATOR_ID:
        return

    args = message.text.split()

    if len(args) < 4:
        bot.reply_to(
            message,
            "❌ Использование:\n/createcar название скорость цена"
        )
        return

    car_name = args[1]

    try:
        speed = int(args[2])
        price = int(args[3])
    except:
        bot.reply_to(message, "❌ Скорость и цена должны быть числами.")
        return

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO cars_shop (
            car_name,
            speed,
            price
        )
        VALUES (?, ?, ?)
        """,
        (
            car_name,
            speed,
            price
        )
    )

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"🚗 Машина {car_name} создана!"
    )
@bot.message_handler(commands=["blueprints"])
def blueprints_command(message):

    check_blueprint_refresh()

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, car_name, amount, price
    FROM blueprint_shop
    """)

    items = cursor.fetchall()

    text = "📜 Магазин чертежей\n\n"

    for item in items:

        text += (
            f"#{item[0]}\n"
            f"🚗 {item[1]}\n"
            f"📜 {item[2]} чертежей\n"
            f"💰 {item[3]}$\n\n"
        )

    text += "Покупка: /buybp ID"

    conn.close()

    bot.reply_to(message, text)
@bot.message_handler(commands=["buybp"])
def buybp_command(message):

    args = message.text.split()

    if len(args) < 2:
        return

    item_id = int(args[1])

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT car_name, amount, price
    FROM blueprint_shop
    WHERE id = ?
    """, (item_id,))

    item = cursor.fetchone()

    if not item:
        conn.close()
        return

    cursor.execute("""
    SELECT balance
    FROM users
    WHERE user_id = ?
    """, (str(message.from_user.id),))

    balance = cursor.fetchone()[0]

    if balance < item[2]:

        bot.reply_to(
            message,
            "❌ Недостаточно денег."
        )

        conn.close()
        return

    cursor.execute("""
    UPDATE users
    SET balance = balance - ?
    WHERE user_id = ?
    """, (
        item[2],
        str(message.from_user.id)
    ))

    cursor.execute("""
    UPDATE user_cars
    SET blueprints = blueprints + ?
    WHERE user_id = ?
    """, (
        item[1],
        str(message.from_user.id)
    ))

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"✅ Куплено {item[1]} чертежей."
    )
    
@bot.message_handler(commands=["upstar"])
def upstar_command(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT stars, blueprints, speed
    FROM user_cars
    WHERE user_id = ?
    """, (str(message.from_user.id),))

    car = cursor.fetchone()

    if not car:

        conn.close()
        return

    stars = car[0]
    blueprints = car[1]

    need = stars * 10

    if blueprints < need:

        bot.reply_to(
            message,
            f"❌ Нужно {need} чертежей."
        )

        conn.close()
        return

    cursor.execute("""
    UPDATE user_cars
    SET stars = stars + 1,
        blueprints = blueprints - ?,
        speed = speed + 20
    WHERE user_id = ?
    """, (
        need,
        str(message.from_user.id)
    ))

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"⭐ Машина улучшена до {stars+1} звезды!"
    )   
    
@bot.message_handler(commands=["mycars"])
def garage_command(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT car_name, speed, turbo, engine, tires, stars, blueprints, active
    FROM user_cars
    WHERE user_id = ?
    """, (user_id,))

    cars = cursor.fetchall()
    conn.close()

    if not cars:
        bot.reply_to(message, "🚫 У вас нет машин.")
        return

    text = "🏎 Ваш гараж:\n\n"

    for car in cars:
        # car[0]=name, car[1]=speed, car[2]=turbo, car[3]=engine, car[4]=tires...
        
        # Превращаем None в 0 для каждого параметра
        base_speed = car[1] if car[1] is not None else 0
        turbo = car[2] if car[2] is not None else 0
        engine = car[3] if car[3] is not None else 0
        tires = car[4] if car[4] is not None else 0
        
        active_text = " ✅ АКТИВНАЯ" if car[7] == 1 else ""

        # Теперь здесь гарантированно нет None
        final_speed = base_speed + (turbo * 20) + (engine * 15) + (tires * 10)

        text += (
            f"🚗 {car[0]}{active_text}\n"
            f"⚡ Скорость: {final_speed} км/ч\n"
            f"🌀 Турбо: {turbo} lvl\n"
            f"🔧 Двигатель: {engine} lvl\n"
            f"🛞 Шины: {tires} lvl\n"
            f"⭐ Звезды: {car[5] or 0}\n"
            f"📜 Чертежи: {car[6] or 0}\n\n"
        )


    bot.reply_to(message, text)

@bot.message_handler(commands=["checkcars"])
def checkcars(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM user_cars
    WHERE user_id = ?
    """, (str(message.from_user.id),))

    cars = cursor.fetchall()

    conn.close()

    bot.reply_to(message, str(cars))
import threading
from flask import Flask, request, jsonify

# Создаем Flask-приложение
app = Flask(__name__)

# Твой маршрут для получения машин
# Эта функция создаст базу данных, если её нет
def setup_database():
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_cars (
            user_id TEXT,
            car_name TEXT
        )
    """)
    conn.commit()
    conn.close()

# Вызываем один раз при старте
setup_database()

@app.route('/get_cars', methods=['GET'])
def get_cars():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "No user_id"}), 400

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT car_name, price 
        FROM user_cars 
        WHERE user_id = ?
    """, (str(user_id),))
    
    rows = cursor.fetchall()
    conn.close()

    cars_list = [{"car_name": row[0], "price": row[1] or 0} for row in rows]
    
    return jsonify(cars_list)
@bot.message_handler(commands=["cases"])
def cases_command(message):

    bot.reply_to(
        message,
        "🎁 Кейсы\n\n"
        "/buycase - купить кейс\n"
        "/opencase - открыть кейс"
    )
@bot.message_handler(commands=["buycase"])
def buycase_command(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE user_id=?",
        (user_id,)
    )

    balance = cursor.fetchone()[0]

    if balance < 50000:
        bot.reply_to(message, "❌ Не хватает денег.")
        conn.close()
        return

    cursor.execute(
        "UPDATE users SET balance=balance-50000 WHERE user_id=?",
        (user_id,)
    )

    cursor.execute("""
    INSERT OR IGNORE INTO cases
    (user_id, case_count)
    VALUES (?,0)
    """, (user_id,))

    cursor.execute("""
    UPDATE cases
    SET case_count=case_count+1
    WHERE user_id=?
    """, (user_id,))

    conn.commit()
    conn.close()

    bot.reply_to(message, "🎁 Кейс куплен!")
@bot.message_handler(commands=["opencase"])
def opencase_command(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT case_count FROM cases WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchone()

    if not data or data[0] <= 0:
        bot.reply_to(message, "❌ У вас нет кейсов.")
        conn.close()
        return

    reward = random.choice([
        ("money", 50000),
        ("money", 100000),
        ("fuel", 50),
        ("bp", 5),
        ("bp", 10)
    ])

    cursor.execute("""
    UPDATE cases
    SET case_count=case_count-1
    WHERE user_id=?
    """, (user_id,))

    if reward[0] == "money":

        cursor.execute("""
        UPDATE users
        SET balance=balance+?
        WHERE user_id=?
        """, (reward[1], user_id))

        text = f"💰 Вы получили {reward[1]}$"

    elif reward[0] == "fuel":

        cursor.execute("""
        UPDATE users
        SET fuel=fuel+?
        WHERE user_id=?
        """, (reward[1], user_id))

        text = f"⛽ Вы получили {reward[1]} бензина"

    else:

        cursor.execute("""
        UPDATE user_cars
        SET blueprints=blueprints+?
        WHERE user_id=?
        """, (reward[1], user_id))

        text = f"📜 Вы получили {reward[1]} чертежей"

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"🎁 Кейс открыт!\n\n{text}"
    )
    
@bot.message_handler(commands=["offers"])
def offers_command(message):

    bot.reply_to(
        message,
        "🔥 Офферы дня\n\n"
        "1️⃣ 20 чертежей - 150000$\n"
        "2️⃣ 5 кейсов - 200000$\n"
        "3️⃣ 100 бензина - 100000$\n\n"
        "Купить:\n"
        "/buyoffer 1"
    )
@bot.message_handler(commands=["buyoffer"])
def buyoffer_command(message):

    args = message.text.split()

    if len(args) < 2:
        return

    offer = int(args[1])

    if offer == 1:
        bot.reply_to(message, "📜 Получено 20 чертежей")
    elif offer == 2:
        bot.reply_to(message, "🎁 Получено 5 кейсов")
    elif offer == 3:
        bot.reply_to(message, "⛽ Получено 100 бензина")
@bot.message_handler(commands=["loadcars"])
def load_cars(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cars_shop")

    for car in cars_shop:

        cursor.execute(
            """
            INSERT INTO cars_shop
            (car_name, speed, price)
            VALUES (?, ?, ?)
            """,
            car
        )

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        "✅ Машины загружены!"
    )
    
@bot.message_handler(commands=["cars"])
def cars_command(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT car_name, speed, price FROM cars_shop")

    cars = cursor.fetchall()

    conn.close()

    if not cars:
        bot.reply_to(message, "🚫 Машин пока нет.")
        return

    text = "🚗 Автосалон:\n\n"

    for car in cars:

        text += (
            f"🚘 {car[0]}\n"
            f"⚡ Скорость: {car[1]} км/ч\n"
            f"💰 Цена: {car[2]}$\n\n"
        )

    text += "🛒 Купить: /buycar название"

    bot.reply_to(message, text)
    
@bot.message_handler(commands=["buycar"])
def buycar(message):

    args = message.text.replace("/buycar ", "").strip()

    if not args:
        bot.reply_to(
            message,
            "❌ Использование:\n/buycar название"
        )
        return

    car_name = args
    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # Машина из магазина
    cursor.execute(
        """
        SELECT speed, price
        FROM cars_shop
        WHERE car_name = ?
        """,
        (car_name,)
    )

    car = cursor.fetchone()

    if not car:
        bot.reply_to(message, "❌ Машина не найдена.")
        conn.close()
        return

    speed, price = car

    # Уже есть машина?
    cursor.execute(
        """
        SELECT 1
        FROM user_cars
        WHERE user_id = ? AND car_name = ?
        """,
        (user_id, car_name)
    )

    if cursor.fetchone():
        bot.reply_to(message, "❌ У вас уже есть эта машина.")
        conn.close()
        return

    # Баланс
    cursor.execute(
        "SELECT balance FROM users WHERE user_id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        bot.reply_to(message, "❌ Пользователь не найден.")
        conn.close()
        return

    balance = user[0]

    if balance < price:
        bot.reply_to(message, "❌ Недостаточно денег.")
        conn.close()
        return

    # Проверяем есть ли уже машины (для active)
    cursor.execute(
        """
        SELECT 1
        FROM user_cars
        WHERE user_id = ?
        """,
        (user_id,)
    )

    has_cars = cursor.fetchone()

    active = 1 if not has_cars else 0

    # списание денег
    cursor.execute(
        """
        UPDATE users
        SET balance = balance - ?
        WHERE user_id = ?
        """,
        (price, user_id)
    )

    # добавление машины (ВАЖНО: добавили active)
    cursor.execute(
        """
        INSERT INTO user_cars
        (user_id, car_name, speed, turbo, engine, tires, stars, blueprints, active)
        VALUES (?, ?, ?, 0, 0, 0, 0, 0, ?)
        """,
        (user_id, car_name, speed, active)
    )

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"🚗 Вы купили {car_name}!"
    )

@bot.message_handler(commands=["selectcar"])
def selectcar(message):

    args = message.text.replace("/selectcar ", "")

    if not args:
        bot.reply_to(
            message,
            "❌ Использование:\n/selectcar название"
        )
        return

    car_name = args

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM user_cars
        WHERE user_id = ? AND car_name = ?
        """,
        (user_id, car_name)
    )

    car = cursor.fetchone()

    if not car:
        bot.reply_to(
            message,
            "❌ У вас нет этой машины."
        )

        conn.close()
        return

    cursor.execute(
        """
        UPDATE user_cars
        SET active = 0
        WHERE user_id = ?
        """,
        (user_id,)
    )

    cursor.execute(
        """
        UPDATE user_cars
        SET active = 1
        WHERE user_id = ? AND car_name = ?
        """,
        (user_id, car_name)
    )

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"🏎 Активная машина:\n{car_name}"
    )  
@bot.message_handler(commands=["giftcar"])
def giftcar(message):

    if message.from_user.id != CREATOR_ID:
        return

    args = message.text.split(maxsplit=2)

    if len(args) < 3:

        bot.reply_to(
            message,
            "❌ Использование:\n/giftcar id машина"
        )

        return

    target_id = args[1]
    car_name = args[2]

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT speed, price
        FROM cars_shop
        WHERE car_name = ?
        """,
        (car_name,)
    )

    car = cursor.fetchone()

    if not car:

        bot.reply_to(
            message,
            "❌ Машина не найдена."
        )

        conn.close()
        return

    speed, price = car
    
    cursor.execute(
        """
        INSERT INTO user_cars
        (
            user_id,
            car_name,
            speed
        )
        VALUES (?, ?, ?)
        """,
        (
            target_id,
            car_name,
            speed
        )
    )

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"🎁 Машина {car_name} подарена!"
    )
    
    
@bot.message_handler(commands=["upgrade"])
def upgrade_car(message):

    args = message.text.split()

    if len(args) < 2:
        bot.reply_to(
            message,
            "⚙️ Использование:\n/upgrade turbo\n/upgrade engine\n/upgrade tires"
        )
        return

    upgrade_type = args[1].lower()

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT balance FROM users
    WHERE user_id = ?
    """, (user_id,))

    balance = cursor.fetchone()[0]

    price = 50000

    if balance < price:
        bot.reply_to(message, "❌ Недостаточно денег.")
        conn.close()
        return

    if upgrade_type == "turbo":

        cursor.execute("""
        UPDATE user_cars
        SET turbo = turbo + 1
        WHERE user_id = ?
        """, (user_id,))

    elif upgrade_type == "engine":

        cursor.execute("""
        UPDATE user_cars
        SET engine = engine + 1
        WHERE user_id = ?
        """, (user_id,))

    elif upgrade_type == "tires":

        cursor.execute("""
        UPDATE user_cars
        SET tires = tires + 1
        WHERE user_id = ?
        """, (user_id,))

    else:
        bot.reply_to(message, "❌ Неизвестная прокачка.")
        conn.close()
        return

    cursor.execute("""
    UPDATE users
    SET balance = balance - ?
    WHERE user_id = ?
    """, (price, user_id))

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"✅ Улучшение {upgrade_type} куплено за {price}$"
    )
    
@bot.message_handler(commands=["race"])
def race_command(message):

    if not message.reply_to_message:
        bot.reply_to(
            message,
            "🏁 Ответьте на сообщение игрока:\n/race ставка"
        )
        return

    args = message.text.split()

    if len(args) < 2:
        bot.reply_to(message, "❌ Укажите ставку.")
        return

    try:
        bet = int(args[1])
    except:
        bot.reply_to(message, "❌ Ставка должна быть числом.")
        return

    user1 = str(message.from_user.id)
    user2 = str(message.reply_to_message.from_user.id)

    update_fuel(user1)
    update_fuel(user2)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # БЕНЗИН
    cursor.execute("""
    SELECT fuel
    FROM users
    WHERE user_id = ?
    """, (user1,))

    fuel1 = cursor.fetchone()[0]

    cursor.execute("""
    SELECT fuel
    FROM users
    WHERE user_id = ?
    """, (user2,))

    fuel2 = cursor.fetchone()[0]

    if fuel1 < 25:
        bot.reply_to(
            message,
            "⛽ У вас недостаточно бензина."
        )
        conn.close()
        return

    if fuel2 < 25:
        bot.reply_to(
            message,
            "⛽ У соперника недостаточно бензина."
        )
        conn.close()
        return

    # БАЛАНС
    cursor.execute("""
    SELECT balance
    FROM users
    WHERE user_id = ?
    """, (user1,))

    balance1 = cursor.fetchone()[0]

    cursor.execute("""
    SELECT balance
    FROM users
    WHERE user_id = ?
    """, (user2,))

    balance2 = cursor.fetchone()[0]

    if balance1 < bet:
        bot.reply_to(message, "❌ У вас недостаточно денег.")
        conn.close()
        return

    if balance2 < bet:
        bot.reply_to(message, "❌ У соперника недостаточно денег.")
        conn.close()
        return

    # МАШИНЫ
    cursor.execute("""
    SELECT car_name, speed, turbo, engine, tires
    FROM user_cars
    WHERE user_id = ? AND active = 1
    """, (user1,))

    car1 = cursor.fetchone()

    cursor.execute("""
    SELECT car_name, speed, turbo, engine, tires
    FROM user_cars
    WHERE user_id = ? AND active = 1
    """, (user2,))

    car2 = cursor.fetchone()

    if not car1 or not car2:
        bot.reply_to(message, "🚫 У кого-то нет машины.")
        conn.close()
        return

    # СКОРОСТЬ
    boost1 = random.randint(0, 40)
    boost2 = random.randint(0, 40)

    speed1 = (
        car1[1]
        + car1[2] * 20
        + car1[3] * 35
        + car1[4] * 15
        + boost1
    )

    speed2 = (
        car2[1]
        + car2[2] * 20
        + car2[3] * 35
        + car2[4] * 15
        + boost2
    )

    player1 = message.from_user.first_name
    player2 = message.reply_to_message.from_user.first_name

    # АНИМАЦИЯ
    msg = bot.reply_to(
        message,
        "🚦 Гонщики выезжают на старт..."
    )

    time.sleep(1)

    bot.edit_message_text(
        f"""
🏁 DRAG RACE

🚗 {player1} — {car1[0]}
🚘 {player2} — {car2[0]}

🔴 3
""",
        message.chat.id,
        msg.message_id
    )

    time.sleep(1)

    bot.edit_message_text(
        f"""
🏁 DRAG RACE

🚗 {player1} — {car1[0]}
🚘 {player2} — {car2[0]}

🟠 2
""",
        message.chat.id,
        msg.message_id
    )

    time.sleep(1)

    bot.edit_message_text(
        f"""
🏁 DRAG RACE

🚗 {player1} — {car1[0]}
🚘 {player2} — {car2[0]}

🟡 1
""",
        message.chat.id,
        msg.message_id
    )

    time.sleep(1)

    frames = [

f"""
🏁 DRAG RACE

🚗═................🏁
🚘═................🏁
""",

f"""
🏁 DRAG RACE

🚗════.............🏁
🚘═══..............🏁
""",

f"""
🏁 DRAG RACE

🚗════════.........🏁
🚘═══════..........🏁
""",

f"""
🏁 DRAG RACE

🚗════════════.....🏁
🚘══════════.......🏁
""",

f"""
🏁 DRAG RACE

🚗════════════════🏁
🚘═══════════════🏁
"""
    ]

    for frame in frames:

        bot.edit_message_text(
            frame,
            message.chat.id,
            msg.message_id
        )

        time.sleep(0.7)

    # ПОБЕДИТЕЛЬ
    if speed1 > speed2:

        winner = user1
        loser = user2
        winner_name = player1

    else:

        winner = user2
        loser = user1
        winner_name = player2
    cursor.execute("""
    SELECT clan_id
    FROM clan_members
    WHERE user_id = ?
     """, (winner,))

    clan = cursor.fetchone()

    if clan:

     cursor.execute("""
    UPDATE clans
    SET points = points + 5
    WHERE clan_id = ?
    """, (clan[0],))
    cursor.execute("""
    INSERT OR IGNORE INTO race_rating
    (user_id, wins)
    VALUES (?, 0)
    """, (winner,))

    cursor.execute("""
    UPDATE race_rating
    SET wins = wins + 1
    WHERE user_id = ?
    """, (winner,))

    # ДЕНЬГИ
    cursor.execute("""
    UPDATE users
    SET balance = balance + ?
    WHERE user_id = ?
    """, (bet, winner))

    cursor.execute("""
    UPDATE users
    SET balance = balance - ?
    WHERE user_id = ?
    """, (bet, loser))

    # БЕНЗИН
    cursor.execute("""
    UPDATE users
    SET fuel = fuel - 25
    WHERE user_id = ?
    """, (user1,))

    cursor.execute("""
    UPDATE users
    SET fuel = fuel - 25
    WHERE user_id = ?
    """, (user2,))

    conn.commit()
    conn.close()

    bot.edit_message_text(
        f"""
🏁 Гонка завершена!

🚗 {player1}: {speed1} км/ч
🔥 Буст: +{boost1}

🚘 {player2}: {speed2} км/ч
🔥 Буст: +{boost2}

⛽ -25 бензина

🏆 Победитель: {winner_name}
💰 Выигрыш: {bet}$
""",
        message.chat.id,
        msg.message_id
    )
    
@bot.message_handler(commands=["rating"])
def rating_command(message):

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT end_time
    FROM race_season
    WHERE id = 1
    """)

    end_time = cursor.fetchone()[0]

    remaining = end_time - int(time.time())

    hours = remaining // 3600
    minutes = (remaining % 3600) // 60

    cursor.execute("""
    SELECT user_id, wins
    FROM race_rating
    ORDER BY wins DESC
    LIMIT 100
    """)

    players = cursor.fetchall()

    text = (
        f"🏆 РЕЙТИНГ ГОНЩИКОВ\n\n"
        f"⏳ До конца сезона: {hours}ч {minutes}м\n\n"
    )

    place = 1

    for player in players:

        uid = player[0]
        wins = player[1]

        try:
            user = bot.get_chat(uid)
            name = user.first_name
        except:
            name = f"ID {uid}"

        if place == 1:
            medal = "🥇"
        elif place == 2:
            medal = "🥈"
        elif place == 3:
            medal = "🥉"
        else:
            medal = f"{place}."

        if place <= 10:
            reward = "💎 ТОП НАГРАДА"
        else:
            reward = "🎁 ОБЫЧНАЯ НАГРАДА"

        text += (
            f"{medal} {name}\n"
            f"🏁 Побед: {wins}\n"
            f"{reward}\n\n"
        )

        place += 1

    conn.close()

    bot.reply_to(message, text)
    
@bot.message_handler(commands=["seasonreward"])
def season_reward(message):

    if message.from_user.id != CREATOR_ID:
        return

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT user_id, wins
    FROM race_rating
    ORDER BY wins DESC
    LIMIT 100
    """)

    players = cursor.fetchall()

    place = 1

    for player in players:

        user_id = player[0]

        # ТОП 1-10
        if place == 1:
             reward = 5000000

        elif place == 2:
             reward = 3000000

        elif place == 3:
             reward = 2000000

        elif place <= 10:
             reward = 1000000

        else:
               reward = 100000

        cursor.execute("""
        UPDATE users
        SET balance = balance + ?
        WHERE user_id = ?
        """, (
            reward,
            user_id
        ))

        try:

            bot.send_message(
                user_id,
                f"🏆 Вы получили награду за сезон!\n"
                f"🎁 Награда: {reward}$\n"
                f"📊 Место: {place}"
            )

        except:
            pass

        place += 1

    # НОВЫЙ СЕЗОН
    new_time = int(time.time()) + 172800

    cursor.execute("""
    UPDATE race_season
    SET end_time = ?
    WHERE id = 1
    """, (new_time,))

    # ОЧИЩАЕМ РЕЙТИНГ
    cursor.execute("DELETE FROM race_rating")

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        "✅ Награды сезона выданы!"
    )
@bot.message_handler(commands=["fuel"])
def fuel_command(message):

    user_id = str(message.from_user.id)

    update_fuel(user_id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT fuel
    FROM users
    WHERE user_id = ?
    """, (user_id,))

    fuel = cursor.fetchone()[0]

    conn.close()

    bot.reply_to(
        message,
        f"⛽ Бензин: {fuel}/100"
    )
@bot.message_handler(commands=["broadcast"])
def broadcast(message):
    # Проверка, чтобы это мог делать только админ (замените 123456789 на свой
    # ID)
    if message.from_user.id != 5633124867:
        bot.reply_to(message, "❌ Эта команда доступна только администратору.")
        return

    # Получаем текст рассылки (всё, что после /broadcast)
    text = message.text.replace("/broadcast", "").strip()
    if not text:
        bot.reply_to(message, "⚠️ Напишите текст после команды: /broadcast [ваш текст]")
        return

    # Получаем всех пользователей из базы
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    conn.close()

    # Отправляем сообщение каждому
    count = 0
    for user in users:
        try:
            bot.send_message(
                user[0], f"📢 **Обновление бота:**\n\n{text}", parse_mode="Markdown"
            )
            count += 1
        except BaseException:
            # Если пользователь заблокировал бота, ничего не делаем
            pass

    bot.reply_to(
        message, f"✅ Рассылка завершена! Сообщение получили {count} пользователей."
    )
    
@bot.message_handler(commands=["blackjack"])
def blackjack(message):

    args = message.text.split()

    if len(args) < 2:
        bot.reply_to(message, "❌ Использование: /blackjack сумма")
        return

    try:
        bet = int(args[1])
    except:
        bot.reply_to(message, "❌ Введите число.")
        return

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE user_id = ?",
        (user_id,)
    )

    data = cursor.fetchone()

    if not data:
        conn.close()
        return

    balance = data[0]

    if bet <= 0:
        conn.close()
        return

    if balance < bet:
        bot.reply_to(message, "❌ Недостаточно денег.")
        conn.close()
        return

    player = [
        draw_card(),
        draw_card()
    ]

    dealer = [
        draw_card(),
        draw_card()
    ]

    blackjack_games[user_id] = {
        "bet": bet,
        "player": player,
        "dealer": dealer
    }

    text = (
        f"🃏 Blackjack\n\n"
        f"Ваши карты: {player}\n"
        f"Сумма: {sum(player)}\n\n"
        f"Карта дилера: {dealer[0]}\n\n"
        f"/hit — взять карту\n"
        f"/stand — остановиться"
    )

    bot.reply_to(message, text)

    conn.close()
    
def draw_card():
    return random.choice(cards_deck)


def calculate_total(cards):

    total = sum(card[1] for card in cards)

    aces = sum(
        1 for card in cards
        if card[1] == 11
    )

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total


def format_cards(cards):
    return " ".join(card[0] for card in cards)
    
@bot.message_handler(commands=["hit"])
def bj_hit(message):

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in blackjack_rooms:
        return

    room = blackjack_rooms[chat_id]

    current_id = room["turn_order"][
        room["current_turn"]
    ]

    if user_id != current_id:
        return

    player = room["players"][user_id]

    player["cards"].append(
        draw_card()
    )

    total = calculate_total(player["cards"])

    if total > 21:

        player["busted"] = True
        player["stood"] = True

        bot.reply_to(
            message,
            f"💥 Перебор!\n"
            f"{player['cards']} = {total}"
        )

    else:

        bot.reply_to(
            message,
            f"🃏 Ваши карты:\n"
            f"{format_cards(player['cards'])}"
        )

    next_turn(room, message)
    
@bot.message_handler(commands=["stand"])
def bj_stand(message):

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in blackjack_rooms:
        return

    room = blackjack_rooms[chat_id]

    current_id = room["turn_order"][
        room["current_turn"]
    ]

    if user_id != current_id:
        return

    room["players"][user_id]["stood"] = True

    bot.reply_to(
        message,
        "✋ Ход завершён."
    )

    next_turn(room, message)
    
def next_turn(room, message):

    room["current_turn"] += 1

    if room["current_turn"] >= len(room["turn_order"]):

        finish_blackjack(room, message)
        return

    next_id = room["turn_order"][
        room["current_turn"]
    ]
    
    player = room["players"][next_id]

    total = calculate_total(player["cards"])

    bot.reply_to(
        message,
        f"👉 Ход: "
        f"{room['players'][next_id]['name']}\n"
        f"/hit или /stand или /double"
    )
    
def finish_blackjack(room, message):

    while calculate_total(room["dealer"]) < 17:
        room["dealer"].append(
            draw_card()
        )

    dealer_total = calculate_total(room["dealer"])

    text = (
        f"🎲 Дилер:\n"
        f"{format_cards(room['dealer'])} = {dealer_total}\n\n"
    )

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    for pid, player in room["players"].items():
          
          bet_amount = room["bet"]

          if player["doubled"]:
              bet_amount *= 2

          total = calculate_total(player["cards"])

          result = ""

          if total > 21:

            cursor.execute(
                "UPDATE users SET balance = balance - ? WHERE user_id = ?",
                (room["bet"], pid)
            )

            result = "💀 Проиграл"

          elif dealer_total > 21 or total > dealer_total:

            cursor.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id = ?",
                (room["bet"], pid)
            )

            result = f"🎉 Выиграл {room['bet']}$"

          elif total < dealer_total:

            cursor.execute(
                "UPDATE users SET balance = balance - ? WHERE user_id = ?",
                (room["bet"], pid)
            )

            result = "💀 Проиграл"

          else:
            result = "🤝 Ничья"

          text += (
            f"{player['name']} — "
            f"{player['cards']} = {total}\n"
            f"{result}\n\n"
        )

    conn.commit()
    conn.close()

    bot.reply_to(message, text)

    del blackjack_rooms[
        str(message.chat.id)
    ]
    
@bot.message_handler(commands=["bjroom"])
def create_bj_room(message):

    if message.chat.type == "private":
        bot.reply_to(
            message,
            "❌ Играть можно только в группе."
        )
        return

    args = message.text.split()

    if len(args) < 2:
        bot.reply_to(
            message,
            "❌ Использование: /bjroom ставка"
        )
        return

    try:
        bet = int(args[1])
    except:
        return

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id in blackjack_rooms:
        bot.reply_to(
            message,
            "❌ Комната уже существует."
        )
        return

    blackjack_rooms[chat_id] = {
        "bet": bet,
        "players": {
            user_id: {
                "name": get_user_display_name(message.from_user),
                "cards": [],
                "stood": False,
                "busted": False,
                "doubled": False
            }
        },
        "dealer": [],
        "turn_order": [user_id],
        "current_turn": 0,
        "started": False,
        "creator": user_id
    }

    bot.reply_to(
        message,
        f"🃏 Blackjack комната создана!\n\n"
        f"💰 Ставка: {bet}$\n\n"
        f"👥 Игроки:\n"
        f"- {get_user_display_name(message.from_user)}\n\n"
        f"/joinbj — войти\n"
        f"/startbj — начать"
    )
    
@bot.message_handler(commands=["joinbj"])
def join_bj(message):

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in blackjack_rooms:
        return

    room = blackjack_rooms[chat_id]

    if room["started"]:
        bot.reply_to(message, "❌ Игра уже началась.")
        return

    if user_id in room["players"]:
        return

    room["players"][user_id] = {
        "name": get_user_display_name(message.from_user),
        "cards": [],
        "stood": False,
        "busted": False,
        "doubled": False
    }

    room["turn_order"].append(user_id)

    players_text = "\n".join([
        f"- {p['name']}"
        for p in room["players"].values()
    ])

    bot.reply_to(
        message,
        f"✅ Игрок присоединился!\n\n"
        f"👥 Игроки:\n{players_text}"
    )
    
@bot.message_handler(commands=["startbj"])
def start_bj(message):

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in blackjack_rooms:
        return

    room = blackjack_rooms[chat_id]

    if room["creator"] != user_id:
        bot.reply_to(message, "❌ Только создатель может начать.")
        return

    room["started"] = True

    for pid in room["players"]:

        room["players"][pid]["cards"] = [
            draw_card(),
            draw_card()
        ]

    room["dealer"] = [
        draw_card(),
        draw_card()
    ]

    text = "🃏 Blackjack начался!\n\n"

    for player in room["players"].values():

        total = calculate_total(player["cards"])

        cards_text = format_cards(player["cards"])

        text += (
            f"{player['name']} — "
            f"{cards_text} = {total}\n"
        )

        text += (
           f"\n🎲 Карта дилера: "
           f"{room['dealer'][0]}"
    )

        current_id = room["turn_order"][0]

        text += (
        f"\n\n👉 Ход: "
        f"{room['players'][current_id]['name']}\n"
        f"/hit или /stand или /double"
    )

        bot.reply_to(message, text)
    
@bot.message_handler(commands=["double"])
def bj_double(message):

    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    if chat_id not in blackjack_rooms:
        return

    room = blackjack_rooms[chat_id]

    current_id = room["turn_order"][
        room["current_turn"]
    ]

    if user_id != current_id:
        return

    player = room["players"][user_id]

    if player["doubled"]:
        bot.reply_to(
            message,
            "❌ Вы уже удвоили ставку."
        )
        return

    player["doubled"] = True

    player["cards"].append(
        draw_card()
    )

    total = calculate_total(
        player["cards"]
    )

    bot.reply_to(
        message,
        f"💰 Ставка удвоена!\n"
        f"🃏 Карты: "
        f"{format_cards(player['cards'])}\n"
        f"📊 Сумма: {total}"
    )

    if total > 21:

        player["busted"] = True
        next_turn(room, message)

        bot.reply_to(
            message,
            "💥 Перебор!"
        )

    player["stood"] = True

    next_turn(room, message)
@bot.message_handler(commands=["collect"])
def collect_profit(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(profit) FROM businesses WHERE owner_id = ?",
        (user_id,)
    )

    total_profit = cursor.fetchone()[0]

    if total_profit is None or total_profit == 0:
        bot.reply_to(message, "❌ У вас нет бизнесов.")
    else:

        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (total_profit, user_id)
        )

        conn.commit()

        bot.reply_to(
            message,
            f"💰 Вы собрали {total_profit} монет прибыли!"
        )

    conn.close()


@bot.message_handler(commands=["createnft"])
def create_nft(message):
    # 1. Проверка прав
    if message.from_user.id != CREATOR_ID:
        return

    # 2. Разбор аргументов (ВАЖНО: здесь мы определяем name, rarity, price)
    args = message.text.split()
    if len(args) < 4:
        bot.reply_to(message, "⚠️ Использование: /createnft [Название] [Редкость] [Цена]")
        return
    
    name = args[1]
    rarity = args[2]
    price = int(args[3])

    # 3. Теперь, когда переменные определены, можно идти в базу
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO nft_items (owner_id, item_name, rarity, price, for_sale)
        VALUES (?, ?, ?, ?, 0)
    """, (str(CREATOR_ID), name, rarity, price))
    
    nft_id = cursor.lastrowid
    conn.commit()
    conn.close()

    bot.reply_to(message, f"✅ NFT создан!\n🆔 ID: {nft_id}\n🖼 Название: {name}\n💎 Редкость: {rarity}\n💰 Цена: {price}")


@bot.message_handler(commands=["mynfts"])
def my_nfts(message):

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT nft_id, nft_name, rarity, price
        FROM nfts
        WHERE owner_id = ?
    """,
        (user_id,),
    )

    nfts = cursor.fetchall()

    conn.close()

    if not nfts:

        bot.reply_to(message, "❌ У вас нет NFT.")

        return

    text = "🎁 Ваши NFT:\n\n"

    for nft in nfts:

        nft_id, name, rarity, price = nft

        text += f"🆔 #{nft_id}\n" f"🖼 {name}\n" f"💎 {rarity}\n" f"💰 {price}\n\n"

    bot.reply_to(message, text, parse_mode='HTML')


@bot.message_handler(commands=["giftnft"])
def gift_nft(message):

    args = message.text.split()

    if len(args) < 3:

        bot.reply_to(message, "⚠️ Использование:\n" "/giftnft ID_NFT ID_игрока")

        return

    nft_id = args[1]
    target_id = args[2]

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT owner_id, nft_name
        FROM nft_items
        WHERE nft_id = ?
    """,
        (nft_id,),
    )

    nft = cursor.fetchone()

    if not nft:

        bot.reply_to(message, "❌ NFT не найден.")
        conn.close()
        return

    owner_id, nft_name = nft

    if owner_id != str(message.from_user.id):

        bot.reply_to(message, "❌ Это не ваш NFT.")

        conn.close()
        return

    cursor.execute(
        """
        UPDATE nfts
        SET owner_id = ?
        WHERE nft_id = ?
    """,
        (target_id, nft_id),
    )

    conn.commit()
    conn.close()

    bot.reply_to(message, f"🎁 NFT {nft_name} передан игроку {target_id}")


@bot.message_handler(commands=["sellnft"])
def sell_nft(message):

    args = message.text.split()

    if len(args) < 3:
        bot.reply_to(message, "/sellnft ID_NFT ЦЕНА")
        return

    nft_id = args[1]

    try:
        price = int(args[2])
    except BaseException:
        bot.reply_to(message, "❌ Цена должна быть числом.")
        return

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT owner_id
        FROM nft_items
        WHERE nft_id = ?
    """,
        (nft_id,),
    )

    data = cursor.fetchone()

    if not data:
        bot.reply_to(message, "❌ NFT не найден.")
        conn.close()
        return

    if data[0] != user_id:
        bot.reply_to(message, "❌ Это не ваш NFT.")
        conn.close()
        return

    cursor.execute(
        """
        UPDATE nft_items
        SET price = ?, for_sale = 1
        WHERE nft_id = ?
    """,
        (price, nft_id),
    )

    conn.commit()
    conn.close()

    bot.reply_to(message, f"💰 NFT #{nft_id} выставлен на продажу за {price} монет.")


@bot.message_handler(commands=["buynft"])
def buy_nft(message):

    args = message.text.split()

    if len(args) < 2:
        bot.reply_to(message, "/buynft ID_NFT")
        return

    nft_id = args[1]

    buyer_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT owner_id, item_name, price, for_sale
        FROM nft_items
        WHERE nft_id = ?
    """,
        (nft_id,),
    )

    nft = cursor.fetchone()

    if not nft:
        bot.reply_to(message, "❌ NFT не найден.")
        conn.close()
        return

    seller_id, name, price, for_sale = nft

    if for_sale != 1:
        bot.reply_to(message, "❌ NFT не продается.")
        conn.close()
        return

    if seller_id == buyer_id:
        bot.reply_to(message, "❌ Нельзя купить свой NFT.")
        conn.close()
        return

    # баланс покупателя
    cursor.execute(
        """
        SELECT balance
        FROM users
        WHERE user_id = ?
    """,
        (buyer_id,),
    )

    buyer_balance = cursor.fetchone()[0]

    if buyer_balance < price:
        bot.reply_to(message, "❌ Недостаточно монет.")
        conn.close()
        return

    # баланс продавца
    cursor.execute(
        """
        SELECT balance
        FROM users
        WHERE user_id = ?
    """,
        (seller_id,),
    )

    seller_balance = cursor.fetchone()[0]

    cur# перевод денег
    cursor.execute(
        """
        UPDATE users
        SET balance = ?
        WHERE user_id = ?
    """,
        (buyer_balance - price, buyer_id),
    )

    cursor.execute(
        """
        UPDATE users
        SET balance = ?
        WHERE user_id = ?
    """,
        (seller_balance + price, seller_id),
    )

    # передача NFT
    cursor.execute(
        """
        UPDATE nft_items
        SET owner_id = ?, for_sale = 0
        WHERE nft_id = ?
    """,
        (buyer_id, nft_id),
    )

    conn.commit()
    conn.close()

    bot.reply_to(message, f"🎉 Вы купили NFT '{name}' за {price} монет!")


@bot.message_handler(commands=["nftmarket"])
def nft_market(message):
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nft_id, item_name, rarity, price FROM nft_items WHERE for_sale = 1")
    items = cursor.fetchall()
    conn.close()

    if not items:
        bot.reply_to(message, "🛒 Рынок NFT пуст.")
        return

    text = "🛒 NFT Market\n\n"
    for nft in items:
        nft_id, name, rarity, price = nft
        text += f"🆔 #{nft_id}\n🎁 {name}\n💎 {rarity}\n💰 {price}\n\n"
    
    bot.reply_to(message, text, parse_mode='HTML')


@bot.message_handler(commands=["addbiz"])
def add_business(message):
    # Только админ
    if message.from_user.id != 5633124867:
        return

    args = message.text.split("|")  # Разделитель | чтобы удобно писать
    if len(args) < 3:
        bot.reply_to(message, "⚠️ Использование: /addbiz | Название | Прибыль")
        return

    name = args[1].strip()
    profit = int(args[2].strip())

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO businesses (name, owner_id, price, profit) VALUES (?, NULL, 0, ?)",
        (name, profit),
    )
    conn.commit()
    conn.close()
    bot.reply_to(
        message, f"✅ Бизнес '{name}' создан! Теперь его можно выставить на аукцион."
    )


@bot.message_handler(commands=["paybiz"])
def pay_business(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Использование: /paybiz [Название]")
        return

    name = args[1]
    user_id = str(message.from_user.id)
    cost = 5000  # Цена продления на сутки

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # Проверка баланса
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    balance = cursor.fetchone()[0]

    if balance < cost:
        bot.reply_to(message, "❌ Недостаточно средств для оплаты налога!")
    else:
        # Продлеваем на 24 часа
        new_expiry = int(time.time()) + (24 * 60 * 60)
        cursor.execute(
            "UPDATE users SET balance = balance - ? WHERE user_id = ?", (cost, user_id)
        )
        cursor.execute(
            "UPDATE businesses SET expiry_date = ? WHERE name = ? AND owner_id = ?",
            (new_expiry, name, user_id),
        )
        conn.commit()
        bot.reply_to(message, f"✅ Бизнес '{name}' продлен на 24 часа!")
    conn.close()


# аукцион


@bot.message_handler(commands=["start_auction"])
def start_auction(message):
    if message.from_user.id != 5633124867:
        return

    args = message.text.split("|")
    if len(args) < 3:
        bot.reply_to(message, "⚠️ Использование: /start_auction | Название | Время_мин")
        return

    name = args[1].strip()
    duration = int(args[2].strip()) * 60

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # Ищем свободный бизнес
    cursor.execute(
        "SELECT id FROM businesses WHERE name = ? AND owner_id IS NULL", (name,)
    )
    if not cursor.fetchone():
        bot.reply_to(message, "❌ Такого свободного бизнеса нет!")
    else:
        end_time = int(time.time()) + duration
        cursor.execute("DELETE FROM auction")
        cursor.execute(
            "INSERT INTO auction (item_name, end_time, current_bid) VALUES (?, ?, 0)",
            (name, end_time),
        )
        conn.commit()
        bot.send_message(message.chat.id, f"📢 Аукцион на бизнес '{name}' открыт!")
    conn.close()


@bot.message_handler(commands=["bid"])
def place_bid(message):
    args = message.text.split()
    if len(args) < 2:
        return
    try:
        bid = int(args[1])
    except ValueError:
        return

    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT item_name, current_bid, highest_bidder, end_time FROM auction"
    )
    auc = cursor.fetchone()

    if not auc:
        bot.reply_to(message, "❌ Аукцион сейчас не проводится.")
        conn.close()
        return

    # ПРОВЕРКА ВРЕМЕНИ (сначала проверяем время)
    if int(time.time()) > auc[3]:
        # Аукцион завершен. Закрываем его, если еще не закрыли.
        winner = auc[2]
        item = auc[0]
        if winner:
            expiry = int(time.time()) + (24 * 60 * 60)
            cursor.execute(
                "UPDATE businesses SET owner_id = ?, expiry_date = ? WHERE name = ?",
                (winner, expiry, item),
            )
            # ВАЖНО: говорим, кто именно победил (winner), а не тот, кто
            # прислал сообщение
            bot.reply_to(
                message,
                f"🏆 Аукцион завершен! Победитель: {winner}. Бизнес '{item}' ваш!",
            )
        else:
            bot.reply_to(message, "🏁 Аукцион завершен, ставок не было.")

        cursor.execute("DELETE FROM auction")
        conn.commit()
        conn.close()
        return  # Выходим, ставку не принимаем

    # 3. ЕСЛИ АУКЦИОН ИДЕТ:
    if bid <= auc[1]:
        bot.reply_to(message, f"❌ Ставка должна быть больше {auc[1]}!")
    else:
        cursor.execute(
            "UPDATE auction SET current_bid = ?, highest_bidder = ?", (bid, user_id)
        )
        conn.commit()
        bot.reply_to(message, f"✅ Ставка {bid} принята!")

    conn.close()


@bot.message_handler(commands=["allbiz"])
def show_all_biz(message):
    try:
        conn = sqlite3.connect("game_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, owner_id FROM businesses")
        bizs = cursor.fetchall()

        if not bizs:
            bot.reply_to(message, "Список бизнесов пока пуст.")
        else:
            # Если owner_id пустой (None), пишем "Свободен"
            text = "🏢 **Список бизнесов:**\n" + "\n".join(
                [
                    f"• {b[0]} | Владелец: {'Свободен' if b[1] is None else f'ID {b[1]}'}"
                    for b in bizs
                ]
            )
            bot.reply_to(message, text, parse_mode="Markdown")
        conn.close()
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")


@bot.message_handler(commands=["mybiz"])
def show_my_biz(message):
    user_id = str(message.from_user.id)
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # 1. Запрашиваем 3 поля: имя, прибыль И дату окончания
    cursor.execute(
        "SELECT name, profit, expiry_date FROM businesses WHERE owner_id = ?",
        (user_id,),
    )
    bizs = cursor.fetchall()

    if not bizs:
        bot.reply_to(message, "🏢 У вас пока нет купленных бизнесов.")
    else:
        text = "💼 **Ваши бизнесы:**\n"
        # 2. Идем циклом по каждому бизнесу
        for b in bizs:
            name, profit, expiry = b[0], b[1], b[2]

            # 3. Делаем красивый статус даты
            if expiry and expiry > time.time():
                date_str = datetime.datetime.fromtimestamp(expiry).strftime(
                    "%d.%m.%Y %H:%M"
                )
                status = f"Оплачен до: {date_str}"
            else:
                status = "⚠️ Срок истек"

            # 4. Собираем строку: имя + прибыль + статус
            text += f"• {name} | 💰 {profit}/час | {status}\n"

        bot.reply_to(message, text, parse_mode="Markdown")
    conn.close()


@bot.message_handler(commands=["check_auction"])
def check_auction(message):
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT item_name, current_bid, end_time FROM auction")
    auc = cursor.fetchone()

    if not auc:
        bot.reply_to(message, "Аукцион сейчас не проводится.")
    else:
        remaining = int(auc[2] - time.time())
        if remaining > 0:
            bot.reply_to(message, f"📢 Лот: {
                auc[0]}\n💰 Текущая ставка: {
                auc[1]}\n⏳ Осталось: {
                remaining //
                60} мин. {
                remaining %
                60} сек.")
        else:
            bot.reply_to(message, "Аукцион завершен! Ожидайте обработки.")
    conn.close()


@bot.message_handler(commands=["buybiz"])
def buy_business(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(
            message,
            "⚠️ Использование: /buybiz [название]. Доступны: Шахта, Завод, Нефтевышка, Авиакомпания",
        )
        return

    biz_name = args[1]
    user_id = str(message.from_user.id)

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # 1. Ищем бизнес
    cursor.execute(
        "SELECT id, price, owner_id FROM businesses WHERE name = ?", (biz_name,)
    )
    biz = cursor.fetchone()

    if not biz:
        bot.reply_to(message, "❌ Такого бизнеса нет!")
    elif biz[2] is not None:
        bot.reply_to(message, "❌ Этот бизнес уже кем-то куплен!")
    else:
        # 2. Проверяем баланс
        cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        user_bal = cursor.fetchone()[0]

        if user_bal < biz[1]:
            bot.reply_to(message, f"❌ Недостаточно средств! Нужно: {biz[1]}")
        else:
            # 3. Покупаем
            cursor.execute(
                "UPDATE users SET balance = balance - ? WHERE user_id = ?",
                (biz[1], user_id),
            )
            cursor.execute(
                "UPDATE businesses SET owner_id = ? WHERE name = ?", (user_id, biz_name)
            )
            conn.commit()
            bot.reply_to(message, f"🎉 Поздравляем! Вы купили {biz_name} за {
                biz[1]} монет.")

    conn.close()


@bot.message_handler(commands=["promo"])
def promo_command(message):
    user_id = str(message.from_user.id)
    display_name = get_user_display_name(message.from_user)

    check_and_register_user(user_id, display_name)

    args = message.text.split()

    if len(args) < 2:
        bot.reply_to(message, "⚠️ Использование: /promo [код]")
        return

    promo_code = args[1].upper()

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # Проверка промокода
    cursor.execute(
        "SELECT reward, max_uses, uses FROM promos WHERE code = ?", (promo_code,)
    )

    promo = cursor.fetchone()

    if not promo:
        bot.reply_to(message, "❌ Промокод не найден.")
        conn.close()
        return

    reward, max_uses, uses = promo

    # Проверка лимита активаций
    if uses >= max_uses:
        bot.reply_to(message, "❌ Лимит активаций промокода исчерпан.")
        conn.close()
        return

    # Проверка: активировал ли пользователь
    cursor.execute(
        "SELECT * FROM promo_activations WHERE user_id = ? AND promo_code = ?",
        (user_id, promo_code),
    )

    if cursor.fetchone():
        bot.reply_to(message, "❌ Вы уже активировали этот промокод.")
        conn.close()
        return

    # Начисляем деньги
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))

    balance = cursor.fetchone()[0]
    new_balance = balance + reward

    cursor.execute(
        "UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id)
    )

    # Обновляем uses
    cursor.execute("UPDATE promos SET uses = uses + 1 WHERE code = ?", (promo_code,))

    # Записываем активацию
    cursor.execute(
        """
        INSERT INTO promo_activations
        (user_id, promo_code, activated_at)
        VALUES (?, ?, ?)
        """,
        (user_id, promo_code, int(time.time())),
    )

    conn.commit()
    conn.close()

    bot.reply_to(
        message,
        f"🎉 Промокод активирован!\n"
        f"💰 Получено: {reward} монет\n"
        f"💳 Баланс: {new_balance}",
    )


@bot.message_handler(commands=["promote"])
def promote_user(message):
    # ПРОВЕРКА: только ваш ID имеет доступ к этой команде
    if message.from_user.id != CREATOR_ID:
        bot.reply_to(message, "❌ У вас нет прав для этой команды!")
        return

    # Разбираем сообщение
    args = message.text.split()

    # 1. Если ответили на сообщение
    if message.reply_to_message:
        target_id = str(message.reply_to_message.from_user.id)
        # Если после команды написали роль (например, /promote Админ), берем
        # её, иначе "админ"
        new_role = args[1] if len(args) > 1 else "админ"
    # 2. Если ввели ID (например, /promote 123456789 Админ)
    else:
        if len(args) < 2:
            bot.reply_to(
                message,
                "⚠️ Использование: /promote [ID] [Роль] или ответ на сообщение: /promote [Роль]",
            )
            return
        target_id = args[1]
        new_role = args[2] if len(args) > 2 else "админ"

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # Проверяем, существует ли пользователь в базе
    cursor.execute("SELECT username FROM users WHERE user_id = ?", (target_id,))
    if cursor.fetchone():
        # ОБНОВЛЯЕМ РОЛЬ
        cursor.execute(
            "UPDATE users SET role = ? WHERE user_id = ?", (new_role, target_id)
        )
        conn.commit()
        bot.reply_to(message, f"✅ Пользователю {target_id} назначена роль: {new_role}")
    else:
        bot.reply_to(message, "❌ Пользователь с таким ID не найден в базе.")

    conn.close()


@bot.message_handler(commands=["coin"])
def coin_command(message):
    user_id = message.from_user.id
    args = message.text.split()

    # Теперь бот проверяет, ввели ли и ставку, и сторону монетки
    if len(args) < 3:
        bot.reply_to(
            message,
            "⚠️ Использование: /coin [ставка] [орел/решка]\nПример: /coin 100 орел",
        )
        return

    try:
        bet = int(args[1])
        choice = args[2].lower()
    except ValueError:
        bot.reply_to(message, "⚠️ Ставка должна быть числом!")
        return

        if choice not in ["орел", "решка"]:
            bot.reply_to(message, "⚠️ Выберите 'орел' или 'решка'!")
            return

    # --- СЮДА ВСТАВЛЯЕТЕ КОД ---
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (str(user_id),))
    bal = cursor.fetchone()[0]

    if bal < bet:
        bot.reply_to(message, "❌ Недостаточно средств!")
        conn.close()
        return

    result = random.choices([0, 1, 2], weights=[45, 45, 10])[0]

    if result == 2:
        new_balance = bal + 100000
        cursor.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            (new_balance, str(user_id)),
        )
        bot.reply_to(
            message, f"🪙 Монетка упала на РЕБРО! \n💰 Вы получаете 100,000 монет!"
        )
    else:
        outcome = "орел" if result == 0 else "решка"
        if choice == outcome:
            new_balance = bal + bet
            bot.reply_to(message, f"🪙 Выпал {outcome}! Вы выиграли: +{bet} монет.")
        else:
            new_balance = bal - bet
            bot.reply_to(message, f"🪙 Выпал {outcome}. Вы проиграли {bet} монет.")

        cursor.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            (new_balance, str(user_id)),
        )

    conn.commit()
    conn.close()
    # ---------------------------


@bot.message_handler(commands=["buytitle"])
def buytitle(message):
    # Разделяем сообщение на команду и сам титул
    parts = message.text.split(maxsplit=1)

    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Использование: /buytitle [Ваш титул]")
        return

    custom_title = parts[1]
    price = 500 + (len(custom_title) * 100)

    if len(custom_title) > 15:
        bot.reply_to(message, "❌ Слишком длинный титул! Максимум 15 символов.")
        return

    # Подключаемся к базе
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    try:
        # Получаем данные пользователя
        cursor.execute(
            "SELECT balance FROM users WHERE user_id = ?", (str(message.from_user.id),)
        )
        row = cursor.fetchone()

        if row is None:
            bot.reply_to(message, "❌ Вы не зарегистрированы. Напишите /start")
        else:
            balance = row[0]
            if balance >= price:
                # Обновляем баланс И ТИТУЛ
                cursor.execute(
                    "UPDATE users SET balance = ?, title = ? WHERE user_id = ?",
                    (balance - price, custom_title, str(message.from_user.id)),
                )
                conn.commit()
                bot.reply_to(
                    message,
                    f"✅ Успешно! Новый титул: {custom_title}. Списано: {price} монет.",
                )
            else:
                bot.reply_to(
                    message, f"❌ Недостаточно средств. У вас {balance}, нужно {price}."
                )
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ошибка базы данных: {e}")
    finally:
        conn.close()


@bot.message_handler(commands=["createpromo"])
def create_promo(message):

    if message.from_user.id != CREATOR_ID:
        return

    args = message.text.split()

    if len(args) < 4:
        bot.reply_to(message, "Использование:\n/createpromo КОД НАГРАДА КОЛИЧЕСТВО")
        return

    code = args[1].upper()

    try:
        reward = int(args[2])
        max_uses = int(args[3])
    except ValueError:
        bot.reply_to(message, "Неверные числа.")
        return

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO promos (code, reward, max_uses)
            VALUES (?, ?, ?)
            """,
            (code, reward, max_uses),
        )

        conn.commit()

        bot.reply_to(
            message,
            f"✅ Промокод создан:\n"
            f"🎟 Код: {code}\n"
            f"💰 Награда: {reward}\n"
            f"👥 Использований: {max_uses}",
        )

    except sqlite3.IntegrityError:
        bot.reply_to(message, "❌ Такой промокод уже существует.")

    conn.close()


@bot.message_handler(commands=["titles"])
def titles_command(message):
    uid = str(message.from_user.id)
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # Получаем титул пользователя из базы
    cursor.execute("SELECT title FROM users WHERE user_id = ?", (uid,))
    result = cursor.fetchone()
    conn.close()

    current_title = result[0] if result else "Игрок"

    bot.reply_to(
        message,
        f"🛒 Ваш текущий титул: «{current_title}»\n\n"
        f"Чтобы купить новый, используйте: /buytitle [Название]",
    )


def myid_command(message):
    bot.reply_to(message, f"🔍 Ваш Telegram ID: {message.from_user.id}")


@bot.message_handler(commands=["chats"])
def list_chats(message):
    if message.from_user.id != CREATOR_ID:
        return
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id, chat_title FROM groups")
    all_chats = cursor.fetchall()
    conn.close()
    if not all_chats:
        bot.reply_to(message, "📋 Список групп пуст.")
        return
    text = "📂 Список чатов, где добавлен бот:\n\n"
    for cid, ctitle in all_chats:
        text += f"▪️ {ctitle} (ID: {cid})\n"
    bot.reply_to(message, text, parse_mode='HTML')


@bot.message_handler(content_types=["new_chat_members"])
def on_bot_added(message):
    for mem in message.new_chat_members:
        if mem.id == bot.get_me().id:
            conn = sqlite3.connect("game_database.db")
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO groups (chat_id, chat_title) VALUES (?, ?)",
                (str(message.chat.id), message.chat.title),
            )
            conn.commit()
            conn.close()
            try:
                bot.send_message(CREATOR_ID, f"🔔 Меня добавили в чат: {
                    message.chat.title}\nID: {
                    message.chat.id}")
            except BaseException:
                pass


# Словарь для хранения активных дуэлей
# Формат: {id_второго_игрока: (id_первого_игрока, ставка)}
pending_duels = {}


@bot.message_handler(commands=["duel"])
def duel_command(message):
    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "⚠️ Использование: /duel @username [сумма]")
        return

    # Здесь упрощенно: считаем, что второй игрок в ответе на его сообщение
    if not message.reply_to_message:
        bot.reply_to(
            message, "⚠️ Нужно ответить на сообщение игрока, которого вызываете!"
        )
        return

    opponent_id = message.reply_to_message.from_user.id
    challenger_id = message.from_user.id
    bet = int(args[2])

    # Записываем вызов
    pending_duels[opponent_id] = (challenger_id, bet)
    bot.reply_to(
        message,
        f"⚔️ Вызов отправлен! Игрок должен ответить /accept, чтобы принять дуэль на {bet} монет.",
    )


@bot.message_handler(commands=["accept"])
def accept_duel(message):
    opponent_id = message.from_user.id
    if opponent_id not in pending_duels:
        bot.reply_to(message, "❌ Нет активных вызовов для вас.")
        return

    challenger_id, bet = pending_duels.pop(opponent_id)

    # Случайный победитель
    winner = random.choice([challenger_id, opponent_id])

    # Получаем имя победителя
    try:
        member = bot.get_chat_member(message.chat.id, winner)
        winner_name = member.user.first_name
    except BaseException:
        winner_name = f"Игрок с ID {winner}"

    # Тут должна быть ваша логика обновления БД (update balance...)

    bot.reply_to(message, f"🏆 Победитель дуэли: {winner_name}! Он забирает {
        bet *
        2} монет!")


@bot.message_handler(commands=["givemoney"])
def give_money(message):
    sender_id = message.from_user.id

    # Проверка: является ли пользователь админом/создателем вообще
    if not is_user_admin(sender_id):
        bot.reply_to(message, "❌ Вы не являетесь Администратором бота.")
        return

    target_id = None
    amount = 0
    args = message.text.split()

    # 1. Сценарий через Reply (ответ на сообщение)
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        if len(args) < 2:
            bot.reply_to(
                message, "⚠️ Использование в ответ на сообщение: /givemoney [сумма]"
            )
            return
        try:
            amount = int(args[1])
        except ValueError:
            bot.reply_to(message, "⚠️ Сумма должна быть числом!")
            return
    # 2. Сценарий по ID текстом
    else:
        if len(args) < 3:
            bot.reply_to(
                message,
                "⚠️ Использование: /givemoney [ID] [сумма] или ответом на сообщение: /givemoney [сумма]",
            )
            return
        target_id = args[1]
        try:
            amount = int(args[2])
        except ValueError:
            bot.reply_to(message, "⚠️ Сумма должна быть числом!")
            return

    # ОГРАНИЧЕНИЕ ДЛЯ АДМИНОВ: Если это не Создатель, то он может выдать
    # деньги ТОЛЬКО самому себе
    if int(sender_id) != CREATOR_ID and str(target_id) != str(sender_id):
        bot.reply_to(
            message,
            "❌ Как администратор, вы можете выдавать монеты только самому себе! Игрокам выдавать запрещено.",
        )
        return

    check_and_register_user(target_id, "Игрок")

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (str(target_id),))
    balance = cursor.fetchone()[0]

    new_balance = balance + amount
    cursor.execute(
        "UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, str(target_id))
    )
    conn.commit()
    conn.close()

    bot.reply_to(
        message, f"✅ Успешно выдано {amount} монет пользователю (ID: {target_id})."
    )


@bot.message_handler(commands=["admins"])
def admins_command(message):
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()

    # Запрашиваем из базы всех, у кого роль НЕ "Игрок"
    cursor.execute("SELECT user_id, username, role FROM users WHERE role != 'Игрок'")
    admins = cursor.fetchall()
    conn.close()

    if not admins:
        bot.reply_to(message, "👑 На данный момент администраторов нет.")
        return

    text = "👑 Список администрации:\n\n"
    for u_id, u_name, u_role in admins:
        # Показываем имя из базы или ID, если имя "Игрок"
        display = u_name if u_name != "Игрок" else f"ID {u_id}"
        text += f"🔹 {display} — {u_role}\n"

    bot.reply_to(message, text, parse_mode='HTML')


@bot.message_handler(commands=["roulette"])
def roulette_command(message):
    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(
            message,
            "⚠️ Использование: /roulette [ставка] [цвет: red/black/green]\nПример: /roulette 100 red",
        )
        return

    try:
        bet = int(args[1])
        color_bet = args[2].lower()
    except ValueError:
        bot.reply_to(message, "⚠️ Ставка должна быть числом!")
        return

    if color_bet not in ["red", "black", "green"]:
        bot.reply_to(message, "⚠️ Цвет должен быть: red, black или green.")
        return

    user_id = message.from_user.id

    # Подключение к БД
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (str(user_id),))
    row = cursor.fetchone()

    if not row or row[0] < bet:
        bot.reply_to(message, "❌ Недостаточно средств!")
        conn.close()
        return

    balance = row[0]

    # Логика рулетки
    # 0-46: Red, 47-93: Black, 94-99: Green (Зеленый выпадает редко)
    roll = random.randint(0, 99)
    if roll < 47:
        winner_color = "red"
    elif roll < 94:
        winner_color = "black"
    else:
        winner_color = "green"

    # Расчет результата
    if color_bet == winner_color:
        if winner_color == "green":
            win_amount = bet * 10
        else:
            win_amount = bet * 2

        new_balance = balance + win_amount - bet
        result_text = f"🎉 Выпало: {
            winner_color.upper()}! Вы выиграли {win_amount} монет!"
    else:
        new_balance = balance - bet
        result_text = f"😔 Выпало: {
            winner_color.upper()}. Вы проиграли {bet} монет."

    cursor.execute(
        "UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, str(user_id))
    )
    conn.commit()
    conn.close()

    bot.reply_to(
        message, f"🎰 РУЛЕТКА 🎰\n\n{result_text}\n💰 Ваш баланс: {new_balance}"
    )


@bot.message_handler(commands=["whoami"])
def whoami_command(message):
    user_id = message.from_user.id
    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, role, balance FROM users WHERE user_id = ?", (str(user_id),)
    )
    data = cursor.fetchone()
    conn.close()

    if data:
        name, role, bal = data
        bot.reply_to(
            message,
            f"👤 Ваш ID: {user_id}\n📝 Имя в базе: {name}\n👑 Роль: {role}\n💰 Баланс: {bal}",
        )
    else:
        bot.reply_to(message, "⚠️ Вы еще не зарегистрированы в базе.")


@bot.message_handler(commands=["start"])
def start_command(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Если это группа, проверяем статус того, кто написал /start
    if message.chat.type in ["group", "supergroup"]:
        try:
            member_status = bot.get_chat_member(chat_id, user_id).status
            # Если это создатель (creator) или администратор (administrator)
            # группы
            if member_status in ["creator", "administrator"]:
                # Присваиваем ему роль "Админ" в базе, если у него еще нет прав
                conn = sqlite3.connect("game_database.db")
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET role = ? WHERE user_id = ?",
                    ("Админ", str(user_id)),
                )
                conn.commit()
                conn.close()
        except BaseException:
            pass  # Если бот не может получить статус

    # Дальше идет ваш стандартный код регистрации пользователя...
    log_group_activity(message)
    # ... и вывод сообщения


@bot.message_handler(commands=["takemoney"])
def take_money(message):
    MY_OWN_ID = 5633124867

    if message.from_user.id != MY_OWN_ID:
        bot.reply_to(message, "❌ Вы не являетесь Администратором бота.")
        return

    args = message.text.split()

    # Логика определения ID и суммы
    if message.reply_to_message:
        target_id = message.reply_to_message.from_user.id
        try:
            amount = int(args[1])
        except (ValueError, IndexError):
            bot.reply_to(message, "⚠️ Использование: /takemoney [сумма]")
            return
    else:
        if len(args) < 3:
            bot.reply_to(message, "⚠️ Использование: /takemoney [ID] [сумма]")
            return
        target_id = args[1]
        try:
            amount = int(args[2])
        except ValueError:
            bot.reply_to(message, "⚠️ Сумма должна быть числом!")
            return

    conn = sqlite3.connect("game_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (str(target_id),))
    row = cursor.fetchone()

    if row:
        balance = row[0]
        new_balance = max(0, balance - amount)  # Чтобы баланс не ушел в минус
        cursor.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            (new_balance, str(target_id)),
        )
        conn.commit()
        bot.reply_to(
            message,
            f"✅ Успешно изъято {amount} монет у ID {target_id}. Остаток: {new_balance}",
        )
    else:
        bot.reply_to(message, "❌ Пользователь не найден в базе.")
    conn.close()
@bot.message_handler(func=lambda message: True)
def handle_bad_words(message):

    # Только группы
    if message.chat.type not in ["group", "supergroup"]:
        return

    # Если текста нет
    if not message.text:
        return

    user_id = message.from_user.id

    if user_id == CREATOR_ID:
        return

    text = normalize_text(message.text)

    found = False

    for word in bad_words:

        if word in text:
            found = True
            break

    if not found:
        return

    # Удаляем сообщение
    try:
        bot.delete_message(
            message.chat.id,
            message.message_id
        )
    except:
        pass

    # Если пользователя нет в warnings
    if user_id not in warnings:
        warnings[user_id] = 0

    warnings[user_id] += 1

    warns = warnings[user_id]

    # Красивое имя
    if message.from_user.username:
        user = f"@{message.from_user.username}"
    else:
        user = message.from_user.first_name

    # МУТ ПОСЛЕ 3 ПРЕДУПРЕЖДЕНИЙ
    if warns >= 4:

        try:

            bot.restrict_chat_member(
                message.chat.id,
                user_id,
                until_date=int(time.time()) + 600,
                can_send_messages=False
            )

            bot.send_message(
                message.chat.id,
                f"🔇 {user} получил мут на 10 минут за оскорбления."
            )

        except:
            bot.send_message(
                message.chat.id,
                f"❌ Не удалось выдать мут {user}.\n"
                f"Проверь права бота."
            )

        # Сброс предупреждений
        warnings[user_id] = 0

    else:

        bot.send_message(
            message.chat.id,
            f"⚠️ {user}\n"
            f"Предупреждение {warns}/3\n"
            f"Не используйте оскорбления."
        )
bot.add_custom_filter(
    telebot.custom_filters.StateFilter(bot)
)
# Обязательно добавьте этот запуск в самый конец файла!
def run_flask():
    # Render ОБЯЗАТЕЛЬНО требует порт из переменной окружения
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Запускаем Flask всегда
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # ЗАПУСКАЕМ БОТА ТОЛЬКО ЕСЛИ ЭТО НЕ RENDER
    # Проверяем, есть ли переменная RENDER (Render её ставит автоматически)
    if not os.environ.get("RENDER"):
        print("Запуск бота в локальном режиме...")
        bot.infinity_polling()
    else:
        print("Работаем в режиме сервера (бот отключен для Render)...")
        # Чтобы скрипт не вылетал на Render, добавим бесконечный цикл
        import time
        while True:
            time.sleep(60)
