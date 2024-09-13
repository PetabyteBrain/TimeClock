create database IF NOT EXISTS TimeClockDB;
use TimeClockDB;

create table User(
	id int PRIMARY KEY,
    FOREIGN KEY (onlineTime_Fid) 
      REFERENCES OnlineTime (id),
	FOREIGN KEY (totalTime_Fid) 
      REFERENCES TotalTime (id),
    FOREIGN KEY (permission_Fid) 
      REFERENCES Permission (id),
    firstName varchar(255),
    lastName varchar(255),
    tagNum varchar(255),
    email varchar(255),
    password text	/* sha2("your passsword", 512) */
    );
    
create table Permissions(
	id int PRIMARY KEY,
    permissionLevel varchar(255),
    title varchar(255)
    );

create table TotalTime(
	id int PRIMARY KEY,
    FOREIGN KEY (user_Fid) 
      REFERENCES User (id),
	FOREIGN KEY (onlineTime_Fid) 
      REFERENCES OnlineTime (id),
    sumTime varchar(255),
    daysWorked varchar(255),
    breakTime varchar(255)
    );
    
create table OnlineTime(
	id int PRIMARY KEY,
    FOREIGN KEY (user_Fid) 
      REFERENCES User (id),
	FOREIGN KEY (totalTime_Fid) 
      REFERENCES TotalTime (id),
    dateTimeStart datetime,
    dateTimeStop datetime,
    break int
    );

select * from User;
select * from Permissions;
select * from TotalTime;
select * from OnlineTime;
show tables;
/*
drop database TimeClockDB;
*/