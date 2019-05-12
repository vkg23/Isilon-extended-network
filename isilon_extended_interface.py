import sys
import ipaddress
import socket
from subprocess import Popen, DEVNULL
import subprocess
import time

myarray = []
ip_pools = {}
protocolString = ['smb','worm']
username = 'admin'

def collectdata(mycluster,command):
	print ("Collecting Data: ", mycluster,command,' => ',end='', flush=True)
	rawarray=[]
	try:
		cli_result = subprocess.check_output(['/usr/bin/ssh','-l',username,mycluster,command])
		rawarray=cli_result.decode("utf-8")
	except:
		print ("Failed!")
		sys.exit()
	else:
		print(f'Done. {len(rawarray)} lines received')
		return(rawarray)


def valid_ip(address):
		try:
			parts=address.split(".")
			if len(parts) == 4:
				return True
		except:
			return False

def get_iplist(data):
	print(f'Fetching IPs configured:',end='',flush=True)
	result = []
	for eachline in data.split('\n'):
			if eachline != '':
				myarray.append(eachline)
	for i in  range(1,len(myarray)):
		line=myarray[i]
		address=line.split()[-1]
		if valid_ip(address) == True:
			result.append(address)
	print(f':{len(result)} ip\'s')
	return(result)


def mass_ping(iplist):
	print(f'Triggering Ping for {len(iplist)} ip\'s: ',end='',flush=True)
	p = {} # ip -> process
	result = {}
	timeout = 50 #seconds
	for ip in iplist:
		p[ip]=subprocess.Popen(['ping','-c2',ip],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	#check Stats
	start_time = time.time()
	while p:
		for ip, proc in p.items():
			elapsed_time = time.time() - start_time
			if elapsed_time < timeout:
				if proc.poll() is not None: # ping finished
					del p[ip] # remove from the process list
					if proc.poll() == 0:
						y=proc.stdout.readlines()
						ploss=y[-2].decode("utf-8").split(',')[2].split()[0]
						rtt_avg=y[-1].decode("utf-8").split('/')[4]
						z=rtt_avg + 'ms(' + ploss + ')'
					else:
						z='xx'
					result[ip] = z
					break
			else:
				proc.kill()
				del p[ip]
				z = 'TimeOut'
				result[ip] = z
				break
	print(f' Done')
	return (result)

def mass_smbShareCheck(iplist):
	myarg = 'more SANTeam_Monitor_Flagfile.txt'
	p = {}
	q = {}
	#protocolString = ['smb','worm']
	print(f'Triggering SmbClient ShareCheck for SMB pool ip\'s matching names {protocolString}: ',end='',flush=True)
	for ip in iplist:
		x = findipPool(ip)
		if  protocolString[0] in x or protocolString[1] in x:
			ip_arg='\\\\'+ ip + '\\santeam_test'
			p[ip]=Popen(['smbclient',ip_arg,'-A','mysmbcfg.cfg','-c',myarg],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		else:
			q[ip] = "skip"

	start_time = time.time()
	while p:
		for ip, proc in p.items():
			elapsed_time = time.time() - start_time
			if elapsed_time < 5:
				if proc.poll() is not None: # ping finished
					del p[ip] # remove from the process list
					x=proc.stdout.readlines()[-1] #Usually errors are see in
					if proc.returncode == 0:
						if 'Alpha23' in str(x):
							q[ip] = "OK[Active]"
						else:
							q[ip] = "NOK[Miss_File]!"
					elif proc.returncode == 1:
						q[ip] = "NOK[Failed]!"
					else:
						q[ip] = "NOK[Unknwn.error]!"
					break
			else:
				proc.kill()
				q[ip] = "NOK[Timeout]!"
				del p[ip]
				break
	print(f' done')
	return (q)

def get_ip_pool():
	pools = {}
	ID = ''
	iplistdict = {}
	for line in isi_pool_list_v.split('\n'):
		if ID == '':
			if line.find('ID:') != -1:
				ID = line.split()[1]
				pools[ID] ={}
				#print(ID)
		if ID != "":
			if line.find('IP Ranges:') != -1:
				IPR = line.split()[2:]
				pools[ID]['iplist'] = IPR
				ID = ''
	#print(pools)
	for key in pools.keys():
		iplistdict[key] = {}
		iplistdict[key]['flist'] = []
		for item in pools[key]['iplist']:
			if item != '-':
				if item.find('-') != -1:
					tmparray = []
					low=item.split('-')[0].strip(',')
					high=item.split('-')[1].strip(',')
					start_ip = ipaddress.IPv4Address(low)
					end_ip = ipaddress.IPv4Address(high)
					for ip_int in range(int(start_ip), int(end_ip)+1):
						ip1 = str(ipaddress.IPv4Address(ip_int))
						iplistdict[key]['flist'].append(ip1)
				else:
					thisip = item.strip(',')
					iplistdict[key]['flist'].append(thisip)
	return (iplistdict)


def findipPool(whichip):
	poolname=''
	for key in ip_pools.keys():
		if whichip in ip_pools[key]['flist']:
				poolname=key.split('.')[2]
				break
	if poolname != '':
		return(poolname)
	else:
		return("NA")

def getfqdn(iplist):
	print (f'Fetching for any Reverselookup Names for {len(iplist)} ip\'s:',end='',flush	=True)
	result = {}
	for ip in iplist:
		try:
			hname=socket.gethostbyaddr(address)[0]
			result[ip] = hname
		except:
			result[ip] = "***"
	print(Done)
	return(result)





mycluster = input("Cluster Name?: ")

isi_interface_list_out=collectdata(mycluster,'isi network interface list')
isi_pool_list_v=collectdata(mycluster,'isi network pools list -v')

iplist = get_iplist(isi_interface_list_out)
mass_ping_stat = mass_ping(iplist)
ip_pools = get_ip_pool()
mass_smbShareCheck_stat=mass_smbShareCheck(iplist)



print ('Generating Extended \'isi network interface\' output')
print (f'prints \033[1;31;40m RedColour\033[0;37;40m if NOK for Ping/ShareCheck result\n\n')
time.sleep(1)
print(myarray[0],'\033[2;33;40m {:17} {:20}  {:40} \033[0;37;40m'.format("Ping_RTT/(%Ploss)","SmbClient-ShareCheck","isiBugfix:NetPool",)) #heading Print.
for i in  range(1,len(myarray)):
	line=myarray[i]
	address=line.split()[-1]
	if valid_ip(address) == True:
			print(line,' ',end='',flush=True)
			NewCol1Value = mass_ping_stat[address]
			NewCol3Value = findipPool(address)
			NewCol2Value = mass_smbShareCheck_stat[address]
			if 'xx' in NewCol1Value or 'NOK' in NewCol2Value:
				print ('\033[1;31;40m{:17} {:20}  {:40}\033[0;37;40m'.format(NewCol1Value,NewCol2Value,NewCol3Value))
			else:
				print ('{:17} {:20}  {:40}'.format(NewCol1Value,NewCol2Value,NewCol3Value))

	else:
		print (line)
	time.sleep(.200)



