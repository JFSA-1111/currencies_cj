CREATE TABLE PRICE
(
    price_id        serial PRIMARY KEY,
    last_updated    TIMESTAMP   NOT NULL,
    time_registered TIMESTAMP   NOT NULL,
    value           float8      NOT NULL,
    service         VARCHAR(50) NOT NULL
);