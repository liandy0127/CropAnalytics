from psycopg2 import sql
from app import get_db_conn
import csv

def get_table_names():
    conn = get_db_conn()
    cursor = conn.cursor()
    
    query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'crops'  -- update the schema name if necessary
        ORDER BY table_name;
    """
    
    cursor.execute(query)
    tables = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return [table[0] for table in tables]

def export_table_to_csv(table_name, export_path):
    conn = get_db_conn()
    cursor = conn.cursor()
    
    export_query = sql.SQL("COPY {} TO STDOUT WITH CSV HEADER").format(sql.Identifier(table_name))
    file_path = f"{export_path}/{table_name}.csv"
    
    with open(file_path, 'w') as f:
        cursor.copy_expert(export_query, f)
    
    cursor.close()
    conn.close()
    
    return file_path

def upload_file_to_db(file_path, table_name):
    conn = get_db_conn()
    cursor = conn.cursor()
    
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        columns = next(reader)  # Get the column names from the first line of the file
        query = sql.SQL('INSERT INTO {} ({}) VALUES ({})').format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        
        for row in reader:
            cursor.execute(query, row)
    
    conn.commit()
    cursor.close()
    conn.close()
