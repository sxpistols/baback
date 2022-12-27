from run import db
from passlib.hash import pbkdf2_sha256 as sha256
from flask_mysqldb import MySQL
import json
from flask_cors import CORS
# from sqlalchemy import create_engine
# import pymysql
import os
import pandas as pd
from datetime import datetime
import seaborn as sns
import pandas.io.formats.excel


class Report():
    @classmethod
    def getReport(cls, tanggal, user_role):
        # cls.query.filter_by(user_id = user_id).first
        # print(tanggal,flush=True)

        if(user_role == '6'):
            divisix = 'SDO'
        else:
            divisix = 'PMO'

        
        concat = pd.core.frame.DataFrame
        bul = datetime.strptime(tanggal,'%Y-%m')
        bulan = bul.strftime('%b')
        tahun = bul.strftime('%Y')
        tahun = tahun[2:4]
        print('DIVISIX :::: '+divisix,flush=True)

        query = "select distinct karyawan.fullname,timesheet.tanggal_01,timesheet.tanggal_02,timesheet.tanggal_03,timesheet.tanggal_04,timesheet.tanggal_05, \
timesheet.tanggal_06,timesheet.tanggal_07,timesheet.tanggal_08,timesheet.tanggal_09,timesheet.tanggal_10,timesheet.tanggal_11,timesheet.tanggal_12, \
timesheet.tanggal_13,timesheet.tanggal_14,timesheet.tanggal_15,timesheet.tanggal_16,timesheet.tanggal_17,timesheet.tanggal_18,timesheet.tanggal_19, \
timesheet.tanggal_20,timesheet.tanggal_21,timesheet.tanggal_22,timesheet.tanggal_23,timesheet.tanggal_24, \
timesheet.tanggal_25,timesheet.tanggal_26,timesheet.tanggal_27,timesheet.tanggal_28,timesheet.tanggal_29, \
timesheet.tanggal_30,timesheet.tanggal_31 from karyawan left join ( \
select b.fullname fullname, \
 sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '01' then '1' end) as tanggal_01, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '02' then '1' end) as tanggal_02, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '03' then '1' end) as tanggal_03, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '04' then '1' end) as tanggal_04, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '05' then '1' end) as tanggal_05, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '06' then '1' end) as tanggal_06, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '07' then '1' end) as tanggal_07, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '08' then '1' end) as tanggal_08, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '09' then '1' end) as tanggal_09, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '10' then '1' end) as tanggal_10, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '11' then '1' end) as tanggal_11, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '12' then '1' end) as tanggal_12, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '13' then '1' end) as tanggal_13, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '14' then '1' end) as tanggal_14, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '15' then '1' end) as tanggal_15, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '16' then '1' end) as tanggal_16, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '17' then '1' end) as tanggal_17, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '18' then '1' end) as tanggal_18, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '19' then '1' end) as tanggal_19, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '20' then '1' end) as tanggal_20, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '21' then '1' end) as tanggal_21, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '22' then '1' end) as tanggal_22, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '23' then '1' end) as tanggal_23, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '24' then '1' end) as tanggal_24, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '25' then '1' end) as tanggal_25, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '26' then '1' end) as tanggal_26, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '27' then '1' end) as tanggal_27, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '28' then '1' end) as tanggal_28, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '29' then '1' end) as tanggal_29, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '30' then '1' end) as tanggal_30, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '31' then '1' end) as tanggal_31 \
from boardactions a, trello_karyawan b \
  where substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+tanggal+"' \
  and a.username = b.trelloid \
  group by fullname) as timesheet \
 on lower(karyawan.fullname) = lower(timesheet.fullname) \
where karyawan.divisi in ('"+divisix+"') and karyawan.posisi != 'Support Surveillance' and status = 'Active' order by karyawan.fullname asc;"

        query2 = "select distinct karyawan.fullname fullname, \
case when timesheet.tanggal_01 is not null then 'Hadir' else '' end as '01-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_02 is not null then 'Hadir' else '' end as '02-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_03 is not null then 'Hadir' else '' end as '03-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_04 is not null then 'Hadir' else '' end as '04-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_05 is not null then 'Hadir' else '' end as '05-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_06 is not null then 'Hadir' else '' end as '06-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_07 is not null then 'Hadir' else '' end as '07-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_08 is not null then 'Hadir' else '' end as '08-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_09 is not null then 'Hadir' else '' end as '09-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_10 is not null then 'Hadir' else '' end as '10-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_11 is not null then 'Hadir' else '' end as '11-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_12 is not null then 'Hadir' else '' end as '12-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_13 is not null then 'Hadir' else '' end as '13-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_14 is not null then 'Hadir' else '' end as '14-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_15 is not null then 'Hadir' else '' end as '15-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_16 is not null then 'Hadir' else '' end as '16-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_17 is not null then 'Hadir' else '' end as '17-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_18 is not null then 'Hadir' else '' end as '18-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_19 is not null then 'Hadir' else '' end as '19-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_20 is not null then 'Hadir' else '' end as '20-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_21 is not null then 'Hadir' else '' end as '21-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_22 is not null then 'Hadir' else '' end as '22-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_23 is not null then 'Hadir' else '' end as '23-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_24 is not null then 'Hadir' else '' end as '24-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_25 is not null then 'Hadir' else '' end as '25-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_26 is not null then 'Hadir' else '' end as '26-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_27 is not null then 'Hadir' else '' end as '27-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_28 is not null then 'Hadir' else '' end as '28-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_29 is not null then 'Hadir' else '' end as '29-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_30 is not null then 'Hadir' else '' end as '30-"+bulan+"-"+tahun+"', \
case when timesheet.tanggal_31 is not null then 'Hadir' else '' end as '31-"+bulan+"-"+tahun+"' \
from karyawan left join (  \
select b.fullname fullname,  \
 sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '01' then '1' end) as tanggal_01, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '02' then '1' end) as tanggal_02, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '03' then '1' end) as tanggal_03, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '04' then '1' end) as tanggal_04, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '05' then '1' end) as tanggal_05, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '06' then '1' end) as tanggal_06, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '07' then '1' end) as tanggal_07, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '08' then '1' end) as tanggal_08, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '09' then '1' end) as tanggal_09, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '10' then '1' end) as tanggal_10, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '11' then '1' end) as tanggal_11, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '12' then '1' end) as tanggal_12, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '13' then '1' end) as tanggal_13, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '14' then '1' end) as tanggal_14, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '15' then '1' end) as tanggal_15, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '16' then '1' end) as tanggal_16, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '17' then '1' end) as tanggal_17, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '18' then '1' end) as tanggal_18, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '19' then '1' end) as tanggal_19, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '20' then '1' end) as tanggal_20, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '21' then '1' end) as tanggal_21, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '22' then '1' end) as tanggal_22, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '23' then '1' end) as tanggal_23, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '24' then '1' end) as tanggal_24, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '25' then '1' end) as tanggal_25, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '26' then '1' end) as tanggal_26, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '27' then '1' end) as tanggal_27, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '28' then '1' end) as tanggal_28, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '29' then '1' end) as tanggal_29, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '30' then '1' end) as tanggal_30, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '31' then '1' end) as tanggal_31 \
from boardactions a, trello_karyawan b \
  where substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+tanggal+"' \
  and a.username = b.trelloid \
  group by fullname) as timesheet \
 on lower(karyawan.fullname) = lower(timesheet.fullname) \
where karyawan.divisi in ('"+divisix+"') and karyawan.posisi != 'Support Surveillance' and status = 'Active' order by karyawan.fullname asc;"

        print(query2,flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        df = pd.read_sql(query, db.session.bind)

        # print(df,flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter('Timesheet_Karyawan_'+bulan+'_20'+tahun+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='YlOrRd').highlight_null('white').to_excel(writer, sheet_name ='Timesheet-'+bulan, startrow=1,startcol=1, index=True)
        writer.save()

        ### REPORT UNTUK HRD
        df = pd.read_sql(query2, db.session.bind)

        # print(df,flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter('Timesheet_HRD_Karyawan_'+bulan+'_20'+tahun+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name ='Timesheet-'+bulan, startrow=1,startcol=1, index=True)
        writer.save()


        db.session.close()
        return { 'Report': a }, 200

    @classmethod
    def getBoards(cls, tahun, bulan, tanggal,user_role):
        # cls.query.filter_by(user_id = user_id).first
        # print(tanggal,flush=True)
        if(user_role == '6'):
            query = "select id boardid,name boardname, 'Riset' project_type, 'ACTIVE' status,shortUrl url,substring(CONVERT_TZ(dateLastActivity,'+00:00','+07:00'),1,19) lastactivity \
from board where \
substring(CONVERT_TZ(dateLastActivity,'+00:00','+07:00'),1,4) = '"+tahun+"' \
and name in (select * from ( select distinct name from ( \
select b.name,b.id,tk.fullname,type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,19) tanggal \
from boardactions a, trello_karyawan tk, board b, karyawan k \
where a.username  = tk.trelloid \
and b.id = a.board_id  \
and tanggal >= subdate(current_date, 60) \
and k.fullname  = tk.fullname \
and k.divisi = 'SDO' \
and substring(CONVERT_TZ(a.tanggal,'+00:00','+07:00'),1,4) = '"+tahun+"' \
order by tanggal desc) a) as subq ) \
order by dateLastActivity desc;" 
        else:
            query = "select * from (select id boardid,name boardname,shortUrl url,substring(CONVERT_TZ(dateLastActivity,'+00:00','+07:00'),1,19) lastactivity \
from board where \
substring(CONVERT_TZ(dateLastActivity,'+00:00','+07:00'),1,4) = '"+tahun+"' \
and name in (select * from ( select distinct name from ( \
select b.name,b.id,tk.fullname,type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,19) tanggal \
from boardactions a, trello_karyawan tk, board b, karyawan k \
where a.username  = tk.trelloid \
and b.id = a.board_id  \
and tanggal >= subdate(current_date, 60) \
and k.fullname  = tk.fullname \
and k.divisi = 'PMO' \
and substring(CONVERT_TZ(a.tanggal,'+00:00','+07:00'),1,4) = '"+tahun+"' \
order by tanggal desc) a) as subq ) \
order by dateLastActivity desc) a \
left join project_setting ps \
ON a.boardid = ps.board where ps.projectdiv = 'PMO';" 
            query = "select * from (select id boardid,name boardname,shortUrl url,substring(CONVERT_TZ(dateLastActivity,'+00:00','+07:00'),1,19) lastactivity \
from board bb, project_setting ps where \
ps.board = bb.id \
and ps.status = 'ACTIVE' \
and bb.name in (select * from ( select distinct name from ( \
select b.name,b.id,tk.fullname,type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,19) tanggal \
from boardactions a, trello_karyawan tk, board b, karyawan k \
where a.username  = tk.trelloid  \
and b.id = a.board_id  \
and k.fullname  = tk.fullname \
order by tanggal desc) a) as subq ) \
order by dateLastActivity desc) a \
left join project_setting ps \
ON a.boardid = ps.board where ps.projectdiv = 'PMO';" 
        # print(query,flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        dbQuery = "select fullname,b.name board_name, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '01' then '1' end) as '01-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '02' then '1' end) as '02-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '03' then '1' end) as '03-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '04' then '1' end) as '04-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '05' then '1' end) as '05-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '06' then '1' end) as '06-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '07' then '1' end) as '07-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '08' then '1' end) as '08-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '09' then '1' end) as '09-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '10' then '1' end) as '10-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '11' then '1' end) as '11-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '12' then '1' end) as '12-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '13' then '1' end) as '13-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '14' then '1' end) as '14-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '15' then '1' end) as '15-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '16' then '1' end) as '16-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '17' then '1' end) as '17-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '18' then '1' end) as '18-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '19' then '1' end) as '19-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '20' then '1' end) as '20-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '21' then '1' end) as '21-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '22' then '1' end) as '22-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '23' then '1' end) as '23-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '24' then '1' end) as '24-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '25' then '1' end) as '25-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '26' then '1' end) as '26-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '27' then '1' end) as '27-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '28' then '1' end) as '28-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '29' then '1' end) as '29-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '30' then '1' end) as '30-"+bulan+"', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '31' then '1' end) as '31-"+bulan+"' \
from boardactions a, board b \
where a.board_id = b.id \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+tanggal+"' \
group by fullname,board_name order by board_name,fullname;"


        df = pd.read_sql(dbQuery, db.session.bind)

        # print(df,flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')
		# Timesheet_Trello_PerProject_'+bulan+'_'+tahun+'.xlsx
        writer = pd.ExcelWriter('Board_Report_PerProject_'+bulan+'_'+tahun+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name ='Timesheet-'+bulan, startrow=1,startcol=1, index=True)
        writer.save()

        db.session.close()

        return { 'Boards': a }, 200

    @classmethod
    def allBoards(cls, user_role):
        # cls.query.filter_by(user_id = user_id).first
        # print(tanggal,flush=True)
        query = "select name, shortUrl, substring(dateLastActivity, 1,10) lastactivity from board;"
        # print(query,flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        db.session.close()

        return { 'Boards': a }, 200

    @classmethod
    def getBoardsNot(cls, tahun, user_role):
        # cls.query.filter_by(user_id = user_id).first
        # print(tanggal,flush=True)
        query = "select distinct name,id from ( \
select b.name,b.id,tk.fullname,type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,19) tanggal \
from boardactions a, trello_karyawan tk, board b, karyawan k \
where a.username  = tk.trelloid \
and b.id = a.board_id  \
and tanggal >= subdate(current_date, 60) \
and k.fullname  = tk.fullname \
and k.divisi = 'PMO' \
and substring(CONVERT_TZ(a.tanggal,'+00:00','+07:00'),1,4) = '"+tahun+"' \
order by tanggal desc) a where id not in (select board from project_setting ps );" 

        query = "select distinct name,id from ( \
select b.name,b.id,tk.fullname,type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,19) tanggal \
from boardactions a, trello_karyawan tk, board b, karyawan k \
where a.username  = tk.trelloid \
and b.id = a.board_id  \
and k.fullname  = tk.fullname and k.divisi in ('PMO', 'Owner') \
order by tanggal desc) a where id not in (select board from project_setting ps );" 

        query = "select distinct name,id from ( \
select b.name,b.id,tk.fullname,type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,19) tanggal \
from boardactions a, trello_karyawan tk, board b, karyawan k \
where a.member_username  = tk.trelloid \
and b.id = a.board_id  \
and k.fullname  = tk.fullname \
and k.posisi = 'Project Manager' \
order by tanggal desc) a where id not in (select board from project_setting ps );"

        # print(query,flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        db.session.close()

        return { 'Boards': a }, 200

    @classmethod
    def getDetail(cls, boardid, tanggal):
        # cls.query.filter_by(user_id = user_id).first
        # print(boardid,flush=True)
        # print(tanggal,flush=True)
        query = "select c.fullname,b.name board_name,b.id board_id, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '01' then '1' end) as tanggal_01, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '02' then '1' end) as tanggal_02, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '03' then '1' end) as tanggal_03, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '04' then '1' end) as tanggal_04, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '05' then '1' end) as tanggal_05, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '06' then '1' end) as tanggal_06, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '07' then '1' end) as tanggal_07, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '08' then '1' end) as tanggal_08, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '09' then '1' end) as tanggal_09, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '10' then '1' end) as tanggal_10, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '11' then '1' end) as tanggal_11, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '12' then '1' end) as tanggal_12, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '13' then '1' end) as tanggal_13, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '14' then '1' end) as tanggal_14, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '15' then '1' end) as tanggal_15, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '16' then '1' end) as tanggal_16, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '17' then '1' end) as tanggal_17, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '18' then '1' end) as tanggal_18, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '19' then '1' end) as tanggal_19, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '20' then '1' end) as tanggal_20, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '21' then '1' end) as tanggal_21, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '22' then '1' end) as tanggal_22, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '23' then '1' end) as tanggal_23, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '24' then '1' end) as tanggal_24, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '25' then '1' end) as tanggal_25, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '26' then '1' end) as tanggal_26, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '27' then '1' end) as tanggal_27, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '28' then '1' end) as tanggal_28, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '29' then '1' end) as tanggal_29, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '30' then '1' end) as tanggal_30, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '31' then '1' end) as tanggal_31 \
from boardactions a,board b, trello_karyawan c \
  where board_id = '"+boardid+"' \
  and a.board_id = b.id \
  and b.name = (select name from board where id = '"+boardid+"' order by dateLastActivity desc limit 1) \
  and a.username = c.trelloid \
  and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+tanggal+"' \
  group by fullname,board_name,board_id \
"

        query="select distinct c.fullname fullname,b.name board_name,a.type type,substring(CONVERT_TZ(a.tanggal,'+00:00','+07:00'),1,19) tanggal,a.text comment \
  from boardactions a,board b, trello_karyawan c \
  where board_id = '"+boardid+"' \
  and a.board_id = b.id \
  and a.username = c.trelloid  \
  and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
  order by tanggal desc;"

        query="select distinct c.fullname fullname,b.name board_name,a.type type,substring(CONVERT_TZ(a.tanggal,'+00:00','+07:00'),1,19) tanggal,concat(substring(a.text,1,50),'...') comment \
  from boardactions a,board b, trello_karyawan c \
  where board_id = '"+boardid+"' \
  and a.board_id = b.id \
  and a.username = c.trelloid  \
  and tanggal >= subdate(current_date, 10) \
  order by tanggal desc;"

        print('BOAAAAAARD ID ', flush=True)
        print(boardid, flush=True)


		# print(query, flush=True)
        cur = db.session()
        resultproxy = cur.execute(query)
        # print(query, flush=True)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        db.session.close()

        # if a is not nullable:
        return { 'Boards': a }, 200

    @classmethod
    def getDetailD(cls, boardid, tanggal):
        query="select distinct c.fullname fullname,b.name board_name,a.type type,substring(CONVERT_TZ(a.tanggal,'+00:00','+07:00'),1,19) tanggal,a.text comment \
  from boardactions a,board b, trello_karyawan c \
  where board_id = '"+boardid+"' \
  and a.board_id = b.id \
  and a.username = c.trelloid  \
  and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
  order by tanggal desc;"

        print('BOAAAAAARD ID ', flush=True)
        print(boardid, flush=True)


		# print(query, flush=True)
        cur = db.session()
        resultproxy = cur.execute("select distinct name from board where id = '"+boardid+"'")
        boardname = resultproxy.fetchone()[0]
        # print(resultproxy.fetchone()[0], flush=True)
        # print(query, flush=True)
        # d, a = {}, []
        # for rowproxy in resultproxy:
        #     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        #     for column, value in rowproxy.items():
        #         # build up the dictionary
        #         d = {**d, **{column: value}}
        #     a.append(d)
        print(boardname,flush=True)
        df = pd.read_sql(query, db.session.bind)

        # print(df,flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter('DailyDetail_'+boardid+'_'+tanggal+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name = boardname[0:10]+'_'+tanggal, startrow=1,startcol=1, index=True)
        writer.save()

        db.session.close()
        return { 'Status': 'Success' }, 200
        

        # if a is not nullable:

    @classmethod
    def getDetailM(cls, boardid, tanggal):

        query="select distinct c.fullname fullname,b.name board_name,a.type type,substring(CONVERT_TZ(a.tanggal,'+00:00','+07:00'),1,19) tanggal,a.text comment \
  from boardactions a,board b, trello_karyawan c \
  where board_id = '"+boardid+"' \
  and a.board_id = b.id \
  and a.username = c.trelloid  \
  and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+tanggal+"' \
  order by tanggal desc;"
  
        cur = db.session()
        resultproxy = cur.execute("select distinct name from board where id = '"+boardid+"'")
        boardname = resultproxy.fetchone()[0]
        print(boardname,flush=True)
        
        df = pd.read_sql(query, db.session.bind)

        # print(df,flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter('MonthlyDetail_'+boardid+'_'+tanggal+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name = boardname[0:10]+'_'+tanggal, startrow=1,startcol=1, index=True)
        writer.save()

        db.session.close()
        return { 'Status': 'Success' }, 200
        
    @classmethod
    def projectMandays(cls, tahun):
        # cls.query.filter_by(user_id = user_id).first
        # print(tanggal,flush=True)

        concat = pd.core.frame.DataFrame


        query = "select a.id,a.project,k.fullname,cl.nama,a.jumlah, a.project_type,a.status,a.projectdiv ,a.mandays,a.nilai_project,a.no_po,a.nama_po from ( \
select aa.id id,aa.project project,aa.jumlah jumlah,pm.client,pm.status, pm.project_type, pm.projectdiv ,pm.pm,pm.nilai_project,pm.mandays mandays, pm.no_po,pm.nama_po \
from (select id, name as project, replace('' + sum(jumlah),'.','') as jumlah from ( \
select distinct b2.id,b.fullname,b2.name as name, \
substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) as tanggal, \
1 as jumlah from boardactions b, board b2 \
where b.board_id  = b2.id \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,4) = '"+tahun+"' \
order by tanggal desc) as DATA \
group by id,name \
order by tanggal desc) aa \
LEFT JOIN project_setting pm \
ON aa.id = pm.board) a, client cl, karyawan k \
where a.pm = k.user_id \
and cl.id = a.client and a.projectdiv = 'PMO';"

		# print(query, flush=True)
        cur = db.session()
        resultproxy = cur.execute(query)
        # print(query, flush=True)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        df = pd.read_sql(query, db.session.bind)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter('ProjectMandays_'+tahun+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='YlOrRd').highlight_null('white').to_excel(writer, sheet_name ='Timesheet-'+tahun, startrow=1,startcol=1, index=True)
        writer.save()
        db.session.close()

        # if a is not nullable:
        return { 'Mandays': a }, 200

    @classmethod
    def getBoardDaily(cls, tanggal):
        # cls.query.filter_by(user_id = user_id).first
        # print(tanggal,flush=True)

        concat = pd.core.frame.DataFrame
        # bul = datetime.strptime(tanggal,'%Y-%m')
        # bulan = bul.strftime('%b')
        tahun=tanggal.split('-')[0]
        bulan=tanggal.split('-')[1]
        hari=tanggal.split('-')[2]
        print(tahun, flush=True)
        print(bulan, flush=True)
        print(hari, flush=True)
        # print(bulan, flush=True)
        # print(hari, flush=True)

        query = "select fullname,b.name board_name, \
            sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '"+hari+"' then '1' end) as 'Nov-"+hari+"' \
            from boardactions a, board b \
            where a.board_id = b.id \
            and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"'  \
            group by fullname,board_name order by board_name,fullname;"
        print(query, flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        # print(type(a),flush=True)
        # print(resultproxy,flush=True	)
        # df = pd.DataFrame.from_records(resultproxy.fetchall())
        df = pd.read_sql(query, db.session.bind)

        # print(df,flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter('Board_Daily_'+tanggal+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name ='Board-'+tanggal, startrow=1,startcol=1, index=True)
        writer.save()

        db.session.close()
        return { 'Report': a }, 200

    @classmethod
    def getBoardMonthly(cls, tanggal):
        # cls.query.filter_by(user_id = user_id).first
        # print(tanggal,flush=True)

        concat = pd.core.frame.DataFrame
        # bul = datetime.strptime(tanggal,'%Y-%m')
        # bulan = bul.strftime('%b')
        tahun=tanggal.split('-')[0]
        bulan=tanggal.split('-')[1]
        hari=tanggal.split('-')[2]
        print(tahun, flush=True)
        print(bulan, flush=True)
        print(hari, flush=True)
        # print(bulan, flush=True)
        # print(hari, flush=True)

        query = "select c.fullname,b.name board_name, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '01' then '1' end) as '01', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '02' then '1' end) as '02', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '03' then '1' end) as '03', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '04' then '1' end) as '04', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '05' then '1' end) as '05', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '06' then '1' end) as '06', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '07' then '1' end) as '07', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '08' then '1' end) as '08', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '09' then '1' end) as '09', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '10' then '1' end) as '10', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '11' then '1' end) as '11', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '12' then '1' end) as '12', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '13' then '1' end) as '13', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '14' then '1' end) as '14', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '15' then '1' end) as '15', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '16' then '1' end) as '16', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '17' then '1' end) as '17', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '18' then '1' end) as '18', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '19' then '1' end) as '19', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '20' then '1' end) as '20', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '21' then '1' end) as '21', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '22' then '1' end) as '22', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '23' then '1' end) as '23', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '24' then '1' end) as '24', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '25' then '1' end) as '25', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '26' then '1' end) as '26', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '27' then '1' end) as '27', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '28' then '1' end) as '28', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '29' then '1' end) as '29', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '30' then '1' end) as '30', \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '31' then '1' end) as '31' \
from boardactions a, board b, trello_karyawan c \
where a.board_id = b.id \
and a.username = c.trelloid \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+tahun+"-"+bulan+"' \
group by fullname,board_name order by board_name,fullname;"
        print(query, flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        # print(type(a),flush=True)
        # print(resultproxy,flush=True	)
        # df = pd.DataFrame.from_records(resultproxy.fetchall())
        df = pd.read_sql(query, db.session.bind)

        # print(df,flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter('Board_Monthly_'+tahun+''+bulan+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name ='Board-Monthly-'+tahun+''+bulan, startrow=1,startcol=1, index=True)
        writer.save()

        db.session.close()
        return { 'Report': a }, 200


    @classmethod
    def getBoardName(cls, boardid):
        # cls.query.filter_by(user_id = user_id).first
        # print(tanggal,flush=True)
        print('BOAAAAAARD ID ', flush=True)
        print(boardid, flush=True)


		# print(query, flush=True)
        cur = db.session()
        resultproxy = cur.execute("select distinct name from board where id = '"+boardid+"'")
        boardname = resultproxy.fetchone()[0]

        db.session.close()
        return { 'boardname': boardname }, 200

    @classmethod
    def getBoardMembersMandays(cls, boardid):

        query = "select count(1) mandays, fullname, posisi from ( \
select distinct username,tk.fullname,kk.posisi, substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) tanggal \
from boardactions b, trello_karyawan tk , karyawan kk \
where board_id = '"+boardid+"' \
and kk.fullname = tk.fullname \
and tk.trelloid = b.username) aa \
group by fullname;"
        cur = db.session()

        resultproxy = cur.execute(query) 

        # print(query, flush=True)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        db.session.close()

        # if a is not nullable:
        return { 'Members': a }, 200

    @classmethod
    def getDailyActivity(cls, tanggal, role):
        print('ROLLLEEEEEEE ROLE ROLE : '+role,flush=True)
        if(role=='2'):
            print('ROLLLEEEEEEE ROLE ROLE : '+role,flush=True)
            query="select distinct karyawan.fullname fullname, tanggal,name,board_id from karyawan left join( \
    select fullname, name,tanggal,board_id, count(1) jumlah from ( \
    select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type,a.board_id board_id \
    from boardactions a, trello_karyawan tk, board b \
    where a.username  = tk.trelloid \
    and b.id = a.board_id  \
    and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
    order by fullname asc) a \
    group by fullname, name ) as timesheet \
    on lower(karyawan.fullname) = lower(timesheet.fullname)  \
    where karyawan.divisi in ('PMO') and status = 'Active' order by karyawan.fullname asc;"
        elif(role=='6'):
            query="select distinct karyawan.fullname fullname, tanggal,name,board_id from karyawan left join( \
    select fullname, name,tanggal,board_id, count(1) jumlah from ( \
    select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type,a.board_id board_id \
    from boardactions a, trello_karyawan tk, board b \
    where a.username  = tk.trelloid \
    and b.id = a.board_id  \
    and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
    order by fullname asc) a \
    group by fullname, name ) as timesheet \
    on lower(karyawan.fullname) = lower(timesheet.fullname)  \
    where karyawan.divisi in ('SDO') and status = 'Active' order by karyawan.fullname asc;"
        else:
            query="select distinct karyawan.fullname fullname, tanggal,name,board_id from karyawan left join( \
    select fullname, name,tanggal,board_id, count(1) jumlah from ( \
    select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type,a.board_id board_id \
    from boardactions a, trello_karyawan tk, board b \
    where a.username  = tk.trelloid \
    and b.id = a.board_id  \
    and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
    order by fullname asc) a \
    group by fullname, name ) as timesheet \
    on lower(karyawan.fullname) = lower(timesheet.fullname)  \
    where karyawan.divisi in ('PMO') and status = 'Active' order by karyawan.fullname asc;"



        cur = db.session()
        resultproxy = cur.execute(query)
        # print(query, flush=True)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        db.session.close()

        # if a is not nullable:
        return { 'Activity': a }, 200


    @classmethod
    def getRepDailyAct(cls, tanggal):
        query="select distinct karyawan.fullname, name from karyawan left join( \
select fullname, name,tanggal,count(1) jumlah from ( \
select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
from boardactions a, trello_karyawan tk, board b \
where a.username  = tk.trelloid \
and b.id = a.board_id  \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
order by fullname asc) a \
group by fullname, name ) as timesheet \
on lower(karyawan.fullname) = lower(timesheet.fullname)  \
where karyawan.divisi in ('PMO','SDO','RMO') and status='Active' order by karyawan.fullname asc"

        # print(resultproxy.fetchone()[0], flush=True)
        # print(query, flush=True)
        # d, a = {}, []
        # for rowproxy in resultproxy:
        #     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        #     for column, value in rowproxy.items():
        #         # build up the dictionary
        #         d = {**d, **{column: value}}
        #     a.append(d)
        df = pd.read_sql(query, db.session.bind)

        # print(df,flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter('DailyAct_'+tanggal+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name = 'DailyAct_'+tanggal, startrow=1,startcol=1, index=True)
        writer.save()

        db.session.close()
        return { 'Status': 'Success' }, 200

    @classmethod
    def getlastten(cls,user_role):
        try:
            cur = db.session()
            if(user_role == '6'):
                query = "select b.name,b.id,tk.fullname,type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,19) tanggal \
    from boardactions a, trello_karyawan tk, board b, karyawan k \
    where a.username  = tk.trelloid \
    and k.fullname = tk.fullname \
    and k.divisi = 'SDO' \
    and b.id = a.board_id  \
    and tanggal >= subdate(current_date, 1) \
    order by tanggal desc limit 10;"
            else:
                query = "select b.name,b.url,b.id,tk.fullname,type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,19) tanggal \
    from boardactions a, trello_karyawan tk, board b \
    where a.username  = tk.trelloid \
    and b.id = a.board_id  \
    order by tanggal desc limit 10;"

            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            return { 'LastTen' : a }, 200
        except:
            return { 'OK' : 'OS' }        

    @classmethod
    def getAddBoardList(cls, tahun, bulan):
        try:
            cur = db.session()
            query = "select b.fullname,k.role_trello,board_id,bb.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,16) tanggal \
from boardactions b,board bb,karyawan k \
where type in ('createBoard') \
and b.board_id = bb.id \
and b.fullname = k.fullname \
and k.statuskaryawan != 'Resign' \
order by substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,16) desc;"
# and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,4) = '"+tahun+"' 
# and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),6,2) = '"+bulan+"' 

            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            return { 'boardList' : a }, 200
        except:
            return { 'OK' : 'OS' }  

            

    @classmethod
    def getAddBoardMember(cls, tahun, bulan):
        try:
            cur = db.session()
            query = "select b.fullname,k.role_trello,board_id,bb.name,member_fullname, substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,16) tanggal \
from boardactions b,board bb,karyawan k \
where type in ('addMemberToBoard') \
and b.board_id = bb.id \
and b.fullname = k.fullname \
and k.statuskaryawan != 'Resign' \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,4) = '"+tahun+"' \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),6,2) = '"+bulan+"' \
order by substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,16) desc;"



            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            return { 'boardList' : a }, 200
        except:
            return { 'OK' : 'OS' }


            
    @classmethod
    def monthlyactkaryawanlist(cls,tahun, user_role):
        try:
            cur = db.session()

            
            if(user_role == '6'):
                query = "select fullname,trelloid,count(1) projects from ( \
    select distinct k.fullname,tk.trelloid,bd.name from karyawan k, trello_karyawan tk, boardactions b, board bd \
    where k.fullname  = tk.fullname \
    and b.username = tk.trelloid \
    and b.board_id = bd.id \
    and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = DATE_FORMAT(CURRENT_DATE(),'%Y-%m') \
    )b \
    group by fullname,trelloid;"
            else:
                query = "select fullname,trelloid,count(1) projects from ( \
    select distinct k.fullname,tk.trelloid,bd.name from karyawan k, trello_karyawan tk, boardactions b, board bd \
    where k.fullname  = tk.fullname \
    and b.username = tk.trelloid \
    and b.board_id = bd.id and k.divisi = 'PMO' \
    and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = DATE_FORMAT(CURRENT_DATE(),'%Y-%m') \
    )b \
    group by fullname,trelloid;"

            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            return { 'karyawanlist' : a }, 200
        except:
            return { 'OK' : 'OS' }

    
    @classmethod
    def monthlyact(cls, trelloid, bulan):
        try:
            cur = db.session()
            # query = "select k.fullname,tk.trelloid from karyawan k, trello_karyawan tk \
                # where k.fullname  = tk.fullname;"
            query = "select distinct k.fullname,tk.trelloid,bd.name,bd.id from karyawan k, trello_karyawan tk, boardactions b, board bd \
where k.fullname  = tk.fullname \
and b.username = tk.trelloid \
and b.board_id = bd.id \
and tk.trelloid = '"+trelloid+"' \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+bulan+"';"

            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)

            df = pd.read_sql(query, db.session.bind)

            # print(df,flush=True)
            cm = sns.light_palette("green", as_cmap=True)

            s = df.style.background_gradient(cmap='viridis')

            writer = pd.ExcelWriter('Monthly_'+trelloid+'_'+bulan+'.xlsx', engine='xlsxwriter')
            df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name ='Monthly-'+bulan, startrow=1,startcol=1, index=True)
            writer.save()

            db.session.close()
            
            return { 'detail' : a }, 200
        except:
            return { 'OK' : 'OS' }


    @classmethod
    def monthlyactd(cls, trelloid, bulan):
        cur = db.session()
        # query = "select k.fullname,tk.trelloid from karyawan k, trello_karyawan tk \
            # where k.fullname  = tk.fullname;"
        query = "select distinct k.fullname,tk.trelloid,bd.name,bd.id from karyawan k, trello_karyawan tk, boardactions b, board bd \
where k.fullname  = tk.fullname \
and b.username = tk.trelloid \
and b.board_id = bd.id \
and tk.trelloid = '"+trelloid+"' \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+bulan+"';"

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        # print(type(a),flush=True)
        # print(resultproxy,flush=True	)
        # df = pd.DataFrame.from_records(resultproxy.fetchall())
        df = pd.read_sql(query, db.session.bind)

        # print(df,flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter('Board_Daily_'+bulan+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name ='Board-'+bulan, startrow=1,startcol=1, index=True)
        writer.save()

        db.session.close()
        return { 'Report': a }, 200


    @classmethod
    def projectmdetail(cls, project_id):
        try:
            cur = db.session()
            query = "select a.id,a.project,k.fullname,cl.nama,a.jumlah,a.status,a.mandays,a.nilai_project,a.start_date,a.end_date,a.project_type,a.projectdiv,a.no_po,a.nama_po,a.noproject,a.namaproject,a.invoice1,a.invoice2 from ( \
select aa.id id,aa.project project,aa.jumlah jumlah,pm.client, pm.status,pm.pm,pm.nilai_project,pm.mandays mandays, \
pm.start_date,pm.end_date,pm.project_type,pm.projectdiv,pm.no_po,pm.nama_po,pm.noproject,pm.namaproject,pm.invoice1,pm.invoice2 from (select id, name as project, replace('' + sum(jumlah),'.','') as jumlah from ( \
select distinct b2.id,b.fullname,b2.name as name, substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) as tanggal, \
1 as jumlah from boardactions b, board b2 \
where b.board_id  = b2.id \
and b.board_id = '"+project_id+"' \
order by tanggal desc) as DATA \
group by id,name \
order by tanggal desc) aa \
LEFT JOIN project_setting pm \
ON aa.id = pm.board) a, client cl, karyawan k \
where a.pm = k.user_id \
and cl.id = a.client;"

            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            return { 'Project' : a }, 200
        except:
            return { 'Status' : 'Failed' }

    @classmethod
    def pmndaysupdate(cls, board,startd,endd,mandays,nilai,status,no_po,nama_po,project_type,noproject,namaproject,invoice1,invoice2):
        query = "update project_setting set status='"+status+"',start_date='"+startd+"',end_date='"+endd+"', \
            mandays='"+mandays+"',nilai_project='"+nilai+"',no_po='"+no_po+"',nama_po='"+nama_po+"',project_type='"+project_type+"',noproject='"+noproject+",namaproject='"+namaproject+"', invoice1 = '"+invoice1+"', invoice2 = '"+invoice2+"' where board = '"+board+"'" 
        print(query,flush=True)

        try:
            cur = db.session()
            query = "update project_setting set status='"+status+"',start_date='"+startd+"',end_date='"+endd+"', mandays='"+mandays+"',nilai_project='"+nilai+"',no_po='"+no_po+"',nama_po='"+nama_po+"',project_type='"+project_type+"',noproject='"+noproject+"',namaproject='"+namaproject+"', invoice1 = '"+invoice1+"', invoice2 = '"+invoice2+"' where board = '"+board+"';" 
            resultproxy = cur.execute(query)

            print(query,flush=True)
            db.session.commit()

            db.session.close()

            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : 'Something Wrong' }
