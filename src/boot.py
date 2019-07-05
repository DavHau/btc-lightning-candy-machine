import webrepl
from settings import wifi_network, wifi_password


def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(wifi_network, wifi_password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def set_time():
    from ntptime import settime
    while True:
        try:
            settime()
            break
        except Exception:
            pass


do_connect()
set_time()
webrepl.start()
