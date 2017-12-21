# Cloak
<img src='https://i.imgur.com/m3scSAO.png' />
Cloak is an intelligent python backdoor framework.

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
For now, <b>Cloak</b> can backdoor python scripts but I am looking forward to do the same for <b>C</b>, <b>bash</b> and <b>perl</b> scripts.
I will also work on generation and binding of <b>exe</b> and <b>apk</b> payloads.<br>
Currently, the default connection method is <b>https</b> and Cloak creates a staged and reverse payload. So, of course the I will try to extend its capabilities which also includes bypassing lowkey AV solutions in windows.<br>
If you like the idea, help me achieve the goals. The code is well documented so if you want to contribute you are not going to face any problems.
Modify the code, add and improve and start a pull request.<br>
If you find a bug in the code don't hesitate to start an issue.<br>

<b>Email:</b> s0md3v@gmail.com
<b>Twitter:</b> @s0md3v
