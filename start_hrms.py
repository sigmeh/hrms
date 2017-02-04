#!/usr/bin/env python
import subprocess,sys,requests,os,time
def start_server():

	print '*** starting server ***'
	subprocess.Popen(['python hrms_server.py &'],shell=True)						#start server
	time.sleep(.5)
	subprocess.Popen(['open -a firefox http://localhost:8000/hrms'],shell=True)		#open page in firefox browser; change browser preference here

def main():																			#remove "-a firefox" to open in default browser
	print;print '*** hrms starting ***'
	proc = subprocess.Popen(['ps -fA | grep python'],stdout=subprocess.PIPE,shell=True).communicate()[0]	#check for active python processes
	server_running = [x.split() for x in proc.split('\n') if 'hrms_server.py' in x.split()]					#check for active hrms_server.py
	
	if server_running:
		print '*** found server running ***'
		print '*** the following information is available:'
		print ' '.join(server_running[0])											#print information about running server
		kill_server = ''
		while kill_server not in list('ynq'):										#option to kill server
			kill_server = raw_input('Kill active server? (y n q): ')
		if kill_server == 'q':														#quit
			print '*** exiting ***';sys.exit()
		if kill_server == 'y':														#kill server
			kill_command = 'kill ' + server_running[0][1]
			subprocess.Popen([kill_command],shell=True)
			start_server()															#start server
		if kill_server == 'n':														#do not kill server
			try:
				subprocess.Popen(['open -a http://localhost:8000/hrms'],shell=True)				#try localhost
			except:
				print 'hrms_server.py seems to have been spawned elsewhere. Kill process to continue.' 	#server started from elsewhere
	else:
		start_server() 

if __name__ == '__main__':
	main()


