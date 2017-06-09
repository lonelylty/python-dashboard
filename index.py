# coding=utf-8

from bottle import route, run, template,static_file
import ws_con
import json
from collections import OrderedDict


@route('/static/<filepath:path>')
def server_static(filepath):
       return static_file(filepath, root='./static/')


@route('/index/<num>')
def index(num):
	if num==None:
		num=10
	int_num=int(num)
	jlist=ws_con.connect_server(int_num)


	# 1. number of unique macaddr_client by hostname
	# 2. number of unique macaddr_client by channel
	# 3. all macaddr_client data recorded sorted by time received.
	dicbyHost=OrderedDict()
	dicbyChannel=OrderedDict()
	dicReuslt=OrderedDict()		

	for i in jlist:
		hostkey=i['hostname']+i['macaddr_client']
		channelkey=i['channel']+i['macaddr_client']
		
		if hostkey in dicbyHost:
			pass
		else:
			dicbyHost.setdefault(hostkey,i['hostname'])

		if channelkey in dicbyChannel:
			pass
		else:
			dicbyChannel.setdefault(channelkey,i['channel'])

	for k,v in dicbyHost:
		if v in dicReuslt:
			dicReuslt[v]=dicReuslt[v]+1
		else:
			dicReuslt.setdefault(v,1)
	
	xhost=json.dumps(list(dicReuslt.keys()))
	yhostCnt=json.dumps(list(dicReuslt.values()))
	dicReuslt.clear()

	for k,v in dicbyChannel:
		if v in dicReuslt:
			dicReuslt[v]=dicReuslt[v]+1
		else:
			dicReuslt.setdefault(v,1)

	xChannel=json.dumps(list(dicReuslt.keys()))
	ychannCnt=json.dumps(list(dicReuslt.values()))

	return template('index.html',xhost=xhost,yhostCnt=yhostCnt,xChannel=xChannel,ychannCnt=ychannCnt)

run(host='localhost', port=8084)