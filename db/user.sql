CREATE DATABASE IF NOT EXISTS practice;

USE practice;

DROP TABLE IF EXISTS user;

CREATE TABLE
    user (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        name VARCHAR(50) NOT NULL,
        email varchar(100) NOT NULL,
        phone INT UNSIGNED NOT NULL,
        address varchar(250) NOT NULL,
        PRIMARY KEY (id)
    );

INSERT INTO
    user (id, name, email, phone, address)
VALUES (
        1,
        'Bruce Wayne',
        'brucewayne@gmail.com',
        218928398,
        'Earth'
    ), (
        2,
        'Barry Allen',
        'barryallen@gmail.com',
        423234324,
        'Earth'
    );