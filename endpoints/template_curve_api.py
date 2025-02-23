from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection

bp = Blueprint('template_curve_api', __name__)

@bp.route('/Template_Curve_Api_Get_Curve', methods=['GET'])
def get_curve():
    template_id = request.args.get('template_id')  # Get template_id from query string
    if not template_id:
        return jsonify({"error": "Missing template_id parameter"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Calling the stored procedure with template_id
        cursor.callproc('Template_Curve_Api_Get_Curve', [template_id])
        
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

@bp.route('/Template_Curve_Api_Update_Template_Curve', methods=['POST'])
def save_template_curve():
    data = request.json
    template_id = data['template_id']
    curves = data['curves']  # Assuming curves is a list of dictionaries

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Delete existing curves for the template
        cursor.execute("DELETE FROM template_curve WHERE template_id = %s", (template_id,))

        # Insert new curves
        insert_query = "INSERT INTO template_curve (template_id, sequence, time, temperature) VALUES (%s, %s, %s, %s)"
        for curve in curves:
            cursor.execute(insert_query, (template_id, curve['sequence'], curve['time'], curve['temperature']))
        
        conn.commit()
        return jsonify({'message': 'Template curves updated successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()