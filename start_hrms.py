#!/usr/bin/env python
import subprocess,sys,requests,os,time
def start_server():
	print '*** starting server ***'
	subprocess.Popen(['python hrms_server.py &'],shell=True)
	subprocess.Popen(["(echo 'Spawned from: '; pwd) > $HOME/p/server_data.txt"],shell=True)
	time.sleep(.5)
	subprocess.Popen(['open -a firefox http://localhost:8000/hrms'],shell=True)
def main():
	print;print '*** hrms starting ***'
	proc = subprocess.Popen(['ps -fA | grep python'],stdout=subprocess.PIPE,shell=True).communicate()[0]
	server_running = [x.split() for x in proc.split('\n') if 'server.py' in x.split() or 'hrms_server.py' in x.split()]
	
	if server_running:
		print '*** found server running ***'
		print '*** the following information is available:'
		print ' '.join(server_running[0])
		with open('/Users/markharvey/p/server_data.txt','r') as f:
			server_data = f.read().split('\n')[1]
		print '*** server_data.txt reads:'
		print 'Spawned from: '
		print '\t',server_data
		
		current_directory = subprocess.Popen(['pwd'],stdout=subprocess.PIPE,shell=True).communicate()[0].replace('\n','')
		print 'Current directory is:'
		print '\t',current_directory
		time.sleep(.5)
		if current_directory == server_data:
			subprocess.Popen(['open -a firefox http://localhost:8000/hrms'],shell=True)
		else:
			kill_server = ''
			while kill_server not in list('ynq'):
				kill_server = raw_input('Kill active server? (y n q): ')
			if kill_server == 'q':
				print '*** exiting ***';sys.exit()
			if kill_server == 'y':
				kill_command = 'kill ' + server_running[0][1]
				subprocess.Popen([kill_command],shell=True)
				start_server()	
			if kill_server == 'n':
				print 'Server was spawned elsewhere. Kill process and start server to continue.'
	else:
		start_server() 

if __name__ == '__main__':
	main()


