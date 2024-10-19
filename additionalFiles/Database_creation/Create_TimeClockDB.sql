CREATE DATABASE IF NOT EXISTS TimeClockDB;
USE TimeClockDB;

CREATE TABLE Permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    permissionLevel VARCHAR(255),
    title VARCHAR(255)
);

CREATE TABLE OnlineTime (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dateTimeStart DATETIME,
    dateTimeStop DATETIME,
    break INT
);

CREATE TABLE TotalTime (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sumTime VARCHAR(255),
    daysWorked VARCHAR(255),
    breakTime VARCHAR(255)
);

CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(255),
    lastName VARCHAR(255),
    tagNum VARCHAR(255),
    email VARCHAR(255),
    password TEXT, /* sha2("your password", 512) */
    permission_Fid INT,
    onlineTime_Fid INT,
    totalTime_Fid INT,
    FOREIGN KEY (permission_Fid) REFERENCES Permissions(id),
    FOREIGN KEY (onlineTime_Fid) REFERENCES OnlineTime(id),
    FOREIGN KEY (totalTime_Fid) REFERENCES TotalTime(id)
);

ALTER TABLE TotalTime 
    ADD user_Fid INT,
    ADD onlineTime_Fid INT,
    ADD FOREIGN KEY (user_Fid) REFERENCES User(id),
    ADD FOREIGN KEY (onlineTime_Fid) REFERENCES OnlineTime(id);

ALTER TABLE OnlineTime 
    ADD user_Fid INT,
    ADD totalTime_Fid INT,
    ADD FOREIGN KEY (user_Fid) REFERENCES User(id),
    ADD FOREIGN KEY (totalTime_Fid) REFERENCES TotalTime(id);

-- Test the schema with select queries
SELECT * FROM User;
SELECT * FROM Permissions;
SELECT * FROM TotalTime;
SELECT * FROM OnlineTime;

-- Display tables in the database
SHOW TABLES;

/*
DROP DATABASE TimeClockDB;
*/
