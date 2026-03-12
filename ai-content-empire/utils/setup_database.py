import os
import yaml
from supabase import create_client, Client

def get_supabase_config():
    """Reads the Supabase configuration from the config file."""
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def execute_sql_script(supabase_client: Client, sql_script_path: str):
    """Executes the SQL script against the Supabase database."""
    try:
        with open(sql_script_path, 'r') as f:
            sql_script = f.read()
        
        # The supabase-py library does not directly support executing raw SQL scripts.
        # This is a placeholder for the correct implementation using a proper database driver.
        # For now, we will print the SQL script to be executed.
        print("Executing SQL script:")
        print(sql_script)
        print("\nNOTE: Manual execution of the SQL script is required.")

    except Exception as e:
        print(f"Error executing SQL script: {e}")

if __name__ == '__main__':
    config = get_supabase_config()
    supabase_url = config.get('supabase_url')
    supabase_anon_key = config.get('supabase_anon_key')
    sql_script_path = os.path.join(os.path.dirname(__file__), '../database/database.sql')

    if supabase_url and supabase_anon_key:
        print("Supabase configuration found. Attempting to connect...")
        try:
            supabase: Client = create_client(supabase_url, supabase_anon_key)
            print("Supabase client created successfully.")
            
            # This is where the SQL execution would happen, but it's not supported directly.
            execute_sql_script(supabase, sql_script_path)

        except Exception as e:
            print(f"Error creating Supabase client: {e}")
    else:
        print("Supabase configuration not found in config.yaml.")
