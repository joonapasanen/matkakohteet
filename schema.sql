CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE Destinations (
    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE Images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    image_url TEXT NOT NULL,
    FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id) ON DELETE CASCADE
);

CREATE TABLE Categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE DestinationCategories (
    destination_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (destination_id, category_id),
    FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE
);

CREATE TABLE Comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);