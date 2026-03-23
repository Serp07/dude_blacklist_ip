<a href="#"><img alt="updater_list_for_mikrotik last commit (main)" src="https://img.shields.io/github/last-commit/Serp07/dude_blacklist_ip/main?color=green&style=flat"></a>
<a href="#"><img alt="updater_list_for_mikrotik License" src="https://img.shields.io/github/license/Serp07/dude_blacklist_ip?color=orange&style=flat"></a>
[![required RouterOS version](https://img.shields.io/badge/RouterOS-7.xx-yellow?style=flat)](https://mikrotik.com/download/changelogs/)
[![required RouterOS version](https://img.shields.io/badge/RouterOS-6.xx-yellow?style=flat)](https://mikrotik.com/download/changelogs/)
# MikroTik dude blacklist ip Address List
IP Address List is based on detecting port scans through traps, as well as random connections to the dude server or the Mikrotik itself.
To add in automatic mode, you just need to create a script in Mikrotik.

###Script for adding
```
/tool fetch url="https://raw.githubusercontent.com/Serp07/dude_blacklist_ip/main/dude_blacklist.rsc" mode=https dst-path=dude_blacklist.rsc

:delay 2

/import file=dude_blacklist.rsc

:if ([:len [/ip firewall filter find comment="AUTO_BLACKLIST_DROP"]] = 0) do={

    /ip firewall filter add \
        chain=forward \
        in-interface=ether1 \
        src-address-list=Dude_blacklist \
        action=drop \
        comment="AUTO_BLACKLIST_DROP" \
      

}

}
```
