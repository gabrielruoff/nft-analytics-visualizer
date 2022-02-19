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
        # build request params
        params = self._build_request_params(_params, "assets")

        # submit request to the OpenSea api
        response = requests.request("GET", self.endpoints["assets"], params=params)
        # if response OK
        if response.status_code == 200:
            response = json.loads(response.text)
            assets = []
            for asset in response['assets']:
                assets.append(Asset(asset))
            return assets
        raise Exception(
            "[Error] request returned code {} with reason {}".format(response.status_code, response.reason))

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
            return response
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
        _num_loops = int(math.ceil(limit / 300))
        events = []
        for loop in range(1, _num_loops+1):
            params['offset'] = loop * 300
            # set limit
            if limit - ((loop-1) * 300) > 300:
                params['limit'] = 300
            else:
                params['limit'] = limit - ((loop-1) * 300)
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

        for contract in jsonData['primary_asset_contracts']:
            if contract["asset_contract_type"] == "non-fungible":
                self.ERC721Address = contract["address"]

        self.stats = jsonData['stats']
        self.floor = jsonData['stats']['floor_price']


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

