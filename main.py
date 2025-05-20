import bluetooth
from machine import Pin
import time
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

# Инициализация BLE
ble = bluetooth.BLE()
ble.active(True)

SERVICE_UUID = bluetooth.UUID(0x1234)  # Уникальный UUID сервиса

# Функция для обработки найденных устройств
def scan_callback(addr_type, addr, adv_data):
    print("Найдено устройство:", addr)
    # Преобразуем рекламные данные в строку и ищем нужный UUID
    adv_data_str = ''.join([chr(i) for i in adv_data])
    if str(SERVICE_UUID) in adv_data_str:
        print(f"Найдено устройство с нужным UUID: {addr}")

# Функция для старта сканирования
def start_scan():
    print("Начало сканирования...")
    ble.gap_scan(2000, 30000, 30000)  # Сканирование 2 секунды
    # Подключаем callback для обработки результатов сканирования
    ble.gap_scan_cb(scan_callback)

# Подключение к устройству
def connect_to_device(addr):
    print(f"Подключаемся к {addr}...")
    ble.gap_connect(addr)


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

        start_scan()

        time.sleep(5)  # Пауза между попытками подключения


start()
