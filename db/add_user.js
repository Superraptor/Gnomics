// add_user.js

const sqlite3 = require('sqlite3').verbose();

let db = new sqlite3.Database(__dirname + '/store/gnomics.db', sqlite3.OPEN_READWRITE, (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log("Connected to the GNOMICS database.");
});

const bcrypt = require('bcrypt');
const salt_rounds = 10;

var email = "sample_email@gmail.com";
var username = "fake";
var plaintext_password = "passwd";
var chemspider_api_key = "idfjiosfjos";
var umls_username = "idfjiosfjos";
var umls_password = "idfjiosfjos";
var umls_api_key = "idfjiosfjos";
var eol_api_key = "idfjiosfjos";

bcrypt.genSalt(salt_rounds, function(err, salt) {
    bcrypt.hash(plaintext_password, salt, null, function(err, hash) {
        console.log("Adding user...");
        db.serialize(function() {
            db.run('INSERT INTO users(email, username, password, chemspider_api_key, umls_username, umls_password, umls_api_key, eol_api_key) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', [email, username, hash, chemspider_api_key, umls_username, umls_password, umls_api_key, eol_api_key], function(err) {
                if (err) {
                    return console.log(err.message);
                }
                console.log("User added.");
            });
        });
    });
});