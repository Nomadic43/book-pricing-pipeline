CREATE TABLE IF NOT EXISTS staging_exchange_rates(
    rate_date DATE PRIMARY KEY,
    base_currency VARCHAR(3) NOT NULL,
    target_currency VARCHAR(3) NOT NULL,
    rate NUMERIC(10, 4) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw_products(
    scrapped_date DATE NOT NULL,
    title TEXT,
    price_gbp NUMERIC(10,2),
    category TEXT,
    availability TEXT 
);

CREATE TABLE IF NOT EXISTS products(
    product_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    availability_count INTEGER,
    price_gbp NUMERIC(10, 2),
    price_inr NUMERIC(10, 2),
    price_tier TEXT,
    rate_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);