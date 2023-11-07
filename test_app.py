import base64
import json
import unittest
import os
from config import TestingConfig
from service_broker_app import create_app

class BrokerAPITestCase(unittest.TestCase):
    def setUp(self):
    # Apply the TestingConfig here
        self.client = create_app(TestingConfig)
        self.app = self.client.test_client()
    
    def test_health_check(self):
        response = self.app.get('/v2/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'OK')
    
    def test_catalog(self):
        # Assuming 'admin'/'admin' is the correct username/password
        credentials = 'Basic ' + base64.b64encode(b'admin:admin').decode('utf-8')
        response = self.app.get('/v2/catalog', headers={"Authorization": credentials,"X-Broker-Api-Version":'2.15'})
        self.assertEqual(response.status_code, 200)
    
    def test_provision(self):
        credentials = 'Basic ' + base64.b64encode(b'admin:admin').decode('utf-8')
        data = {}  # Add your data payload here if needed
        response = self.app.put('/v2/service_instances/123', headers={"Authorization": credentials,"X-Broker-Api-Version":'2.15'}, data=json.dumps(data))
        self.assertEqual(response.status_code, 201)
    
    # Add more tests for bind, unbind, deprovision, etc.
    

if __name__ == '__main__':
    unittest.main()
