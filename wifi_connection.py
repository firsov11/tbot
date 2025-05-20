import network
import time
import ntptime

def connect_wifi(wifi_ssid="POCO", wifi_password="33331111"):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  time.sleep(1)
  result = wlan.scan()
  print(result)
  print("Try to connect to Wi-Fi...")
  try:
    wlan.connect(wifi_ssid, wifi_password)
    for _ in range(10):
      time.sleep(1)
      if wlan.isconnected():
        break
    if wlan.isconnected():
      ssid = wlan.config('ssid')
      print(f"Connected to: {ssid}")
      print(f"Connected! IP: {wlan.ifconfig()[0]}")
      ntptime.settime()
      return wlan
    else:
      print("Don`t connect to Wi-Fi! " + str(wlan.status()))
      wlan.disconnect()
      return None
  except Exception as e:
    print(f"Error connection: {e}")
    return None