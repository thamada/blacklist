#!/usr/bin/env python2.7
#Time-stamp: <2017-01-07 07:55:39 hamada>
import time
import glob
import Queue
import sys
import os.path
import logging as LG
import commands
import re

def gen_code(quotes):
    c = '''
iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD

iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT
iptables -P FORWARD DROP

iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -I INPUT -p icmp --icmp-type 0 -j ACCEPT
iptables -I INPUT -p icmp --icmp-type 8 -j ACCEPT

'''

    for s in quotes:
        c += 'iptables -A INPUT -m state --state NEW -p tcp -s '+ s +' --dport 22 -j DROP' + "\n"

    c +='''

iptables -A INPUT -p tcp --dport 22 -j ACCEPT

iptables -A INPUT -m limit --limit 1/s -j LOG --log-prefix '[IPTABLES INPUT] : '
iptables -A INPUT -j DROP
iptables -A FORWARD -m limit --limit 1/s -j LOG --log-prefix '[IPTABLES FORWARD] : '
iptables -A FORWARD -j DROP
'''
    return c


def gen_logger():
    # create logger
    logger = LG.getLogger(os.path.basename(__file__))
    logger.setLevel(LG.DEBUG)

    # create console handler and set level to debug
    ch = LG.StreamHandler()
    ch.setLevel(LG.DEBUG)
    
    # create formatter
    formatter = LG.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # add formatter to ch
    ch.setFormatter(formatter)
    
    # add ch to logger
    logger.addHandler(ch)
    
    # 'application' code
    ## logger.debug('debug message')
    ## logger.info('info message')
    ## logger.warn('warn message')
    ## logger.error('error message')
    ## logger.critical('critical message')
    return logger

def gen_blacklist(ifname, logger):
    # Get list of quates from arguments
    try:
        if not os.path.isfile(ifname):
            logger.error('File with black list not found!: %s', ifname)
            sys.exit(0)
        logger.info('Processing file with black list: %s', ifname)
    except:
        logger.error('Pass file path to black list!')
        sys.exit(0)
    
    blacklist  = [line.strip() for line in open(ifname)]

    pattern = r"#"

    blacklist2 = [ ]
    for line in blacklist:
        matchOB = re.split(pattern, line)
        l = matchOB[0]
        if l is not '':
            blacklist2.append(l)

    '''
    for line in blacklist2:
        print line
    '''

    return (blacklist2)


'''
!! What a Wonderful World. !!
'''
if __name__ == "__main__":
    logger = gen_logger()
    blacklist = gen_blacklist(sys.argv[1], logger)
    print gen_code(blacklist)
    
