CREATE DATABASE IF NOT EXISTS TimeClockDB;
USE TimeClockDB;

CREATE TABLE Permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    permissionLevel VARCHAR(255),
    title VARCHAR(255)
);

CREATE TABLE `User` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    tagNum VARCHAR(255),
    email VARCHAR(255),
    password TEXT, /* sha2("your password", 512) */
    permission_id INT,
    FOREIGN KEY (permission_id) REFERENCES Permissions(id)
);

CREATE TABLE OnlineTime (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dateTimeStart DATETIME,
    dateTimeStop DATETIME,
    breakTime INT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES `User`(id)
);

CREATE TABLE TotalTime (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sumTime TIME,
    daysWorked INT,
    breakTime TIME,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES `User`(id)
);

-- Test the schema with select queries
SELECT * FROM `User`;
SELECT * FROM Permissions;
SELECT * FROM TotalTime;
SELECT * FROM OnlineTime;

-- Display tables in the database
SHOW TABLES;


-- DROP DATABASE TimeClockDB;

