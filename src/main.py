from time import sleep

import display as dp
from machine import Pin

from .opennode import LightningInvoice

price_sat = 100
candy_pin = Pin(10, Pin.OUT)
candy_pin.off()

display = dp.PaperDisplay2()


def new_invoice():
    invoice = LightningInvoice.gen_invoice(price_sat)
    print('New invoice created:')
    print(invoice.__dict__)
    qr_code = dp.gen_qr(invoice.payreq)
    display.set_matrix(qr_code)
    display.show()
    return invoice


def give_candy():
    candy_pin.on()
    sleep(1)
    candy_pin.off()


def main():
    ln_invoice = new_invoice()
    while True:
        sleep(0.2)
        if ln_invoice.paid:
            print('CAAANDDYYYYY!!!!!!')
            give_candy()
            display.clear(True)
            ln_invoice = new_invoice()
            continue
        if ln_invoice.expired:
            ln_invoice = new_invoice()


main()
