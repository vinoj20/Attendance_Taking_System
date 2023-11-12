import mysql.connector

class Database:
    def __init__(self):
        try:
            self.config = {
                'MYSQL_HOST': 'localhost',
                'MYSQL_USER': 'root',
                'MYSQL_PASSWORD': '',
                'MYSQL_DB': 'attendancemsystem'
            }

            # Create MySQL connection
            self.mysql_conn = mysql.connector.connect(
                host=self.config['MYSQL_HOST'],
                user=self.config['MYSQL_USER'],
                password=self.config['MYSQL_PASSWORD'],
                database=self.config['MYSQL_DB']
            )

            self.isconnected=True # Set the attribute to True if the connection is successful 
        except mysql.connector.Error as e:
            self.isconnected = False  # Set the attribute to False if there's an error during connection
            print(f"Error connecting to the database: {e}")

    def run_query(self, query,params=None):
         # Create a cursor object to execute queries
        cursor = self.mysql_conn.cursor(dictionary=True)  # Fetch rows as dictionaries

        try:
            # Execute the query with optional parameters
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            # Fetch all the results
            result = cursor.fetchall()

            # Get the row count
            row_count = cursor.rowcount
            
            # Return the row count and query result
            return row_count, result
        except mysql.connector.Error as error:
            # Handle any errors that occur during query execution
            print(f"Error executing query: {error}")
            raise  # Optionally raise the error to propagate it to the caller
        finally:
            # Close the cursor
            cursor.close()
            # Close the connection
            self.mysql_conn.close()
    
    
    def perform_insert(self, query, params=None):
        # Create a cursor object to execute queries
        cursor = self.mysql_conn.cursor()

        try:
            # Execute the insert query with optional parameters
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            # Commit the changes to the database
            self.mysql_conn.commit()

            # Get the number of affected rows (usually 1 for INSERT)
            row_count = cursor.rowcount
            
            # Return the number of affected rows
            return row_count
        except mysql.connector.Error as error:
            # Handle any errors that occur during query execution
            print(f"Error executing insert query: {error}")
            # Optionally, you can rollback the transaction here if needed
            self.mysql_conn.rollback()
            raise  # Optionally raise the error to propagate it to the caller
        finally:
            # Close the cursor
            cursor.close()

    def perform_update(self, query, params=None):
        # The implementation for UPDATE is similar to INSERT, so we can reuse the code
        return self.perform_insert(query, params)

    def perform_update_subtraction(self, tablename,column_name,condition_column, subtraction_amount, condition_value):
        # Create a cursor object to execute queries
        cursor = self.mysql_conn.cursor()

        try:
            # Construct the update query with the subtraction operation
            update_query = f"UPDATE {tablename} SET {column_name} = {column_name} - %s WHERE {condition_column} = %s"
            update_params = (subtraction_amount, condition_value)

            # Execute the update query with the specified parameters
            cursor.execute(update_query, update_params)

            # Commit the changes to the database
            self.mysql_conn.commit()

            # Get the number of affected rows (number of rows updated)
            row_count = cursor.rowcount
            
            # Return the number of affected rows
            return row_count
        except mysql.connector.Error as error:
            # Handle any errors that occur during query execution
            print(f"Error executing update query: {error}")
            # Optionally, you can rollback the transaction here if needed
            self.mysql_conn.rollback()
            raise  # Optionally raise the error to propagate it to the caller
        finally:
            # Close the cursor
            cursor.close()