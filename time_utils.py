import ntptime
import time

def get_current_time():
    try:
        # Получаем время с NTP-сервера
        ntptime.settime()  # Устанавливает системное время с NTP-сервера
        current_time = time.localtime()  # Получаем текущее время
        formatted_time = "{:02}:{:02}:{:02}".format(current_time[3], current_time[4], current_time[5])
        return formatted_time
    except Exception as e:
        return f"Ошибка при получении времени: {str(e)}"
