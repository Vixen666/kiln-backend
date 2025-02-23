from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection

bp = Blueprint('template_util_api', __name__)

@bp.route('/Template_Util_Api_Duplicate_Template', methods=['POST'])
def Template_Util_Api_Duplicate_Template():
    data = request.json
    old_template_id = data['old_template_id']
    new_template_name = data['new_template_name']
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)  # Use dictionary cursor to return data as dictionaries
        cursor.callproc('Template_Util_Api_Duplicate_Template', [old_template_id, new_template_name])
        connection.commit()
        return jsonify({'message': 'Template duplicated successfully'}), 200
    except mysql.connector.Error as error:
        print("Failed to duplicate template: {}".format(error))
        return jsonify({'error': str(error)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
