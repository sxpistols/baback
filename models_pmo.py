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

class ClientModel(db.Model):
    __tablename__ = 'client'
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

class karyawanPMO():

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
        query = "select user_id,fullname from karyawan where divisi = 'PMO' and posisi='Project Manager' and status = 'Active'"

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


class ProjectState(db.Model):
    __tablename__ = 'project_state'
    id_project = db.Column(db.String(100), primary_key = True)
    status = db.Column(db.String(10), primary_key=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class ProjectSetting(db.Model):
    __tablename__ = 'project_setting'
    board = db.Column(db.String(100), primary_key = True)
    pm = db.Column(db.String(100), primary_key = True)
    client = db.Column(db.String(100))
    project_type = db.Column(db.String(20))
    nilai_project = db.Column(db.String(20))
    mandays = db.Column(db.String(10))
    start_date = db.Column(db.String(25))
    end_date = db.Column(db.String(25))
    projectdiv = db.Column(db.String(6))
    created_by = db.Column(db.String(50), primary_key = True)
    timenow = db.Column(db.String(25), primary_key = True)
    noproject = db.Column(db.String(25))
    namaproject = db.Column(db.String(150))
    no_po = db.Column(db.String(25))
    nama_po = db.Column(db.String(150))
    invoice1 = db.Column(db.String(150))
    invoice2 = db.Column(db.String(150))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()



class Project(db.Model):
    __tablename__ = 'project'
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
    where karyawan.divisi in ('PMO') \
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
    where karyawan.divisi in ('PMO') \
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
    def dashboard_summary(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            query = "select (select count(1) from karyawan where divisi = 'PMO' and fullname != 'Admin Trello' and UPPER(status) = 'ACTIVE' and \
            posisi != 'Quality Control' and resource = 'PMO' ) pmo, \
(select count(1) from karyawan where divisi = 'SDO' and UPPER(status) = 'ACTIVE' and posisi != 'Quality Control' and resource = 'SDO') sdo, \
(select count(1) from karyawan where posisi = 'Quality Control' and UPPER(status) = 'ACTIVE' and resource != 'RMO') qc, \
(select count(1) from karyawan where UPPER(status) = 'ACTIVE' and resource = 'RMO') rmo;"

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
    def dashboard_pmo(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            query = "select count(1) pmo from ( \
select distinct k2.fullname from boardactions b2, karyawan k2, trello_karyawan tk2 where board_id in ( \
select distinct board_id from boardactions b where username in ( \
select tk.trelloid  from karyawan k, trello_karyawan tk  \
where divisi = 'PMO' and UPPER(status) = 'ACTIVE' \
and posisi = 'Project Manager' and user_id not like 'arief.dolants%' and user_id != 'salwa' \
and k.fullname = tk.fullname)) \
and k2.fullname = tk2.fullname  \
and tk2.trelloid = b2.username \
and k2.divisi = 'PMO' and upper(status) = 'ACTIVE' and posisi != 'Quality Control') X;"

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
    def dashboard_pmochart(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            query = "select client, resource from ( \
select nama client, count(1) resource from ( \
select distinct fullname, nama from ( \
select distinct b.board_id, b.username,k.fullname, posisi, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid  \
and k.fullname = tk.fullname  \
and k.resource = 'PMO' \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in ( \
select board  from project_setting ps, board b, client c \
where upper(status) = 'Active' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv != 'SDO' \
and c.id = ps.client) \
) Z, project_setting p, client c \
where posisi != 'Quality Control' \
and divisi = 'PMO' \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id \
and Z.board_id = p.board \
) CC \
group by nama ) BB \
UNION  \
Select 'Others', count(1) resource  from ( \
select fullname, posisi, divisi, status from karyawan where fullname not in ( \
select distinct fullname from ( \
select distinct b.board_id, b.username,k.fullname, posisi, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid \
and k.fullname = tk.fullname \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in ( \
select board  from project_setting ps, board b, client c \
where upper(status) = 'Active' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv != 'SDO' \
and c.id = ps.client) \
) Z, project_setting p, client c \
where posisi != 'Quality Control' \
and divisi = 'PMO' \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id  \
and Z.board_id = p.board \
order by fullname asc) \
and posisi != 'Quality Control' \
and divisi = 'PMO' \
and resource = 'PMO' \
and upper(status) = 'ACTIVE') XX;"

            resultproxy = cur.execute(query)
            d, a = {}, []
            # chartData = []

            for rowproxy in resultproxy:
                # chartData.append(list(rowproxy))
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            # print(chartData, flush=True)
            return { 'Resource' : a }, 200
        except:
            return { 'OK' : 'OS' } 

    @classmethod
    def dashboard_pmosharing(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            query = "select  \
   case when posisi = 'Developer' THEN 'Dev' \
   		when posisi = 'Developer Analyst' THEN 'Dev An' \
   		when posisi = 'Project Admin' THEN 'PA' \
   		when posisi = 'Project Manager' THEN 'PM' \
   		when posisi = 'System Administrator' THEN 'Sys Admin' \
   		when posisi = 'System Analyst' THEN 'SA' \
   		when posisi = 'Technical Writer' THEN 'TW' \
   		ELSE 'Other' \
   	END as 'posisi',\
COUNT(CASE WHEN jumlah = 1  THEN 1 END) AS 'satu', \
COUNT(CASE WHEN jumlah = 2  THEN 1 END) AS 'double', \
COUNT(CASE WHEN jumlah > 2  THEN 1 END) AS 'morethan' \
from ( \
select * from ( \
select k.user_id, k.posisi, count(1) jumlah from ( \
select XY.board, XY.user_id, ps.client,c.nama from ( \
select distinct board, user_id from assignment_karyawan ak where upper(status) = 'ACTIVE') XY, project_setting ps, client c \
where ps.board = XY.board \
and c.id = ps.client) MMM, karyawan k  \
where k.user_id = MMM.user_id \
and k.fullname != 'Admin Trello' \
and k.posisi != 'Quality Control' \
and k.divisi = 'PMO' \
and k.resource = 'PMO' \
and upper(k.status) = 'ACTIVE' \
group by user_id) NNN) XXXX \
group by posisi \
order by posisi asc;"

            resultproxy = cur.execute(query)
            d, a = {}, []
            # chartData = []

            for rowproxy in resultproxy:
                # chartData.append(list(rowproxy))
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            # print(chartData, flush=True)
            return { 'Resource' : a }, 200
        except:
            return { 'OK' : 'OS' } 

    @classmethod
    def dashboard_sdodipmo(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            query = "select k.user_id, k.fullname,substring(b.name,1,25) name, k.posisi, client, substring(nama,1,25) nama, projectdiv, count(1) jumlah from ( \
select XY.board, XY.user_id, ps.client,c.nama, ps.projectdiv from ( \
select distinct board, user_id from assignment_karyawan ak where upper(status) = 'ACTIVE') XY, project_setting ps, client c \
where ps.board = XY.board \
and ps.projectdiv = 'PMO' \
and c.id = ps.client \
and upper(ps.status) = 'ACTIVE') MMM, karyawan k, board b \
where k.user_id = MMM.user_id \
and b.id = MMM.board \
and k.posisi != 'Quality Control' \
and k.divisi = 'SDO' \
and k.resource = 'SDO' \
and upper(k.status) = 'ACTIVE' \
group by user_id;"

            resultproxy = cur.execute(query)
            d, a = {}, []
            # chartData = []

            for rowproxy in resultproxy:
                # chartData.append(list(rowproxy))
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            # print(chartData, flush=True)
            return { 'Resource' : a }, 200
        except:
            return { 'OK' : 'OS' } 


    @classmethod
    def dashboard_pmoforsdo(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            query = "select k.user_id, k.fullname,substring(b.name,1,25) name, k.posisi, client, substring(nama,1,25) nama, projectdiv, count(1) jumlah from ( \
select XY.board, XY.user_id, ps.client,c.nama, ps.projectdiv from ( \
select distinct board, user_id from assignment_karyawan ak where upper(status) = 'ACTIVE') XY, project_setting ps, client c \
where ps.board = XY.board \
and ps.projectdiv = 'SDO' \
and c.id = ps.client \
and upper(ps.status) = 'ACTIVE') MMM, karyawan k, board b \
where k.user_id = MMM.user_id \
and b.id = MMM.board \
and k.posisi != 'Quality Control' \
and k.divisi = 'PMO' \
and k.resource = 'PMO' \
and upper(k.status) = 'ACTIVE'  \
group by user_id;;"

            resultproxy = cur.execute(query)
            d, a = {}, []
            # chartData = []

            for rowproxy in resultproxy:
                # chartData.append(list(rowproxy))
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            # print(chartData, flush=True)
            return { 'Resource' : a }, 200
        except:
            return { 'OK' : 'OS' } 

    @classmethod
    def dashboard_pmoposisi(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            query = "select posisi, count(1) jumlah from karyawan k \
where divisi = 'PMO' and resource = 'PMO' and upper(status) = 'ACTIVE' \
and posisi != 'Quality Control' \
group by posisi;"

            resultproxy = cur.execute(query)
            d, a = {}, []
            # chartData = []

            for rowproxy in resultproxy:
                # chartData.append(list(rowproxy))
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            # print(chartData, flush=True)
            return { 'Resource' : a }, 200
        except:
            return { 'OK' : 'OS' } 

    @classmethod
    def dashboard_pmostatusk(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            query = "select case when posisi = 'Developer' THEN 'Dev' \
   		when posisi = 'Developer Analyst' THEN 'Dev An'  \
   		when posisi = 'Project Admin' THEN 'PA' \
   		when posisi = 'Project Manager' THEN 'PM' \
   		when posisi = 'System Administrator' THEN 'Sys Admin'  \
   		when posisi = 'System Analyst' THEN 'SA'  \
   		when posisi = 'Technical Writer' THEN 'TW' \
   		ELSE 'Other' \
   	END as 'posisi', \
COUNT(CASE WHEN upper(statuskaryawan) = 'TETAP' THEN 1 END) AS 'tetap', \
COUNT(CASE WHEN upper(statuskaryawan) = 'KONTRAK' THEN 1 END) AS 'kontrak' \
from karyawan  \
where divisi = 'PMO' and resource = 'PMO' and upper(status) = 'ACTIVE' \
and posisi != 'Quality Control' \
group by posisi;"

            resultproxy = cur.execute(query)
            d, a = {}, []
            # chartData = []

            for rowproxy in resultproxy:
                # chartData.append(list(rowproxy))
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            # print(chartData, flush=True)
            return { 'Resource' : a }, 200
        except:
            return { 'OK' : 'OS' } 


    @classmethod
    def dashboard_pmosdoother(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            query = "select 'PMO' divisi, count(1) resource from (  \
select distinct fullname from (  \
select distinct b.board_id, b.username,k.fullname, posisi, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid  \
and k.fullname = tk.fullname \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in ( \
select board  from project_setting ps, board b, client c \
where upper(status) = 'Active' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv = 'PMO' \
and c.id = ps.client) \
and k.divisi = 'PMO' \
and k.resource = 'PMO' \
) Z, project_setting p, client c  \
where posisi != 'Quality Control'  \
and divisi = 'PMO'  \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id  \
and Z.board_id = p.board  \
order by fullname asc) S \
UNION \
select 'SDO' divisi, count(1) resource from ( \
select distinct k.user_id, k.divisi from ( \
select XY.board, XY.user_id, ps.client,c.nama, ps.projectdiv from ( \
select distinct board, user_id from assignment_karyawan ak where upper(status) = 'ACTIVE') XY, project_setting ps, client c \
where ps.board = XY.board \
and ps.projectdiv = 'PMO' \
and c.id = ps.client \
and upper(ps.status) = 'ACTIVE') MMM, karyawan k, board b \
where k.user_id = MMM.user_id \
and b.id = MMM.board \
and k.divisi = 'SDO' \
and k.posisi != 'Quality Control' \
and upper(k.status) = 'ACTIVE' )XY group by divisi \
UNION \
Select 'PMO-OTHER' divisi, count(1) resource  from ( \
select fullname, posisi, divisi, status from karyawan where fullname not in ( \
select distinct fullname from ( \
select distinct b.board_id, b.username,k.fullname, posisi, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid  \
and k.fullname = tk.fullname \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in ( \
select board  from project_setting ps, board b, client c \
where upper(status) = 'Active' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv = 'PMO' \
and c.id = ps.client) \
) Z, project_setting p, client c \
where posisi != 'Quality Control' \
and divisi = 'PMO' \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id  \
and Z.board_id = p.board \
order by fullname asc) \
and posisi != 'Quality Control' \
and divisi = 'PMO' \
and resource = 'PMO' \
and upper(status) = 'ACTIVE') XX \
UNION \
select 'RMO' divisi, count(1) resource from (  \
select distinct fullname from (  \
select distinct b.board_id, b.username,k.fullname, posisi, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid  \
and k.fullname = tk.fullname \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in ( \
select board  from project_setting ps, board b, client c \
where upper(status) = 'Active' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv = 'PMO' \
and c.id = ps.client) \
and k.divisi = 'PMO' \
and k.resource = 'RMO' \
) Z, project_setting p, client c  \
where posisi != 'Quality Control'  \
and divisi = 'PMO'  \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id  \
and Z.board_id = p.board  \
order by fullname asc) S ;"

            resultproxy = cur.execute(query)
            d, a = {}, []
            # chartData = []

            for rowproxy in resultproxy:
                # chartData.append(list(rowproxy))
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            # print(chartData, flush=True)
            return { 'Resource' : a }, 200
        except:
            return { 'OK' : 'OS' } 


    @classmethod
    def dashboard_pmopercent(cls):
        try:
            import datetime
            start_date = datetime.datetime.now() - datetime.timedelta(10)

            cur = db.session()

            TOTAL = "select count(1) totalRes from (select distinct fullname from ( \
select distinct b.board_id, b.username,k.fullname, posisi, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid \
and k.fullname = tk.fullname \
and k.resource = 'PMO' \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in ( \
select board  from project_setting ps, board b, client c \
where upper(status) = 'Active' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv != 'SDO' \
and c.id = ps.client) \
) Z, project_setting p, client c \
where posisi != 'Quality Control' \
and fullname != 'Admin Trello' \
and divisi = 'PMO' \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id \
and Z.board_id = p.board \
order by fullname asc \
)PP;"

            resultTotal = cur.execute(TOTAL)
            for e in resultTotal:
                RTOTAL = e.totalRes

            # print(type(RTOTAL),flush=True)
            query = "select client, resource, FORMAT((resource/"+str(RTOTAL)+")*100,0) persentase from ( \
select nama client, count(1) resource from ( \
select distinct fullname, nama from ( \
select distinct b.board_id, b.username,k.fullname, posisi, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid  \
and k.fullname = tk.fullname \
and k.resource = 'PMO' \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in ( \
select board  from project_setting ps, board b, client c \
where upper(status) = 'Active' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv != 'SDO' \
and c.id = ps.client) \
) Z, project_setting p, client c \
where posisi != 'Quality Control' \
and divisi = 'PMO' \
and Z.fullname != 'Admin Trello' \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id  \
and Z.board_id = p.board \
) CC \
group by nama ) BB \
UNION \
Select 'Others', count(1) resource,FORMAT((count(1)/"+str(RTOTAL)+")*100,0) persentase  from ( \
select fullname, posisi, divisi, status from karyawan where fullname not in ( \
select distinct fullname from ( \
select distinct b.board_id, b.username,k.fullname, posisi, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid \
and k.fullname = tk.fullname \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in ( \
select board  from project_setting ps, board b, client c \
where upper(status) = 'Active' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv != 'SDO' \
and c.id = ps.client) \
) Z, project_setting p, client c \
where posisi != 'Quality Control' \
and divisi = 'PMO' \
and Z.fullname != 'Admin Trello' \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id \
and Z.board_id = p.board \
order by fullname asc) \
and posisi != 'Quality Control' \
and divisi = 'PMO' \
and fullname != 'Admin Trello' \
and resource = 'PMO' \
and upper(status) = 'ACTIVE') XX;"

            query = "select * from (select nama client, \
COUNT(CASE WHEN resource = 'PMO' THEN 1 END) AS 'pmo', \
COUNT(CASE WHEN resource = 'RMO' THEN 1 END) AS 'rmo' \
from (  \
select distinct fullname, nama,resource  from (  \
select distinct b.board_id, b.username,k.fullname, posisi, k.resource, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid  \
and k.fullname = tk.fullname \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in (  \
select board  from project_setting ps, board b, client c \
where upper(status) = 'ACTIVE' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv != 'SDO' \
and c.id = ps.client) \
) Z, project_setting p, client c \
where posisi != 'Quality Control' \
and divisi = 'PMO' \
and Z.fullname != 'Admin Trello' \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id  \
and Z.board_id = p.board \
) CC \
group by nama \
UNION \
Select 'Others', \
COUNT(CASE WHEN resource = 'PMO' THEN 1 END) AS 'pmo', \
COUNT(CASE WHEN resource = 'RMO' THEN 1 END) AS 'rmo' \
from ( \
select fullname, posisi, divisi, resource from karyawan where fullname not in ( \
select distinct fullname from ( \
select distinct b.board_id, b.username,k.fullname, posisi, divisi, k.status from boardactions b, karyawan k , trello_karyawan tk \
where b.username = tk.trelloid \
and k.fullname = tk.fullname \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between substring(CURDATE() - INTERVAL 1 MONTH,1,10) AND substring(CURDATE(),1,10) \
and board_id in ( \
select board  from project_setting ps, board b, client c \
where upper(status) = 'ACTIVE' \
and ps.board = b.id \
and project_type ='Project' \
and projectdiv != 'SDO' \
and c.id = ps.client) \
) Z, project_setting p, client c \
where posisi != 'Quality Control' \
and divisi = 'PMO' \
and Z.fullname != 'Admin Trello' \
and upper(Z.status) = 'ACTIVE' \
and p.client = c.id \
and Z.board_id = p.board \
order by fullname asc) \
and posisi != 'Quality Control' \
and divisi = 'PMO' \
and fullname != 'Admin Trello' \
and upper(status) = 'ACTIVE') XX ) ZZ;"

            
            # print(query,flush=True)
            resultproxy = cur.execute(query)
            d, a = {}, []

            # chartData = []
            for rowproxy in resultproxy:
                # print(list(rowproxy), flush=True)
                # chartData.append(list(rowproxy))

                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}

                a.append(d)
            
            # print(chartData,flush=True)
            

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
    def resourceidle(cls):
        
        try:
            import datetime
            start_date = datetime.datetime.now()# - datetime.timedelta(1)
            

            cur = db.session()

            query = "select distinct abb.fullname fullname,cuti.keterangan keterangan from  ( \
            select distinct karyawan.fullname from karyawan left join(  \
            select fullname,  name,tanggal,count(1) jumlah from (  \
            select tk.fullname, b.name,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal,type \
            from boardactions a, trello_karyawan tk, board b \
            where a.username  = tk.trelloid \
            and b.id = a.board_id \
            and substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) = '"+str(start_date)[0:10]+"' \
            order by fullname asc) a \
            group by fullname, tanggal, name ) as timesheet  \
            on lower(karyawan.fullname) = lower(timesheet.fullname)  \
            where karyawan.divisi in ('PMO') \
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
    def resourceidledaily(cls,tanggal):
        
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
            group by fullname, tanggal,name ) as timesheet  \
            on lower(karyawan.fullname) = lower(timesheet.fullname)  \
            where karyawan.divisi in ('PMO','SDO', 'DSO', 'RMO') \
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
    def resourcemandays(cls, user_role, tahun):
        try:

            cur = db.session()
            if(user_role == '6'):
                query = "select fullname, jumlah, \
    case when lebih < 0 then \"\" \
    else lebih \
    end lebih \
    from ( \
    select fullname, cast(sum(jumlah) AS CHAR) jumlah, cast(sum(jumlah)-264 AS CHAR) Lebih from ( \
    select count(1) jumlah,fullname,tanggal from ( \
    select distinct k.fullname,b.board_id,substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) tanggal from karyawan k, trello_karyawan tk, boardactions b \
    where k.fullname  = tk.fullname \
    and tk.trelloid = b.username) AAA \
    group by fullname,tanggal) ABB \
    where substring(tanggal,1,4) = YEAR(CURRENT_DATE) \
    group by fullname \
    order by fullname ASC) l;"
            else:
                query = "select fullname, jumlah, \
  case when lebih < 0 then \"\" \
  else lebih \
  end lebih \
  from ( \
select fullname, cast(sum(jumlah) AS CHAR) jumlah, cast(sum(jumlah)-264 AS CHAR) Lebih from ( \
select count(1) jumlah,fullname,tanggal from ( \
select distinct k.fullname,b.board_id,substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) tanggal from karyawan k, trello_karyawan tk, boardactions b \
where k.fullname  = tk.fullname \
and tk.trelloid = b.username \
and k.divisi = 'PMO') AAA \
group by fullname,tanggal) ABB \
where substring(tanggal,1,4) = '"+tahun+"' \
group by fullname \
order by fullname ASC) l;"

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

    @classmethod
    def mandaysProjectFin(cls, user_role, tahun,bulan,board):
        concat = pd.core.frame.DataFrame

        query = "select fullname,name,posisi,t01,t02,t03,t04,t05,t06,t07,t08,t09,t10,t11,t12,t13,t14,t15, \
	t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30,t31, \
	t01+t02+t03+t04+t05+t06+t07+t08+t09+t10+t11+t12+t13+t14+t15+t16+t17+t18+t19+t20+t21+t22+t23+t24+t25+t26+t27+t28+t29+t30+t31 jumlah from ( \
        select yy.fullname,yy.name, yy.posisi, \
case when yy.t01 != '0'  then FORMAT(1/LULULU.t01,2) else yy.t01 end as 't01', \
case when yy.t02 != '0'  then FORMAT(1/LULULU.t02,2) else yy.t02 end as 't02', \
case when yy.t03 != '0'  then FORMAT(1/LULULU.t03,2) else yy.t03 end as 't03', \
case when yy.t04 != '0'  then FORMAT(1/LULULU.t04,2) else yy.t04 end as 't04', \
case when yy.t05 != '0'  then FORMAT(1/LULULU.t05,2) else yy.t05 end as 't05', \
case when yy.t06 != '0'  then FORMAT(1/LULULU.t06,2) else yy.t06 end as 't06', \
case when yy.t07 != '0'  then FORMAT(1/LULULU.t07,2) else yy.t07 end as 't07', \
case when yy.t08 != '0'  then FORMAT(1/LULULU.t08,2) else yy.t08 end as 't08', \
case when yy.t09 != '0'  then FORMAT(1/LULULU.t09,2) else yy.t09 end as 't09', \
case when yy.t10 != '0'  then FORMAT(1/LULULU.t10,2) else yy.t10 end as 't10', \
case when yy.t11 != '0'  then FORMAT(1/LULULU.t11,2) else yy.t11 end as 't11', \
case when yy.t12 != '0'  then FORMAT(1/LULULU.t12,2) else yy.t12 end as 't12', \
case when yy.t13 != '0'  then FORMAT(1/LULULU.t13,2) else yy.t13 end as 't13', \
case when yy.t14 != '0'  then FORMAT(1/LULULU.t14,2) else yy.t14 end as 't14', \
case when yy.t15 != '0'  then FORMAT(1/LULULU.t15,2) else yy.t15 end as 't15', \
case when yy.t16 != '0'  then FORMAT(1/LULULU.t16,2) else yy.t16 end as 't16', \
case when yy.t17 != '0'  then FORMAT(1/LULULU.t17,2) else yy.t17 end as 't17', \
case when yy.t18 != '0'  then FORMAT(1/LULULU.t18,2) else yy.t18 end as 't18', \
case when yy.t19 != '0'  then FORMAT(1/LULULU.t19,2) else yy.t19 end as 't19', \
case when yy.t20 != '0'  then FORMAT(1/LULULU.t20,2) else yy.t20 end as 't20', \
case when yy.t21 != '0'  then FORMAT(1/LULULU.t21,2) else yy.t21 end as 't21', \
case when yy.t22 != '0'  then FORMAT(1/LULULU.t22,2) else yy.t22 end as 't22', \
case when yy.t23 != '0'  then FORMAT(1/LULULU.t23,2) else yy.t23 end as 't23', \
case when yy.t24 != '0'  then FORMAT(1/LULULU.t24,2) else yy.t24 end as 't24', \
case when yy.t25 != '0'  then FORMAT(1/LULULU.t25,2) else yy.t25 end as 't25', \
case when yy.t26 != '0'  then FORMAT(1/LULULU.t26,2) else yy.t26 end as 't26', \
case when yy.t27 != '0'  then FORMAT(1/LULULU.t27,2) else yy.t27 end as 't27', \
case when yy.t28 != '0'  then FORMAT(1/LULULU.t28,2) else yy.t28 end as 't28', \
case when yy.t29 != '0'  then FORMAT(1/LULULU.t29,2) else yy.t29 end as 't29', \
case when yy.t30 != '0'  then FORMAT(1/LULULU.t30,2) else yy.t30 end as 't30', \
case when yy.t31 != '0'  then FORMAT(1/LULULU.t31,2) else yy.t31 end as 't31' \
     FROM( \
        select * from (select distinct karyawan.fullname fullname,karyawan.posisi, timesheet.name,timesheet.id, \
case when timesheet.tanggal_01 is not null then '1' else '0' end as 't01',  \
case when timesheet.tanggal_02 is not null then '1' else '0' end as 't02',  \
case when timesheet.tanggal_03 is not null then '1' else '0' end as 't03',  \
case when timesheet.tanggal_04 is not null then '1' else '0' end as 't04',  \
case when timesheet.tanggal_05 is not null then '1' else '0' end as 't05',  \
case when timesheet.tanggal_06 is not null then '1' else '0' end as 't06',  \
case when timesheet.tanggal_07 is not null then '1' else '0' end as 't07',  \
case when timesheet.tanggal_08 is not null then '1' else '0' end as 't08',  \
case when timesheet.tanggal_09 is not null then '1' else '0' end as 't09',  \
case when timesheet.tanggal_10 is not null then '1' else '0' end as 't10',  \
case when timesheet.tanggal_11 is not null then '1' else '0' end as 't11',  \
case when timesheet.tanggal_12 is not null then '1' else '0' end as 't12',  \
case when timesheet.tanggal_13 is not null then '1' else '0' end as 't13',  \
case when timesheet.tanggal_14 is not null then '1' else '0' end as 't14',  \
case when timesheet.tanggal_15 is not null then '1' else '0' end as 't15',  \
case when timesheet.tanggal_16 is not null then '1' else '0' end as 't16',  \
case when timesheet.tanggal_17 is not null then '1' else '0' end as 't17',  \
case when timesheet.tanggal_18 is not null then '1' else '0' end as 't18',  \
case when timesheet.tanggal_19 is not null then '1' else '0' end as 't19',  \
case when timesheet.tanggal_20 is not null then '1' else '0' end as 't20',  \
case when timesheet.tanggal_21 is not null then '1' else '0' end as 't21',  \
case when timesheet.tanggal_22 is not null then '1' else '0' end as 't22',  \
case when timesheet.tanggal_23 is not null then '1' else '0' end as 't23',  \
case when timesheet.tanggal_24 is not null then '1' else '0' end as 't24',  \
case when timesheet.tanggal_25 is not null then '1' else '0' end as 't25',  \
case when timesheet.tanggal_26 is not null then '1' else '0' end as 't26',  \
case when timesheet.tanggal_27 is not null then '1' else '0' end as 't27',  \
case when timesheet.tanggal_28 is not null then '1' else '0' end as 't28',  \
case when timesheet.tanggal_29 is not null then '1' else '0' end as 't29',  \
case when timesheet.tanggal_30 is not null then '1' else '0' end as 't30',  \
case when timesheet.tanggal_31 is not null then '1' else '0' end as 't31'  \
from karyawan inner join ( select b.fullname fullname,  bb.name ,bb.id, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '01' then '1' end) as tanggal_01,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '02' then '1' end) as tanggal_02,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '03' then '1' end) as tanggal_03,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '04' then '1' end) as tanggal_04,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '05' then '1' end) as tanggal_05,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '06' then '1' end) as tanggal_06,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '07' then '1' end) as tanggal_07,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '08' then '1' end) as tanggal_08,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '09' then '1' end) as tanggal_09,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '10' then '1' end) as tanggal_10,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '11' then '1' end) as tanggal_11,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '12' then '1' end) as tanggal_12,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '13' then '1' end) as tanggal_13,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '14' then '1' end) as tanggal_14,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '15' then '1' end) as tanggal_15,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '16' then '1' end) as tanggal_16,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '17' then '1' end) as tanggal_17,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '18' then '1' end) as tanggal_18,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '19' then '1' end) as tanggal_19,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '20' then '1' end) as tanggal_20,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '21' then '1' end) as tanggal_21,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '22' then '1' end) as tanggal_22,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '23' then '1' end) as tanggal_23,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '24' then '1' end) as tanggal_24,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '25' then '1' end) as tanggal_25,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '26' then '1' end) as tanggal_26,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '27' then '1' end) as tanggal_27,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '28' then '1' end) as tanggal_28,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '29' then '1' end) as tanggal_29,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '30' then '1' end) as tanggal_30,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '31' then '1' end) as tanggal_31  \
from boardactions a, trello_karyawan b, board bb  \
  where substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+tahun+"-"+bulan+"'  \
  and a.username = b.trelloid  \
  and a.board_id = bb.id \
  group by fullname,board_id \
  order by fullname asc) as timesheet  \
 on lower(karyawan.fullname) = lower(timesheet.fullname)  \
where karyawan.posisi != 'Support Surveillance' and karyawan.posisi != 'Trello Admin' and status = 'Active' order by karyawan.fullname asc) z \
where id = '"+board+"') yy \
LEFT JOIN (select fullname,posisi,sum(t01)t01,sum(t02)t02,sum(t03)t03,sum(t04)t04,sum(t05)t05, \
sum(t06)t06,sum(t07)t07,sum(t08)t08,sum(t09)t09,sum(t10)t10,sum(t11)t11,sum(t12)t12, \
sum(t13)t13,sum(t14)t14,sum(t15)t15,sum(t16)t16,sum(t17)t17,sum(t18)t18,sum(t19)t19, \
sum(t20)t20,sum(t21)t21,sum(t22)t22,sum(t23)t23,sum(t24)t24,sum(t25)t25,sum(t26)t26, \
sum(t27)t27,sum(t28)t28,sum(t29)t29,sum(t30)t30,sum(t31)t31 from ( \
select distinct karyawan.fullname fullname,karyawan.posisi, timesheet.name,timesheet.id, \
case when timesheet.tanggal_01 is not null then '1' else '0' end as 't01',  \
case when timesheet.tanggal_02 is not null then '1' else '0' end as 't02',  \
case when timesheet.tanggal_03 is not null then '1' else '0' end as 't03',  \
case when timesheet.tanggal_04 is not null then '1' else '0' end as 't04',  \
case when timesheet.tanggal_05 is not null then '1' else '0' end as 't05',  \
case when timesheet.tanggal_06 is not null then '1' else '0' end as 't06',  \
case when timesheet.tanggal_07 is not null then '1' else '0' end as 't07',  \
case when timesheet.tanggal_08 is not null then '1' else '0' end as 't08',  \
case when timesheet.tanggal_09 is not null then '1' else '0' end as 't09',  \
case when timesheet.tanggal_10 is not null then '1' else '0' end as 't10',  \
case when timesheet.tanggal_11 is not null then '1' else '0' end as 't11',  \
case when timesheet.tanggal_12 is not null then '1' else '0' end as 't12',  \
case when timesheet.tanggal_13 is not null then '1' else '0' end as 't13',  \
case when timesheet.tanggal_14 is not null then '1' else '0' end as 't14',  \
case when timesheet.tanggal_15 is not null then '1' else '0' end as 't15',  \
case when timesheet.tanggal_16 is not null then '1' else '0' end as 't16',  \
case when timesheet.tanggal_17 is not null then '1' else '0' end as 't17',  \
case when timesheet.tanggal_18 is not null then '1' else '0' end as 't18',  \
case when timesheet.tanggal_19 is not null then '1' else '0' end as 't19',  \
case when timesheet.tanggal_20 is not null then '1' else '0' end as 't20',  \
case when timesheet.tanggal_21 is not null then '1' else '0' end as 't21',  \
case when timesheet.tanggal_22 is not null then '1' else '0' end as 't22',  \
case when timesheet.tanggal_23 is not null then '1' else '0' end as 't23',  \
case when timesheet.tanggal_24 is not null then '1' else '0' end as 't24',  \
case when timesheet.tanggal_25 is not null then '1' else '0' end as 't25',  \
case when timesheet.tanggal_26 is not null then '1' else '0' end as 't26',  \
case when timesheet.tanggal_27 is not null then '1' else '0' end as 't27',  \
case when timesheet.tanggal_28 is not null then '1' else '0' end as 't28',  \
case when timesheet.tanggal_29 is not null then '1' else '0' end as 't29',  \
case when timesheet.tanggal_30 is not null then '1' else '0' end as 't30',  \
case when timesheet.tanggal_31 is not null then '1' else '0' end as 't31'  \
from karyawan inner join ( select b.fullname fullname,  bb.name ,bb.id, \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '01' then '1' end) as tanggal_01,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '02' then '1' end) as tanggal_02,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '03' then '1' end) as tanggal_03,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '04' then '1' end) as tanggal_04,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '05' then '1' end) as tanggal_05,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '06' then '1' end) as tanggal_06,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '07' then '1' end) as tanggal_07,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '08' then '1' end) as tanggal_08,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '09' then '1' end) as tanggal_09,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '10' then '1' end) as tanggal_10,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '11' then '1' end) as tanggal_11,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '12' then '1' end) as tanggal_12,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '13' then '1' end) as tanggal_13,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '14' then '1' end) as tanggal_14,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '15' then '1' end) as tanggal_15,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '16' then '1' end) as tanggal_16,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '17' then '1' end) as tanggal_17,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '18' then '1' end) as tanggal_18,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '19' then '1' end) as tanggal_19,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '20' then '1' end) as tanggal_20,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '21' then '1' end) as tanggal_21,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '22' then '1' end) as tanggal_22,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '23' then '1' end) as tanggal_23,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '24' then '1' end) as tanggal_24,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '25' then '1' end) as tanggal_25,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '26' then '1' end) as tanggal_26,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '27' then '1' end) as tanggal_27,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '28' then '1' end) as tanggal_28,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '29' then '1' end) as tanggal_29,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '30' then '1' end) as tanggal_30,  \
sum(case when substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),9,2) = '31' then '1' end) as tanggal_31  \
from boardactions a, trello_karyawan b, board bb  \
  where substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,7) = '"+tahun+"-"+bulan+"'  \
  and a.username = b.trelloid  \
  and a.board_id = bb.id \
  group by fullname,board_id \
  order by fullname asc) as timesheet  \
 on lower(karyawan.fullname) = lower(timesheet.fullname)  \
where karyawan.posisi != 'Support Surveillance' and status = 'Active' order by karyawan.fullname asc)XX  \
group by fullname) LULULU \
ON yy.fullname = LULULU.fullname )XZ;"


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
        # df2 = pd.read_sql(query2, db.session.bind)

        # print(df2, flush=True)
        cm = sns.light_palette("green", as_cmap=True)

        s = df.style.background_gradient(cmap='viridis')

        writer = pd.ExcelWriter(board+'_'+tahun+'_'+bulan+'.xlsx', engine='xlsxwriter')
        df.style.set_table_styles([{'selector': 'th','props': [('background-color', 'black'),('color', 'cyan')]}]).background_gradient(cmap='YlOrRd').highlight_null('white').to_excel(writer, sheet_name=board+'-'+tahun+''+bulan, startrow=1,startcol=1, index=True)
        # df.to_excel(writer, sheet_name=board+'_'+tahun+'_'+bulan+'.xlsx',num_format = "0.0%")
        writer.save()
        db.session.close()

        # if a is not nullable:
        return { 'Mandays': a }, 200

    @classmethod
    def activityByDate(cls, karyawan,dateassignment,endassignment):
        cur = db.session()
        resultproxy = cur.execute("select bd.name,k.fullname,substring(b.text,1,50) text,b.type,substring(CONVERT_TZ(tanggal,'+00:00','+07:00'),1,10) tanggal from boardactions b, karyawan k , trello_karyawan tk, board bd \
where k.user_id = '"+karyawan+"' \
and k.fullname = tk.fullname \
and b.username = tk.trelloid \
and bd.id = b.board_id \
and substring(CONVERT_TZ(b.tanggal,'+00:00','+07:00'),1,10) between '"+dateassignment+"' and '"+endassignment+"' \
order by tanggal asc;")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        return { 'Project': a }, 200

    @classmethod
    def appraisalteam(cls, userid):
        try:

            cur = db.session()

            query = "select a.user_id,a.fullname,a.posisi,a.divisi,ak.appraisalid,ak.pm,ak.performance, \
            ak.potential,ak.attitude,ak.periode,ak.createdate from ( \
            select k.user_id,k.fullname,k.posisi, k.divisi from karyawan k,trello_karyawan tk where tk.trelloid in ( \
select distinct username from boardactions b where board_id in (select board from project_setting ps \
where upper(status) = 'ACTIVE' and pm = '"+userid+"') ) \
and k.fullname = tk.fullname \
and divisi != 'Owner' \
and k.user_id != '"+userid+"' ) a \
left join appraisal_karyawan ak \
ON a.user_id = ak.user_id;"

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
            
            return { 'appraisalteam': a }, 200
        except:
            return { 'Status' : 'Something Wrong' }

class Appraisal(db.Model):
    __tablename__ = 'jadwal_appraisal'
    tahun = db.Column(db.String(4), primary_key = True)
    semester = db.Column(db.String(1), primary_key = True)
    status = db.Column(db.String(1), primary_key = True)
    createdby = db.Column(db.String(50))
    createdate = db.Column(db.String(20), default=("current_timestamp()"))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def listjadwalappraisal(cls):
        try:
            cur = db.session()

            query = "select * from jadwal_appraisal where status = '1';"

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
            
            return { 'jadwalappraisal': a }, 200
        except:
            return { 'Status' : 'Something Wrong' }
