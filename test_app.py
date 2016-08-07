#!/usr/bin/env python3

import os
import app as eic_status
import unittest

class EicStatusTestCase(unittest.TestCase):

    def setUp(self):
        self.app = eic_status.app.test_client()
        self.version = "v1.0"

    def test_echo(self):
        '''Test that echo returns a result'''
        resp = self.app.get("/echo")
        assert 'result' in resp.data.decode('utf-8')

    def test_hello_world(self):
        '''Test the obligatory Hello, World response'''
        resp = self.app.get("/")
        assert 'Hello, World!' == resp.data.decode('utf-8')

    def test_check_agents_status(self):
        '''Test that check agents status returns a status'''
        resp = eic_status.check_agents()
        assert 'status' in resp

    def test_apiv1_agents(self):
        '''
        Test that when the api v1.0 is called with
        agents, agents is a key in the return
        '''
        resp = self.app.get('/eic-status/api/v1.0/agents')
        assert 'agents' in resp.data.decode('utf-8')

    def test_apiv1_all(self):
        '''
        Test that when the api v1.0 is called with
        all, agents is a key inthe return
        '''
        resp = self.app.get('/eic-status/api/v1.0/all')
        assert 'agents' in resp.data.decode('utf-8')

    def tearDown(self):
        os.environ = {}

if __name__ == "__main__":
    unittest.main()
