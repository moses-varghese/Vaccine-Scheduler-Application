CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Patient (
    Username_P varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username_P)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Appointment (
    appointment_id varchar(255),
    Time date,
    Username_P varchar(255) REFERENCES Patient,
    Username varchar(255) REFERENCES Caregivers,
    Name varchar(255) REFERENCES Vaccines,
    PRIMARY KEY (appointment_id)
);