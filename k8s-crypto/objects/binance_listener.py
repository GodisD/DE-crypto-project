import sys
from credentials import API_KEY, API_SECRET, MONGO_USER, MONGO_PASSWORD
from binance import ThreadedWebsocketManager
from binance.client import Client
from pymongo import MongoClient



class BinanceListener:

    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.client = Client(API_KEY, API_SECRET)
        self.mongo_client = MongoClient(f'mongodb://localhost:27017')
        self.db = self.mongo_client[f'landing_sockets_{self.symbol}']

        for db in self.mongo_client.list_databases():
            print(db)

    def handle_socket_message(self, msg):
        # print(msg)
        col = self.db['book_depth']
        res = col.insert_one(msg)
        print(res)


    def handle_futures_socket_message(self, msg):
        col = self.db['bookTickerFutures']
        res = col.insert_one(msg)
        print("Arroz",res)
    
    def main(self):


        self.twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=API_SECRET)
        self.twm.start()

        self.twm.start_depth_socket(symbol = self.symbol, callback=self.handle_socket_message)
        self.twm.start_futures_multiplex_socket(streams=[f"{self.symbol.lower()}@bookTicker"], callback=self.handle_futures_socket_message)


        self.twm.join()


if __name__ == "__main__":
   

   bl = BinanceListener(sys.argv[1])

   print(bl.mongo_client.list_database_names())
   
   print(f"Listening for symbol {bl.symbol}..")
   bl.main()
