import json
import os
from .base_service import BaseService

class GenericService(BaseService):
    def __init__(self, db_connection):
        super().__init__(db_connection)
        current_dir = os.path.dirname(__file__)
        # Construct the path to the service_operations.json file
        operations_file_path = os.path.join(current_dir, 'service_operations.json')
        with open(operations_file_path, 'r') as f:
            self.operations = json.load(f)  # Load all services

    def execute_operation(self, service_name, operation_key, **kwargs):
        if service_name not in self.operations:
            raise ValueError(f"Service {service_name} not defined.")

        service_operations = self.operations[service_name]
        
        if operation_key not in service_operations:
            raise ValueError(f"Operation {operation_key} not defined for service {service_name}.")
        

        
        operation_config = service_operations[operation_key]
        operation_name = operation_config['operation_name']
        fetch_mode = operation_config['fetch_mode']

        expected_params = operation_config['parameters']
        missing_params = [param for param in expected_params if param not in kwargs]
        if missing_params:
            raise ValueError(f"Missing required parameters: {missing_params}")

        # Map kwargs to the parameters defined in the operation_config
        parameters = [kwargs[param] for param in operation_config['parameters'] if param in kwargs]
        return self.perform_db_operation(operation_name, parameters, fetch_mode=fetch_mode)
