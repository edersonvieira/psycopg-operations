import os, psycopg2

current_environment = os.environ.get('ENVIRONMENT')
dbpass = os.environ.get('DBPASS')
in_production = current_environment == "PRODUCTION"

connection_infos = {
    "dev": {
        "dbname": "",
        "user": "",
        "password": "",
        "host": "",
        "port": ""
    },
    "prod": {
        "dbname": "",
        "user": "",
        "password": dbpass,
        "host": "",
        "port": ""
    }
}

def db_connection():
    try:
        connection = psycopg2.connect(**connection_infos['dev' if not in_production else 'prod'])
        print("Connected")
        return connection
    except Exception as e:
        print("Connection failed:", e)
        return None