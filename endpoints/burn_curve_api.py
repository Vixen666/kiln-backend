from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection
import functools

bp = Blueprint('burn_curve_api', __name__)

@bp.route('/Burn_Curve_Api_Get_Curve', methods=['GET'])
def Burn_Curve_Api_Get_Curve():
    burn_id = request.args.get('burn_id')
    print(burn_id)
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Calling the stored procedure with template_id
        cursor.callproc('Burn_Curve_Api_Get_Curve', [burn_id])
        
        # Extracting the stored procedure results
        for result in cursor.stored_results():
            curve_data = result.fetchall()
        
        return jsonify(curve_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()