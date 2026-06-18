CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE Destinations (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    value TEXT NOT NULL,
    UNIQUE (title, value)
);

CREATE TABLE DestinationCategories (
    id INTEGER PRIMARY KEY,
    destination_id INTEGER,
    title TEXT,
    value TEXT,
    FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id) ON DELETE CASCADE
);

CREATE TABLE Images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id) ON DELETE CASCADE
);

CREATE TABLE Comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

INSERT INTO Categories (title, value) VALUES 
('Hinta', 'halpa'),
('Hinta', 'kohtalainen'),
('Hinta', 'kallis'),
('Lemmikit', 'sallittu'),
('Lemmikit', 'ei sallittu'),
('Aamiainen', 'sisältyy'),
('Aamiainen', 'ei sisälly'),
('Näköala', 'meri'),
('Näköala', 'kaupunki'),
('Näköala', 'vuoristo');