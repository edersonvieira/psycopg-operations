import os, psycopg2

current_environment = os.environ.get('AMBIENTE')
dbpass = os.environ.get('DBPASS')
in_production = current_environment == "PRODUCAO"

connection_infos = {
    "dev":{
        "dbname": "db_hidro",
        "user": "db_hidro",
        "password": "JUXmBki9Pq6E2mWaenqz",
        "host": "afiradatabasev2-developer.csucdunwmefz.us-east-1.rds.amazonaws.com",
        "port": "5432"
    },
    "prod": {
        "dbname": "db_hidro",
        "user": "db_hidro",
        "password": dbpass,
        "host": "afiraiodatabasev2.csucdunwmefz.us-east-1.rds.amazonaws.com",
        "port": "5432"
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