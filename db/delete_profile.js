// delete_profile.js

function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

async function delete_profile(user_name, user_email, user_password, callback) {
    const sqlite3 = require('sqlite3').verbose();
    const bcrypt = require('bcrypt');
    const express = require('express');
    var app = express();
    const session = require('express-session');
    const cookieParser = require('cookie-parser');
    const salt_rounds = 10;
    
    // Note that __dirname will not work when called
    // within this file.
    let db = new sqlite3.Database(__dirname + '/db/store/gnomics.db', sqlite3.OPEN_READWRITE, (err) => {
        if (err) {
            console.error(err.message);
        }
        console.log("Connected to the GNOMICS database.");
    });
    
    if (user_name == null) {
        bcrypt.genSalt(salt_rounds, function(err, salt) {
            console.log("Deleting user...");
            db.serialize(function() {
                db.run('DELETE FROM users WHERE email = ? AND password = ?', [user_email, user_password], function(err) {
                    if (err) {
                        return console.log(err.message);
                    }
                    console.log("User deleted.");
                    console.log(`Row(s) deleted ${this.changes}`);
                    callback(true);
                });
            });
        });
    } else {
        bcrypt.genSalt(salt_rounds, function(err, salt) {
            console.log("Deleting user...");
            db.serialize(function() {
                db.run('DELETE FROM users WHERE username = ? AND password = ?', [user_name, user_password], function(err) {
                    if (err) {
                        return console.log(err.message);
                    }
                    console.log("User deleted.");
                    console.log(`Row(s) deleted ${this.changes}`);
                    callback(true);
                });
            });
        });
    };
    
    db.close();
    
};