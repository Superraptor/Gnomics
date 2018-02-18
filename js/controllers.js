/*global angular, console, $, alert*/
/*jslint plusplus: true*/

/* Needed to reconnect to the existing client. */
const zerorpc = require("zerorpc");
var client = new zerorpc.Client(heartbeat=null, timeout=null, heartbeatInterval=10000000);
client.connect("tcp://127.0.0.1:4242");

/* Create app for sessions. */
const express = require('express');
var app = express();
const session = require('express-session');
const cookieParser = require('cookie-parser');

/* Add for opening external browser windows */
const shell = electron.shell;

/* Remote required for meta-window operations */
const remote = require('electron').remote;

(function () {
    'use strict';
    
    var gnomicsControllers = angular.module('gnomicsControllers', []);
    
    /* SERVICES */
    gnomicsControllers.service('SharedProperties', function () {
        var user_email, user_name, user_password_hash, chemspider_api_key, umls_username, umls_password, umls_api_key, eol_api_key, dpla_api_key, elsevier_api_key, fda_api_key, isbndb_api_key, ncbo_api_key, omim_api_key, openphacts_app_id, openphacts_app_key, springer_api_key, chemspider_security_token;
        
        var logged_in = false;
        
        this.setUserFields = function (result) {
            console.log("SET RESULT:")
            console.log(result);
            user_email = result.email;
            user_name = result.username;
            user_password_hash = result.password;
            chemspider_api_key = result.chemspider_api_key;
            chemspider_security_token = result.chemspider_api_key;
            umls_username = result.umls_username;
            umls_password = result.umls_password;
            umls_api_key = result.umls_api_key;
            eol_api_key = result.eol_api_key;
            dpla_api_key = result.dpla_api_key;
            elsevier_api_key = result.elsevier_api_key;
            fda_api_key = result.fda_api_key;
            isbndb_api_key = result.isbndb_api_key;
            ncbo_api_key = result.ncbo_api_key;
            omim_api_key = result.omim_api_key;
            openphacts_app_id = result.openphacts_app_id;
            openphacts_app_key = result.openphacts_app_key;
            springer_api_key = result.springer_api_key;
            
            logged_in = true;
        };
        
        this.getUserFields = function () {
            return {
                user_email: user_email,
                user_name: user_name,
                user_password_hash: user_password_hash,
                chemspider_api_key: chemspider_api_key,
                chemspider_security_token: chemspider_api_key,
                umls_username: umls_username,
                umls_password: umls_password,
                umls_api_key: umls_api_key,
                eol_api_key: eol_api_key,
                dpla_api_key: dpla_api_key,
                elsevier_api_key: elsevier_api_key,
                fda_api_key: fda_api_key,
                isbndb_api_key: isbndb_api_key,
                ncbo_api_key: ncbo_api_key,
                omim_api_key: omim_api_key,
                openphacts_app_id: openphacts_app_id,
                openphacts_app_key: openphacts_app_key,
                springer_api_key: springer_api_key
            }
        };
        
        this.delUserFields = function () {
            user_email = null;
            user_name = null;
            user_password_hash = null;
            chemspider_api_key = null;
            chemspider_security_token = null;
            umls_username = null;
            umls_password = null;
            umls_api_key = null;
            eol_api_key = null;
            dpla_api_key = null;
            elsevier_api_key = null;
            fda_api_key = null;
            isbndb_api_key = null;
            ncbo_api_key = null;
            omim_api_key = null;
            openphacts_app_id = null;
            openphacts_app_key = null;
            springer_api_key = null;
            
            logged_in = false;
        }
        
        this.getLoginStatus = function () {
            return logged_in;
        };
        
    });
    
    /* DIRECTIVES */
    gnomicsControllers.directive('backButton', function() {
        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                element.bind('click', goBack);
                function goBack() {
                    history.back();
                    scope.$apply();
                }
            }
        }
    });
    
    gnomicsControllers.directive('forwardButton', function() {
        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                element.bind('click', goForward);
                function goForward() {
                    history.forward();
                    scope.$apply();
                }
            }
        }
    });
    
    /* VIEW CONTROLLERS */
    gnomicsControllers.run(function ($rootScope) {});
    
    gnomicsControllers.controller('indexCtrl', ['$scope', '$http', '$location', '$window', '$resource', 'SharedProperties', '$compile', '$timeout', function ($scope, $http, $location, $window, $resource, SharedProperties, $compile, $timeout) {
        
        var exit_modal = document.getElementById('exit-list-obj');
        console.log(exit_modal);
        exit_modal.onclick = function() {
            console.log("HERE");
            document.querySelector('#exitModal').click();
        };
        
        $scope.loginModal = function () {
            document.querySelector('#loginModal').click();
        };
        
        $scope.logoutModal = function () {
            document.querySelector('#logoutModal').click();
        };
        
        $scope.changeToolbar = function () {
            
            console.log(SharedProperties.getLoginStatus())
            
            if (SharedProperties.getLoginStatus()) {
                
                var help_block = document.getElementById('help-list-obj');
                
                var parent = document.getElementById('nav-list');
                var child_1 = document.getElementById('login-list-obj');
                try {
                    parent.removeChild(child_1);
                } catch(err) {
                    console.log(err.message);
                };
                
                var new_child_1 = document.createElement('li');
                new_child_1.setAttribute('id', 'logout-list-obj');
                new_child_1.innerHTML += "<a id='collapse-link' href ng-click='logoutModal()'><span id='sub-span'><span class='glyphicon glyphicon-log-out' aria-hidden='true'></span> Logout</span></a>";
                parent.insertBefore(new_child_1, help_block);
                $compile(new_child_1)($scope);
                
                var new_child_2 = document.createElement('li');
                new_child_2.setAttribute('id', 'library-list-obj');
                new_child_2.innerHTML += "<a id='collapse-link' href='#/library'><span id='sub-span'><span class='glyphicon glyphicon-book' aria-hidden='true'></span> Library</span></a>";
                parent.insertBefore(new_child_2, new_child_1);
                // $compile(new_child_2)($scope);
                
                var new_child_3 = document.createElement('li');
                new_child_3.setAttribute('id', 'profile-list-obj');
                new_child_3.innerHTML += "<a id='collapse-link' href='#/profile' class='profile-link'><span id='sub-span'><span class='glyphicon glyphicon-user' aria-hidden='true'></span> Profile</span></a>";
                parent.insertBefore(new_child_3, new_child_2);
                // $compile(new_child_3)($scope);
                
            } else {
                
                var help_block = document.getElementById('help-list-obj');
                
                var parent = document.getElementById('nav-list');
                var child_1 = document.getElementById('logout-list-obj');
                try {
                    parent.removeChild(child_1);
                } catch(err) {
                    console.log(err.message);
                };
                var child_2 = document.getElementById('profile-list-obj');
                try {
                    parent.removeChild(child_2);
                } catch(err) {
                    console.log(err.message);
                };
                var child_3 = document.getElementById('library-list-obj');
                try {
                    parent.removeChild(child_3);
                } catch(err) {
                    console.log(err.message);
                };
                
                console.log(parent);
                console.log(help_block);
                
                var new_child_1 = document.createElement('li');
                new_child_1.setAttribute('id', 'login-list-obj');
                new_child_1.innerHTML += "<a id='collapse-link' href ng-click='loginModal()'><span id='sub-span'><span class='glyphicon glyphicon-log-in' aria-hidden='true'></span> Login</span></a>";
                parent.insertBefore(new_child_1, help_block);
                $compile(new_child_1)($scope);
                
            };
            
        };
        
        $scope.init = function () {
            $scope.changeToolbar();
        };
    }]);
    
    gnomicsControllers.controller('homeCtrl', ['$scope', '$location', 'SharedProperties', function ($scope, $location, SharedProperties) {

        $scope.searchQuery = null;
        $scope.searchType = "all";
        
        $scope.location = $location;
        
        $scope.init = function () {
            
            var loader = document.getElementsByClassName("loader");
            loader[0].style.visibility = "hidden";
                                               
            $scope.searchQuery = $location.search().query;
            $scope.searchType = $location.search().search_type;
            
            console.log($scope.searchQuery)
            console.log($scope.searchType)
            
            if ($scope.searchQuery && $scope.searchType) {
                
                $scope.searchDict = {};
                if (SharedProperties.getLoginStatus()) {
                    $scope.searchDict = {
                        search_query: $scope.searchQuery,
                        search_type: $scope.searchType,
                        user: SharedProperties.getUserFields()
                    };
                } else {
                    $scope.searchDict = {
                        search_query: $scope.searchQuery,
                        search_type: $scope.searchType,
                        user: null
                    };
                }
                console.log($scope.searchDict);
                
                var loader = document.getElementById("loader");
                loader.style.visibility = "visible";
                
                if ($scope.searchQuery && $scope.searchType == "all") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            var temp_html_string = '';
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                temp_html_string += "<h3 id='search-type-header'>" + key + "</h3>" + "<hr>";
                                if (res[key] && res[key].length && res[key][0] && res[key][0].length && res[key].length > 5) {
                                    temp_html_string += "<div style='height:250px; overflow-y:auto;'>";
                                }
                                for (var i = 0, l = res[key].length; i < l; i++) {
                                    for (var j = 0, m = res[key][i].length; j < m; j++) {
                                        //console.log(res[key][i][j].identifier)
                                        temp_html_string += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[key][i][j].identifier + "&identifier_type=" + res[key][i][j].identifier_type + "&language=" + (res[key][i][j].language || "") + "&taxon=" + res[key][i][j].taxon + "&source=" + res[key][i][j].source + "&object=" + key + "'>" + res[key][i][j].identifier_type + ": " + res[key][i][j].identifier + " " + "(" + res[key][i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[key][i][j].name == null ? '' : res[key][i][j].name) + "</div></div>";
                                    };
                                };
                                if (res[key] && res[key].length && res[key][0] && res[key][0].length) {
                                    temp_html_string += "</div>";
                                }
                            };
                            /* Delete content and then add content. */
                            loader.style.visibility = "hidden";
                            search_content[0].innerHTML = '';
                            search_content[0].innerHTML += temp_html_string;
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "adverse_event") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=adverse event'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "anatomical_structure") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=anatomical structure'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "assay") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=assay'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "biological_process") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=biological process'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "cell_line") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=cell line'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "cellular_component") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=cellular component'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "clinical_trial") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=clinical trial'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "compound") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=compound'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "disease") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=disease'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "drug") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=drug'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "enzyme") {
                    console.log("TO DO: NOT COMPLETED.");
                } else if ($scope.searchQuery && $scope.searchType == "gene") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=gene'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "molecular_function") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=molecular function'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "pathway") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=pathway'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "phenotype") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=phenotype'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "procedure") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=procedure'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "protein") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=protein'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "reference") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=reference'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "symptom") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=symptom'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "taxon") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=taxon'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "tissue") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=tissue'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "transcript") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=transcript'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else if ($scope.searchQuery && $scope.searchType == "variation") {
                    client.invoke("search", $scope.searchDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            var search_content = document.getElementsByClassName("result-set");

                            /* Delete content and then add content. */
                            search_content[0].innerHTML = '';
                            loader.style.visibility = "hidden";
                            for (var i = 0, l = res.length; i < l; i++) {
                                //console.log(res[i])
                                for (var j = 0, m = res[i].length; j < m; j++) {
                                    //console.log(res[i][j].identifier)
                                    search_content[0].innerHTML += "<div class='panel panel-default'><div class='panel-heading'><a id='result-link' href='#/object?identifier=" + res[i][j].identifier + "&identifier_type=" + res[i][j].identifier_type + "&language=" + res[i][j].language + "&taxon=" + res[i][j].taxon + "&source=" + res[i][j].source + "&object=variation'>" + res[i][j].identifier_type + ": " + res[i][j].identifier + " " + "(" + res[i][j].source + ")" + "</a></div><div class='panel-body'>" + (res[i][j].name == null ? '' : res[i][j].name) + "</div></div>";
                                };
                            };
                        };
                    });
                } else {
                    console.log("No search type was selected or something went wrong.");
                };
            };
        };
        
        /* Use query to create a new URL for search. */
        $scope.searchFunction = function (searchQuery, searchType) {
            $scope.location = $scope.location.url("/home?query=" + searchQuery + "&search_type=" + searchType);
            
        };
        
    }]);
    
    gnomicsControllers.controller('createProfileCtrl', ['$scope', '$http', '$resource', 'SharedProperties', '$timeout', '$location', function ($scope, $http, $resource, SharedProperties, $timeout, $location) {
        
        $scope.GoHome = function () {
            $location.path("/");
        };
        
        $scope.CreateProfile = function (username, email, password, repeat_password, chemspider_api_key, umls_username, umls_password, umls_api_key, eol_api_key, dpla_api_key, elsevier_api_key, fda_api_key, isbndb_api_key, ncbo_api_key, omim_api_key, openphacts_app_id, openphacts_app_key, springer_api_key) {
            $scope.username = username;
            $scope.email = email;
            $scope.password = password;
            $scope.repeat_password = repeat_password;
            
            $scope.chemspider_api_key = chemspider_api_key;
            $scope.umls_username = umls_username;
            $scope.umls_password = umls_password;
            $scope.umls_api_key = umls_api_key;
            $scope.eol_api_key = eol_api_key;
            
            $scope.dpla_api_key = dpla_api_key;
            $scope.elsevier_api_key = elsevier_api_key;
            $scope.fda_api_key = fda_api_key;
            $scope.isbndb_api_key = isbndb_api_key;
            $scope.ncbo_api_key = ncbo_api_key;
            $scope.omim_api_key = omim_api_key;
            $scope.openphacts_app_id = openphacts_app_id;
            $scope.openphacts_app_key = openphacts_app_key;
            $scope.springer_api_key = springer_api_key;
            
            console.log($scope.dpla_api_key);
            
            /* Add check for if username or email is blank. */
            if ($scope.password == $scope.repeat_password) {
                
                create_profile($scope.username, $scope.email, $scope.password, $scope.chemspider_api_key, $scope.umls_username, $scope.umls_password, $scope.umls_api_key, $scope.eol_api_key, $scope.dpla_api_key, $scope.elsevier_api_key, $scope.fda_api_key, $scope.isbndb_api_key, $scope.ncbo_api_key, $scope.omim_api_key, $scope.openphacts_app_id, $scope.openphacts_app_key, $scope.springer_api_key, function(results) {

                    console.log(results);
                    
                    login($scope.username, $scope.password, function(results) {

                        console.log(results);
                        SharedProperties.setUserFields(results);
                        console.log("HERE");
                        $timeout(function() {
                            $('#index-ctrl-init-span').click();
                        }, 1);
                        $timeout(function() {
                            console.log("This is where we are.")
                            $('.profile-link').click();
                        }, 1);
                        $location.path("/profile");
                        
                    });
                });

            } else {
                console.log("Passwords don't match!");
            };
        }
        
    }]);
    
    gnomicsControllers.controller('editProfileCtrl', ['$scope', '$http', '$resource', 'SharedProperties', '$window', '$location', '$timeout', function ($scope, $http, $resource, SharedProperties, $window, $location, $timeout) {
        
        $scope.init = function () {
            $scope.user_fields = SharedProperties.getUserFields();
            
            console.log($scope.user_fields);
            
            $scope.email = $scope.user_fields.user_email;
            $scope.password = $scope.user_fields.user_password_hash;
            $scope.user_name = $scope.user_fields.user_name;
            
            $scope.chemspider_api_key = $scope.user_fields.chemspider_api_key;
            $scope.umls_username = $scope.user_fields.umls_username;
            $scope.umls_password = $scope.user_fields.umls_password;
            $scope.umls_api_key = $scope.user_fields.umls_api_key;
            $scope.eol_api_key = $scope.user_fields.eol_api_key;
            
            $scope.dpla_api_key = $scope.user_fields.dpla_api_key;
            $scope.elsevier_api_key = $scope.user_fields.elsevier_api_key;
            $scope.fda_api_key = $scope.user_fields.fda_api_key;
            $scope.isbndb_api_key = $scope.user_fields.isbndb_api_key;
            $scope.ncbo_api_key = $scope.user_fields.ncbo_api_key;
            $scope.omim_api_key = $scope.user_fields.omim_api_key;
            $scope.openphacts_app_id = $scope.user_fields.openphacts_app_id;
            $scope.openphacts_app_key = $scope.user_fields.openphacts_app_key;
            $scope.springer_api_key = $scope.user_fields.springer_api_key;
        };
        
        $scope.GoToProfile = function () {
            $location.path("/profile");
        };
        
        /* FIX EVERYTHING BELOW!!!! */
        /* Reset user fields, redirect to profile, etc. ... */
        $scope.EditProfile = function(username, email, current_password, new_password, repeat_new_password, chemspider_api_key, umls_username, umls_password, umls_api_key, eol_api_key, dpla_api_key, elsevier_api_key, fda_api_key, isbndb_api_key, ncbo_api_key, omim_api_key, openphacts_app_id, openphacts_app_key, springer_api_key) {
            // New fields. Figure this out? Also need to check that these are the same.
            $scope.current_password = current_password
            $scope.new_password = new_password;
            $scope.repeat_new_password = repeat_new_password;
            
            if ($scope.new_password) {
                console.log("Checking new password...");
            } else {
                $scope.new_password = $scope.current_password;
                $scope.repeat_new_password = $scope.current_password;
            };
            
            $scope.email = email;
            $scope.user_name = username;
            
            $scope.chemspider_api_key = chemspider_api_key;
            $scope.umls_username = umls_username;
            $scope.umls_password = umls_password;
            $scope.umls_api_key = umls_api_key;
            $scope.eol_api_key = eol_api_key;
            
            $scope.dpla_api_key = dpla_api_key;
            $scope.elsevier_api_key = elsevier_api_key;
            $scope.fda_api_key = fda_api_key;
            $scope.isbndb_api_key = isbndb_api_key;
            $scope.ncbo_api_key = ncbo_api_key;
            $scope.omim_api_key = omim_api_key;
            $scope.openphacts_app_id = openphacts_app_id;
            $scope.openphacts_app_key = openphacts_app_key;
            $scope.springer_api_key = springer_api_key;
            
            /* Add check for if username or email is blank. */
            if ($scope.new_password == $scope.repeat_new_password) {
            
                edit_profile($scope.user_name, $scope.email, $scope.current_password, $scope.new_password, $scope.new_repeat_password, $scope.chemspider_api_key, $scope.umls_username, $scope.umls_password, $scope.umls_api_key, $scope.eol_api_key, $scope.dpla_api_key, $scope.elsevier_api_key, $scope.fda_api_key, $scope.isbndb_api_key, $scope.ncbo_api_key, $scope.omim_api_key, $scope.openphacts_app_id, $scope.openphacts_app_key, $scope.springer_api_key, function(results) {

                    console.log(results);
                    SharedProperties.setUserFields(results); // Set the user fields again. ALL OF THEM.
                    $scope.set_stuff = SharedProperties.getUserFields(results);
                    console.log("SET STUFF");
                    console.log($scope.set_stuff);
                    console.log("HERE");
                    $timeout(function() {
                        console.log("This is where we are.")
                        $('.profile-link').click();
                    }, 1);
                    $location.path("/profile");
                });
                
            } else {
                console.log("Passwords don't match!");
            };
        };
    }]);
    
    gnomicsControllers.controller('profileCtrl', ['$scope', 'SharedProperties', '$location', function ($scope, SharedProperties, $location) {
        
        $scope.init = function () {
            $scope.user_fields = SharedProperties.getUserFields();
            
            console.log($scope.user_fields);
            
            $scope.email = $scope.user_fields.user_email;
            $scope.user_name = $scope.user_fields.user_name;
            
            $scope.chemspider_api_key = $scope.user_fields.chemspider_api_key;
            $scope.umls_username = $scope.user_fields.umls_username;
            $scope.umls_password = $scope.user_fields.umls_password;
            $scope.umls_api_key = $scope.user_fields.umls_api_key;
            $scope.eol_api_key = $scope.user_fields.eol_api_key;
            
            $scope.dpla_api_key = $scope.user_fields.dpla_api_key;
            $scope.elsevier_api_key = $scope.user_fields.elsevier_api_key;
            $scope.fda_api_key = $scope.user_fields.fda_api_key;
            $scope.isbndb_api_key = $scope.user_fields.isbndb_api_key;
            $scope.ncbo_api_key = $scope.user_fields.ncbo_api_key;
            $scope.omim_api_key = $scope.user_fields.omim_api_key;
            $scope.openphacts_app_id = $scope.user_fields.openphacts_app_id;
            $scope.openphacts_app_key = $scope.user_fields.openphacts_app_key;
            $scope.springer_api_key = $scope.user_fields.springer_api_key;
        };
        
        $scope.deleteModal = function () {
            document.querySelector('#deleteModal').click();
        };
        
        $scope.editProfile = function () {
            $location.path("/edit_profile");
        };
        
    }]);
    
    gnomicsControllers.controller('libraryCtrl', ['$scope', function ($scope) {
        
        $scope.init = function () {
            
        };
        
    }]);
    
    gnomicsControllers.controller('helpCtrl', ['$scope', function ($scope) {}]);
    
    gnomicsControllers.controller('settingsCtrl', ['$scope', function ($scope) {}]);
    
    gnomicsControllers.controller('objectCtrl', ['$scope', '$location', 'SharedProperties', function ($scope, $location, SharedProperties) {
        
        $scope.propertyNameIden = 'identifier_type';
        $scope.reverseIden = false;

        $scope.sortByIden = function(propertyNameIden) {
            $scope.reverseIden = ($scope.propertyNameIden === propertyNameIden) ? !$scope.reverseIden : false;
            $scope.propertyNameIden = propertyNameIden;
        };
        
        $scope.propertyNameProp = 'property';
        $scope.reverseProp = false;

        $scope.sortByProp = function(propertyNameProp) {
            $scope.reverseProp = ($scope.propertyNameProp === propertyNameProp) ? !$scope.reverseProp : false;
            $scope.propertyNameProp = propertyNameProp;
        };
        
        $scope.currentPageIden = 1;
        $scope.pageSizeIden = 25;
        $scope.qIden = {};
        
        $scope.currentPageProp = 1;
        $scope.pageSizeProp = 25;
        $scope.qProp = {};
        
        $scope.interaction_obj_sort_dict = {};
        
        $scope.init = function () {
            console.log($location.url());
            
            $scope.identifier = $location.search().identifier;
            $scope.identifier_type = $location.search().identifier_type;
            $scope.language = $location.search().language;
            $scope.taxon = $location.search().taxon;
            $scope.source = $location.search().source;
            $scope.object_type = $location.search().object;
        
            $scope.page_title = $scope.identifier_type + ": " + $scope.identifier + " (" + $scope.source + ")";
            
            $scope.idenDict = {};
            if (SharedProperties.getLoginStatus()) {
                $scope.idenDict = {
                    identifier: $scope.identifier,
                    identifier_type: $scope.identifier_type,
                    source: $scope.source,
                    language: $scope.language == "null" ? null : $scope.language,
                    taxon: $scope.taxon == "null" ? null : $scope.taxon,
                    object_type: $scope.object_type,
                    user: SharedProperties.getUserFields()
                };
            } else {
                $scope.idenDict = {
                    identifier: $scope.identifier,
                    identifier_type: $scope.identifier_type,
                    source: $scope.source,
                    language: $scope.language == "null" ? null : $scope.language,
                    taxon: $scope.taxon == "null" ? null : $scope.taxon,
                    object_type: $scope.object_type,
                    user: null
                };
            }
            
            var self = this;
            $scope.identifiers = [];
            $scope.properties = [];
            $scope.interaction_objects = [];
            if ($scope.object_type == "Adverse%20Events" || $scope.object_type == "Adverse Events" || $scope.object_type == "adverse event" || $scope.object_type == "adverse%20event") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Anatomical%20Structures" || $scope.object_type == "Anatomical Structures" || $scope.object_type == "anatomical structure") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Assays" || $scope.object_type == "assay") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Biological%20Processes" || $scope.object_type == "Biological Processes" || $scope.object_type == "biological process") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Cell%20Lines" || $scope.object_type == "Cell Lines" || $scope.object_type == "cell line") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Cellular%20Components" || $scope.object_type == "Cellular Components" || $scope.object_type == "cellular component") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Clinical%20Trials" || $scope.object_type == "Clinical Trials" || $scope.object_type == "clinical trial") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Compounds" || $scope.object_type == "compound") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                            console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
            
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            // console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
            } else if ($scope.object_type == "Diseases" || $scope.object_type == "disease") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Drugs" || $scope.object_type == "drug") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Genes" || $scope.object_type == "gene" || $scope.object_type == "Gene") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Molecular%20Functions" || $scope.object_type == "Molecular Functions" || $scope.object_type == "molecular function") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Pathways" || $scope.object_type == "pathway") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Phenotypes" || $scope.object_type == "phenotype") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
            
            } else if ($scope.object_type == "Procedures" || $scope.object_type == "procedure") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Protein" || $scope.object_type == "Proteins" || $scope.object_type == "protein") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "References" || $scope.object_type == "reference") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
            
            } else if ($scope.object_type == "Symptom" || $scope.object_type == "symptom") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Taxa" || $scope.object_type == "taxon") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Tissues" || $scope.object_type == "tissue") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Transcript" || $scope.object_type == "Transcripts" || $scope.object_type == "transcript") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else if ($scope.object_type == "Variations" || $scope.object_type == "variation") {
                client.invoke("identifiers", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            //console.log(res);
                            $scope.identifiers = res;
                            $scope.$apply();
                        };
                    });
                
                client.invoke("properties", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                for (var i = 0 ; i < res[key].length; i++) {
                                    if(res[key][i] !== null) {
                                        res_array.push({
                                            property: key,
                                            value: res[key][i]
                                        });
                                    };
                                };
                            };
                            $scope.properties = res_array;
                            console.log(res_array)
                            $scope.$apply();
                        };
                    });
                
                client.invoke("interactions", $scope.idenDict, (error, res) => {
                        if (error) {
                           console.error(error);
                        } else {
                            console.log(res);
                            var res_array = []
                            var sorted_keys = Object.keys(res).sort();
                            for (let key of sorted_keys) {
                                var temp_dict = {
                                    type: key,
                                    identifier_array: []
                                };
                                
                                for (let iden_obj of res[key]) {
                                    for (let iden of iden_obj) {
                                    //    console.log(iden);
                                        temp_dict.identifier_array.push(iden);
                                    };
                                };
                                
                                console.log(temp_dict.identifier_array);
                                
                                res_array.push(temp_dict);
                                
                                $scope.interaction_obj_sort_dict[key] = {
                                    propertyName: 'identifier_type',
                                    reverse: false,
                                    sortBy: function(propertyName) {
                                        $scope.interaction_obj_sort_dict[key].reverse = ($scope.interaction_obj_sort_dict[key].propertyName === propertyName) ? !$scope.interaction_obj_sort_dict[key].reverse : false;
                                        $scope.interaction_obj_sort_dict[key].propertyName = propertyName;
                                    },
                                    currentPage: 1,
                                    pageSize: 25,
                                    q: ""
                                };
                            };
                            
                            console.log($scope.interaction_obj_sort_dict);
                            
                            console.log("FULL ARRAY:");
                            console.log(res_array);
                            $scope.interaction_objects = res_array;
                            $scope.$apply();
                        };
                    });
                
            } else {
                console.log($scope.object_type)
                console.log("Object type not yet supported.");
            }
        };
        
    }]);
    
    /* MODAL CONTROLLERS */
    gnomicsControllers.controller('loginCtrl', ['$scope', '$http', '$resource', 'SharedProperties', '$window', '$location', '$timeout', function ($scope, $http, $resource, SharedProperties, $window, $location, $timeout) {
        
        $scope.init = function () {
            console.log("HERE");
        };
        
        $scope.keygen = function(key_len) {
            var i, key = "";
            var characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
            var charactersLength = characters.length;
            
            for (i = 0; i < key_len; i++) {
                key += characters.substr(Math.floor((Math.random() * charactersLength) + 1), 1);
            };
            
            return key;
        };
        
        $scope.login = function(user, password) {
            console.log(user);
            console.log(password);
            
            login(user, password, function(results) {
                
                console.log(results);
                SharedProperties.setUserFields(results);
                console.log("HERE");
                $timeout(function() {
                    $('#index-ctrl-init-span').click();
                }, 1);
                $timeout(function() {
                    $('#login-close-button').click();
                }, 1);
                $location.path("/profile");
            });
        };
        
    }]);
    
    gnomicsControllers.controller('logoutCtrl', ['$scope', '$http', '$resource', 'SharedProperties', '$window', '$location', '$timeout', function ($scope, $http, $resource, SharedProperties, $window, $location, $timeout) {
        
        $scope.init = function () {
        };
        
        $scope.logout = function() {
            SharedProperties.delUserFields();
            console.log("HERE");
            $timeout(function() {
                $('#index-ctrl-init-span').click();
            }, 1);
            $timeout(function() {
                $('#logout-close-button').click();
            }, 1);
            $location.path("/home");
        };
        
    }]);
    
    gnomicsControllers.controller('deleteProfileCtrl', ['$scope', '$http', '$resource', 'SharedProperties', '$window', '$location', '$timeout', function ($scope, $http, $resource, SharedProperties, $window, $location, $timeout) {
        
        $scope.init = function () {
        };
        
        $scope.delete = function() {
            $scope.user_fields = SharedProperties.getUserFields();
            
            $scope.email = $scope.user_fields.user_email;
            $scope.password = $scope.user_fields.user_password_hash;
            $scope.user_name = $scope.user_fields.user_name;
            
            delete_profile($scope.user_name, $scope.email, $scope.password, function(results) {
                
                console.log(results);
                SharedProperties.delUserFields();
                console.log("HERE");
                $timeout(function() {
                    $('#index-ctrl-init-span').click();
                }, 1);
                $timeout(function() {
                    $('#logout-close-button').click();
                }, 1);
                $location.path("/home");
            });
        };
    }]);
    
    gnomicsControllers.controller('exitCtrl', ['$scope', '$http', '$resource', 'SharedProperties', '$window', '$location', function ($scope, $http, $resource, SharedProperties, $window, $location) {
        
        $scope.init = function () {
        };
        
        $scope.exit = function() {
            var window = remote.getCurrentWindow();
            window.close();
        };
    }]);
    
}());