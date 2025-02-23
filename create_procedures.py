import mysql.connector
import json
db_config = {
    'user': 'kiln',
    'password': 'kiln',
    'host': 'localhost',
    'database': 'KILN'
}
def connect_to_database():
    return mysql.connector.connect(**db_config)

def fetch_table_schema(cursor, table_name):
    cursor.execute(f"DESCRIBE {table_name}")
    columns_details = cursor.fetchall()
    schema_json = [
        {
            "field": field,
            "type": type_,
            "null": null,
            "key": key,
            "default": default,
            "extra": extra
        } for field, type_, null, key, default, extra in columns_details
    ]
    pretty_json = json.dumps(schema_json, indent=4)
    print(pretty_json)

    columns = {col[0]: {'type': col[1], 'null': col[2], 'key': col[3]} for col in columns_details}
    primary_keys = [col[0] for col in columns_details if col[3] == 'PRI']
    return columns, primary_keys

def fetch_primary_keys(cursor, table_name, database_name):
    query = """
    SELECT COLUMN_NAME 
    FROM information_schema.KEY_COLUMN_USAGE 
    WHERE TABLE_NAME = %s 
      AND CONSTRAINT_NAME = 'PRIMARY' 
      AND TABLE_SCHEMA = %s;
    """
    cursor.execute(query, (table_name, database_name))
    primary_keys = [row[0] for row in cursor.fetchall()]
    return primary_keys


def generate_procedures(db_connection, cursor, table_name, columns, primary_keys):
    # Example: Generate SQL for "Get_All" procedure
    capitalized_name = table_name.capitalize()
    get_all_sql = f"""
    DROP PROCEDURE IF EXISTS `{capitalized_name}_Api_Get_All`;
    CREATE PROCEDURE `{capitalized_name}_Api_Get_All`()
    BEGIN
        SELECT * FROM `{table_name}`;
    END
    """
    for result in cursor.execute(get_all_sql, multi=True):
        pass

    # Define the SQL for Get_By_Keys
    keys_params = ", ".join([f"IN p_{key} {column['type']}" for key, column in columns.items() if key in primary_keys])
    where_clause = " AND ".join([f"{key} = p_{key}" for key in primary_keys])
    get_by_keys_sql = f"""
    DROP PROCEDURE IF EXISTS `{capitalized_name}_Api_Get_By_Keys`;
    CREATE PROCEDURE `{capitalized_name}_Api_Get_By_Keys`({keys_params})
    BEGIN
        SELECT * FROM `{table_name}` WHERE {where_clause};
    END;
    """
    for result in cursor.execute(get_by_keys_sql, multi=True):
        pass  # This is necessary to actually execute the statements


    # Define the SQL for Insert
    insert_params = ", ".join([f"IN p_{column_name} {details['type']}" for column_name, details in columns.items()])
    insert_columns = ", ".join(columns.keys())
    insert_values = ", ".join([f"p_{column_name}" for column_name in columns.keys()])
    insert_sql = f"""
    DROP PROCEDURE IF EXISTS `{capitalized_name}_Api_Insert`;
    CREATE PROCEDURE `{capitalized_name}_Api_Insert`({insert_params})
    BEGIN
        INSERT INTO `{table_name}`({insert_columns}) VALUES ({insert_values});
    END;
    """
    for result in cursor.execute(insert_sql, multi=True):
        pass  # This is necessary to actually execute the statements


    # Define the SQL for Update
    update_params = insert_params
    update_set_clause = ", ".join([f"{column_name} = p_{column_name}" for column_name in columns.keys() if column_name not in primary_keys])
    update_sql = f"""
    DROP PROCEDURE IF EXISTS `{capitalized_name}_Api_Update`;
    CREATE PROCEDURE `{capitalized_name}_Api_Update`({update_params})
    BEGIN
        UPDATE `{table_name}` SET {update_set_clause} WHERE {where_clause};
    END;
    """
    for result in cursor.execute(update_sql, multi=True):
        pass  # This is necessary to actually execute the statements

    # Define the SQL for Delete
    delete_sql = f"""
    DROP PROCEDURE IF EXISTS `{capitalized_name}_Api_Delete`;
    CREATE PROCEDURE `{capitalized_name}_Api_Delete`({keys_params})
    BEGIN
        DELETE FROM `{table_name}` WHERE {where_clause};
    END;
    """
    for result in cursor.execute(delete_sql, multi=True):
        pass  # This is necessary to actually execute the statements
    db_connection.commit()







def generate_flask_endpoint_code_from_columns(table_name, columns_details):
    capitalized_name = table_name.capitalize()
    # Extract column names, excluding primary keys if not needed for the insert
    print(columns_details)
    columns =  [col for col in columns_details]
    print(columns)
    primary_keys = [col for col in columns_details if col[3] == 'PRI']

    # Start defining the Flask endpoint





    code = f"""@app.route('/{capitalized_name}_Insert', methods=['POST'])
def {capitalized_name}_Api_Insert():
    data = request.json
    missing_parameters = []
    proc_args = []\n"""

    # Generate checks for missing parameters and prepare arguments


    for column_name in columns:
        code += f"""    if {column_name} not in data:
        missing_parameters.append('{column_name}')
    else:
        proc_args.append(data['{column_name}'])\n\n"""

    # Add handling for missing parameters
    code += """    if missing_parameters:
        return jsonify({"error": "Missing parameters", "missing": missing_parameters}), 400\n"""

    # Add code to execute the stored procedure
    code += f"""    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.callproc('{capitalized_name}_Api_Insert', proc_args)
        conn.commit()
        return jsonify({{"success": True}})
    except Exception as e:
        return jsonify({{"error": str(e)}}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()\n"""
    print(code)    


    code = f"""@app.route('/{capitalized_name}_Api_Update', methods=['POST'])
def {capitalized_name}_Api_Update():
    data = request.json
    missing_parameters = []
    proc_args = []\n"""

    # Generate checks for missing parameters and prepare arguments
    for column_name in columns:
        code += f"""    if {column_name} not in data:
        missing_parameters.append('{column_name}')
    else:
        proc_args.append(data['{column_name}'])\n\n"""

    # Add handling for missing parameters
    code += """    if missing_parameters:
        return jsonify({"error": "Missing parameters", "missing": missing_parameters}), 400\n"""

    # Add code to execute the stored procedure
    code += f"""    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.callproc('{capitalized_name}_Api_Update', proc_args)
        conn.commit()
        return jsonify({{"success": True}})
    except Exception as e:
        return jsonify({{"error": str(e)}}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()\n"""
    print(code)


# Define the Flask endpoint for Get_By_Keys
    get_by_keys_code = f"""@app.route('/{capitalized_name}_Api_Get_By_Keys', methods=['GET'])
    def {capitalized_name}_Api_Get_By_Keys():
        missing_parameters = []\n"""

    # Generate checks for missing primary key parameters
    for key in primary_keys:
        get_by_keys_code += f"""    {key} = request.args.get('{key}')
        if not {key}:
            missing_parameters.append('{key}')\n"""

    # Add handling for missing primary key parameters
    get_by_keys_code += """    if missing_parameters:
            return jsonify({"error": "Missing primary key parameter(s)", "missing": missing_parameters}), 400\n"""

    # Add code to execute the stored procedure
    proc_args = ", ".join(primary_keys)
    get_by_keys_code += f"""    try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('{capitalized_name}_Api_Get_By_Keys', [{proc_args}])
            
            # Assuming the first result set contains the data
            for result in cursor.stored_results():
                data = result.fetchall()
            return jsonify(data)
        except Exception as e:
            return jsonify({{"error": str(e)}}), 500
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()\n"""

    print(get_by_keys_code)




    get_all_code = f"""@app.route('/{capitalized_name}_Api_Get_All', methods=['GET'])
def {capitalized_name}_Api_Get_All():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('{capitalized_name}_Api_Get_All')
        
        # Assuming the first result set contains the data
        for result in cursor.stored_results():
            data = result.fetchall()
        return jsonify(data)
    except Exception as e:
        return jsonify({{"error": str(e)}}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()\n"""
    print(get_all_code)

    return code


def main(table_name):
    db_connection = connect_to_database()
    cursor = db_connection.cursor()
    columns, primary_keys = fetch_table_schema(cursor, table_name)


    procedures = generate_procedures(db_connection, cursor, table_name, columns, primary_keys)
    # Print or execute generated procedures

    cursor.close()
    #endpoint_code = generate_flask_endpoint_code_from_columns(table_name, columns)

    # Print the generated code

if __name__ == "__main__":
    main('burn_temperature_data')  # replace 'your_table_name' with the actual table name