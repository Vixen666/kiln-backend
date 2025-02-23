from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection
from services.generic_service import GenericService
from utils.generic_post_handler import execute_generic_get, execute_generic_post
from services.function_services import FunctionServices

import json

bp = Blueprint('generic_api', __name__)
generic_service = GenericService(db_connection= get_db_connection())
function_services_instance = FunctionServices()

@bp.route('/<service_name>/<operation_key>', methods=['GET'])
def handle_generic_get_operation(service_name, operation_key):
    # Using request.args to handle query parameters
    parameters = request.args.to_dict()
    
    # Assuming execute_generic_get is adjusted to handle parameters from request.args
    result, status_code = execute_generic_get(service_name, operation_key, parameters, function_services_instance)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), status_code
    return jsonify(result), status_code

@bp.route('/<service_name>/<operation_key>', methods=['POST'])
def handle_generic_post_operation(service_name, operation_key):
    # Using request.args to handle query parameters
    parameters = request.json
    
    # Assuming execute_generic_get is adjusted to handle parameters from request.args
    result, status_code = execute_generic_post(service_name, operation_key, parameters)
    if isinstance(result, dict) and "error" in result:
        return jsonify(result), status_code
    return jsonify(result), status_code