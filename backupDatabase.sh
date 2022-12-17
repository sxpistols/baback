#!/bin/bash

export PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/labs247/.local/bin:/home/labs247/bin

cd /home/labs247/dolswork/back

echo "START"
TANGGAL=`date +%d%b%Y`

mysqldump -u employee -p"Syabian247#" employee > backupDatabaseMendoan.${TANGGAL}.sql

gzip backupDatabaseMendoan.${TANGGAL}.sql

ls -lrt backupDatabaseMendoan.${TANGGAL}.sql.gz
echo "Backup Done!"
