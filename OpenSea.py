import datetime
import json
import math
import time
# import js2py
import requests
import os
from dotenv import load_dotenv


class OpenSea:
    def __init__(self):
        load_dotenv()
        self.request_delay = 3
        self.api_keys = {
            "opensea": os.environ.get("OPENSEA_API_KEY")
        }
        self.endpoints = {
            "assets": "https://api.opensea.io/api/v1/assets",
            "events": "https://api.opensea.io/api/v1/events",
            "orders": "https://api.opensea.io/wyvern/v1/orders",
            "collection": "https://api.opensea.io/collection/",
            "collections": "https://api.opensea.io/collections/",
            "events": "https://api.opensea.io/api/v1/events"
        }
        self.api_limits = {
            "events": 300,
            "assets": 50
        }
        self.param_names = {
            "assets": [
                "limit",
                "offset",
                "token_ids",
                "image_url",
                "background_color",
                "name",
                "external_link",
                "asset_contract_address",
                "owner",
                "traits",
                "last_sale",
            ],
            "events": [
                "asset_contract_address",
                "collection_slug",
                "token_id",
                "account_address",
                "event_type",
                "only_opensea",
                "auction_type",
                "offset",
                "limit",
                "occurred_before",
                "occurred_after"
            ],
            "collections": [
                "limit",
            ]
        }
        self.request_headers = {
            "Accept": "application/json",
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _build_request_params(self, _params, request_type):
        # build request params
        params = {}
        for i, _param in enumerate(_params):
            # if the param was passed
            if _param:
                params[self.param_names[request_type][i]] = _param
        return params

    def get_assets(self, limit, offset="", token_ids="", image_url="", background_color="", name="", external_link="",
                   asset_contract="", owner="", traits="", last_sale=""):

        _params = [limit, offset, token_ids, image_url, background_color, name, external_link, asset_contract, owner,
                   traits, last_sale]
        # build request params and headers
        # build request params
        params = self._build_request_params(_params, "assets")
        headers = self.request_headers
        headers["X-API-KEY"] = self.api_keys["opensea"]

        # 50 is api limit
        apilimit = self.api_limits["assets"]
        _num_loops = int(math.ceil(limit / apilimit))
        assets = []
        for loop in range(1, _num_loops + 1):
            params['offset'] = loop * apilimit
            # set limit
            if limit - ((loop - 1) * apilimit) > apilimit:
                params['limit'] = apilimit
            else:
                params['limit'] = int(limit - ((loop - 1) * apilimit))
            # submit request to the OpenSea api
            response = requests.request("GET", self.endpoints["assets"], params=params, headers=headers)
            # if response OK
            if response.status_code == 200:
                response = json.loads(response.text)
                for asset in response['assets']:
                    assets.append(Asset(asset))
            else:
                raise Exception(
                    "[Error] request returned code {} with reason {}".format(response.status_code, response.reason))
            if loop < _num_loops + 1:
                time.sleep(3)
        return assets

    def get_collection(self, name):
        # create request url
        url = self.endpoints["collection"] + str(name)
        # submit request to the OpenSea api
        response = requests.request("GET", url)
        if response.status_code == 200:
            response = json.loads(response.text)
            return Collection(response['collection'])
        raise Exception(
            "[Error] request returned code {} with reason {}".format(response.status_code, response.reason))

    def get_collections(self, limit=300):
        # create request url
        url = self.endpoints["collections"]
        _params = [limit]
        # build request params and headers
        params = self._build_request_params(_params, "collections")
        headers = self.request_headers
        headers["X-API-KEY"] = self.api_keys["opensea"]
        # submit request to the OpenSea api
        response = requests.request("GET", self.endpoints['collections'], params=params, headers=headers)
        if response.status_code == 200:
            response = json.loads(response.text)
            c = []
            for collection in response['collections']:
                c.append(Collection(collection))
            return c
        raise Exception(
            "[Error] request returned code {} with reason {}".format(response.status_code, response.reason))

    def get_events(self, limit, asset_contract_address="", collection_slug="", token_id="", account_address="",
                   event_type="",
                   only_opensea="", auction_type="", offset="", occurred_before="", occurred_after=""):
        _params = [asset_contract_address, collection_slug, token_id, account_address, event_type, only_opensea,
                   auction_type, offset, limit, occurred_before, occurred_after]

        # build request params and headers
        params = self._build_request_params(_params, "events")
        headers = self.request_headers
        headers["X-API-KEY"] = self.api_keys["opensea"]

        # 300 is api limit
        apilimit = self.api_limits["events"]
        _num_loops = int(math.ceil(limit / apilimit))
        events = []
        for loop in range(1, _num_loops+1):
            params['offset'] = loop * apilimit
            # set limit
            if limit - ((loop-1) * apilimit) > apilimit:
                params['limit'] = apilimit
            else:
                params['limit'] = int(limit - ((loop-1) * apilimit))
            # submit request to the OpenSea api
            response = requests.request("GET", self.endpoints["events"], params=params, headers=headers)
            # if response OK
            # print(response.text)
            if response.status_code == 200:
                response = json.loads(response.text)
                for event in response['asset_events']:
                    events.append(Event(event))
            else:
                raise Exception(
                    "[Error] request returned code {} with reason {}".format(response.status_code, response.reason))
            if loop < _num_loops+1:
                time.sleep(3)
        return events



class Asset:
    def __init__(self, jsonData):
        self.js = {
            'buy':
                """
                            import * as Web3 from 'web3'
                            import {{ OpenSeaPort, Network }} from 'opensea-js'
        
                            // This example provider won't let you make transactions, only read-only calls:
                            const provider = new Web3.providers.HttpProvider('https://mainnet.infura.io')
        
                            const seaport = new OpenSeaPort(provider, {{
                              networkName: Network.Main,
                              // apiKey: YOUR_API_KEY
                            }})
                            const order = await seaport.api.getOrder({{ side:
                                OrderSide.Sell,
                                asset_contract_address: "{}"}},
                                token_id: {}}}
                                }})
                            const accountAddress = "{}"}} // The buyer's wallet address, also the taker
                            const transactionHash = await this.props.seaport.fulfillOrder({{ order, accountAddress }})
                            function getTransactionHash(transactionHash){{
                                return transactionHash
                            }}
                            getTransactionHash(transactionHash)
                """
        }
        self.jsonData = jsonData
        self.token_id = None
        if 'token_id' in jsonData:
            self.token_id = jsonData['token_id']
        self.name = jsonData['name']

        if jsonData['sell_orders']:
            self.current_price = jsonData['sell_orders'][0]['current_price']
        else:
            self.current_price = None

        self.ERC721address = None
        if jsonData["asset_contract"]["asset_contract_type"] == "non-fungible":
            self.ERC721address = jsonData["asset_contract"]["address"]

    # def buy(self, buyer_address):
    #     buyOrder = self.js['buy'].format(self.ERC721address, self.token_id, buyer_address)
    #     order = js2py.eval_js6(buyOrder)
    #     return order


class Collection:
    def __init__(self, jsonData):
        self.jsonData = jsonData

        self.events = None
        self.event_dates = None

        for contract in jsonData['primary_asset_contracts']:
            if contract["asset_contract_type"] == "non-fungible":
                self.ERC721Address = contract["address"]
                self.events = self.get_event_data()
                self.get_event_data()

        print(self.jsonData)
        self.stats = jsonData['stats']
        print('got here')

        # get stats
        self.floorPrice = (self.stats['floor_price'])
        self.marketCap = (self.stats['market_cap'])
        self.numReports = (self.stats['num_reports'])
        self.averagePrice = (self.stats['average_price'])
        self.numOwners = (self.stats['num_owners'])
        self.count = (self.stats['count'])
        self.totalSupply = (self.stats['total_supply'])
        self.totalSales = (self.stats['total_sales'])
        self.totalVolume = (self.stats['total_volume'])
        self.thirtyDayAvgPrice = (self.stats['thirty_day_average_price'])
        self.thirtyDaySales = (self.stats['thirty_day_sales'])
        self.thirtyDayChange = (self.stats['thirty_day_change'])
        self.thirtyDayVolume = (self.stats['thirty_day_volume'])
        self.sevenDayAvgPrice = (self.stats['seven_day_average_price'])
        self.sevenDaySales = (self.stats['seven_day_sales'])
        self.sevenDayChange = (self.stats['seven_day_change'])
        self.sevenDayVolume = (self.stats['seven_day_volume'])
        self.oneDayAvgPrice = (self.stats['one_day_average_price'])
        self.oneDaySales = (self.stats['one_day_sales'])
        self.oneDayChange = (self.stats['one_day_change'])
        self.oneDayVolume = (self.stats['one_day_volume'])

        # get other important data
        self.image = (self.jsonData['image_url'])
        # collection pic url

        for contract in jsonData['primary_asset_contracts']:
            if contract["asset_contract_type"] == "non-fungible":
                self.ERC721Address = contract["address"]
                self.events = self.get_event_data()
                self.event_dates = [datetime.datetime.strptime(event.created_date, "%Y-%m-%dT%H:%M:%S.%f") for event in self.events]
                self.assets = self.get_asset_data()

    def get_event_data(self):
        with OpenSea() as oS:
            events = oS.get_events(300, asset_contract_address=self.ERC721Address, event_type="successful")
            return events

    def get_asset_data(self):
        with OpenSea() as oS:
            assets = oS.get_assets(50, asset_contract=self.ERC721Address)
            return assets


class Event:
    def __init__(self, jsonData):
        self.jsonData = jsonData
        self.token_id = None
        self.ERC721address = None
        self.name = None

        if jsonData['asset'] is not None:
            if 'token_id' in jsonData['asset']:
                self.token_id = jsonData['asset']['token_id']
            self.name = jsonData['asset']['name']
            if jsonData["asset"]["asset_contract"]["asset_contract_type"] == "non-fungible":
                self.ERC721address = jsonData["asset"]["asset_contract"]["address"]
        self.created_date = jsonData['created_date']
        self.is_private = jsonData['is_private']
        self.payment_token = jsonData['payment_token']
        self.total_price = jsonData['total_price']
        self.event_type = jsonData['event_type']

