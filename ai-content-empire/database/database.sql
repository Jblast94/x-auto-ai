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

-- Database function for daily summary
CREATE OR REPLACE FUNCTION get_daily_revenue_summary(start_date DATE)
RETURNS TABLE(platform TEXT, total_revenue DECIMAL, transaction_count BIGINT) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.platform,
        SUM(r.amount) as total_revenue,
        COUNT(r.*) as transaction_count
    FROM revenue_events r
    WHERE r.created_at >= start_date
    GROUP BY r.platform;
END; 
$$ LANGUAGE plpgsql;
