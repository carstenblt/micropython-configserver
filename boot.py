import gc
import webrepl
import network
import wifi_database
import time
gc.collect()

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)

for wifi in wifi_database.iter_wifis():
    sta_if.connect(wifi[0], wifi[1])
    for i in range(50):
        time.sleep_ms(100)
        if sta_if.isconnected():
            wifi_database.active_wifi = wifi[0]
            break
    if wifi_database.active_wifi is not None:
       	break
if wifi_database.active_wifi is None:
    sta_if.active(False)

webrepl.start()
gc.collect()