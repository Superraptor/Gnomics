PRIMARY DISCLAIMER: This README, associated documentation, and the program itself are currently in Alpha 0.2; thus, they should be considered incomplete. All errors in software, README, etc. should be noted as GitHub issues. I will try to answer all issues with expediency. Thank you for using *GNOMICS*.

SECONDARY DISCLAIMER(S): Do not rely on openFDA to make decisions regarding medical care. Always speak to your health provider about the risks and benefits of FDA-regulated products. For more information, please review the OpenFDA Terms of Service, available [here](https://open.fda.gov/terms/).

NOBLE CODER LICENSE: If you are an individual user or an educational institution, you can redistribute it and/or modify it under the terms of the BSD 3-Clause License.

Copyright (c) 2015, University of Pittsburgh
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of [project] nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

For all other users, licensing is decided on a case by case basis through Nexi Inc.

If you have any questions about licensing, please Nexi at: http://nexihub.com/contact

# GNOMICS

The World Wide Web is an indispensable tool for biomedical researchers who are striving to understand the molecular basis of phenotype. However, it presents challenges too, in the form of proliferation of data resources, with heterogeneity ranging from their content to functionality to interfaces. This often frustrates researchers who have to visit multiple sites, get familiar with their interfaces, and learn how to use them or extract knowledge from them and still never feel sure they have tracked down all the information they might need. *GNOMICS* (Genomic Nomenclature Omnibus and Multifaceted Informatics and Computational Suite), a suite with both a programmatic interface and a GUI, was envisioned as an answer to this challenge. *GNOMICS* allows for extensible biomedical functionality, including identifier conversion, pathway enrichment, sequence alignment, and reference gathering, among others. It combines usage of other biological and chemical database application programming interfaces (APIs) to deliver uniform data which is easy to further manipulate and parse.

## Installation

Because three different interfaces are available for using *GNOMICS*, the installation instructions can differ, sometimes greatly, especially from system to system.

### Windows

First, install Git. This can be done by downloading it from the Git website, [here](http://git-scm.com/download/win). After clicking on the link, the download should start automatically. Note that this source is a project called Git for Windows, ostensibly separate from Git itself. An alternative, for automated installation is the [Git Chocolatey package](https://chocolatey.org/packages/git), which is community maintained. The other alternative is to install GitHub for Windows, which includes the command-line version of Git as well as the GUI (it also works with Powershell). This final version can be downloaded [here](http://windows.github.com/).

(TODO: Continue with Git instructions)

Running the Electron version of the application can be somewhat difficult on Windows systems. Once everything is downloaded, Electron must be built from the source. This must be done from an Administrator Windows PowerShell (right-clicking on the PowerShell icon will provide this option if using an administrator account).

First run `npm install -g npm-windows-upgrade` as mentioned [here](https://stackoverflow.com/questions/18412129/how-can-i-update-npm-on-windows). Following this, run `npm rebuild`. Each time a new rebuild is run, be sure to run `./node_modules/.bin/electron-rebuild`. If any other packages cannot be found when the Electron window is opened, run an `npm install`. For example, if `express` is missing, run `npm install express --save`. After each new `npm install`, be sure to run `./node_modules/.bin/electron-rebuild` again.

Additionally, if an `Error: Lost remote after 10000ms` occurs, remember to change lines 31 and 34 in `./gnomics_app/node_modules/zerorpc/lib/client.js`. Line 31 should read `var DEFAULT_TIMEOUT = 30000;` and Line 34 should read `var DEFAULT_HEARTBEAT = 1000000;`.

If general, if there are errors, follow these steps:

1. Delete the folder `node_modules`.
2. Make sure the Electron versions in `package.json` and `package-lock.json` is `1.7.11`. The Electron version is on Line 21 in `package.json` and on Line 514 in `package-lock.json`.
3. Run `npm install --save`.
4. Run `npm rebuild`.
5. Run `./node_modules/.bin/electron-rebuild`.
6. Run `npm install express --save`.
7. Run `./node_modules/.bin/electron-rebuild`.
8. Run `npm install cookie-parser --save`.
9. Run `./node_modules/.bin/electron-rebuild`.
10. Run `npm install bcrypt --save`.
11. Run `./node_modules/.bin/electron-rebuild`.
12. Change lines 31 and 34 in `./gnomics_app/node_modules/zerorpc/lib/client.js`. Line 31 should read `var DEFAULT_TIMEOUT = 30000;` and Line 34 should read `var DEFAULT_HEARTBEAT = 1000000;`.

### Mac OS

Install Git first, using any of various methods. Typically the easiest is to install the Xcode Command Line Tools. On Mavericks (10.9) or above, this can be done just by running `git` from the Terminal the very first time. If not installed already, you will be prompted to install. For a more up-to-date version, use a binary installer, which can be downloaded [here](http://git-scm.com/download/mac). Another method is to install it as part of the GitHub for Mac application; their GUI Git Tool has an option to install command line tools as well. It can be downloaded from the GitHub for Mac website, [here](http://mac.github.com).

### Unix

For Linux platforms, install the basic Git tools using the binary installer. For example, on Fedora, RHEL, CentOS, and related RPM-based distros, use `dnf`:

```
sudo dnf install git-all
```

However, if using a Debian-based distribution (such as Ubuntu), use `apt-get`:

```
sudo apt-get install git-all
```

If your platform does not fall under either of these categories, utilize any of the various instructions located [here](http://git-scm.com/download/linux).

## Usage

### Configuration

### Programmatic Interface (Command-Line)
Running the programmatic (CMD) interface is currently similar to running any local package (a global package version of *GNOMICS* is under development). Therefore, once the Git repository is downloaded and unpacked, several further packages may be necessary to access all of *GNOMICS*' onboard functionalities. Finally, the Python version used in testing *GNOMICS* is 3.4, although other versions of interest may enter development soon.

A partial list of these Python dependencies includes:
* `__future__`
* `Bio`
* `GEOparse`
* `SPARQLWrapper`
* `bibtexparser`
* `bioservices`
* `bs4`
* `chembl_webresource_client`
* `chemspipy`
* `cirpy`
* `clinical_trials`
* `csv`
* `decimal`
* `eutils`
* `faulthandler`
* `ftplib`
* `goatools`
* `gzip`
* `intermine`
* `io`
* `isbnlib`
* `itertools`
* `json`
* `libchebipy`
* `lxml`
* `metapub`
* `mygene`
* `myvariant`
* `nltk`
* `numpy`
* `orcid`
* `os`
* `pandas`
* `pdfx`
* `pubchempy`
* `pubmed_lookup`
* `pybtex`
* `pymedtermino`
* `pytaxize`
* `re`
* `refextract`
* `requests`
* `ruamel`
* `scholarly`
* `shutil`
* `signal`
* `ssl`
* `string`
* `subprocess`
* `sys`
* `tempfile`
* `threading`
* `time`
* `timeit`
* `urlextract`
* `urllib`
* `urllib3`
* `wikidata`
* `wikipedia`
* `word_forms`
* `xml`
* `xmltodict`
* `yaml`
* `zerorpc`
* `zmq`

All of these packages should be available via using `pip`, `conda`, or `easy_install`. These packages will eventually be packaged with *GNOMICS* to make the installation process smoother.

In addition, running Noble Coder (`NobleCoder-1.0.jar`) requires a Java Runtime Environment installation.

### Electron Interface
To run the Electron interface, first make sure that no processes are running on port 4242. To check this on Windows, open a command prompt and run the command `netstat -a -o -n`. This will list all protocols being run. If TCP 127.0.0.1:4242 does not appear in the list, Electron can be run. However, if it does appear in the list, check the PID (last column of the `netstat` output) and then run `taskkill /F /PID $PID` where `$PID` is the aforementioned PID. For example, if the PID is 20284, run `taskkill /F /PID 20284`.

Once the port is cleared, open two command prompts or bash shells and change directories in both to `gnomics` (the top level directory). Once there, run `python ./gnomics/api.py` in one prompt and `../gnomics/node_modules/electron/dist/electron.exe ../gnomics` in the other.

Note that running `python ../gnomics/node_modules/electron/dist/electron.exe ../gnomics` will result in the following error or a variant of this error:

```
File "../gnomics/node_modules/electron/dist/electron.exe", line 1
SyntaxError: Non-UTF-8 code starting with '\x90' in file ../gnomics_app/node_modules/electron/dist/electron.exe on line 1, but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
```

### Executable Interface
The executable interface is still in development.

## Contributing
* Charles Kronk (Head Developer)

## History
* 30 November 2017: The first alpha version (0.1) was uploaded to GitHub.
* 24 January 2018: A small incremental alpha (version 0.1.1) was uploaded in order to fix a critical Electron security vulnerability. See [here](https://electronjs.org/blog/protocol-handler-fix) for more details.
* 18 February 2018: A large alpha update was issued (0.2).

## Credits
Created by Charles Kronk.

## License
Copyright (c) 2017, Charles Kronk
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the authors and should not be interpreted as representing official policies, either expressed or implied, of the FreeBSD Project.