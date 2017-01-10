# Copyright (c) 2017 by Tsuyoshi Hamada. All rights reserved

target = iptables.sh

all:
	./generate.py ./blacklist.txt > ${target}
	chmod 755 ${target}


