import piface.pfio as pfio
from time import sleep
pfio.init()
out_list = [1, 2, 3, 4]
print "Press Ctrl-C to end"
try:
	while True:
		for i in range(4):
			pfio.digital_write(out_list[i-1],0)
			pfio.digital_write(out_list[i],1)
			sleep(1)
except:
	pfio.init()
