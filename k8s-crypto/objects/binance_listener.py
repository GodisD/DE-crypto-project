import sys
from credentials import API_KEY, API_SECRET, MONGO_USER, MONGO_PASSWORD
from binance import ThreadedWebsocketManager
from binance.client import Client
from pymongo import MongoClient



class BinanceListener:

    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.client = Client(API_KEY, API_SECRET)
        self.mongo_client = MongoClient(f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@127.0.0.1:27017/admin')
        self.db = self.mongo_client[f'landing_sockets_{self.symbol}']

    def handle_socket_message(self, msg, socket):
        print(msg)
        col = self.db[socket]
        col.insert_one(msg)
    
    def main(self):

        status = self.client.get_system_status()
        print(status)

        info = self.client.get_exchange_info()
        print(info)

        self.twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=API_SECRET)
        self.twm.start()

        self.twm.start_depth_socket(symbol = self.symbol, callback=self.handle_socket_message(socket = 'depth_socket'))

        self.twm.join()


if __name__ == "__main__":
   

   bl = BinanceListener(sys.argv[1])

   print(bl.mongo_client.list_database_names())
   
   print(f"Listening for symbol {bl.symbol}..")
   bl.main()
