DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  phone_country VARCHAR(4) NOT NULL,
  phone_area VARCHAR(255) NOT NULL,                 /* 3 digits NXX where N=2-9 */
  phone_central_office_code1 VARCHAR(255) NOT NULL, /* 3 digits NXX where X=0-9 */
  phone_central_office_code2 VARCHAR(255) NOT NULL, /* 3 digits XXX */
  email VARCHAR(255) NOT NULL
);

INSERT INTO customers VALUES(DEFAULT, 'John Doe',       '+1', '202', '555', '0033', 'john.doe@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Angel Mate',     '+1', '202', '555', '0467', 'angel.mate@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Mister Ed',      '+1', '225', '555', '0163', 'horse@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Oscar Wilde',    '+1', '225', '555', '0114', 'oscar.w@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Rapton',         '+1', '307', '555', '0126', 'rapton@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Ana Margarida',  '+1', '307', '555', '0182', 'a.margarida@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Ink Mate',       '+1', '808', '555', '0193', 'ink.mate@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Iron Maiden',    '+1', '808', '555', '0162', 'iron.maiden@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Sepultura',      '+1', '614', '555', '0165', 'sepultura@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Morbid Angel',   '+1', '614', '555', '0154', 'm.angel@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Sentenced',      '+1', '605', '555', '0137', 'sentenced@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Agnostic Front', '+1', '605', '555', '0191', 'a.front@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'King Diamond',   '+1', '785', '555', '0182', 'King Diamond@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Accept',         '+1', '785', '555', '0131', 'accept@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Uriah Heep',     '+1', '202', '555', '0141', 'uriah@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'John Travolta',  '+1', '502', '555', '0104', 'trav@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Local Hero',     '+1', '502', '555', '0132', 'l.hero@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Matrix',         '+1', '502', '555', '0144', 'm@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Bacalhau',       '+1', '803', '555', '0182', 'bac@hotmail.com');
INSERT INTO customers VALUES(DEFAULT, 'Kome Restus',    '+1', '515', '555', '0138', 'kome@hotmail.com');

SELECT * FROM customers;

