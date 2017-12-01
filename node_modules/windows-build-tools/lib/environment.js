'use strict';

var path = require('path');
var utils = require('./utils');

/**
 * Uses PowerShell to configure the environment for
 * msvs_version 2015 and npm python 2.7
 *
 * @params variables an object with paths for different environmental variables
 *
 * @returns {Promise}
 */
function setEnvironment(variables) {
  var pythonPath = path.join(variables.python.pythonPath);
  var pythonExePath = path.join(pythonPath, 'python.exe');
  var scriptPath = path.join(__dirname, '..', 'ps1', 'set-environment.ps1');
  var maybeAddToPath = process.env.npm_config_add_python_to_path ? ' -AddPythonToPath' : '';
  var psArgs = '& {& \'' + scriptPath + '\' -pythonPath \'' + pythonPath + '\' -pythonExePath \'' + pythonExePath + '\'' + maybeAddToPath + ' }';
  var args = ['-ExecutionPolicy', 'Bypass', '-NoProfile', '-NoLogo', psArgs];

  return utils.executeChildProcess('powershell.exe', args);
}

module.exports = setEnvironment;