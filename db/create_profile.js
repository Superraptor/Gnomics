// create_profile.js

function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

async function create_profile(user_name, user_email, user_password, user_chemspider_api_key, user_umls_username, user_umls_password, user_umls_api_key, user_eol_api_key, user_dpla_api_key, user_elsevier_api_key, user_fda_api_key, user_isbndb_api_key, user_ncbo_api_key, user_omim_api_key, user_openphacts_app_id, user_openphacts_app_key, springer_api_key, callback) {
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
    
    bcrypt.genSalt(salt_rounds, function(err, salt) {
        bcrypt.hash(user_password, salt, null, function(err, hash) {
            console.log("Adding user...");
            db.serialize(function() {
                db.run('INSERT INTO users(email, username, password, chemspider_api_key, umls_username, umls_password, umls_api_key, eol_api_key, dpla_api_key, elsevier_api_key, fda_api_key, isbndb_api_key, ncbo_api_key, omim_api_key, openphacts_app_id, openphacts_app_key, springer_api_key) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [user_email, user_name, hash, user_chemspider_api_key, user_umls_username, user_umls_password, user_umls_api_key, user_eol_api_key, user_dpla_api_key, user_elsevier_api_key, user_fda_api_key, user_isbndb_api_key, user_ncbo_api_key, user_omim_api_key, user_openphacts_app_id, user_openphacts_app_key, springer_api_key], function(err) {
                    if (err) {
                        return console.log(err.message);
                    }
                    console.log("User added.");
                    callback(true);
                });
            });
        });
    });
    
};