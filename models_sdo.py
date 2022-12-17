from run import db
from passlib.hash import pbkdf2_sha256 as sha256
from flask_mysqldb import MySQL
import json
from flask_cors import CORS
from datetime import datetime
################## PMO
import pandas as pd
from datetime import datetime
import seaborn as sns
import pandas.io.formats.excel

class ClientModelSDO(db.Model):
    __tablename__ = 'client'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)
    nama = db.Column(db.String(120), unique = True, nullable = False)
    alamat = db.Column(db.String(120), unique = True, nullable = False)
    createdate = db.Column(db.String(20), nullable = False)
    createdby = db.Column(db.String(30), nullable = False)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    


    @classmethod
    def find_by_name(cls, nama):
        return cls.query.filter_by(nama = nama).first()

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select * from client")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Client': a }, 200

class karyawanSDO():

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select * from karyawan where divisi = 'PMO' and status = 'Active'")

        print('SINI NIH ',flush=True)

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Karyawan': a }, 200

    @classmethod
    def find_pm(cls):
        # cls.query.filter_by(user_id = user_id).first
        query = "select fullname from karyawan where divisi = 'PMO' and posisi='Project Manager' and status = 'Active'"

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
        return { 'PM': a }, 200

    @classmethod
    def find_sa(cls):
        # cls.query.filter_by(user_id = user_id).first
        query = "select fullname from karyawan where divisi = 'PMO' and posisi='System Analyst' and status = 'Active'"

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
        return { 'SA': a }, 200

    @classmethod
    def find_dev(cls):
        # cls.query.filter_by(user_id = user_id).first
        query = "select fullname from karyawan where divisi = 'PMO' and posisi != 'System Analyst' and status = 'Active' AND posisi != 'Project Manager' AND posisi like 'Dev%'"

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
        return { 'Dev': a }, 200

    @classmethod
    def find_qc(cls):
        # cls.query.filter_by(user_id = user_id).first
        query = "select fullname from karyawan where divisi = 'PMO' and posisi = 'Quality Control' and status = 'Active'"

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
        return { 'QC': a }, 200

    @classmethod
    def find_tw(cls):
        # cls.query.filter_by(user_id = user_id).first
        query = "select fullname from karyawan where divisi = 'PMO' and posisi = 'Technical Writer' and status = 'Active'"

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
        return { 'TW': a }, 200

    @classmethod
    def find_pa(cls):
        # cls.query.filter_by(user_id = user_id).first
        query = "select fullname from karyawan where divisi = 'PMO' and posisi = 'Project Admin' and status = 'Active'"

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
        return { 'PA': a }, 200


class ProjectStateSDO(db.Model):
    __tablename__ = 'project_state'
    __table_args__ = {'extend_existing': True}
    id_project = db.Column(db.String(100), primary_key = True)
    status = db.Column(db.String(10), primary_key=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class ProjectSDO(db.Model):
    __tablename__ = 'project'
    __table_args__ = {'extend_existing': True}
    id_project = db.Column(db.String(100), primary_key = True)
    project = db.Column(db.String(50))
    client = db.Column(db.String(50))
    po_name = db.Column(db.String(50))
    cr_name = db.Column(db.String(50))
    jenis = db.Column(db.String(20))
    mulai = db.Column(db.String(10),primary_key = True)
    selesai = db.Column(db.String(10),primary_key = True)
    posisi = db.Column(db.String(100),primary_key = True)
    resource_name = db.Column(db.String(100),primary_key = True)
    createdby = db.Column(db.String(50))
    createdate = db.Column(db.String(20))
    status = db.Column(db.String(10))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def update_resource(cls, id_project, resource_name):
        try:
            cur = db.session()
            query = "update project set status = 'Active' where id_project = '"+id_project+"' and resource_name = '"+resource_name+"'"
            resultproxy = cur.execute(query)
            db.session.commit()
            print(query, flush=True)
            # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

            # d, a = {}, []
            # for rowproxy in resultproxy:
            #     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            #     for column, value in rowproxy.items():
            #         # build up the dictionary
            #         d = {**d, **{column: value}}
            #     a.append(d)
            
            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : 'Something Wrong' }

    @classmethod
    def find_by_resource(cls, id_project,resource_name):
        return cls.query.filter_by(id_project = id_project, resource_name=resource_name).first()

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select distinct a.id_project,a.project,a.client,a.po_name,a.cr_name,a.jenis,a.mulai,a.selesai from project a, project_state b where a.id_project = b.id_project and b.status = 'Active'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Project': a }, 200

    @classmethod
    def summary(cls, user_role):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(1)
            cur = db.session()

            if(user_role == '6'):
                query = "select ( \
select count(1) active from ( \
select distinct name from ( \
select b.name,b.id,tk.fullname,type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,19) tanggal \
from boardactions a, trello_karyawan tk, board b, karyawan k \
where a.username  = tk.trelloid \
and b.id = a.board_id  \
and tanggal >= subdate(current_date, 1) \
and k.fullname  = tk.fullname \
and k.divisi = 'SDO' \
and substring(CONVERT_TZ(a.tanggal,'+00:00','+07:00'),1,10) > '"+str(start_date)[0:10]+"' \
order by tanggal desc limit 10) a ) b ) as activeProject, \
( \
select count(1) resourceActive from ( \
select distinct karyawan.fullname from karyawan left join( \
select fullname,  name,tanggal,count(1) jumlah from ( \
select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
from boardactions a, trello_karyawan tk, board b \
where a.username  = tk.trelloid \
and b.id = a.board_id \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) > '"+str(start_date)[0:10]+"' \
order by fullname asc) a \
group by fullname, name ) as timesheet \
on lower(karyawan.fullname) = lower(timesheet.fullname)  \
where karyawan.divisi in ('SDO') \
and status = 'Active' \
and timesheet.name is not null  \
order by karyawan.fullname asc) b ) as resourceActive, \
( \
select count(1) resourceIdle from ( \
select distinct karyawan.fullname from karyawan left join( \
select fullname,  name,tanggal,count(1) jumlah from ( \
select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
from boardactions a, trello_karyawan tk, board b \
where a.username  = tk.trelloid \
and b.id = a.board_id  \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) > '"+str(start_date)[0:10]+"' \
order by fullname asc) a \
group by fullname, name ) as timesheet \
on lower(karyawan.fullname) = lower(timesheet.fullname)  \
where karyawan.divisi in ('SDO') \
and status = 'Active' \
and timesheet.name is null \
order by karyawan.fullname asc) b ) as ResourceIdle, \
( \
select count(1) jumlah from karyawan where divisi = 'SDO' and status = 'Active' \
)as resourcePMO;"

            else:
                query = "select ( \
    select count(1) active from ( \
    select distinct a.name from boardactions b, board a \
    where a.id = b.board_id  \
    and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) > '"+str(start_date)[0:10]+"') a ) as activeProject, \
    ( \
    select count(1) resourceActive from ( \
    select distinct karyawan.fullname from karyawan left join( \
    select fullname,  name,tanggal,count(1) jumlah from ( \
    select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
    from boardactions a, trello_karyawan tk, board b \
    where a.username  = tk.trelloid \
    and b.id = a.board_id \
    and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) > '"+str(start_date)[0:10]+"' \
    order by fullname asc) a \
    group by fullname, name ) as timesheet \
    on lower(karyawan.fullname) = lower(timesheet.fullname)  \
    where karyawan.divisi in ('PMO','SDO', 'RMO') \
    and status = 'Active' \
    and timesheet.name is not null  \
    order by karyawan.fullname asc) b ) as resourceActive, \
    ( \
    select count(1) resourceIdle from ( \
    select distinct karyawan.fullname from karyawan left join( \
    select fullname,  name,tanggal,count(1) jumlah from ( \
    select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
    from boardactions a, trello_karyawan tk, board b \
    where a.username  = tk.trelloid \
    and b.id = a.board_id  \
    and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) > '"+str(start_date)[0:10]+"' \
    order by fullname asc) a \
    group by fullname, name ) as timesheet \
    on lower(karyawan.fullname) = lower(timesheet.fullname)  \
    where karyawan.divisi in ('PMO','SDO','RMO') \
    and status = 'Active' \
    and timesheet.name is null \
    order by karyawan.fullname asc) b ) as ResourceIdle, \
    ( \
    select count(1) jumlah from karyawan where divisi = 'PMO' and status = 'Active'  \
    )as resourcePMO;"

            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            return { 'Summary' : a }, 200
        except:
            return { 'OK' : 'OS' }

    @classmethod
    def resource_summary(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()
            query = "select * from ( \
select posisi, count(1) jumlah from karyawan where divisi = 'PMO' group by posisi) as aa \
order by CAST(jumlah as SIGNED INTEGER) asc"

            query = "select tanggal posisi, count(1) jumlah from ( \
select distinct tk.fullname,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal \
from boardactions a, trello_karyawan tk, board b \
where a.username  = tk.trelloid \
and b.id = a.board_id  \
and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) > '"+str(start_date)[0:10]+"' \
order by fullname asc)a \
group by tanggal;"

            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            return { 'Resource' : a }, 200
        except:
            return { 'OK' : 'OS' }


            

    @classmethod
    def resourceactive(cls):
        try:
            cur = db.session()
            query = "select * from resource_active"
            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            return { 'Resource' : a }, 200
        except:
            return { 'OK' : 'OS' }

    @classmethod
    def resourceidlesdo(cls):
        
        try:
            import datetime
            start_date = datetime.datetime.now()# - datetime.timedelta(1)
            

            cur = db.session()
            query = "select distinct karyawan.fullname from karyawan left join( \
            select fullname,  name,tanggal,count(1) jumlah from ( \
            select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
            from boardactions a, trello_karyawan tk, board b \
            where a.username  = tk.trelloid \
            and b.id = a.board_id \
            and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) > '"+str(start_date)[0:10]+"' \
            order by fullname asc) a \
            group by fullname, name ) as timesheet \
            on lower(karyawan.fullname) = lower(timesheet.fullname)  \
            where karyawan.divisi ='SDO' \
            and karyawan.posisi != 'Support Surveillance' \
            and status = 'Active' \
            and timesheet.name is null \
            order by karyawan.fullname asc;"

            query = "select distinct abb.fullname fullname,cuti.keterangan keterangan from  ( \
            select distinct karyawan.fullname from karyawan left join(  \
            select fullname,  name,tanggal,count(1) jumlah from (  \
            select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
            from boardactions a, trello_karyawan tk, board b \
            where a.username  = tk.trelloid \
            and b.id = a.board_id \
            and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+str(start_date)[0:10]+"' \
            order by fullname asc) a \
            group by fullname, name ) as timesheet  \
            on lower(karyawan.fullname) = lower(timesheet.fullname)  \
            where karyawan.divisi in ('SDO') \
            and karyawan.posisi != 'Support Surveillance' \
            and status = 'Active'  \
            and timesheet.name is null \
            order by karyawan.fullname asc) abb left join ( \
            select fullname, keterangan from cutikaryawan where tanggal_cuti = '"+str(start_date)[0:10]+"') as cuti \
            on lower(abb.fullname) = lower(cuti.fullname);"

            print(query,flush=True)
            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            return { 'Resource' : a }, 200
        except:
            return { 'Resource' : 'OS' }

    @classmethod
    def resourceidledailysdo(cls,tanggal):
        
        try:
            # import datetime

            cur = db.session()
            query = "select distinct karyawan.fullname from karyawan left join( \
            select fullname,  name,tanggal,count(1) jumlah from ( \
            select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type Sy\
            from boardactions a, trello_karyawan tk, board b \
            where a.username  = tk.trelloid \
            and b.id = a.board_id \
            and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
            order by fullname asc) a \
            group by fullname, name ) as timesheet \
            on lower(karyawan.fullname) = lower(timesheet.fullname)  \
            where karyawan.divisi in ('PMO','SDO','RMO') \
            and karyawan.posisi != 'Support Surveillance' \
            and status = 'Active' \
            and timesheet.name is null \
            order by karyawan.fullname asc;"

            query = "select distinct abb.fullname fullname,cuti.keterangan keterangan from  ( \
            select distinct karyawan.fullname from karyawan left join(  \
            select fullname,  name,tanggal,count(1) jumlah from (  \
            select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
            from boardactions a, trello_karyawan tk, board b \
            where a.username  = tk.trelloid \
            and b.id = a.board_id \
            and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
            order by fullname asc) a \
            group by fullname, name ) as timesheet  \
            on lower(karyawan.fullname) = lower(timesheet.fullname)  \
            where karyawan.divisi in ('SDO') \
            and karyawan.posisi != 'Support Surveillance' \
            and status = 'Active'  \
            and timesheet.name is null \
            order by karyawan.fullname asc) abb left join ( \
            select fullname, keterangan from cutikaryawan where tanggal_cuti = '"+tanggal+"') as cuti \
            on lower(abb.fullname) = lower(cuti.fullname);"

            print(query,flush=True)
            resultproxy = cur.execute(query)
            d, a = {}, []

            for rowproxy in resultproxy:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)                     
            return { 'Resource' : a }, 200
        except:
            return { 'Resource' : 'OS' }

    @classmethod
    def resourceidledailyD(cls,tanggal):
        
        try:
            # import datetime

            cur = db.session()
            query = "select distinct karyawan.fullname from karyawan left join( \
            select fullname,  name,tanggal,count(1) jumlah from ( \
            select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
            from boardactions a, trello_karyawan tk, board b \
            where a.username  = tk.trelloid \
            and b.id = a.board_id \
            and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
            order by fullname asc) a \
            group by fullname, name ) as timesheet \
            on lower(karyawan.fullname) = lower(timesheet.fullname)  \
            where karyawan.divisi in ('PMO','SDO','RMO') \
            and status = 'Active' \
            and timesheet.name is null \
            order by karyawan.fullname asc;"

            query = "select distinct abb.fullname fullname,cuti.keterangan keterangan from  ( \
            select distinct karyawan.fullname from karyawan left join(  \
            select fullname,  name,tanggal,count(1) jumlah from (  \
            select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
            from boardactions a, trello_karyawan tk, board b \
            where a.username  = tk.trelloid \
            and b.id = a.board_id \
            and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+tanggal+"' \
            order by fullname asc) a \
            group by fullname, name ) as timesheet  \
            on lower(karyawan.fullname) = lower(timesheet.fullname)  \
            where karyawan.divisi in ('PMO','SDO', 'DSO','RMO') \
            and status = 'Active'  \
            and timesheet.name is null \
            order by karyawan.fullname asc) abb left join ( \
            select fullname, keterangan from cutikaryawan where tanggal_cuti = '"+tanggal+"') as cuti \
            on lower(abb.fullname) = lower(cuti.fullname);"

            df = pd.read_sql(query, db.session.bind)

            print(query,flush=True)
            cm = sns.light_palette("green", as_cmap=True)

            s = df.style.background_gradient(cmap='viridis')

            writer = pd.ExcelWriter('ResIdle_'+tanggal+'.xlsx', engine='xlsxwriter')
            df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='viridis').highlight_null('white').to_excel(writer, sheet_name = 'ResIdle_'+tanggal+'.xlsx', startrow=1,startcol=1, index=True)
            writer.save()

            db.session.close()
            return { 'Status': 'Success' }, 200
        except:
            return { 'Resource' : 'OS' }            

    @classmethod
    def return_all_hist(cls):
        cur = db.session()
        resultproxy = cur.execute("select distinct a.id_project,a.project,a.client,a.po_name,a.cr_name,a.jenis,a.mulai,a.selesai from project a, project_state b where a.id_project = b.id_project and b.status = 'Close'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Project': a }, 200

    @classmethod
    def project_detail(cls, id_project):
        cur = db.session()
        resultproxy = cur.execute("select distinct id_project,project,client,po_name,cr_name,jenis,mulai,selesai,DATE_FORMAT(STR_TO_DATE(mulai,'%Y-%m-%d'), '%W, %e %M %Y') as mulaix,DATE_FORMAT(STR_TO_DATE(selesai,'%Y-%m-%d'), '%W, %e %M %Y') as selesaix from project where id_project = '"+id_project+"'")
        # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        return { 'Project': a }, 200

    @classmethod
    def project_pm(cls, id_project):
        cur = db.session()
        resultproxy = cur.execute("select distinct resource_name as pm from project where posisi = 'Project Manager' and status = 'Active' and id_project = '"+id_project+"'")
        # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        return { 'Project': a }, 200


    @classmethod
    def project_sa(cls, id_project):
        cur = db.session()
        resultproxy = cur.execute("select distinct resource_name as sa from project where posisi = 'System Analyst' and status = 'Active' and id_project = '"+id_project+"'")
        # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        return { 'Project': a }, 200


    @classmethod
    def project_dev(cls, id_project):
        cur = db.session()
        resultproxy = cur.execute("select distinct resource_name as developer from project where posisi = 'Developer' and status = 'Active' and id_project = '"+id_project+"'")
        # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        
        return { 'Project': a }, 200

    @classmethod
    def project_pa(cls, id_project):
        cur = db.session()
        resultproxy = cur.execute("select distinct resource_name as pa from project where posisi = 'Project Admin' and status = 'Active' and id_project = '"+id_project+"'")
        # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        
        return { 'Project': a }, 200

    @classmethod
    def project_qc(cls, id_project):
        cur = db.session()
        resultproxy = cur.execute("select distinct resource_name as qc from project where posisi = 'Quality Control' and status = 'Active' and id_project = '"+id_project+"'")
        # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        
        return { 'Project': a }, 200

    @classmethod
    def project_tw(cls, id_project):
        cur = db.session()
        resultproxy = cur.execute("select distinct resource_name as tw from project where posisi = 'Technical Writer' and status = 'Active' and id_project = '"+id_project+"'")
        # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)
        
        return { 'Project': a }, 200

    @classmethod
    def project_close(cls, id_project):
        try:
            cur = db.session()
            query = "update project_state set status = 'Close' where id_project = '"+id_project+"'"
            resultproxy = cur.execute(query)
            db.session.commit()
            print(query, flush=True)
            # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

            # d, a = {}, []
            # for rowproxy in resultproxy:
            #     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            #     for column, value in rowproxy.items():
            #         # build up the dictionary
            #         d = {**d, **{column: value}}
            #     a.append(d)
            
            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : 'Something Wrong' }

    @classmethod
    def delResource(cls, id_project, resource_name):
        try:
            cur = db.session()
            query = "update project set status = 'Inactive' where id_project = '"+id_project+"' and resource_name = '"+resource_name+"'"
            resultproxy = cur.execute(query)
            db.session.commit()
            print(query, flush=True)
            # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

            # d, a = {}, []
            # for rowproxy in resultproxy:
            #     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            #     for column, value in rowproxy.items():
            #         # build up the dictionary
            #         d = {**d, **{column: value}}
            #     a.append(d)
            
            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : 'Something Wrong' }

    @classmethod
    def updateTanggal(cls, id_project, selesai):
        try:
            cur = db.session()
            query = "update project set selesai = '"+selesai+"' where id_project = '"+id_project+"'"
            resultproxy = cur.execute(query)
            db.session.commit()
            print(query, flush=True)
            # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

            # d, a = {}, []
            # for rowproxy in resultproxy:
            #     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            #     for column, value in rowproxy.items():
            #         # build up the dictionary
            #         d = {**d, **{column: value}}
            #     a.append(d)
            
            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : 'Something Wrong' }

    @classmethod
    def setmandays(cls, jumlah, boardid,createdby):
        try:
            cur = db.session()
            # delete from project_mandays where boardid='60b735e9ffe7ce70db9645f5';
            # insert into project_mandays (boardid,mandays,createdby,updated) values('60b735e9ffe7ce70db9645f5',1000,'salwa.habsji',CURRENT_DATE());

            query = "delete from project_mandays where boardid = '"+boardid+"';"
            print(query, flush=True)
            resultproxy = cur.execute(query)
            db.session.commit()

            query2 = "insert into project_mandays (boardid,mandays,createdby,updated) values('"+boardid+"',"+jumlah+",'"+createdby+"',CURRENT_DATE());"
            print(query2, flush=True)
            resultproxy = cur.execute(query2)
            db.session.commit()

            # resultproxy = cur.execute("select * from project where id_project = '"+id_project+"'")

            # d, a = {}, []
            # for rowproxy in resultproxy:
            #     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            #     for column, value in rowproxy.items():
            #         # build up the dictionary
            #         d = {**d, **{column: value}}
            #     a.append(d)
            
            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : 'Something Wrong' }

    @classmethod
    def resourcemandays(cls, start, end):
        try:

            if(start):
                print('ADA NIH START', flush=True)
            else:
                print('GA ADA NIH START', flush=True)

            cur = db.session()

            query = "select fullname, cast(sum(jumlah) AS CHAR) jumlah from ( \
select count(1) jumlah,fullname,tanggal from ( \
select distinct k.fullname,b.board_id,substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) tanggal from karyawan k, trello_karyawan tk, boardactions b \
where k.fullname  = tk.fullname \
and tk.trelloid = b.username) AAA \
group by fullname,tanggal) ABB \
where substring(tanggal,1,4) = YEAR(CURRENT_DATE) \
group by fullname \
order by fullname ASC;"

            print(query, flush=True)
            resultproxy = cur.execute(query)
            
            d, a = {}, []
            for rowproxy in resultproxy:
                # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
                for column, value in rowproxy.items():
                    # build up the dictionary
                    d = {**d, **{column: value}}
                a.append(d)
                # print(a,flush=True)
            
            return { 'Mandays': a }, 200
        except:
            return { 'Status' : 'Something Wrong' }
   
    @classmethod
    def resourcedetailmandays(cls, fullname, start, end):
        try:
            if(start):
                print('ADA NIH START', flush=True)
            else:
                print('GA ADA NIH START', flush=True)

            cur = db.session()

            query = "select b.name boardname, a.fullname, a.tanggal from ( \
select distinct k.fullname,b.board_id,substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) tanggal \
from karyawan k, trello_karyawan tk, boardactions b where k.fullname  = tk.fullname and \
tk.trelloid = b.username and k.fullname = '"+fullname+"' \
and substring(tanggal,1,4) = YEAR(CURRENT_DATE)) a, board b \
where a.board_id = b.id \
order by tanggal desc;"

            print(query, flush=True)
            resultproxy = cur.execute(query)
            
            d, a = {}, []
            for rowproxy in resultproxy:
                # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
                for column, value in rowproxy.items():
                    # build up the dictionary
                    d = {**d, **{column: value}}
                a.append(d)
                # print(a,flush=True)
            
            return { 'Mandays': a }, 200
        except:
            return { 'Status' : 'Something Wrong' }
