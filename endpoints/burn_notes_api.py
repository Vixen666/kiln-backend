from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection

bp = Blueprint('oven_notes_api', __name__)


@bp.route('/Burn_notes_Api_Update', methods=['GET'])
def Burn_notes_Api_Update():
    data = request.json
    missing_parameters = []
    proc_args = []
    if 'note_id' not in data:
        missing_parameters.append('note_id')
    else:
        proc_args.append(data['note_id'])

    if 'burn_id' not in data:
        missing_parameters.append('burn_id')
    else:
        proc_args.append(data['burn_id'])

    if 'note_text' not in data:
        missing_parameters.append('note_text')
    else:
        proc_args.append(data['note_text'])

    if 'created_at' in data:
        proc_args.append(data['created_at'])

    if missing_parameters:
        return jsonify({"error": "Missing parameters", "missing": missing_parameters}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('Burn_notes_Api_Update', proc_args)
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


@bp.route('/Burn_notes_Api_Get_All', methods=['GET'])
def Burn_notes_Api_Get_All():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('Burn_notes_Api_Get_All')

        # Assuming the first result set contains the data
        for result in cursor.stored_results():
            data = result.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@bp.route('/Burn_notes_Api_Get_By_Burn', methods=['GET'])
def Burn_notes_Api_Get_By_Burn():
    burn_id = request.args.get('burn_id')
    print(burn_id)
    try:
        conn =get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('Burn_notes_Api_Get_By_Burn', [burn_id])
        
        # Assuming the first result set contains the data
        for result in cursor.stored_results():
            data = result.fetchall()
            print(data)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
