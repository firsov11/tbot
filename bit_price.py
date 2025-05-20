import network
import urequests

def get_bitcoin_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = urequests.get(url)
        data = response.json()  # Преобразуем JSON-ответ в Python-словарь
        price = data["bitcoin"]["usd"]  # Извлекаем цену биткоина в долларах США
        return f"Курс биткоина: ${price}"
    except Exception as e:
        return f"Ошибка при получении курса биткоина: {str(e)}"