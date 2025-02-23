import mysql.connector
import json
import re
db_config = {
    'user': 'kiln',
    'password': 'kiln',
    'host': 'localhost',
    'database': 'KILN'
}
def connect_to_database():
    return mysql.connector.connect(**db_config)



def parse_enum_values(column_type):
    # This regex matches the inner content of an ENUM definition, ignoring the enum('...') wrapper.
    matches = re.findall(r"enum\((.*)\)", column_type)
    if not matches:
        return []

    # Split the matched string into individual enum values, trimming quotes
    values = [value.strip("'") for value in matches[0].split(',')]
    return values

def fetch_table_schema(db_name, table_name):
    db_connection = connect_to_database()
    cursor = db_connection.cursor()

    # SQL query to fetch column details
    query = f"""
    SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_TYPE, CHARACTER_MAXIMUM_LENGTH
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
    ORDER BY ORDINAL_POSITION;
    """

    # Execute the query
    cursor.execute(query, (db_name, table_name))

    # Fetch all the results
    columns = cursor.fetchall()
    print(columns)
    # Close the cursor and connection
    cursor.close()
    db_connection.close()

    # Return the columns information
    return columns

def generate_field_jsx(column_name, data_type, is_nullable, column_default, column_type, CHARACTER_MAXIMUM_LENGTH, variable_name):
    if data_type.lower() == 'enum':
        enum_values = parse_enum_values(column_type)
        options_jsx = '\n'.join([f'<option value="{value}">{value}</option>' for value in enum_values])
        select_jsx = f'''
            <FormControl fullWidth margin="dense" variant="outlined">
                <InputLabel htmlFor="{column_name}">{column_name.capitalize()}</InputLabel>
                <Select
                    key={{`field-${{{{{variable_name}}}.id}}-{column_name}`}}
                    native
                    value={{formData.{column_name} || ''}}
                    onChange={{handleChange}}
                    label="{column_name.capitalize()}"
                    inputProps={{
                        name: '{column_name}',
                        id: '{column_name}',
                    }}
                >
                    <option aria-label="None" value="" />
                    {options_jsx}
                </Select>
            </FormControl>
        '''
        return select_jsx

    react_type = type_mapping.get(data_type, 'text')  # Default to text if type is unknown
    required_attr = '' if is_nullable == 'YES' else 'required'
    default_value_attr = f'defaultValue="{column_default}"' if column_default is not None else ''
    maxLength = CHARACTER_MAXIMUM_LENGTH if CHARACTER_MAXIMUM_LENGTH is not None else 'undefined'
    # Handling special case for boolean (checkbox)
    if react_type == 'checkbox':
        checked_attr = 'defaultChecked' if column_default == '1' else ''
        return f'''
            <FormControlLabel
                key={{`field-${{{{{variable_name}}}.id}}-{column_name}`}}
                name="{column_name}"
                control={{<Checkbox name={{{variable_name}.{column_name}}} color="primary" {checked_attr} />}}
                label="{column_name.capitalize()}"
            />
        '''

    # Template for other types of inputs, including default value
    return f'''
        <TextField
            key={{`field-${{{{{variable_name}}}.id}}-{column_name}`}}
            margin="dense"
            name="{column_name}"
            value={{formData.{column_name}}}
            label="{column_name.capitalize()}"
            type="{react_type}"
            fullWidth
            variant="outlined"
            {required_attr}
            {default_value_attr}
            inputProps={{{{ maxLength: {maxLength} }}}}
        />
    '''

variable_name = 'oven'
columns_info = fetch_table_schema('KILN', 'Oven')
type_mapping = {
    'varchar': 'text',
    'int': 'number',
    'decimal': 'number',
    'tinyint': 'checkbox',  # Assuming tinyint(1) for boolean
    'char': 'text',  # You might want to add a maxLength attribute for this
    'datetime': 'datetime-local'  # Using HTML5 datetime-local input type
}
# Generate JSX code for all columns
form_fields_jsx = [generate_field_jsx(column[0], column[1], column[2], column[3], column[4], column[5], variable_name) for column in columns_info]

# Join all JSX codes into a single string
form_jsx_code = "\n".join(form_fields_jsx)

# This is your generated JSX code for the form fields
with open('react_forms_output.js', 'w') as file:
    file.write(form_jsx_code)