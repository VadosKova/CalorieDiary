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
    [Goal] VARCHAR(50) CHECK ([Goal] IN ('weight loss', 'maintenance', 'weight gain'))
)

CREATE TABLE [Meal] (
    [MealId] INT IDENTITY(1,1) PRIMARY KEY,
    [UserId] INT,
    [FoodName] VARCHAR(100) NOT NULL,
    [WeightInGrams] FLOAT CHECK ([WeightInGrams] > 0),
    [CaloriesPer100g] FLOAT CHECK ([CaloriesPer100g] > 0),
    FOREIGN KEY (UserId) REFERENCES [Users](UserId)
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