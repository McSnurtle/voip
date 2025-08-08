# voip 📢
A simple voice over internet protocol server and client written in python.

## Installation / Quickstart Guide ⏱️
Running voip requires [Python](<https://github.com/McSnurtle/voip.git>) (tested on version 3)! Make sure you have it installed before doing anything.
Installation has been made extremely simple by the `setup.bat` and `setup.sh` scripts. Run the batch script for Windows installation, and the shell script for Unix.

The install script essentially does the following:
```shell
python -m venv \
source ./venv/bin/activate \
pip install -r requirements.txt
```

## Usage
This program operates on a simple paradigm of VoIP (voice over internet protocol) direct computer to computer communications. Depending on the user's configuration files, the server will playback the stream of received audio packets (or chunks), and the client will send the user's microphone data to the server. To see how to specify a server or microphone, see the [Configuration](<https://github.com/McSnurtle/voip/.git>) > Audio > `microphone_id` for details.

Run `server.bat` or `server.sh` to accept and playback data from clients.
Run `client.bat ` or `client.sh` to send microphone data to a server.

## Configuration
Below is a tour of `usr/conf/client.json` options:
| Section | ID | Default | Type | Description |
|---------|----|---------|------|-------------|
| Networking | | | Section | Configuration options for how things are sent over the interwebs. |
| | `server_ip` | 127.0.0.1 | String | The target IPv4 address of the server you would like to stream your microphone to. Defaults to your own computer. |
| | `server_port` | 20000 | Integer | The target port of the server you would like to stream your microphone to. Do not change unless your server provider has told you to. |
| Audio | | | Section | Configuration options for the microphone recording setup. |
| | `microphone_id` | 0 | Integer | The ID number of the microphone you would like to use for streaming. To see a list of options, run `list_microphones.bat`. |
| | `sample_rate` | 44100 | Integer | The exact sample rate of the selected microphone. Careful! Setting this wrong results in some seriously funky sounds! Make sure to tell your server provider what sample rate you are using so they can match it. |
| | `chunk_size` | 441 | Integer | The size of chunks to get from the microphone and send to the server. Do not change this unless your server provider has told you to. |
| | `mysery_number` | 1 | Integer | The coefficient to muliply the `chunk_size` with to determine the number of frames per buffer in PyAudio. |
| | `suppression_level` | 3 | Integer | The level of aggression when applying noise suppression to the microphone. Range: 1 - 3. CAUTION: not fully implemented. |
