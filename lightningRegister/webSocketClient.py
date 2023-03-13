import ssl
import websocket
from data.data import polygon
from dataExtraction import ExtractData

def on_message(ws, message):
    print("procesando mensaje")
    ExtractData(message, polygon)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    #print(ws, close_status_code, close_msg)
    print("Conexión cerrada")

def on_open(ws):
    print("Conexión abierta")
    ws.send("Hola, servidor!")

if __name__ == "__main__":
    websocket.enableTrace(True)
    print("iniciando conexión")
    ws = websocket.WebSocketApp("wss://test.dtect.africa/ws/lightning/fritz",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()