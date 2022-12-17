#!/bin/bash


FN=`ls -lrt *.sql.gz | tail -1 | awk '{print $9}'`

echo git add -f ${FN}
git add -f ${FN}

DAT=`date | sed -e 's/ //g'`
git commit -m "Backup DB ${DAT}"
git push <<EOF
arief.dolants
sexpistols123!
EOF
