CREATE TABLE emissions (
    id SERIAL PRIMARY KEY,
    country VARCHAR(100),
    year INTEGER,
    co2_emission NUMERIC,
    co2_per_capita NUMERIC,
    population NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
