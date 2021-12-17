#!/bin/sh

CERT_FILE=/new_root/etc/ssl/certs/ca-certificates.crt
mkdir -p $(dirname $CERT_FILE)
CERTS=$(find /new_root/usr/share/ca-certificates -type f | sort)

for cert in $CERTS; do
	echo $(basename $cert)
	cat $cert >> $CERT_FILE
done