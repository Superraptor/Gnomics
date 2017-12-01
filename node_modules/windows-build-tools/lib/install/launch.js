'use strict';

var path = require('path');
var spawn = require('child_process').spawn;
var chalk = require('chalk');
var debug = require('debug')('windows-build-tools');

var utils = require('../utils');
var installer = utils.getBuildToolsInstallerPath();

/**
 * Launches the installer, using a PS1 script as a middle-man
 *
 * @returns {Promise.<Object>} - Promise that resolves with the launch-installer result
 */
function launchInstaller() {
  return new Promise(function (resolve, reject) {
    var extraArgs = '';
    var parsedArgs = {};

    if (process.env.npm_config_vcc_build_tools_parameters) {
      try {
        parsedArgs = JSON.parse(process.env.npm_config_vcc_build_tools_parameters);

        if (parsedArgs && parsedArgs.length > 0) {
          extraArgs = parsedArgs.join('%_; ');
        }
      } catch (e) {
        debug('Installer: Parsing additional arguments for VCC build tools failed: ' + JSON.stringify(e));
        debug('Input received: ' + process.env.npm_config_vcc_build_tools_parameters);
      }
    }

    var scriptPath = path.join(__dirname, '..', '..', 'ps1', 'launch-installer.ps1');
    var psArgs = '& {& \'' + scriptPath + '\' -path \'' + installer.directory + '\' -extraBuildToolsParameters \'' + extraArgs + '\' }';
    var args = ['-ExecutionPolicy', 'Bypass', '-NoProfile', '-NoLogo', psArgs];

    debug('Installer: Launching installer in ' + installer.directory + ' with file ' + installer.fileName);

    var child = void 0;

    try {
      child = spawn('powershell.exe', args);
    } catch (error) {
      return reject(error);
    }

    child.stdout.on('data', function (data) {
      debug('Installer: Stdout from launch-installer.ps1: ' + data.toString());

      if (data.toString().includes('Please restart this script from an administrative PowerShell!')) {
        utils.log(chalk.bold.red('Please restart this script from an administrative PowerShell!'));
        utils.log('The build tools cannot be installed without administrative rights.');
        utils.log('To fix, right-click on PowerShell and run "as Administrator".');

        // Bail out
        process.exit(1);
      }
    });

    child.on('exit', function () {
      return resolve();
    });
    child.stdin.end();
  });
}

module.exports = launchInstaller;