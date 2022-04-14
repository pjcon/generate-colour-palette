use clientdb

DROP TABLE IF EXISTS ColourTest;
CREATE TABLE ColourTest (
    timestamp TIMESTAMP NOT NULL,
    cores INT NOT NULL,
    site VARCHAR(255),
    vo VARCHAR(255)
);
