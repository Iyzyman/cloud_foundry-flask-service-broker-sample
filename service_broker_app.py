from flask import Flask, jsonify, request, abort, Response, make_response
from functools import wraps
import logging
from logging.handlers import RotatingFileHandler
import os
from config import MLFlowConfig, AirFlowConfig
from helpers.checks import requires_auth, requires_api_version
import requests

#Flask creation function
def create_app(test_config=None):
    
    app = Flask(__name__, instance_relative_config=True)
    #VARIABLES
    X_BROKER_API_MAJOR_VERSION = 2
    X_BROKER_API_MINOR_VERSION = 15
    X_BROKER_API_VERSION_NAME = 'X-Broker-Api-Version'

    if test_config is not None:
        app.config.from_object(test_config)
        os.environ['SERVICE_TYPE']='test'
    else:
        # Determine the environment and load the appropriate config
        env = os.environ.get('SERVICE_TYPE', 'mlflow')
        if env == 'airflow':
            app.config.from_object(AirFlowConfig)
        else:
            app.config.from_object(MLFlowConfig)
    
    # Set up logging
    if not app.debug:
        log_file = 'testing.log' if app.config['TESTING'] else 'service_broker.log'
        handler = RotatingFileHandler(
            log_file, maxBytes=10000, backupCount=1
        )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.DEBUG)


    app.logger.info('Starting Service Broker for {} env'.format(os.environ.get('SERVICE_TYPE', 'mlflow')))

    @app.errorhandler(412)
    def version_mismatch(error):
        app.logger.warning('Version mismatch or not specified in headers Expected: {}: {}.{}'.format(
            X_BROKER_API_VERSION_NAME,
            X_BROKER_API_MAJOR_VERSION,
            X_BROKER_API_MINOR_VERSION))
        return 'Version mismatch. Expected: {}: {}.{}'.format(
            X_BROKER_API_VERSION_NAME,
            X_BROKER_API_MAJOR_VERSION,
            X_BROKER_API_MINOR_VERSION), 412
    
    # Health Check
    @app.route('/v2/health', methods=['GET'])
    def health_check():
        response = make_response('OK', 200)
        return response

    # Catalog Service
    @app.route('/v2/catalog', methods=['GET'])
    @requires_auth
    @requires_api_version
    def catalog():
        return jsonify(app.config['SERVICE'])

    # Service Creation
    @app.route('/v2/service_instances/<instance_id>', methods=['PUT'])
    @requires_auth
    @requires_api_version
    def provision(instance_id):
        # url = "{}/v1/service_instance/{}".format(API_URL, instance_id)
        #try:
            # response = requests.put(url)

        #     if response.status_code == 201:
            #  app.logger.info('Successfully created service instance with id {}'.format(instance_id))
        #         return jsonify({}), 201
        #     else:
        #         return jsonify({"error": "Request failed with status code: {}".format(response.status_code)}), response.status_code

        # except requests.RequestException as e:
            #app.logger.error('Error: %s', str(e))
            #return jsonify({"error": "An error occurred: {}".format(str(e))}), 500
        app.logger.info('Successfully created service instance with id {}'.format(instance_id))
        return jsonify({}), 201

    # Service Bindings
    @app.route('/v2/service_instances/<instance_id>/service_bindings/<binding_id>', methods=['PUT'])
    @requires_auth
    @requires_api_version
    def bind(instance_id, binding_id):
        
        # url = "{}/v1/bindings/{}/{}".format(API_URL, instance_id, binding_id)
        # credentials=requests.get(url)
        # response = requests.get(url)
        
        # # Check if the request was successful
        # if response.ok:
        #     # Process the credentials received from the API
        #     credentials = response.json()
        #     app.logger.info('Successfully binded service instance with id {} with service {} '.format(binding_id,instance_id))
        #     return jsonify(credentials), 201
        # else:
        #     # Handle errors
        #     app.logger.error('Error: %s', str(e))
        #     return jsonify({"error": "Failed to retrieve credentials"}), response.status_code 
        
        credentials = {
            'uri': 'mysql://user:pass@sample-service-host/sample-db',
            'username': 'user',
            'password': 'pass',
            'host': 'sample-service-host',
            'port': 3306,
            'database': 'sample-db'
        }
        return jsonify({
            'credentials': credentials
        }), 201


    # Service Bindings Removal   
    @app.route('/v2/service_instances/<instance_id>/service_bindings/<binding_id>', methods=['DELETE'])
    @requires_auth
    @requires_api_version
    def unbind(instance_id, binding_id):

        # url = "{}/v1/bindings/{}/{}".format(API_URL, instance_id, binding_id)
        #try:
            # response = requests.delete(url)

        #     if response.status_code == 200:
            #   app.logger.info('Successfully deleted binding for service instance with id {} with service {} '.format(binding_id,instance_id))
        #         return jsonify({}), 200
        #     else:
        #         # If the response's status code is not 200, return the error message
        #         # You might want to include more information in the error message
        #         return jsonify({"error": "Request failed with status code: {}".format(response.status_code)}), response.status_code

        # except requests.RequestException as e:
        #    app.logger.error('Error: %s', str(e))
            #return jsonify({"error": "An error occurred: {}".format(str(e))}), 500
        return jsonify({}), 200

    # Service Deletion
    @app.route('/v2/service_instances/<instance_id>', methods=['DELETE'])
    @requires_auth
    @requires_api_version
    def deprovision(instance_id):
        # url = "{}/v1/service_instance/{}".format(API_URL, instance_id)
        #try:
            # response = requests.delete(url)

        #     if response.status_code == 200:
        #         app.logger.info('Successfully delete service instance with id {}'.format(instance_id))
        #         return jsonify({}), 200
        #     else:
        #         # If the response's status code is not 200, return the error message
        #         # You might want to include more information in the error message
        #         return jsonify({"error": "Request failed with status code: {}".format(response.status_code)}), response.status_code

        # except requests.RequestException as e:
        #    app.logger.error('Error: %s', str(e))
            #return jsonify({"error": "An error occurred: {}".format(str(e))}), 500
        return jsonify({}), 200
    return app



app = create_app()
if __name__ == '__main__':
    port=os.environ('PORT',8080)
    app.run(host='0.0.0.0',port=port)
