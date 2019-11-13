#!/usr/bin/python2

import socket, select, subprocess

# create the listener socket
listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('', 8081))

listener.listen(10)
# put the socket in a list as input to the select command
allsocks = [listener]



while 1:
    # we're only interested in the readers that are ready.
    ready, output, exceptions = select.select(allsocks, [], [])
    for sock in ready:
        # either it's the listening socket:
        if sock == listener:
            c, addr = listener.accept()
            print "New connection from ", addr
            allsocks.append(c)
        # otherwise, it's a command to execute from a
        #  previously established client socket
        else:
            commstr = sock.recv(1024) # max size
            if commstr: # if it's not empty
                # split up into command + arguments
                command = commstr.rstrip().split(" ")
		if (command[0] == "exit"): 
			sock.close()
		        allsocks.remove(sock)
		else:
		        print "Executing command: \n", command
			#was using output to try sending comand with join
			output = ' '.join(command)
		        # want to run with exception handling,
		        # so a mistake doesn't bring the whole server down
		        try:
		            out = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
		        except:
		            out = "Command failed\n"
		            sock.send(out)
		        else: # command finished, send the output to client
		            sock.send(out)
		            # only one command per connection, for now...
		          #sock.close()
		           #allsocks.remove(sock)
s.close()
