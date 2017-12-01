<<<<<<< HEAD
DISCLAIMER: This README, associated documentation, and the program itself are currently in Alpha 0.1; thus, they should be considered incomplete. All errors in software, README, etc. should be noted as GitHub issues. I will try to answer all issues with expediency. Thank you for using *GNOMICS*.

# GNOMICS

The World Wide Web is an indispensable tool for biomedical researchers who are striving to understand the molecular basis of phenotype. However, it presents challenges too, in the form of proliferation of data resources, with heterogeneity ranging from their content to functionality to interfaces. This often frustrates researchers who have to visit multiple sites, get familiar with their interfaces, and learn how to use them or extract knowledge from them and still never feel sure they have tracked down all the information they might need. *GNOMICS* (Genomic Nomenclature Omnibus and Multifaceted Informatics and Computational Suite), a suite with both a programmatic interface and a GUI, was envisioned as an answer to this challenge. *GNOMICS* allows for extensible biomedical functionality, including identifier conversion, pathway enrichment, sequence alignment, and reference gathering, among others. It combines usage of other biological and chemical database application programming interfaces (APIs) to deliver uniform data which is easy to further manipulate and parse.

## Installation

Because three different interfaces are available for using *GNOMICS*, the installation instructions can differ, sometimes greatly, especially from system to system.

### Windows

First, install Git. This can be done by downloading it from the Git website, [here](http://git-scm.com/download/win). After clicking on the link, the download should start automatically. Note that this source is a project called Git for Windows, ostensibly separate from Git itself. An alternative, for automated installation is the [Git Chocolatey package](https://chocolatey.org/packages/git), which is community maintained. The other alternative is to install GitHub for Windows, which includes the command-line version of Git as well as the GUI (it also works with Powershell). This final version can be downloaded [here](http://windows.github.com/).

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
While an official Python package publication is still in the works, most of the component files include example unit tests (where possible) and can be used individually as long as the file hierarchy is in tact.

### Electron Interface
To run the Electron interface, first make sure that no processes are running on port 4242. To check this on Windows, open a command prompt and run the command `netstat -a -o -n`. This will list all protocols being run. If TCP 127.0.0.1:4242 does not appear in the list, Electron can be run. However, if it does appear in the list, check the PID (last column of the `netstat` output) and then run `taskkill /F /PID $PID` where `$PID` is the aforementioned PID. For example, if the PID is 20284, run `taskkill /F /PID 20284`.

Once the port is cleared, open two command prompts or bash shells and change directories in both to `gnomics_app`. Once there, run `python ./gnomics/api.py` in one prompt and `../gnomics_app/node_modules/electron/dist/electron.exe ../gnomics_app` in the other.

However, before doing this, if you are trying to use an account-based profile (i.e. logging users in or out), you will need to initialize the database by running `node ./db/create_db.js`.

### Executable Interface
The executable interface is still in production.

## Contributing
* Charles Kronk (Head Developer)

## History
* 30 November 2017: The first alpha version (0.1) was uploaded to GitHub.

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
=======
# GNOMICS

## Introduction
*Gnomics* is a conceptual application which will utilize several genetics databases in order to allow users to upload a selection of genetic content and then download additional or related genetic information or browse it online.
>>>>>>> 552b1d764d2556cc54032abd5a8cc2739f0a6c4a
