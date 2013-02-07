#!/usr/local/bin/python

import pexpect
import sys
import time

telnet = pexpect.spawn ('ssh -l admin 10.200.255.22')
telnet.logfile = sys.stdout
telnet.expect ('[Pp]assword: ')
telnet.sendline ('ysh3\'Skmt')
telnet.expect ('[$%#]')
telnet.sendline ('conf t')

eth_no = 101
while eth_no < 125 :
    interface_range = 'int eth %s/1/3-36' % eth_no
    trunk_mode = "switchport mode trunk" 
    native_vlan = "switchport trunk native vlan 254"
    allowed_vlan = " switchport trunk allowed vlan 254,2000,2004,2008,2012,2016,2020,2024,2028,2032,2036,2040,2044,2048,2052,2056,2060,2064,2068,2072,2076,2080,2084,2088,2092,2096,2100,2104,2108,2112,2116,2136,2152,2156,2160,2164,2168,2172,2176,2180,2184,2188,2192,2208,2212,2216,2236"
    snmp = "no snmp trap link-status"
    telnet.expect ('[$%#]')
    telnet.sendline (interface_range)
    telnet.expect ('[$%#]')
    telnet.sendline (trunk_mode)
    telnet.expect ('[$%#]')
    telnet.sendline (native_vlan)
    telnet.expect ('[$%#]')
    telnet.sendline (allowed_vlan)
    telnet.expect ('[$%#]')
    telnet.sendline (snmp)
    telnet.expect ('[$%#]')
    telnet.sendline ('exit')
    time.sleep(10)
    eth_no += 1

port_no = 3
lag_base = 3000

#MAKE PORT-CHANNEL
while lag_base < 3500 :
    for port_no in range(3,37) :
        lag_no = lag_base + port_no
        channel_no = 'interface port-channe %s' % lag_no
        trunk_mode = "switchport mode trunk"
        native_vlan = "switchport trunk native vlan 254"
        allowed_vlan = " switchport trunk allowed vlan 254,2000,2004,2008,2012,2016,2020,2024,2028,2032,2036,2040,2044,2048,2052,2056,2060,2064,2068,2072,2076,2080,2084,2088,2092,2096,2100,2104,2108,2112,2116,2136,2152,2156,2160,2164,2168,2172,2176,2180,2184,2188,2192,2208,2212,2216,2236"
        stp = "spanning-tree port type edge trunk"
        vpc = 'vpc %s' % lag_no
        telnet.expect ('[$%#]')
        telnet.sendline (channel_no)
        telnet.expect ('[$%#]')
        telnet.sendline (trunk_mode)
        telnet.expect ('[$%#]')
        telnet.sendline (native_vlan)
        telnet.expect ('[$%#]')
        telnet.sendline (allowed_vlan)
        telnet.expect ('[$%#]')
        telnet.sendline (stp)
        telnet.expect ('[$%#]')
        telnet.sendline (vpc)
        telnet.expect ('[$%#]')
        telnet.sendline ('exit')
        time.sleep(1)
    lag_base += 100

#PORT-CHANNEL APPLY FOR ETHERNET-PORT
#PORT-CHANNEL APPLY FOR ETHERNET-PORT
eth_no2 = 101
lag_base2 = 1100
port_no2 = 3
for eth_no2 in range(101,125) :
    for port_no2 in range(3,37) :
        interface = 'int eth %s/1/%s' % (eth_no2,port_no2)
        lag = lag_base2 + port_no2
        portchanel = "channel-group %s mode active" % lag
        telnet.expect ('[$%#]')
        telnet.sendline (interface)
        telnet.expect ('[$%#]')
        telnet.sendline (portchanel)
    time.sleep(1)
    lag_base2 += 100


telnet.expect ('[$%#]')
telnet.sendline ('end')
telnet.expect ('[$%#]')
telnet.sendline ('exit')
telnet.close
