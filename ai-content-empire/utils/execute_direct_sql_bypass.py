import os
import psycopg2

def execute_sql_direct():
    sql_script_path = os.path.join(os.path.dirname(__file__), '../database/database.sql')
    
    conn_string = "postgresql://postgres.gazdkovkhhemrqqqswfb:yVJFhwkK4H1H0igy@aws-0-us-west-2.pooler.supabase.com:6543/postgres?sslmode=require"
    
    print("Connecting to database...")
    try:
        conn = psycopg2.connect(conn_string)
        conn.autocommit = True
        cursor = conn.cursor()
        
        with open(sql_script_path, 'r') as f:
            sql_script = f.read()
            
        print("Executing SQL...")
        cursor.execute(sql_script)
        print("SQL executed successfully!")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    execute_sql_direct()
