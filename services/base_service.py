class BaseService:
    def __init__(self, db_connection):
        self.db = db_connection

    def perform_db_operation(self, operation_name, parameters, fetch_mode=None):
        cursor = None
        try:
            self.db.reconnect()  
            cursor = self.db.cursor(dictionary=True)
            # Call the stored procedure
            cursor.callproc(operation_name, parameters)
            print("parameters ", parameters)
            # Initial empty result, adjusted based on fetch_mode
            result = None
            # Handling fetch modes
            if fetch_mode == 'one':
                # Fetch the first result set only (useful for single-row results)
                results = next(cursor.stored_results(), None)  # Safely get the first result set if it exists
                result = results.fetchone() if results else None
                
            elif fetch_mode == 'all':
                for test in cursor.stored_results():  # Loop through stored results
                    result = test.fetchall()
                
            else:
                # For operations that don't need to fetch data (insert, update, delete)
                self.db.commit()
                result = {"success": True}
            return result, 200
        except Exception as e:
            print(f"Error perform_db_operation: {e}")
            return {"error": str(e)}, 500
        finally:
            if cursor:
                cursor.close()
