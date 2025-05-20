from machine import Pin, UART
import time
from ld2410 import LD2410
from utelegram import Bot
from wifi_connection import connect_wifi
from led_control import tripl_led
from time_utils import get_current_time
from bit_price import get_bitcoin_price
from command_handler import running_command

TOKEN = "7095069397:AAFBxROL6uzzWupQxBmqhV60nLfHUbqA5VY"
# Инициализация встроенного светодиода
led = Pin(22, Pin.OUT)
# Инициализация бота
bot = Bot(TOKEN)

# Инициализация UART
uart = UART(2, baudrate=256000, tx=17, rx=16, timeout=10)

# Инициализация датчика
sensor = LD2410(uart)

sensor.set_max_values(8, 8, 1500)

# Добавляем обработчики команд
@bot.add_command_handler('on')
def handle_on(update):
    led.value(0)  # Включаем светодиод
    update.reply("Светодиод включен!")
    print("Светодиод включен!")


@bot.add_command_handler('off')
def handle_off(update):
    led.value(1)  # Выключаем светодиод
    update.reply("Светодиод выключен!")
    print("Светодиод выключен!")


@bot.add_command_handler('time')
def handle_time(update):
    current_time = get_current_time()
    update.reply(f"Текущее время: {current_time}")
    print(f"Текущее время: {current_time}")


@bot.add_command_handler('bitcoin')
def handle_bitcoin(update):
    bitcoin_price = get_bitcoin_price()
    update.reply(bitcoin_price)
    print(bitcoin_price)


@bot.add_command_handler('help')
def handle_help(update):
    update.reply("Помоги себе сам")
    print("Команда /help вызвана.")


@bot.add_message_handler(r'.*')  # Будет срабатывать на любое сообщение
def handle_message(update):
    print('USER - ' + repr(update.message['from']['id']))
    text = update.message['text']
    update.reply(f"Вы написали: {text}")


@bot.add_command_handler('start')
def handle_start(update):
    print("Команда старт")
    # Отправляем сообщение с клавиатурой
    id = update.message['chat']['id']
    name = update.message['from']['first_name']
    bot.send_message(id, f"Привет, {name}! Используйте Меню!")
    print("Клавиатура отправлена!")
    print(update.message['from'])

@bot.add_command_handler('status')
def handle_status(update):
    print("Команда /status получена.")
    try:
        chat_id = update.message['chat']['id']
        bot.send_message(chat_id, "Датчик работает!")
        print("Ответ отправлен!")
    except Exception as e:
        print("Ошибка при ответе на /status:", e)


@bot.add_command_handler('radar')
def handle_radar(update):
    print("Команда /radar получена.")

    try:
        sensor.update()  # обязательно обновляем перед чтением
        target_data = sensor.get_target_data()
        print("Target data:", target_data)

        if target_data and isinstance(target_data, tuple) and len(target_data) == 6:
            target_state = target_data[0]
            detection_distance = target_data[1]
            move_distance = target_data[2]

            if target_state == 1:
                message = (
                    f"Обнаружено движение!\n"
                    f"Дистанция: {detection_distance / 100:.2f} м\n"
                    f"Движение: {move_distance / 100:.2f} м"
                )
            else:
                message = "Движения не обнаружено."

        else:
            message = "Нет данных от радара."

        update.reply(message)
        print("Ответ отправлен в Telegram.")

    except Exception as e:
        print("Ошибка в radar handler:", e)
        update.reply("Произошла ошибка при чтении с радара.")


def start():
    print("Программа запущена!")

    bot_running = False
    wlan = connect_wifi()  # Получаем объект wlan после подключения

    while True:
        if not wlan:
            print("Подключение потеряно, пытаемся снова...")
            wlan = connect_wifi()  # Попытаться подключиться снова, если Wi-Fi не подключен

        if wlan and not bot_running:
            print("Запуск бота...")
            try:
                # Запускаем бота в отдельном потоке
                bot_running = True
                bot.start_loop(tripl_led())
            except Exception as e:
                print(f"Ошибка работы бота: {e}")
                bot_running = False

        running_command()

        time.sleep(3)


start()
