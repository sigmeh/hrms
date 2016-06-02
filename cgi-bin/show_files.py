#!/usr/bin/env python
import subprocess,json
print
def main():
	file_list = subprocess.Popen(['ls ./data_files'],stdout=subprocess.PIPE,shell=True).communicate()[0]
	file_list = [x for x in file_list.split('\n') if x[len(x)-3:] == 'csv']
	print json.dumps(file_list)
if __name__ == '__main__':
	main()