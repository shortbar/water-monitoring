import piface.pfio as pfio
from time import sleep

pfio.init()
switch_state = []
info = ["inactive", "active"]

for i in range(8):
    switch_state.append(pfio.digital_read(i+1))
    pfio.digital_write(i+1, switch_state[i])
    if switch_state[i] == 1:
        print "Input {0} is {1}".format(i+1, info[switch_state[i]])

try:
    while True:
        for i in range(8):
            if pfio.digital_read(i+1) != switch_state[i]:
                switch_state[i] = pfio.digital_read(i+1)
                pfio.digital_write(i+1, switch_state[i])
                print "Input {0} is {1}".format(i+1, info[switch_state[i]])
				
            else:
                pass
        sleep(.5)
except:
    pfio.init()
				 
				
