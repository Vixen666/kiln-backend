from flask import request, jsonify
import functools
import json
from database import get_db_connection, close_db_connection

with open('./services/service_operations.json', 'r') as f:
    endpoint_config = json.load(f)

def execute_generic_post(service_name, operation_key, parameters):
    service_config = endpoint_config.get(service_name)
    if not service_config:
        return {"error": f"Service '{service_name}' not found"}, 404

    # Then, check if the operation exists for the given service
    endpoint_details = service_config.get(operation_key)
    if not endpoint_details:
        return {"error": f"Operation '{operation_key}' not found in service '{service_name}'"}, 404


    missing_parameters, provided_parameters = check_parameters(request, endpoint_details['parameters'])
    if missing_parameters:
        return {"error": "Missing parameters", "missing": missing_parameters}, 400

    # Assuming do_GET_call is a function that performs the required operations based on operation_name
    response, status_code = do_POST_call(endpoint_details['operation_name'], provided_parameters)

            # Call the specified function if it exists
    print(endpoint_details)
    return response, status_code


def check_parameters(request, required_params):
    data = request.json
    missing_parameters = []
    provided_parameters = {}
    for param in required_params:
        if param not in data:
            missing_parameters.append(param)
        else:
            provided_parameters[param] = data[param]
    return missing_parameters, provided_parameters




def do_POST_call(endpoint, parameters):
    try:
        # Assuming `get_db_connection` is a function that returns a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        # Here, you might need to map `endpoint` to a specific stored procedure or database logic
        cursor.callproc(endpoint, list(parameters.values()))
        conn.commit()
        return {"success": True}, 200
    except Exception as e:
        print(str(e))
        return {"error": str(e)}, 500
    finally:
        if conn:
            cursor.close()
            conn.close()

def check_get_parameters(request, required_params):
    missing_parameters = []
    provided_parameters = {}
    for param in required_params:
        if param not in request.args:
            missing_parameters.append(param)
        else:
            provided_parameters[param] = request.args.get(param)
    return missing_parameters, provided_parameters


def do_GET_call(endpoint, parameters):
    try:
        # Assuming `get_db_connection` is a function that returns a database connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Here, you might need to map `endpoint` to a specific stored procedure or database logic
        cursor.callproc(endpoint, list(parameters.values()))
        for test in cursor.stored_results():  # Loop through stored results
            result = test.fetchall()
        return result, 200
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if conn:
            cursor.close()
            conn.close()


def execute_generic_get(service_name, operation_key, parameters, function_services):
    service_config = endpoint_config.get(service_name)
    if not service_config:
        return {"error": f"Service '{service_name}' not found"}, 404

    # Then, check if the operation exists for the given service
    endpoint_details = service_config.get(operation_key)
    if not endpoint_details:
        return {"error": f"Operation '{operation_key}' not found in service '{service_name}'"}, 404


    missing_parameters, provided_parameters = check_get_parameters(request, endpoint_details['parameters'])
    if missing_parameters:
        return {"error": "Missing parameters", "missing": missing_parameters}, 400

    # Assuming do_GET_call is a function that performs the required operations based on operation_name
    response, status_code = do_GET_call(endpoint_details['operation_name'], provided_parameters)
        # Call the specified function if it exists
    function_name = endpoint_details.get('function_name')
    if function_name:
        response = getattr(function_services, function_name)(response)
        
    return response, status_code

