/*global angular, console, alert*/

(function () {
    'use strict';
    
    var gnomics = angular.module('gnomics-app', [
        'gnomicsControllers',
        'ngAnimate',
        'ngRoute',
        'ngResource',
        'mgcrea.ngStrap',
        'angularUtils.directives.dirPagination'
    ]);
    
    gnomics.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
        $locationProvider.hashPrefix('');
        
        $routeProvider.
            when('/library', {
                templateUrl: './views/library.html',
                controller: 'libraryCtrl'
            }).
            when('/profile', {
                templateUrl: './views/profile.html',
                controller: 'profileCtrl'
            }).
            when('/help', {
                templateUrl: './views/help.html',
                controller: 'helpCtrl'
            }).
            when('/object', {
                templateUrl: './views/object.html',
                controller: 'objectCtrl'
            }).
            when('/settings', {
                templateUrl: './views/settings.html',
                controller: 'settingsCtrl'
            }).
            when('/create_profile', {
                templateUrl: './views/create_profile.html',
                controller: 'createProfileCtrl'
            }).
            when('/edit_profile', {
                templateUrl: './views/edit_profile.html',
                controller: 'editProfileCtrl'
            }).
            otherwise({
                templateUrl: './views/home.html',
                controller: 'homeCtrl'
            });
    }]);
    
    gnomics.config(['$resourceProvider', function ($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }]);
}());