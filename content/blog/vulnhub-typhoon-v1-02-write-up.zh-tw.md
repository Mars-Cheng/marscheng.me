---
title: "[Vulnhub] Typhoon-v1.02 Write-up"
date: 2019-02-05
author: "Mars Cheng"
summary: "Information gathering java root@kali:~# nmap -sV -p- 192.168.1.104 Starting Nmap 7.70 ( https://nmap.org ) at 2019-02-02 09:07 EST Nmap scan report for 192.168.1.104 Host is up..."
translationKey: "vulnhub-typhoon-v1-02-write-up"
slug: "vulnhub-typhoon-v1-02-write-up"
aliases:
  - /blog/2019/vulnhub-typhoon-v1-02-write-up/
  - /2019/vulnhub-typhoon-v1-02-write-up/
tags:
  - "Penetration Testing"
  - "Vulnhub"
  - "OSCP"
  - "Write-up"
---

# Information gathering

```java
root@kali:~# nmap -sV -p- 192.168.1.104 
Starting Nmap 7.70 ( https://nmap.org ) at 2019-02-02 09:07 EST
Nmap scan report for 192.168.1.104
Host is up (0.0012s latency).
Not shown: 65511 closed ports
PORT      STATE SERVICE     VERSION
21/tcp    open  ftp         vsftpd 3.0.2
22/tcp    open  ssh         OpenSSH 6.6.1p1 Ubuntu 2ubuntu2 (Ubuntu Linux; protocol 2.0)
25/tcp    open  smtp        Postfix smtpd
53/tcp    open  domain      ISC BIND 9.9.5-3 (Ubuntu Linux)
80/tcp    open  http        Apache httpd 2.4.7 ((Ubuntu))
110/tcp   open  pop3        Dovecot pop3d
111/tcp   open  rpcbind     2-4 (RPC #100000)
139/tcp   open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
143/tcp   open  imap        Dovecot imapd (Ubuntu)
445/tcp   open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
631/tcp   open  ipp         CUPS 1.7
993/tcp   open  ssl/imaps?
995/tcp   open  ssl/pop3s?
2049/tcp  open  nfs_acl     2-3 (RPC #100227)
3306/tcp  open  mysql       MySQL (unauthorized)
5432/tcp  open  postgresql  PostgreSQL DB 9.3.3 - 9.3.5
6379/tcp  open  redis       Redis key-value store 4.0.11
8080/tcp  open  http        Apache Tomcat/Coyote JSP engine 1.1
27017/tcp open  mongodb     MongoDB 3.0.15
35295/tcp open  mountd      1-3 (RPC #100005)
35343/tcp open  status      1 (RPC #100024)
37629/tcp open  mountd      1-3 (RPC #100005)
43300/tcp open  nlockmgr    1-4 (RPC #100021)
49661/tcp open  mountd      1-3 (RPC #100005)
MAC Address: 00:0C:29:F4:3B:13 (VMware)
Service Info: Hosts:  typhoon, TYPHOON; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.80 seconds

```
![](https://i.imgur.com/CnCAXTp.png)

* We find many ports open from Nmap result, and we focoused on port 22,80,445 and 8080 to discover vulneraility.


In this machine,there are two exploit paths to get root privilege:
1. Get user privilege firstly, then get root privilege   
2. Get root privilege directly


# Get user privilege methods
In this stage, we use various methods to get user privilege

## 1.【Port 22】SSH login from mongoadmin

* We browse robots.txt, and find the path of disallow /mongoadmin/
![](https://i.imgur.com/TCCxf25.png)

* We get username "typhoon" and password "789456123" from mongoadmin
![](https://i.imgur.com/rHaDktw.png)

* Login SSH service success and get  user(typhoon) privilege
![](https://i.imgur.com/OCEzoFI.png)

## 2.【Port 80】LotusCMS vulnerability using metasploit
* We use dirb tool to enumerate web path, and we find path /cms/
![](https://i.imgur.com/oj3go5h.png)

* We search keyword "lotus cms" with metasploit which used to check whether exist known vulnerability, and use lcms_php_exec module to exploit, and success to get shell and user(www-data) privilege
![](https://i.imgur.com/kQLAtOp.png)


## 3.【Port 80】CVE-2018-7600 vulnerability exploit

* We use dirb tool to enumerate web path, and we find path /drupal/
![](https://i.imgur.com/HeduPhy.png)

* We search keyword "drupel" with metasploit which used to check whether exist known vulnerability, and use drupal_drupalgeddon2 module to exploit, and success to get shell and user(www-data) privilege
![](https://i.imgur.com/3wqCnLC.png)


## 4.【Port 8080】Manager upload using metasploit  
* We connect port 8080 and discover tomcat manager.
![](https://i.imgur.com/jMA9uFG.png)

* We search keyword "tomcat" with metasploit which used to check whether exist known vulnerability
![](https://i.imgur.com/tWyyOaC.png)

* We use tomcat_mgr_upload module to exploit, and success to get shell and user(tomcat7) privilege
![](https://i.imgur.com/exuiUGu.png)

![](https://i.imgur.com/cJHMDqP.png)



# Get root privilege methods based on user privilege
In this stage, we use various methods to get root privilege which based on user pvivilege has been obtained

## 1. Crack /etc/shadow hash
* After we get user(typhoon) privilege, we use command "find /usr/bin/ -perm -4000" to find the command "head" we can exploit
![](https://i.imgur.com/AeZypUZ.png)

* We use command "head /etc/shadow" to get the shadow file , and try to crack it
![](https://i.imgur.com/LD5sa7r.png)

* We crack 3 users hash, and plaintext stores in cracked.txt
![](https://i.imgur.com/IndHQHs.png)

![](https://i.imgur.com/JmQb0jH.png)

* We change user from "typhoon" to "admin". However, user admin as root privilege 

![](https://i.imgur.com/7KrmQdm.png)

## 2. Replace /etc/shadow hash
* After we get user(typhoon) privilege, we use command "find /usr/bin/ -perm -4000" to find the command "vim" we can exploit
![](https://i.imgur.com/AeZypUZ.png)
* We edit "/etc/shadow" with "vim" 
![](https://i.imgur.com/kfDQg7h.png)

* We copy the hash of root in Kali
![](https://i.imgur.com/yutJQt0.png)

* We paste the hash of root in Kali to machine typhoon
![](https://i.imgur.com/qvOtzMG.png)

* we change yser from "typhoon" to "root"
![](https://i.imgur.com/pCsWiNE.png)

## 3. Linux kernel exploit
* After we get user(typhoon) privilege, we get linux kernel version with command "uname -a"
![](https://i.imgur.com/vbxoG7w.png)

* we search kernel exploit with command "searchsploit 3.13.0"
![](https://i.imgur.com/DgjtD3F.png)

* we copy exploit "37292.c" to /var/www/thml 
![](https://i.imgur.com/rX5E50g.png)

* we download file "37292.c" from kali, and compile and execute it.
![](https://i.imgur.com/q9bZtAv.png)

* Success to get root privilege
![](https://i.imgur.com/R8Uodea.png)

# Get root privilege 
## 1.【Port 445】CVE-2017-7494 vulnerability exploit 

* We use nmap script to scan the vulneraility about Samba, and we found that CVE-2017-7494 may exist
![](https://i.imgur.com/Q5aFuMR.png)

* We search keyword "CVE-2017-7494" with metasploit which used to check whether exist known vulnerability
![](https://i.imgur.com/IhKQETg.png)

* We use is_known_pipename module to exploit, and success to get shell and root privilege
![](https://i.imgur.com/cocdf7o.png)
