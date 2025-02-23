from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection
from services.generic_service import GenericService
from utils.generic_post_handler import execute_generic_get, execute_generic_post

import json

bp = Blueprint('oven_api', __name__)
generic_service = GenericService(db_connection= get_db_connection())



@bp.route('/Oven_Api_Get_Oven_By_Id', methods=['GET'])
def Oven_Api_Get_Oven_By_Id():
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to return data as dictionaries
        # Call the stored procedure
        cursor.callproc('Oven_Api_Get_All_Ovens')
        # Fetch the results
        for result in cursor.stored_results():  # Loop through stored results
            templates = result.fetchall()
            return jsonify(templates)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@bp.route('/Oven_Api_Create_Or_Update_Oven', methods=['POST'])
def Oven_Api_Create_Or_Update_Oven():
    data = request.json
    connection = get_db_connection()
    response = {}
    print(data)
    
    if connection:
        cursor = connection.cursor()
        try:
            oven_id = data.get('id')
            if oven_id == '':
                oven_id = None 

            cursor.callproc('Oven_Api_Create_Or_Update_Oven', [
                data.get('id', None),
                data['name'],
                data['max_temp_positive'],
                data['max_temp_negative'],
                data['location'],
                data['power'],
                data.get('thermometer_type', ''),
                data.get('thermometer_pin', None),
                data.get('burner_pin', None)
            ])
            connection.commit()
            response['message'] = 'Oven saved/updated successfully'
        except Error as e:
            connection.rollback()
            response['error'] = str(e)
        finally:
            cursor.close()
            connection.close()
    else:
        response['error'] = 'Database connection failed'
    
    return jsonify(response)