#!/usr/bin/env python
import json
print
def main():
	with open('./ref/fragments.txt','r') as f:
		doc = f.read().split('\n')
	frags = [x.split(',')[0] for x in doc if x.split(',')[0] !=''][::-1]
	print json.dumps(frags)
if __name__ == '__main__':
	main()