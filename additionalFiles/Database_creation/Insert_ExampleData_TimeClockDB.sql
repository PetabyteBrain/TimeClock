USE TimeClockDB;

-- Insert test data into the Permissions table
INSERT INTO Permissions (permissionLevel, title) VALUES 
('Admin', 'Administrator'),
('User', 'Standard User'),
('Manager', 'Manager'),
('Supervisor', 'Supervisor'),
('HR', 'Human Resources'),
('Guest', 'Guest Access');

-- Insert test data into the OnlineTime table
INSERT INTO OnlineTime (dateTimeStart, dateTimeStop, break) VALUES 
('2024-10-20 08:00:00', '2024-10-20 17:00:00', 30),
('2024-10-21 09:00:00', '2024-10-21 18:00:00', 60),
('2024-10-22 08:30:00', '2024-10-22 16:30:00', 45),
('2024-10-22 07:45:00', '2024-10-22 16:45:00', 60),
('2024-10-23 08:30:00', '2024-10-23 17:00:00', 30),
('2024-10-23 09:00:00', '2024-10-23 18:00:00', 45),
('2024-10-24 08:00:00', '2024-10-24 16:30:00', 60),
('2024-10-24 09:15:00', '2024-10-24 17:45:00', 30);

-- Insert test data into the TotalTime table
INSERT INTO TotalTime (sumTime, daysWorked, breakTime) VALUES 
('9 hours', '1 day', '30 minutes'),
('8 hours', '2 days', '1 hour'),
('8 hours', '3 days', '45 minutes'),
('8 hours', '4 days', '1 hour'),
('7.5 hours', '5 days', '30 minutes'),
('9 hours', '6 days', '45 minutes'),
('8.5 hours', '7 days', '1 hour'),
('9.5 hours', '8 days', '30 minutes');

-- Insert test data into the User table
INSERT INTO User (firstName, lastName, tagNum, email, password, permission_Fid, onlineTime_Fid, totalTime_Fid) VALUES 
('John', 'Doe', 'TAG123', 'johndoe@example.com', SHA2('password123', 512), 1, 1, 1),
('Jane', 'Smith', 'TAG456', 'janesmith@example.com', SHA2('password456', 512), 2, 2, 2),
('Tom', 'Brown', 'TAG789', 'tombrown@example.com', SHA2('password789', 512), 3, 3, 3),
('Alice', 'Johnson', 'TAG101', 'alice.johnson@example.com', SHA2('alicepass', 512), 4, 4, 4),
('Bob', 'Williams', 'TAG102', 'bob.williams@example.com', SHA2('bobpass', 512), 5, 5, 5),
('Carol', 'Davis', 'TAG103', 'carol.davis@example.com', SHA2('carolpass', 512), 6, 6, 6),
('David', 'Miller', 'TAG104', 'david.miller@example.com', SHA2('davidpass', 512), 3, 7, 7),
('Eve', 'Wilson', 'TAG105', 'eve.wilson@example.com', SHA2('evepass', 512), 2, 8, 8);

-- Update the TotalTime table to link users and online time
UPDATE TotalTime SET user_Fid = 1, onlineTime_Fid = 1 WHERE id = 1;
UPDATE TotalTime SET user_Fid = 2, onlineTime_Fid = 2 WHERE id = 2;
UPDATE TotalTime SET user_Fid = 3, onlineTime_Fid = 3 WHERE id = 3;
UPDATE TotalTime SET user_Fid = 4, onlineTime_Fid = 4 WHERE id = 4;
UPDATE TotalTime SET user_Fid = 5, onlineTime_Fid = 5 WHERE id = 5;
UPDATE TotalTime SET user_Fid = 6, onlineTime_Fid = 6 WHERE id = 6;
UPDATE TotalTime SET user_Fid = 7, onlineTime_Fid = 7 WHERE id = 7;
UPDATE TotalTime SET user_Fid = 8, onlineTime_Fid = 8 WHERE id = 8;

-- Update the OnlineTime table to link users and total time
UPDATE OnlineTime SET user_Fid = 1, totalTime_Fid = 1 WHERE id = 1;
UPDATE OnlineTime SET user_Fid = 2, totalTime_Fid = 2 WHERE id = 2;
UPDATE OnlineTime SET user_Fid = 3, totalTime_Fid = 3 WHERE id = 3;
UPDATE OnlineTime SET user_Fid = 4, totalTime_Fid = 4 WHERE id = 4;
UPDATE OnlineTime SET user_Fid = 5, totalTime_Fid = 5 WHERE id = 5;
UPDATE OnlineTime SET user_Fid = 6, totalTime_Fid = 6 WHERE id = 6;
UPDATE OnlineTime SET user_Fid = 7, totalTime_Fid = 7 WHERE id = 7;
UPDATE OnlineTime SET user_Fid = 8, totalTime_Fid = 8 WHERE id = 8;

-- Test the data with select queries
SELECT * FROM Permissions;
SELECT * FROM OnlineTime;
SELECT * FROM TotalTime;
SELECT * FROM User;
