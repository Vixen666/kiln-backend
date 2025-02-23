from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection

bp = Blueprint('template_api', __name__)

@bp.route('/Template_Api_Get_All_Templates', methods=['GET'])
def Template_Api_Get_All_Templates():
    try:
        print("Template_Api_Get_All_Templates")
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to return data as dictionaries
        # Call the stored procedure
        cursor.callproc('Template_Api_Get_All_Templates')
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

@bp.route('/Template_Api_Create_Template', methods=['POST'])
def Template_Api_Create_Template():
    data = request.json
    name = data['name']

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Call the stored procedure
        cursor.callproc('Template_Api_Create_Template', [name])
        conn.commit()
        return jsonify({'message': 'Template created successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

