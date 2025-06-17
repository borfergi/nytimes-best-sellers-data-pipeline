-- Create books table
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    title TEXT NOT NULL,
    author TEXT,
    description TEXT,
    publisher TEXT,
    book_uri TEXT, 
    amazon_url TEXT, 
    category TEXT,
    rank INTEGER,
    rank_last_week INTEGER,
    weeks_on_list INTEGER
);

-- Truncate table in case it already exists
TRUNCATE TABLE books;