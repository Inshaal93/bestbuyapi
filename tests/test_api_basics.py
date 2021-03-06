import os
import json
import unittest
import xml.etree.ElementTree as ET

from nose.tools import raises, ok_

from bestbuy import BestBuyAPI
from bestbuy.utils.exceptions import BestBuyAPIError


class TestAPIBasics(unittest.TestCase):
    def setUp(self):

        self.key = os.getenv("BESTBUY_API_KEY")
        # initialize both bestbuy products and categories api both APIs
        # are used arbitrarily to make general tests
        self.bbapi = BestBuyAPI(self.key)

    def tearDown(self):
        pass

    @raises(BestBuyAPIError)
    def test_validate_params(self):
        payload = {"query": "some query", "params": {"fiz": "bazz", "wrong": None}}
        self.bbapi.category._validate_params(payload)

    def test_json_response(self):
        query = "accessories.sku=5985609"
        response = self.bbapi.products.search(query=query, format="json")
        ok_(isinstance(response, dict), "Response cannot be converted to JSON")

    def test_xml_response(self):
        sku_nbr = 5985609
        query = f"sku={sku_nbr}"

        # leaving the format blank will default to xml
        response = self.bbapi.products.search(query=query, format="xml")
        xml_tree = ET.fromstring(response)
        response_sku = xml_tree.getchildren()[0].findall("sku")[0].text
        assert int(response_sku) == sku_nbr
