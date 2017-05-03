#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from ..sdk import BDPClient

ACCESS_TOKEN = "0c78a94144b485b24af4df121c7c7fae"


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = BDPClient(ACCESS_TOKEN)
        # self.client.create_ds("fortest123")

    def test_get_ds(self):
        self.assertEqual("sdk_test_5", str(self.client.get_ds("sdk_test_5")))

    def test_create_ds(self):
        self.assertIsNot(None, self.client.create_ds("testtesttest"))

    def test_delete_ds(self):
        self.assertTrue(self.client.delete_ds("testtesttest"))
