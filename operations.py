from core.db_connection import db_connection

connection = db_connection()

class OperationsSQL:
    def get(table, where):
        query = f"SELECT * FROM {table} WHERE {where} LIMIT 1"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()
                if row:
                    columns = [col[0] for col in cursor.description]
                    return dict(zip(columns, row))
                print("Not found")
                return False
        except Exception as e:
            print(f"Get error: {e}")
            return False
    
    def filter(table, where='', order_by='', ordering='', inner_join='', select='', limit_per_page=5, page=1):
        offset = (page - 1) * limit_per_page
        
        select = '*'
        inner_join = ""
        order_clause = ""
        where_clause = f"WHERE {where}" if where else ""
        if order_by and ordering:
            order_clause = f"ORDER BY {order_by} {ordering}"
        if inner_join:
            inner_join = inner_join
        if select:
            select = select
        
        query = f"""
            SELECT {select} FROM {table}
            {inner_join}
            {where_clause}
            {order_clause}
            LIMIT {limit_per_page} OFFSET {offset}
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            return results
        except Exception as e:
            print(f"Erro ao executar a consulta 'filter': {e}")
            return []
        
    def count(table, field_count='*', where='', inner_join=''):
        select = 'COUNT(' + field_count + ') AS total'
        inner_join = ""
        where = f"WHERE {where}" if where else ""
        if inner_join:
            inner_join = inner_join
        query = f"""
            SELECT {select} FROM {table}
            {inner_join}
            {where}
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            return results
        except Exception as e:
            print(f"Count error: {e}")
            return []
    
    def update(table, where, fields_values):
        set_clause = ", ".join([f"{field} = %s" for field in fields_values])
        query = f"UPDATE {table} SET {set_clause} WHERE {where}"

        values = tuple(fields_values.values())
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Update error: {e}")
            return False
    
    def create(table, fields_values):
        fields = ", ".join([f"{field}" for field in fields_values])
        values_clause = ", ".join([f"%s" for i in fields_values])
        query = f"""
            INSERT INTO {table} ({fields})
            VALUES ({values_clause})
        """
        values = tuple(fields_values.values())

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Insert error: {e}")
            return False
    
    def delete(table, where):
        query = f"""
            DELETE FROM {table}
            WHERE {where}
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Delete error: {e}")
            return False