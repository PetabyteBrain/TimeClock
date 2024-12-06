USE TimeClockDB;

-- Insert data into Permissions table
INSERT INTO Permissions (permissionLevel, title)
VALUES
	('Dev', 'Developer'),
    ('Admin', 'Administrator'),
    ('Supervisor', 'Supervisor'),
    ('User', 'Standard User'),
    ('Guest', 'Guest User');

-- Insert data into User table
INSERT INTO `User` (firstName, lastName, tagNum, email, password, permission_id)
VALUES
    ('John', 'Doe', '12345', 'john.doe@example.com', SHA2('password1', 512), 1),
    ('Jane', 'Smith', '54321', 'jane.smith@example.com', SHA2('password2', 512), 2),
    ('Bob', 'Brown', '67890', 'bob.brown@example.com', SHA2('password3', 512), 3);

-- Insert data into OnlineTime table
INSERT INTO OnlineTime (dateTimeStart, dateTimeStop, breakTime, user_id)
VALUES
    ('2024-11-01 08:00:00', '2024-11-01 17:00:00', 60, 1),
    ('2024-11-02 09:00:00', '2024-11-02 18:00:00', 45, 2),
    ('2024-11-03 10:00:00', '2024-11-03 16:00:00', 30, 3);

-- Insert data into TotalTime table
INSERT INTO TotalTime (sumTime, daysWorked, breakTime, user_id)
VALUES
    ('40:00:00', 5, '5:00:00', 1),
    ('35:00:00', 4, '4:15:00', 2),
    ('25:00:00', 3, '2:30:00', 3);

-- Verify inserted data
SELECT * FROM Permissions;
SELECT * FROM `User`;
SELECT * FROM OnlineTime;
SELECT * FROM TotalTime;
