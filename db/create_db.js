// create_db.js

const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database(__dirname + '/store/gnomics.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log("Connected to the newly created GNOMICS database.");
});

/*
    email (https://tools.ietf.org/html/rfc5321.html):
    - Length for the domain name is 255 octets.
    - Length of the user name / local-part is 64 octets.
    - The '@' symbol is a single octet.
    - This brings the total to 320 characters.
    username
    - Length of 25
    password
    - Length of 59-60 bytes based on modular crypt format.
    chemspider_api_key
    - Length of 36
    umls_username
    - Length of 20
    umls_password
    - Length of 50
    umls_api_key
    - Length of 36
    eol_api_key
    - Length of 40
    dpla_api_key
    - Length of 32
    elsevier_api_key
    - Length of 32
    fda_api_key
    - Length of 40
    isbndb_api_key
    - Length of 8
    ncbo_api_key
    - Length of 36
    omim_api_key
    - Length of 22
    openphacts_app_id
    - Length of 8
    openphacts_app_key
    - Length of 32
    springer_api_key
    - Length of 32
*/
console.log("Creating 'users' table in GNOMICS...");
db.serialize(function() {
    db.run("DROP TABLE IF EXISTS users;");
    
    db.run("CREATE TABLE users (" +
           "email VARCHAR(320) PRIMARY KEY, " +
           "username VARCHAR(25) UNIQUE, " +
           "password BINARY(60) NOT NULL, " +
           "chemspider_api_key VARCHAR(36) UNIQUE, " +
           "umls_username VARCHAR(20) UNIQUE, " +
           "umls_password VARCHAR(50) UNIQUE, " +
           "umls_api_key VARCHAR(36) UNIQUE, " +
           "eol_api_key VARCHAR(40) UNIQUE, " +
           "dpla_api_key VARCHAR(32) UNIQUE, " +
           "elsevier_api_key VARCHAR(32) UNIQUE, " +
           "fda_api_key VARCHAR(40) UNIQUE, " +
           "isbndb_api_key VARCHAR(8) UNIQUE, " +
           "ncbo_api_key VARCHAR(36) UNIQUE, " +
           "omim_api_key VARCHAR(22) UNIQUE, " +
           "openphacts_app_id VARCHAR(8) UNIQUE, " +
           "openphacts_app_key VARCHAR(32) UNIQUE, " +
           "springer_api_key VARCHAR(32) UNIQUE " +
           ");");
});
console.log("Created 'users' table in GNOMICS.");

db.close();