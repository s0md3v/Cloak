# Cloak
<img src='https://i.imgur.com/m3scSAO.png' />
Cloak can backdoor any python script with some tricks.

## What it exactly does?
<b>Cloak</b> generates a python payload via <b>msfvenom</b> and then intelligently injects it into the python script you specify.

To evade basic detection, Cloak breaks the payload into several parts and places it in different places in the code. If you want the victim to run your injected script as root, Cloak can handle that too.
Cloak will be further upgraded in future to support a wide range of payloads, platforms and evasion techniques.

### Demo
<img src='https://i.imgur.com/mEzDJp2.png' />

### Requirements
- msfvenom
- python2

### Contribute
The code is well documented so if you want to contribute you are not going to face any problems.
Modify the code, add and improve and start a pull request.
If you find a bug in the code don't hesitate to start an issue.
You can also mail me at: s0md3v@gmail.com
Or can ping me at my twitter handle: @s0md3v
