import pyodbc

# Define the connection string
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:sketchdb.database.windows.net,1433;"
    "Database=dreamdb;"
    "Uid=db user id;"
    "Pwd= db password;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Establish the connection
try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    print("Connection established successfully!")
    cursor.execute("DELETE FROM DreamInfo")
    conn.close()
except Exception as e:
    print(f"Error connecting to the database: {e}")

# Once you're done with the connection, don't forget to close it

