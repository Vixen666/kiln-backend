from flask import Blueprint, request, jsonify
from database import get_db_connection, close_db_connection
from flask import send_from_directory
from werkzeug.utils import secure_filename
import uuid
import os
from config import UPLOAD_FOLDER
bp = Blueprint('image_api', __name__)

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    burn_id = request.form['burn_id']
    imageType = request.form['imageType']
    print(file, burn_id, imageType)
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        old_img_name = secure_filename(file.filename)
        # Generate a unique new image name
        ext = old_img_name.split('.')[-1]
        new_img_name = f"{uuid.uuid4()}.{ext}"
        print(new_img_name)
        file.save(os.path.join('/home/pi/Development/upload/', new_img_name))
        
        # Insert into database (simplified example, adjust connection details)
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO burn_images (burn_id, phase, new_img_name, old_img_name) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (burn_id, imageType, new_img_name, old_img_name))  # Using burn_id 1 for now
            connection.commit()
        except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return jsonify({'message': 'File uploaded successfully', 'new_img_name': new_img_name}), 200

@bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@bp.route('/Burn_images_Api_Get_By_Burn_Id', methods=['GET'])
def Burn_images_Api_Get_By_Burn_Id():
    burn_id = request.args.get('burn_id')
    phase = request.args.get('phase')
    print(burn_id, phase)
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to return data as dictionaries
        # Call the stored procedure
        cursor.callproc('Burn_images_Api_Get_By_Burn_Id_And_Phase', [burn_id, phase])
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