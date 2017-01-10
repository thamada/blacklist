
target = iptables.sh

all:
	./generate.py ./blacklist.txt > ${target}
	chmod 755 ${target}


