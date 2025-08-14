# voip 📢
A simple voice over internet protocol server and client written in python. A.k.a. a program to make calls.

## Installation / Quickstart Guide ⏱️
Running voip requires [Python](<https://github.com/McSnurtle/voip.git>) (tested on version 3) and [C++ Redistributables](<https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170>) on Windows! Make sure you have them installed before doing anything.
Installation has been made extremely simple by the `setup.bat` and `setup.sh` scripts. Run the batch script for Windows installation, and the shell script for Unix.

The install script essentially does the following:
```shell
python -m venv \
source ./venv/bin/activate \
pip install -r requirements.txt
```

## Usage
This program operates on a simple paradigm of VoIP (voice over internet protocol). To see how to use for group calls, or for direct PC-to-PC communications, see [Examples](<https://github.com/McSnurtle/voip/wiki/Usage#examples-eyes>) on the (highly-experimental-and-just-for-fun) wiki. For how to select a microphone or speakers, see [Client Configuration](<https://github.com/McSnurtle/voip/wiki/Configuration#client-studio_microphone>), also on the (highly-experimental-and-just-for-fun) wiki.

Run `server.bat` or `server.sh` to accept and playback data from clients.
Run `client.bat ` or `client.sh` to send microphone data to a server.

## Configuration
This section has moved to its own wiki page! How cool is that? See it [here](<https://github.com/McSnurtle/voip/wiki/Configuration>).
