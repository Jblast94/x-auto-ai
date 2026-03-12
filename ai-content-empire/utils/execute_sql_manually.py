import os
import yaml
import requests
import json

def get_supabase_config():
    """Reads the Supabase configuration from the config file."""
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def execute_sql_via_api(supabase_url, supabase_anon_key, sql_script_path):
    """Executes the SQL script against the Supabase database using the REST API."""
    try:
        with open(sql_script_path, 'r') as f:
            sql_script = f.read()

        # The Supabase REST API does not directly support executing raw SQL scripts.
        # This is a placeholder for the correct implementation.
        # For now, we will print the SQL script to be executed.
        print("SQL script to be executed:")
        print(sql_script)
        print("\nNOTE: Manual execution of the SQL script is required via the Supabase dashboard.")
        print(f"Go to {supabase_url}/sql to execute the script manually.")

    except Exception as e:
        print(f"Error executing SQL script: {e}")

if __name__ == '__main__':
    config = get_supabase_config()
    supabase_url = config.get('supabase_url')
    supabase_anon_key = config.get('supabase_anon_key')
    sql_script_path = os.path.join(os.path.dirname(__file__), '../database/database.sql')

    if supabase_url and supabase_anon_key:
        print("Supabase configuration found. Attempting to connect...")
        execute_sql_via_api(supabase_url, supabase_anon_key, sql_script_path)
    else:
        print("Supabase configuration not found in config.yaml.")
