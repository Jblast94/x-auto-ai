import os
import yaml

def get_supabase_config():
    """Reads the Supabase configuration from the config file."""
    config_path = os.path.join(os.path.dirname(__file__), '../config/config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def generate_sql_script():
    """Generates the SQL script for the database schema."""
    sql_script = """
-- Revenue tracking tables
CREATE TABLE revenue_sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    platform TEXT NOT NULL,
    type TEXT NOT NULL, -- 'subscription', 'tip', 'affiliate', 'custom'
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE revenue_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES revenue_sources(id),
    amount DECIMAL(10,2) NOT NULL,
    currency TEXT DEFAULT 'USD',
    content_id UUID,
    platform TEXT NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE content_performance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    content_id UUID NOT NULL,
    platform TEXT NOT NULL,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    shares INT DEFAULT 0,
    comments INT DEFAULT 0,
    revenue_generated DECIMAL(10,2) DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Content storage table
CREATE TABLE content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    text TEXT NOT NULL,
    image TEXT NOT NULL,
    platform TEXT NOT NULL,
    character TEXT NOT NULL,
    scheduled_time TIMESTAMPTZ NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Analytics view
CREATE VIEW daily_revenue AS
SELECT 
    DATE(created_at) as date,
    platform,
    SUM(amount) as total_revenue,
    COUNT(*) as transaction_count
FROM revenue_events
GROUP BY DATE(created_at), platform
ORDER BY date DESC;
"""
    return sql_script

if __name__ == '__main__':
    config = get_supabase_config()
    supabase_url = config.get('supabase_url')
    supabase_anon_key = config.get('supabase_anon_key')

    if supabase_url and supabase_anon_key:
        print("Supabase configuration found.")
        sql_script = generate_sql_script()
        print("SQL script to be executed:")
        print(sql_script)
        print("\nNOTE: Manual execution of the SQL script is required via the Supabase dashboard.")
        print(f"Go to {supabase_url}/sql to execute the script manually.")
    else:
        print("Supabase configuration not found in config.yaml.")
