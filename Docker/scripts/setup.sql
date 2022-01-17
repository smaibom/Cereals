CREATE DATABASE cereals;
GO
USE cereals;
GO
CREATE TABLE cerealuser(id INT IDENTITY(1,1) PRIMARY KEY,name VARCHAR(20), pwd VARCHAR(128));
GO
CREATE TABLE cereal (id INT IDENTITY(1,1) PRIMARY KEY, name VARCHAR(50),
                    mfr VARCHAR(50), type VARCHAR(50),
                    calories INT, protein INT,
                    fat INT, sodium INT,
                    fiber FLOAT, carbo FLOAT,
                    sugars INT, potass INT,
                    vitamins INT,shelf INT,
                    weight FLOAT, cups FLOAT,
                    rating INT);
GO
CREATE TABLE cerealpictures (
    id INT IDENTITY(1,1) PRIMARY KEY,
    cerealid INT FOREIGN KEY REFERENCES cereal(id) ON DELETE CASCADE, 
    picturepath VARCHAR(50));
GO

