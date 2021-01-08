# OMRR Simulator

The Simulator is used to send constant messages to the Logserver. Currently it supports 
* DCC
* MFX

## Installation
* Clone this repository
* cd into the directory
* Create virtualenv
* install dependencies with ```pip install -r requirements.txt```
* run the simulator with te parameters below

## Parameters
| short | long        | description                         |
|-------|-------------|-------------------------------------|
| -r    | --random    | randomize time between messages     |
| -n    | --name      | hostname for the simulator          |
| -p    | --protocol  | protocol which is used (dcc or mfx) |
| -l    | --logserver | logserver ip default is localhost   |
| -h    | --help      | show help                           |

## License
see license.md

## Resources
* http://www.skrauss.de/modellbahn/Schienenformat.pdf