import os
# config.py

class Config(object):
    DEBUG = False
    SECRET_KEY = 'your-secret-key'
    TESTING = False
    X_BROKER_API_MAJOR_VERSION = os.environ.get('API_MAJOR_VERSION',2)
    X_BROKER_API_MINOR_VERSION = os.environ.get('API_MINOR_VERSION',15)
    X_BROKER_API_VERSION_NAME = 'X-Broker-Api-Version'
    # other shared config variables

class TestingConfig(Config):
    TESTING=True
    SERVER_URL="http://mflow.example.com"
    DATABASE_URI = 'sqlite:///dev.db'
    SERVICE= {
        'services': [{
            'id': 'service-guid-here',
            'name': 'sample-MLFlow-service',
            'description': 'A sample MLFlow service',
            'bindable': True,
            'plans': [{
                'id': 'plan-guid-here',
                'name': 'default',
                'description': 'Default plan'
            }]
        }]
    }
class MLFlowConfig(Config):
    SERVER_URL="http://mflow.example.com"
    DATABASE_URI = 'sqlite:///dev.db'
    SERVICE= {
        'services': [{
            'id': 'service-guid-here',
            'name': 'sample-MLFlow-service',
            'description': 'A sample MLFlow service',
            'bindable': True,
            'plans': [{
                'id': 'plan-guid-here',
                'name': 'default',
                'description': 'Default plan'
            }]
        }]
    }
   

class AirFlowConfig(Config):
    SERVER_URL="http://airflow.example.com"
    DATABASE_URI = 'sqlite:///prod.db'
    SERVICE= {
        'services': [{
            'id': 'service-guid-here',
            'name': 'sample-AirFlow-service',
            'description': 'A sample AirFlow service',
            'bindable': True,
            'plans': [{
                'id': 'plan-guid-here',
                'name': 'default',
                'description': 'Default plan'
            }]
        }]
    }
    
