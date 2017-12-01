// edit_profile.js

function validateEmail(email) {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

async function edit_profile(user_name, user_email, user_password, new_user_password, repeat_new_user_password, user_chemspider_api_key, user_umls_username, user_umls_password, user_umls_api_key, user_eol_api_key, user_dpla_api_key, user_elsevier_api_key, user_fda_api_key, user_isbndb_api_key, user_ncbo_api_key, user_omim_api_key, user_openphacts_app_id, user_openphacts_app_key, user_springer_api_key, callback) {
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
            bcrypt.hash(new_user_password, salt, null, function(err, new_hash) {
                console.log("Updating user...");

                db.get("SELECT * FROM users WHERE email = ?", [user_email], (err, row) => {
                    if (err) {
                        console.error(err.message);
                    };
                    if(row) {
                        bcrypt.compare(user_password, row.password, function (err, doesMatch) {
                            if (doesMatch) {
                                
                                db.run('UPDATE users SET username = ?, password = ?, chemspider_api_key = ?, umls_username = ?, umls_password = ?, umls_api_key = ?, eol_api_key = ?, dpla_api_key = ?, elsevier_api_key = ?, fda_api_key = ?, isbndb_api_key = ?, ncbo_api_key = ?, omim_api_key = ?, openphacts_app_id = ?, openphacts_app_key = ?, springer_api_key = ? WHERE email = ?', [user_name, new_hash, user_chemspider_api_key, user_umls_username, user_umls_password, user_umls_api_key, user_eol_api_key, user_dpla_api_key, user_elsevier_api_key, user_fda_api_key, user_isbndb_api_key, user_ncbo_api_key, user_omim_api_key, user_openphacts_app_id, user_openphacts_app_key, user_springer_api_key, user_email], function(err) {
                                    if (err) {
                                        return console.log(err.message);
                                    }
                                    console.log("User updated.");
                                    console.log(`Row(s) updated ${this.changes}`);
                                    
                                    db.get("SELECT * FROM users WHERE email = ?", [user_email], (err, row) => {
                                        if (err) {
                                            console.error(err.message);
                                        };
                                        if(row) {
                                            callback(row);
                                        } else {
                                            console.log("Email not found. Please create an account or try another email.")
                                        }
                                    });
                                });
                                
                            } else {
                                // Return that there was no match.
                                console.log("Update was not successful.");
                            }
                        });
                    } else {
                        console.log("Email not found. Please create an account or try another email.");
                    }
                });
            });
        });
    } else {
        bcrypt.genSalt(salt_rounds, function(err, salt) {
            bcrypt.hash(new_user_password, salt, null, function(err, new_hash) {
                console.log("Updating user...");
                
                db.get("SELECT * FROM users WHERE username = ?", [user_name], (err, row) => {
                    if (err) {
                        console.error(err.message);
                    };
                    if(row) {
                        bcrypt.compare(user_password, row.password, function (err, doesMatch) {
                            if (doesMatch) {
                                
                                db.run('UPDATE users SET email = ?, password = ?, chemspider_api_key = ?, umls_username = ?, umls_password = ?, umls_api_key = ?, eol_api_key = ?, dpla_api_key = ?, elsevier_api_key = ?, fda_api_key = ?, isbndb_api_key = ?, ncbo_api_key = ?, omim_api_key = ?, openphacts_app_id = ?, openphacts_app_key = ?, springer_api_key = ? WHERE username = ?', [user_email, new_hash, user_chemspider_api_key, user_umls_username, user_umls_password, user_umls_api_key, user_eol_api_key, user_dpla_api_key, user_elsevier_api_key, user_fda_api_key, user_isbndb_api_key, user_ncbo_api_key, user_omim_api_key, user_openphacts_app_id, user_openphacts_app_key, user_springer_api_key, user_name], function(err) {
                                    if (err) {
                                        return console.log(err.message);
                                    }
                                    console.log("User updated.");
                                    console.log(`Row(s) updated ${this.changes}`);
                                    
                                    db.get("SELECT * FROM users WHERE username = ?", [user_name], (err, row) => {
                                        if (err) {
                                            console.error(err.message);
                                        };
                                        if(row) {
                                            callback(row);
                                        } else {
                                            console.log("Username not found. Please create an account or try another username.")
                                        }
                                    });
                                    
                                });
                            } else {
                                // Return that there was no match.
                                console.log("Update was not successful.");
                            }
                        });
                    } else {
                        console.log("Username not found. Trying with email...")
                        if (user_email == null) {
                            console.log("Email not found. Please create an account or try another email.");
                        } else {
                            
                            db.get("SELECT * FROM users WHERE email = ?", [user_email], (err, row) => {
                                if (err) {
                                    console.error(err.message);
                                };
                                if(row) {
                                    bcrypt.compare(user_password, row.password, function (err, doesMatch) {
                                        if (doesMatch) {

                                            db.run('UPDATE users SET username = ?, password = ?, chemspider_api_key = ?, umls_username = ?, umls_password = ?, umls_api_key = ?, eol_api_key = ?, dpla_api_key = ?, elsevier_api_key = ?, fda_api_key = ?, isbndb_api_key = ?, ncbo_api_key = ?, omim_api_key = ?, openphacts_app_id = ?, openphacts_app_key = ?, springer_api_key = ? WHERE email = ?', [user_name, new_hash, user_chemspider_api_key, user_umls_username, user_umls_password, user_umls_api_key, user_eol_api_key, user_dpla_api_key, user_elsevier_api_key, user_fda_api_key, user_isbndb_api_key, user_ncbo_api_key, user_omim_api_key, user_openphacts_app_id, user_openphacts_app_key, user_springer_api_key, user_email], function(err) {
                                                if (err) {
                                                    return console.log(err.message);
                                                }
                                                console.log("User updated.");
                                                console.log(`Row(s) updated ${this.changes}`);
                                                
                                                db.get("SELECT * FROM users WHERE email = ?", [user_email], (err, row) => {
                                                    if (err) {
                                                        console.error(err.message);
                                                    };
                                                    if(row) {
                                                        callback(row);
                                                    } else {
                                                        console.log("Email not found. Please create an account or try another email.")
                                                    }
                                                });
                                                
                                            });

                                        } else {
                                            // Return that there was no match.
                                            console.log("Update was not successful.");
                                        }
                                    });
                                } else {
                                    console.log("Email not found. Please create an account or try another email.");
                                }
                            });
                        }
                    }
                });
            });
        });
    };
    
    db.close();
    
};