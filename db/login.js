// login.js

function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

async function login(user_supplied_email_or_username, user_supplied_password, callback) {
    const sqlite3 = require('sqlite3').verbose();
    const bcrypt = require('bcrypt');
    const express = require('express');
    var app = express();
    const session = require('express-session');
    const cookieParser = require('cookie-parser');
    
    // Note that __dirname will not work when called
    // within this file.
    let db = new sqlite3.Database(__dirname + '/db/store/gnomics.db', sqlite3.OPEN_READWRITE, (err) => {
        if (err) {
            console.error(err.message);
        }
        console.log("Connected to the GNOMICS database.");
    });

    // Check if email was used.
    if (validateEmail(user_supplied_email_or_username)) {
        console.log('Attempting login using email...')
        db.get("SELECT * FROM users WHERE email = ?", [user_supplied_email_or_username], (err, row) => {
            if (err) {
                console.error(err.message);
            };
            if(row) {
                bcrypt.compare(user_supplied_password, row.password, function (err, doesMatch) {
                    if (doesMatch) {
                        // Login!
                        console.log("Login was successful.");
                        console.log(row);
                        callback(row);
                    } else {
                        // Return that there was no match.
                        console.log("Login was not successful.");
                    }
                });
            } else {
                console.log("Email not found. Please create an account or try another email.")
            }
        });
    } else {
        console.log('Attempting login using username...')
        db.get("SELECT * FROM users WHERE username = ?", [user_supplied_email_or_username], (err, row) => {
            if (err) {
                console.error(err.message);
            };
            if(row) {
                bcrypt.compare(user_supplied_password, row.password, function (err, doesMatch) {
                    if (doesMatch) {
                        // Login!
                        console.log("Login was successful.");
                        callback(row);
                    } else {
                        // Return that there was no match.
                        console.log("Login was not successful.");
                    }
                });
            } else {
                console.log("Username not found. Please create an account or try another username.")
            }
        });
    };
};

// TODO: Figure this out!
var user_supplied_email_or_username = "yo@yahoo.com";
var user_supplied_password = "passwd";

login(user_supplied_email_or_username, user_supplied_password);