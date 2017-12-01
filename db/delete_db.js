// delete_db.js

const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database(__dirname + '/store/gnomics.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log("Connected to the GNOMICS database.");
});

console.log("Dropping 'user' table in GNOMICS...");
db.serialize(function() {
    db.run("DROP TABLE IF EXISTS users;");
});
console.log("'user' table in GNOMICS dropped.");

db.close();