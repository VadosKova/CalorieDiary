--CREATE DATABASE [CalorieDiary]

USE [CalorieDiary]
GO

CREATE TABLE [Users](
	[UserId] INT IDENTITY(1,1) PRIMARY KEY,
    [Username] VARCHAR(50) NOT NULL,
    [Email] VARCHAR(100) NOT NULL UNIQUE,
    [Password] NVARCHAR(100) NOT NULL,
    [Gender] CHAR(1) CHECK ([Gender] IN ('M', 'F')),
    [Age] INT CHECK (Age > 0),
    [Weight] FLOAT CHECK ([Weight] > 0),
    [Height] FLOAT CHECK ([Height] > 0),
    [Goal] VARCHAR(50) CHECK ([Goal] IN ('weight loss', 'maintenance', 'weight gain')),
	[ActivityLevel] VARCHAR(20) DEFAULT 'medium' CHECK ([ActivityLevel] IN ('low', 'medium', 'high'))
)

CREATE TABLE [Meals] (
    [MealId] INT IDENTITY(1,1) PRIMARY KEY,
    [UserId] INT NOT NULL,
    [ProductName] VARCHAR(100) NOT NULL,
    [Weight] FLOAT CHECK ([Weight] > 0),
    [CaloricValue] FLOAT CHECK ([CaloricValue] > 0),
    FOREIGN KEY (UserId) REFERENCES Users(UserId)
)

CREATE TABLE [Activity] (
    [ActivityId] INT IDENTITY(1,1) PRIMARY KEY, 
    [UserId] INT,
    [CalorieIntake] FLOAT CHECK (CalorieIntake > 0),
    [ActivityDate] DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UserId) REFERENCES [Users](UserId)
)

CREATE TABLE [History] (
    [HistoryId] INT IDENTITY(1,1) PRIMARY KEY,
    [UserId] INT,
    [Type] VARCHAR(50) CHECK ([Type] IN ('meal', 'activity')) NOT NULL, 
    [Date] DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (UserId) REFERENCES [Users](UserId)
)