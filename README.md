# Market Profile
Market Profile is a trading technique that was devised by J. Peter Steidlmayer in the 1980s. <br/>
This project takes OHLC(Open, High, Low and Close) data as input in the the form of a Python List or Pandas Dataframe and generates a market profile for the same. The market profile can be saved as a csv or can be further used for making trading decisions.
<br/>
# Installation
The easiest way to install is through pip.
```
pip install market-profile
```
# Usage
Look up the example in examples folder to know about usage.<br/><br/>
There are two types of market-profiles that can be generated.
1. Normal Profile (where each time frame is distinct)
2. Compacted Profile (where timeframes are compacted)
# Command Line Usage
Use market-profile/profile_command_line.py for command line. 
<br/>
Example:  <br/>
```
python profile_command_line.py [location of csv] [duration(ms)] --compact [t,f] --dest [destination to save file to(default is current working directory)] 
```
# TODO
1. ~~Add this repository to PyPi. ~~
2. Add a feature to visualise market-profile
