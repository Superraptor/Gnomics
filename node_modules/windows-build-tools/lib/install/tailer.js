'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var path = require('path');
var fs = require('fs-extra');
var debug = require('debug')('windows-build-tools');
var EventEmitter = require('events');

var utils = require('../utils');

var Tailer = function (_EventEmitter) {
  _inherits(Tailer, _EventEmitter);

  function Tailer(logfile) {
    var encoding = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 'utf8';

    _classCallCheck(this, Tailer);

    var _this = _possibleConstructorReturn(this, (Tailer.__proto__ || Object.getPrototypeOf(Tailer)).call(this));

    _this.logFile = logfile;
    _this.encoding = encoding;
    return _this;
  }

  /**
   * Starts watching a the logfile
   */


  _createClass(Tailer, [{
    key: 'start',
    value: function start() {
      debug('Tail: Waiting for log file to appear in ' + this.logFile);
      this.waitForLogFile();
    }

    /**
     * Stop watching
     */

  }, {
    key: 'stop',
    value: function stop() {
      for (var _len = arguments.length, args = Array(_len), _key = 0; _key < _len; _key++) {
        args[_key] = arguments[_key];
      }

      debug.apply(undefined, ['Tail: Stopping'].concat(args));
      this.emit.apply(this, ['exit'].concat(args));
      clearInterval(this.tail);
    }

    /**
     * Start tailing things
     */

  }, {
    key: 'tail',
    value: function tail() {
      var _this2 = this;

      debug('Tail: Tailing ' + this.logFile);
      this.tail = setInterval(function () {
        _this2.handleData();
      }, 30000);
    }

    /**
     * Handle data and see if there's something we'd like to report
     */

  }, {
    key: 'handleData',
    value: function handleData() {
      var data = void 0;

      try {
        data = fs.readFileSync(this.logFile, this.encoding);
      } catch (err) {
        debug('Tail start: Could not read logfile ' + this.logFile + ': ' + err);
      }

      // Success strings for build tools
      if (data.includes('Variable: IsInstalled = 1') || data.includes('Variable: BuildTools_Core_Installed = ') || data.includes('WixBundleInstalled = 1')) {
        this.stop('success');
        // Success strings for python
      } else if (data.includes('INSTALL. Return value 1') || data.includes('Installation completed successfully') || data.includes('Configuration completed successfully')) {
        // Finding the python installation path from the log file
        var matches = data.match(/Property\(S\): TARGETDIR = (.*)\r\n/);
        var pythonPath = undefined;

        if (matches) {
          pythonPath = matches[1];
        }
        this.stop('success', pythonPath);
      } else if (data.includes('Shutting down, exit code:')) {
        this.stop('failure');
      }

      // Aid garbage collector
      data = undefined;
    }

    /**
     * Waits for a given file, resolving when it's available
     *
     * @param file {string} - Path to file
     * @returns {Promise.<Object>} - Promise resolving with fs.stats object
     */

  }, {
    key: 'waitForLogFile',
    value: function waitForLogFile() {
      var _this3 = this;

      fs.lstat(this.logFile, function (err, stats) {
        if (err && err.code === 'ENOENT') {
          debug('Tail: waitForFile: still waiting');
          setTimeout(_this3.waitForLogFile.bind(_this3), 2000);
        } else if (err) {
          debug('Tail: waitForFile: Unexpected error', err);
          throw new Error(err);
        } else {
          debug('Tail: waitForFile: Found ' + _this3.logFile);
          _this3.tail();
        }
      });
    }
  }]);

  return Tailer;
}(EventEmitter);

module.exports = Tailer;