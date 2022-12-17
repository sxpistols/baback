#!/bin/bash


source venv/bin/activate

if [ -e 'board.csv' ];then
    mv board.csv board.csv.old
fi

python BoardList2.py > board.csv

if [ ! -e 'board.txt' ]; then
    echo "System Error"
    exit
fi

echo "START : at "`date`
#cat board.txt | jsonv id,name,url,shortUrl,idOrganization,dateLastActivity,desc > board.csv
diff board.csv board.csv.old | awk -F"\"" '{if($2!=""){print $2}}'  | sort -u > toproc.txt

####### INI DI DELETE

#awk -F"\"" '{if($2!=""){print $2}}' board.csv | sort -u > toproc.txt

#######
if [ -s 'toproc.txt' ];then
     echo "Ada perubahan Lanjutkan, berikut ini daftar board yang berubah"
     cat toproc.txt
else
     echo "Ga Ada perubahan"
     echo "END : at "`date`
     exit
fi
###############


if [ -e 'list.csv' ]; then
    rm list.csv
    echo "rm list.csv"
fi

if [ -e 'card.csv' ]; then
    rm card.csv
    echo "rm card.csv"
fi

if [ -e 'boardactions.csv' ]; then
    echo "rm boardactions.csv"
    rm boardactions.csv
fi


if [ -e 'toproc.txt' ];then
    for ii in `cat toproc.txt`;do
        echo `date`" : Start Proses Board ID : $ii"
        # python boardDetail.py $ii
        # if [ -e 'boarddetail.txt' ]; then
        #     cat boarddetail.txt | jsonv id,url,shortUrl,idOrganization,desc > boarddetail.csv
        # fi

        python getBoardsList.py $ii
        if [ -e 'boardslist.txt' ];then
            cat boardslist.txt | jsonv id,idBoard,name,closed,pos,softLimit,subscribed >> list.csv
        fi

        python getBoardCards.py $ii
        if [ -e 'boardscard.txt' ];then
            cat boardscard.txt | jsonv id,idBoard,idList,name,closed,pos,due,url >> card.csv
            # echo $ii
        fi

        # for detail in `cat toproc.txt`; do
        echo "python boardAction.py $ii"
        python boardAction.py $ii
        if [ -e 'boardactions.txt' ]; then
            cat boardactions.txt | jsonv id,data.board.id,data.list.id,data.card.id,type,date,memberCreator.id,memberCreator.username,memberCreator.fullName,data.text,data.attachment.id,data.attachment.name,data.attachment.url,member.id,member.username,member.fullName,data.cardSource.id,data.cardSource.name,data.boardSource.id >> boardactions.csv
        fi
            # exit
        # done
        echo `date`" : Selesai Proses Board ID : $ii"
    done

    #### LOAD TO MYSQL
    echo "mysqlimport --fields-terminated-by=, --fields-optionally-enclosed-by='\"' --local -v -u employee -pSyabian247# employee -h localhost list.csv"
    mysqlimport --fields-terminated-by=, --fields-optionally-enclosed-by='\"' --local -v -u employee -pSyabian247# employee -h localhost list.csv
    echo "mysqlimport --fields-terminated-by=, --fields-optionally-enclosed-by='\"' --local -v -u employee -pSyabian247# employee -h localhost card.csv"
    mysqlimport --fields-terminated-by=, --fields-optionally-enclosed-by='\"' --local -v -u employee -pSyabian247# employee -h localhost card.csv

    echo "mysqlimport --fields-terminated-by=, --fields-optionally-enclosed-by='\"' --local -v -u employee -pSyabian247# employee -h localhost boardactions.csv"
    mysqlimport --fields-terminated-by=, --fields-optionally-enclosed-by='\"' --local -v -u employee -pSyabian247# employee -h localhost boardactions.csv

fi


####### INSERT BOARD LIST DI AKHIR
# cp boards_list.csv board.csv
mysqlimport --replace --fields-terminated-by=, --fields-optionally-enclosed-by='\"' --local -v -u employee -pSyabian247# employee -h localhost board.csv

echo "END : at "`date`

