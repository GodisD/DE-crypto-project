import sys
import os 
from binance import ThreadedWebsocketManager
from binance.client import Client
from pymongo import MongoClient

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
MONGO_USER = os.get_env('MONGO_HOSTNAME')



class BinanceListener:

    def __init__(self) -> None:
        self.streams = []
        self.symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'BNBUSDT']
        self.client = Client(API_KEY, API_SECRET)
        self.mongo_client = MongoClient(f'mongodb://mongodb-697b6f857c-fwnhn.mongodb:27017')
        # mongo_client = MongoClient(f'mongodb://crypto:mongopass220694@localhost:27017/cryptodb')

        try: 
            self.mongo_client.list_databases()
        except Exception:
            raise Exception('The connection to db wasnt established... Quiting!')

        try: 
            self.client.ping()
        except Exception:
            raise Exception('The connection to binance wasnt established... Quiting!')


    def create_streams(self):
        for symbol in self.symbols:
            self.streams.extend([f'{symbol.lower()}@trade', f'{symbol.lower()}@kline_1m', f'{symbol.lower()}@depth20'])
        
        print(self.streams)


    def _handle_socket_message(self, msg):
        stream = msg['stream']
        symbol = stream.split('@')[0]
        
        db = self.mongo_client["spot"]
        col = db[f'{symbol}_{stream}']
        col.insert_one(msg)
        print('inserted spot')


    def _handle_futures_socket_message(self, msg):
        stream = msg['stream']
        symbol = stream.split('@')[0]
        
        db = self.mongo_client["futures"]
        col = db[f'{symbol}_{stream}']
        col.insert_one(msg)
        print('inserted futures')
    
    def main(self):

        self.twm = ThreadedWebsocketManager(api_key=API_KEY, api_secret=API_SECRET)
        self.twm.start()

        self.twm.start_multiplex_socket(streams = self.streams, callback=self._handle_socket_message)
        self.twm.start_futures_multiplex_socket(streams=self.streams, callback=self._handle_futures_socket_message)

        self.twm.join()


if __name__ == "__main__":
   

   bl = BinanceListener()
   bl.create_streams()

   bl.main()
