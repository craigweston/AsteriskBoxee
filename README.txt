================
AsteriskBoxee
================
Tested with Python 2.6.6

AsteriskBoxee is a tool written in Python to provide Caller ID functionality on
the Boxee Box from calls received on an Asterisk PBX.

This is done using Boxee's JSON RPC API and Asterisk's AGI interface. 

================
HOW IT WORKS
================

When calls are received on your Asterisk system, an AGI script is executed that
sends a notification request to your Boxee Box via its JSON RPC API. Boxee will
then display the caller's information such as phone number and name on your TV.
This is similar to functionality often seen with satelite/cable TV and phone
packages.

================
USE
================
Please feel free to download use and modify this tool.

================
STEPS TO INSTALL
================

STEP #1: Pairing with the Boxee:

Boxee's JSON RPC requires you to first pair your device. This can be done using
the included command line (client.py) python script included in this package.

Ensure that your Boxee Box and TV are on before running the below command:

    $ ./client.py <host> pair

If successful you should see a pairing dialog with a challenge code appear on
your TV. Enter this pairing code on the command line when prompted.

Once complete you should see a successful pairing message returned. You should
not have to pair your device more then once.

STEP #2: Setup your Asterisk Dialplan:

First, create a symbolic link to the "agi.py" script in your
/var/lib/asterisk/agi-bin and ensure that the script is executable. 

Example:

    $ cd /var/lib/asterisk/agi-bin
    $ ln -s ~/AsterisBoxee/src/agi.py boxee.py

In your extensions.conf configuration file located in your /etc/asterisk
directory you will need to edit your incoming dialplan rules to execute the AGI
script that you just linked. 

Here is an example of what a simple dialplan may look like:

    [incoming]
    exten => _X!,1,Answer()
    exten => _X!,n,AGI(agi.py, "192.168.1.138", "9090")
    exten => _X!,n,Ringing()
    exten => _X!,n,Wait(5)
    exten => _X!,n,Dial(SIP/200)
    exten => _X!,n,Hangup()

Note the two additional arguments in the AGI call. These arguments are
required. The first is the IP of your Boxee Box and the second is the port,
which in most cases should be the default 9090

At this point you will also need to reload your dialplan in asterisk.

Step #3: Test your new installation

You should now be setup and ready to test your new setup.

================
Issues/Problems
================

If you encounter issues please feel free to contact me development@craigweston.ca.
Logging is performed via syslog.


