-- CREATE DATABASE
CREATE DATABASE House;

-- CREATE TABLES
-- CREATE TABLES FOR OLD SUBDIVISION
DROP TABLE IF EXISTS `old_subdivision`;
CREATE TABLE old_subdivision(
    id					INT,
    district			INT,
    sub_url				varchar(20),
    photo				varchar(120),
    build_year			INT,
    house_name			varchar(20),
    address				varchar(30),
    price				varchar(10) NOT NULL,
    property_company	varchar(30),
    developer			varchar(30),
    property_fee		varchar(20),
    house_type			varchar(10),
    surr_envi			varchar(220),
    surr_school			varchar(240),
    surr_traffic		varchar(220),
    surr_business		varchar(200),
    surr_entertain		varchar(210),
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- CREATE TABLE FOR OLD HOUSE (WEAK ENTITY)
DROP TABLE IF EXISTS `old_house`;
CREATE TABLE old_house(
    h_num		INT,
    s_num		INT,
    agent_id 	INT,
    photo		varchar(120),
    room_num	varchar(80) NOT NULL,
    area		varchar(600) NOT NULL,
    price		varchar(10) NOT NULL,
    status		INT,
    orientation	varchar(5),
    PRIMARY KEY (h_num, s_num)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- CREATE MEW SUBDIVISION
DROP TABLE IF EXISTS `new_subdivision`;
CREATE TABLE new_subdivision(
    id					INT,
    district			INT,
    sub_url				varchar(20),
    photo				varchar(120),
    house_name			varchar(20),
    house_status		varchar(5),
    house_type			varchar(10),
    address				varchar(30),
    price				varchar(10) NOT NULL,
    developer			varchar(30),
    surr_traffic		varchar(220),
    surr_school			varchar(240),
    surr_environment	varchar(220),
    surr_business		varchar(200),
    surr_entertain		varchar(210),
    property_fee		varchar(20),
    property_company	varchar(30),
    PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- CREATE TABLE FOR NEW HOUSE (WEAK ENTITY)
DROP TABLE IF EXISTS `new_house`;
CREATE TABLE new_house(
    h_num		INT,
    s_num		INT,
    agent_id 	INT,
    photo		varchar(120),
    room_num	varchar(80) NOT NULL,
    area		varchar(600) NOT NULL,
    price		varchar(10) NOT NULL,
    orientation	varchar(5),
    PRIMARY KEY (h_num, s_num)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- CREATE TABLE FOR USERS
DROP TABLE IF EXISTS `users`;
CREATE TABLE users(
    u_id		INT,
    name	    varchar(30) NOT NULL,
    password	varchar(20) NOT NULL,
    email		varchar(40),
    PRIMARY KEY (u_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- CREATE TABLE FOR AGENTS
DROP TABLE IF EXISTS `agents`;
CREATE TABLE agents(
    u_id		INT,
    name	    varchar(30) NOT NULL,
    password	varchar(20) NOT NULL,
    email		varchar(60),
    phone		varchar(20),
    hire_date	varchar(30) NOT NULL,
    intro		varchar(200),
    PRIMARY KEY (u_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- CREATE TABLE FOR ADMINS
DROP TABLE IF EXISTS `admins`;
CREATE TABLE admins(
    u_id	    INT,
    name	    varchar(30) NOT NULL,
    password	varchar(20) NOT NULL,
    email		varchar(40),
    PRIMARY KEY (u_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- CREATE TABLE FOR DISTRICT
DROP TABLE IF EXISTS `district`;
CREATE TABLE district(
    d_id	INT,
    name	varchar(10),
    PRIMARY KEY (d_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- CREATE TABLE FOR OLD FAV
DROP TABLE IF EXISTS `old_fav`;
CREATE TABLE old_fav(
    sub_id	INT,
    u_id	INT,
    PRIMARY KEY (sub_id, u_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- CREATE TABLE FOR NEW FAV
DROP TABLE IF EXISTS `new_fav`;
CREATE TABLE new_fav(
    sub_id	INT,
    u_id	INT,
    PRIMARY KEY (sub_id, u_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- CREATE TABLE FOR OLD APPLY
DROP TABLE IF EXISTS `old_apply`;
CREATE TABLE old_apply(
    user_id		INT,
    sub_id		INT,
    house_id	INT,
    message		varchar(200),
    PRIMARY KEY(user_id, house_id, sub_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- CREATE TABLE FRO NEW APPLY
DROP TABLE IF EXISTS `new_apply`;
CREATE TABLE new_apply(
    user_id		INT,
    sub_id		INT,
    house_id	INT,
    message		varchar(200),
    PRIMARY KEY(user_id, house_id, sub_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- CREATE TABLE FOR MVP
DROP TABLE IF EXISTS `mvp`;
CREATE TABLE mvp(
    agent_id	INT,
    admin_id	INT,
    date		varchar(15) NOT NULL,
    PRIMARY KEY (agent_id, admin_id, date)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- FOREIGN KEY DECLARATION

-- old
ALTER TABLE old_subdivision ADD FOREIGN KEY (district)REFERENCES district(d_id);
ALTER TABLE old_house ADD FOREIGN KEY (s_num)REFERENCES old_subdivision(id);
-- new
ALTER TABLE new_subdivision ADD FOREIGN KEY (district)REFERENCES district(d_id);
ALTER TABLE new_house ADD FOREIGN KEY (s_num)REFERENCES new_subdivision(id);
-- old_fav
ALTER TABLE old_fav ADD FOREIGN KEY (sub_id)REFERENCES old_subdivision(id);
-- new_fav
ALTER TABLE new_fav ADD FOREIGN KEY (sub_id)REFERENCES new_subdivision(id);
-- mvp
ALTER TABLE mvp ADD FOREIGN KEY (admin_id)REFERENCES admins(u_id);

-- add data into users
LOAD DATA INFILE 'users.txt'
INTO TABLE users
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(u_id, name, password, email);

-- add data into agents
LOAD DATA INFILE 'agents.txt'
INTO TABLE agents
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(u_id, name, password, email, phone, hire_date, intro);

-- add data into district
LOAD DATA INFILE 'district.txt'
INTO TABLE district
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into old_subdivision
LOAD DATA INFILE 'old_subdivision.txt'
INTO TABLE old_subdivision
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into old_house
LOAD DATA INFILE 'old_house.txt'
INTO TABLE old_house
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into new_subdivision
LOAD DATA INFILE 'new_subdivision.txt'
INTO TABLE new_subdivision
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into new_house
LOAD DATA INFILE 'new_house.txt'
INTO TABLE new_house
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into admins
LOAD DATA INFILE 'admin.csv'
INTO TABLE admins
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into mvp
LOAD DATA INFILE 'mvp.txt'
INTO TABLE mvp
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into old_apply
LOAD DATA INFILE 'old_apply.csv'
INTO TABLE old_apply
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into new_apply
LOAD DATA INFILE 'new_apply.txt'
INTO TABLE new_apply
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into old_fav
LOAD DATA INFILE 'old_fav.csv'
INTO TABLE old_fav
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- add data into new_fav
LOAD DATA INFILE 'new_fav.txt'
INTO TABLE new_fav
CHARACTER SET utf8
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;