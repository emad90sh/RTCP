import asyncio
import websockets
import time
import json
import get_token
import get_random_uid
import traceback, sys
import redis


r = redis.Redis()
async def main():
    #defind values
    uid = get_random_uid.random_uid()
    ping_msg = {
        f"id":"{uid}",
        "type":"ping"
    }
    subscribe_msg = {
        "id": uid,                         
        "type": "subscribe",
        "topic": "/market/ticker:BTC-USDT,ETH-USDT",
        "privateChannel": False,           
        "response": True
    }
    unsubscribe_msg = {
        "id": uid,                         
        "type": "unsubscribe",
        "topic": "/market/ticker:BTC-USDT,ETH-USDT",
        "privateChannel": False,           
        "response": True
    }
    btc_price = ""
    eth_price = ""
    last_btc_price = ""
    last_eth_price = ""

    #get token and endpoint address for public channel
    token, endpoint = get_token.get_es_info()

    async with websockets.connect(f'{endpoint}/?token={token}&[connectId={uid}]') as websocket:
        #try to established connection
        while True:
            response = await websocket.recv()
            if json.loads(response)['type'] == "welcome":
                print("Connected")
                break
            else:
                print("cannot established connection \nwait for 3 seconds to try again")
                time.sleep(3)
        await websocket.send(json.dumps(subscribe_msg))

        start_time = time.time()
        # get updated prices
        while True:
            try:
                response_prices = await websocket.recv()
                json_res_price = json.loads(response_prices)
                if "topic" in json_res_price:
                    symbol_topic = json_res_price['topic']
                    if "BTC" in symbol_topic:
                        btc_price = json_res_price['data']['price']
                    elif "ETH" in symbol_topic:
                        eth_price = json_res_price['data']['price']
                if last_btc_price != btc_price:
                    #print(f"BTC = {btc_price}")
                    r.mset({"btc_price": str(btc_price)})
                    last_btc_price = btc_price
                if last_eth_price != eth_price:
                    #print(f"ETH = {eth_price}")
                    r.mset({"eth_price": str(eth_price)})
                    last_eth_price = eth_price

                # send ping message to keep alive connection every 1 minutes
                current_time = time.time()
                if current_time - start_time >= 60.0:
                    await websocket.send(json.dumps(ping_msg))
                    start_time = current_time

                time.sleep(0.01)
            except Exception:
                print(traceback.format_exc())


asyncio.get_event_loop().run_until_complete(main())
