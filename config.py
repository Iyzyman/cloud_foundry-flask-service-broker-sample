# config.py

class Config(object):
    DEBUG = False
    SECRET_KEY = 'your-secret-key'
    TESTING = False
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
    
