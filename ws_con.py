from websocket import create_connection
import websocket
import json

server='ws://cnadashboard.sq2.cards/ws'

# ws = create_connection(server)
# print("Sending 'Hello, World'...")
# for i in range(10000):
#     ws.send(b"Hello, World")
#     print("Sent")
# print("Reeiving...")
# result = ws.recv()
# print("Received '%s'" % result)
# ws.close()

def connect_server(num):
	ws = create_connection(server)
	print ("Sending 'Hello, World'...")
	ws.send("Hello, World")
	lst=[]
	for i in range(num):
		result = ws.recv()
		lst.append(json.loads(result))
		print ("Received '%s'" % result)
	ws.close()
	return lst



def on_message(ws, message):
	print ("{}".format(message))

def on_error(ws, error):
	print ("{}".format(error))

def on_close(ws):
    print ("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print ("thread terminating...")
    # thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(server,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
