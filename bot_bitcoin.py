import ssl
import json

import websocket
import bitstamp.client


def cliente():
    return bitstamp.client.Trading(username = credentials.USERNAME,
                                   key = credentials.KEY,
                                   secret = credentials.KEY)


def comprar(valor):
    trading_client = cliente()
    trading_client.buy_market_order(valor)

def vender(valor):
    trading_client = cliente()
    trading_client.sell_market_order(valor)

def on_open(ws):
    print('## OPEN ##')

    json_subscribe = '''
    {
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}'''
    ws.send(json_subscribe)

def on_close(ws, close_status_code, close_msg):
    print('## CLOSED ##')

def on_error(ws, error):
    print('## ERROR ##')

def on_message(ws, message):
    message = json.loads(message)
    price = message['data']['price']
    print(f'PRICE: {price}')

    if price > 32000:
        vender()
    elif price < 30000:
        comprar()
    else:
        print('Aguardar')


if __name__ == '__main__':
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.",
                                on_open=on_open,
                                on_close=on_close,
                                on_error=on_error,
                                on_message=on_message)

    ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})