zmount.py
=========

ABOUT:
------

zmount is a shell script written in python to 
make ease of connectivity to an SSH/SFTP server
in the terminal through the MacFuse connection
manager 

PREREQUISITES:
--------------

MacFuse

SSHFS

custom "list" file, examples:

1. name:example1, port:27, user:user, ip:192.168.0.113, rdir:/var/www/, ldir:/mount/example, volname:example
2. name:google,   port:,   user:gusr, ip:google.com,    rdir:/,         ldir:/mount/google,  volname:google
3. name:apple,    port:73, user:appl, ip:apple.com,     rdir:,          ldir:/mount/apple,   volname:apple


