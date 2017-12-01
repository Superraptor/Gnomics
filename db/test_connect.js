// connect.js

const sqlite3 = require('sqlite3').verbose();

// Open a database in memory.
let db = new sqlite3.Database(':memory:', (err) => {
    if (err) {
        return console.error(err.message);
    }
    console.log("Connected to the in-memory SQlite database.");
});

// Close the database connection.
db.close((err) => {
    if (err) {
        return console.error(err.message);
    }
    console.log("Closed the database connection successfully.");
});