from run import db
from passlib.hash import pbkdf2_sha256 as sha256
from flask_mysqldb import MySQL
import json
from flask_cors import CORS
import hashlib, binascii, os

# user_id
# fullname
# statuspernikahan
# nik
# identitas
# divisi
# tanggalmasuk
# statuskaryawan
# email
# phone
# alamat
# posisi


class KaryawanShiftModel(db.Model):
    __tablename__ = 'shifting'
    user_id = db.Column(db.String(50), primary_key = True)
    shifttype = db.Column(db.String(1), primary_key = True)
    startdate = db.Column(db.String(10), primary_key = True)
    enddate = db.Column(db.String(10), primary_key = True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select a.fullname, c.site, case when b.shifttype = 1 then 'Pagi' when b.shifttype = 2 then 'Sore' else 'Malam' END as shifttype, b.startdate, b.enddate from karyawan as a,shifting as b, site as c where a.user_id  = b.user_id and STR_TO_DATE(enddate,'%Y-%m-%d') >= current_date() and a.site = c.idsite")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Shift': a }, 200

    @classmethod
    def bayaran_shift(cls):

        cur = db.session()
        resultproxy = cur.execute("select fullname,concat(hari,' hari') as hari,concat(cuti,' hari') as cuti,startdate,enddate,description, FORMAT((hari-cuti) * rupiah,0) as jumlah from bayaran_shift as a, shift_reff as b where a.shifttype = b.shifttype")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Shift': a }, 200

    @classmethod
    def list_supervisor(cls):

        cur = db.session()
        resultproxy = cur.execute("select fullname from karyawan where divisi = 'BSO' and status = 'Active' and posisi in ('Subject Matter Expert', 'Support Leader','Support Specialist')")

        d, a = {}, []
        e = []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
                e.append(value)
            a.append(d)

        # if a is not nullable:
        return a, 200

    @classmethod
    def echo(cls):

        cur = db.session()
        resultproxy = cur.execute("select fullname from karyawan where divisi = 'BSO' and and status = 'Active' posisi in ('Subject Matter Expert', 'Support Leader','Support Specialist')")

        d, a = {}, []
        e = []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
                e.append(value)
            a.append(d)

        # if a is not nullable:
        return list(e), 200

class Assignment():
    @classmethod
    def find_by_id_assignment(cls, id_assignment):
        # cls.query.filter_by(user_id = user_id).first
        print(id_assignment,flush=True)
        query = "select b.fullname,a.tanggal,concat(a.tanggal,' ',a.starttime) as starttime,concat(a.tanggal,' ',a.endtime) as endtime,a.site,a.onsite,a.detail,a.reff,a.status,a.supervisor from assignment as a, karyawan as b where a.user_id = b.user_id and a.id_assignment = '"+id_assignment+"'"
        print(query,flush=True)

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
        return { 'Assignment': a }, 200

    @classmethod
    def getall(cls):
        print(monthly,flush=True)
        query = "select * from assignment_karyawan;"
        print(query,flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        for rowproxy in resultproxy:
            for column, value in rowproxy.items():
                d = {**d, **{column: value}}
            a.append(d)

        return { 'Report': a }, 200

    @classmethod
    def find_pars_monthly(cls, startdate,enddate):
        print(startdate,flush=True)
        query = "select a.fullname, b.dateassignment,b.applicationname,b.assignmenttype,b.supervisor,b.reff from karyawan a, assignment b where (b.dateassignment  between '"+startdate+"' and '"+enddate+"') and approval = 'Done' and a.user_id = b.user_id ;"
        print(query,flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        for rowproxy in resultproxy:
            for column, value in rowproxy.items():
                d = {**d, **{column: value}}
            a.append(d)

        return { 'Report': a }, 200




class KaryawanU():
    @classmethod
    def getuserid(cls, user_id):
        # cls.query.filter_by(user_id = user_id).first
        # query = "select * from karyawan where user_id='"+user_id+"' and status = 'Active'"
        query = "select user_id,a.fullname,statuspernikahan,nik,identitas,divisi,resource,tanggalmasuk,statuskaryawan,email,phone,alamat, \
        posisi,site,telegram,createdby,createdate,pendidikan,institusi,tempatlahir,tanggallahir,status,role_trello,nikkaryawan, \
        jurusan,trelloid, TIMESTAMPDIFF( YEAR, tanggalmasuk, now() ) year,TIMESTAMPDIFF( MONTH, tanggalmasuk, now() ) % 12 as month, \
        FLOOR( TIMESTAMPDIFF( DAY, tanggalmasuk, now() ) % 30.4375 ) as day \
        from karyawan a, trello_karyawan tk where a.user_id='"+user_id+"' and a.fullname = tk.fullname;"

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
        return { 'karyawan': a }, 200


    @classmethod
    def resignK(cls,username):
        try:
            cur = db.session()
            query = "update karyawan set status='InActive' where user_id = '"+username+"'"
            resultproxy = cur.execute(query)
            db.session.commit()

            db.session.close()

            return { 'Status': 'Success' }, 200
        except:
            print('EERRRRRRRRRRRRRRRRRRRRRRRRRRR', flush=True)
            return { 'Status' : 'Something Wrong' }

    @classmethod
    def addresign(cls,createdby,karyawan,tanggal,handover,ket,ket2):
        try:
            cur = db.session()
            query = "update karyawan set status='InActive',resigndate='"+tanggal+"' where user_id = '"+karyawan+"'"
            resultproxy = cur.execute(query)
            db.session.commit()
            db.session.close()

            cur = db.session()
            query = "insert INTO resignkaryawan(userid,handover,project,tanggalhandover,createdby) \
            values ('"+karyawan+"','"+handover+"','"+ket+"','"+ket2+"','"+createdby+"')"
            print(query, flush=True)
            resultproxy = cur.execute(query)
            db.session.commit()
            db.session.close()

            return { 'Status': 'Success' }, 200
        except:
            print('EERRRRRRRRRRRRRRRRRRRRRRRRRRR', flush=True)
            return { 'Status' : 'Something Wrong' }

    @classmethod
    def updateK(cls,username,email,fullname,telegram,divisi,posisi,alamat,telepon,tanggalmasuk,statuskaryawan,identitas,statuspernikahan,pendidikan,trelloid, institusi, nikkaryawan, jurusan, resource):

        try:
            cur = db.session()
            query = "update karyawan set user_id='"+username+"',email='"+email+"',fullname='"+fullname+"',telegram='"+telegram+"',divisi='"+divisi+"',posisi='"+posisi+"',alamat='"+alamat+"',phone='"+telepon+"',tanggalmasuk='"+tanggalmasuk+"',statuskaryawan='"+statuskaryawan+"',identitas='"+identitas+"',statuspernikahan='"+statuspernikahan+"',pendidikan='"+pendidikan+"', institusi='"+institusi+"', nikkaryawan='"+nikkaryawan+"', jurusan='"+jurusan+"', resource='"+resource+"' where user_id = '"+username+"'"
            resultproxy = cur.execute(query)
            db.session.commit()

            query = "update trello_karyawan set trelloid='"+trelloid+"' where fullname='"+fullname+"'"
            resultproxy = cur.execute(query)
            db.session.commit()
            print(query, flush=True)

            db.session.close()

            return { 'Status': 'Success' }, 200
        except:
            print('EERRRRRRRRRRRRRRRRRRRRRRRRRRR', flush=True)
            return { 'Status' : 'Something Wrong' }

class KaryawanAssignmentModel(db.Model):
    __tablename__ = 'assignment_pmo'
    user_id = db.Column(db.String(50), primary_key = True)
    tanggal = db.Column(db.String(10), primary_key = True)
    starttime = db.Column(db.String(50), primary_key = True)
    endtime = db.Column(db.String(50), primary_key = True)
    detail = db.Column(db.String(100), primary_key = True)
    reff = db.Column(db.String(100), primary_key = True)
    status = db.Column(db.String(100), primary_key = True)
    applicationname = db.Column(db.String(100), primary_key = True)
    assignmenttype = db.Column(db.String(100), primary_key = True)
    supervisor = db.Column(db.String(100), primary_key = True)
    dateassignment = db.Column(db.String(10), primary_key = True)
    site = db.Column(db.String(20), primary_key = True)
    onsite = db.Column(db.String(10), primary_key = True)
    approval = db.Column(db.String(10), primary_key = True)
    id_assignment = db.Column(db.String(100))
    timenow = db.Column(db.String(22))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select distinct b.fullname,a.approval,a.id_assignment,a.user_id,a.dateassignment,a.applicationname,a.assignmenttype,a.site,a.onsite,a.supervisor from assignment as a, karyawan as b where a.user_id = b.user_id and a.approval != 'Done'")
        resultproxy = cur.execute("select distinct b.fullname,a.approval,a.id_assignment,a.user_id,a.dateassignment,a.applicationname,a.assignmenttype,a.site,a.onsite,a.supervisor from assignment as a, karyawan as b where a.user_id = b.user_id and a.approval != 'Done'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Assignment': a }, 200

    @classmethod
    # def approveAssignment(cls):
    def approveAssignment(cls, id_assignment):
        # cls.query.filter_by(user_id = user_id).first
        print(id_assignment,flush=True)
        
        try:
            # item = cls.query.filter_by(id_assignment = id_assignment).first()
            # item.approval = 'Done'
            # db.session.commit()

            for row in cls.query.filter_by(id_assignment = id_assignment).all():
                print(row.approval, flush=True)
                row.approval = 'Done'

            db.session.commit()

            return { 'Status': 'OK' }
        except:
            return { 'Status' : 'DB Error' }
        # d, a = {}, []
        # for rowproxy in resultproxy:
        #     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        #     for column, value in rowproxy.items():
        #         # build up the dictionary
        #         d = {**d, **{column: value}}
        #     a.append(d)

        # # if a is not nullable:
        # return { 'Assignment': a }, 200


        
    @classmethod
    def return_done(cls):
        cur = db.session()
        resultproxy = cur.execute("select distinct b.fullname,a.approval,a.id_assignment,a.user_id,a.dateassignment,a.applicationname,a.assignmenttype,a.site,a.onsite,a.supervisor from assignment as a, karyawan as b where a.user_id = b.user_id and a.approval = 'Done'")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Assignment': a }, 200

    @classmethod
    def deleteAssignment(cls, assignment_id):
        query = "delete from assignment_karyawan where assignment_id = '"+assignment_id+"';"
        print(query,flush=True)

        try:

            cur = db.session()
            resultproxy = cur.execute(query)
            db.session.commit()
            db.session.close()
            
            return { 'Status' : 'Success' } 
        except:
            return { 'Status' : 'Failed' } 

    @classmethod
    def return_detail(cls, assignment_id):
        query = "select a.crname,assignment_id,a.user_id,bd.name,pm,assignmenttype,dateassignment,endassignment, \
        extendassignment,a.status,created_by,timenow,b.fullname \
from assignment_karyawan a, karyawan b, board bd where assignment_id = '"+assignment_id+"' \
and a.user_id = b.user_id \
and a.board = bd.id"

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
        return { 'Assignment': a }, 200

    @classmethod
    def email_data(cls, id_assignment):
        # cls.query.filter_by(user_id = user_id).first
        print(id_assignment,flush=True)
        query = "select b.fullname,a.tanggal,a.time,a.site,a.onsite,a.detail,a.reff,a.status,a.supervisor from assignment as a, karyawan as b where a.user_id = b.user_id and a.id_assignment = '"+id_assignment+"'"
        print(query,flush=True)

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
        return list(a)

    @classmethod
    def email_address(cls, id_assignment):
        # cls.query.filter_by(user_id = user_id).first
        print(id_assignment,flush=True)
        query = "select distinct b.email from assignment as a, karyawan as b where a.user_id = b.user_id and a.id_assignment = '"+id_assignment+"'"
        print(query,flush=True)

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
        return a

    @classmethod
    def getfullname(cls, user_id):
        # cls.query.filter_by(user_id = user_id).first
        # print(id_assignment,flush=True)
        query = "select fullname from karyawan where user_id = '"+user_id+"'"
        print(query,flush=True)

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
        return list(a)


class KaryawanAssignment(db.Model):
    __tablename__ = 'assignment_karyawan'
    assignment_id = db.Column(db.String(50), primary_key = True)
    user_id = db.Column(db.String(100), primary_key = True)
    board = db.Column(db.String(100), primary_key = True)
    pm = db.Column(db.String(100), primary_key = True)
    assignmenttype = db.Column(db.String(20))
    dateassignment = db.Column(db.String(25))
    endassignment = db.Column(db.String(25))
    crname = db.Column(db.String(150))
    created_by = db.Column(db.String(25), primary_key = True)
    timenow = db.Column(db.String(25), primary_key = True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select a.crname,a.assignment_id,k.user_id,k.fullname,substr(bd.name,1,50) name, \
        a.pm,a.assignmenttype,a.status,a.extendassignment, \
        a.dateassignment,a.endassignment from assignment_karyawan a, karyawan k , board bd \
     where a.user_id = k.user_id and bd.id = a.board and k.divisi = 'PMO' and a.status != 'DONE';")


        resultproxy = cur.execute("select a.crname,a.assignment_id,k.user_id,k.fullname,substr(bd.name,1,50) name, \
        a.pm,a.assignmenttype,a.status,a.extendassignment, \
        a.dateassignment,a.endassignment from assignment_karyawan a, karyawan k , board bd \
     where a.user_id = k.user_id and bd.id = a.board;")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Assignment': a }, 200

    @classmethod
    def assignmentupdate(cls, assignmentid,startd,endd,typex,status,extendd,crname):
        query = "update assignment_karyawan set status='"+status+"',dateassignment='"+startd+"',endassignment='"+endd+"', \
            type='"+typex+"',extendassignment='"+extendd+"', crname='"+crname+"' where assignment_id = '"+assignmentid+"'"

        print(query,flush=True)

        try:
            cur = db.session()
            if extendd == 'None':
                extendd = ''
            query = "update assignment_karyawan set status='"+status+"',dateassignment='"+startd+"',endassignment='"+endd+"', assignmenttype='"+typex+"',extendassignment='"+extendd+"', crname='"+crname+"' where assignment_id = '"+assignmentid+"'"
            resultproxy = cur.execute(query)

            print(query,flush=True)
            db.session.commit()

            db.session.close()

            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : 'Something Wrong' }

class KaryawanModelTrello(db.Model):
    __tablename__ = 'trello_karyawan'
    fullname = db.Column(db.String(150), primary_key = True)
    trelloid = db.Column(db.String(150))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class KaryawanModel(db.Model):
    __tablename__ = 'karyawan'
    user_id = db.Column(db.String(20), primary_key = True)
    fullname = db.Column(db.String(50), primary_key = True)
    statuspernikahan = db.Column(db.String(10), primary_key = True)
    nik = db.Column(db.String(18), primary_key = True)
    identitas = db.Column(db.String(4), primary_key = True)
    divisi = db.Column(db.String(6), primary_key = True)
    tanggalmasuk = db.Column(db.String(10), primary_key = True)
    statuskaryawan = db.Column(db.String(10), primary_key = True)
    email = db.Column(db.String(100), primary_key = True)
    phone = db.Column(db.String(20), primary_key = True)
    alamat = db.Column(db.String(300), primary_key = True)
    posisi = db.Column(db.String(10), primary_key = True)
    site = db.Column(db.String(10), primary_key = True)
    telegram = db.Column(db.String(50), primary_key = True)
    createdby = db.Column(db.String(25))
    createdate = db.Column(db.String(20))
    tempatlahir = db.Column(db.String(50))
    tanggallahir = db.Column(db.String(10))
    pendidikan = db.Column(db.String(50))
    institusi = db.Column(db.String(50))
    nikkaryawan = db.Column(db.String(20))
    jurusan = db.Column(db.String(100))
    resource = db.Column(db.String(5))

    @classmethod
    def loging(cls, username, desc):
        try:
            query = "INSERT INTO userlog (username, action, tanggal) values ('"+username+"','"+desc+"',CURRENT_TIMESTAMP());"
            cur = db.session()
            resultproxy = cur.execute(query)
            db.session.commit()
            
            return { 'Status' : 'OK' }
        except:
            return { 'Status' : 'Error - Reject data' }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, user_id):
        return cls.query.filter_by(user_id = user_id).first()

    @classmethod
    def find_by_userid(cls, user_id):
        cls.query.filter_by(user_id = user_id).first()
        def to_json(x):
            return {
                'user_id' : x.user_id,
                'fullname': x.fullname,
                'statuspernikahan' : x.statuspernikahan,
                'nik': x.nik,
                'identitas': x.identitas,
                'divisi': x.divisi,
                'tanggalmasuk': x.tanggalmasuk,
                'statuskaryawan': x.statuskaryawan,
                'email': x.email,
                'phone': x.phone,
                'alamat': x.alamat,
                'posisi': x.posisi
            }
        return {'karyawan': list(map(lambda x: to_json(x), KaryawanModel.query.filter_by(user_id = user_id)))}

    @classmethod
    def return_all(cls, user_role):
        cur = db.session()

        if(user_role == '6'):
            resultproxy = cur.execute("select user_id,a.fullname,statuspernikahan,nik,identitas,divisi,tanggalmasuk,statuskaryawan,email,phone, alamat, \
        posisi,resource,site,telegram,createdby,createdate,pendidikan,institusi,tempatlahir,tanggallahir,status,role_trello,nikkaryawan, \
        jurusan,trelloid, TIMESTAMPDIFF( YEAR, tanggalmasuk, now() ) year,TIMESTAMPDIFF( MONTH, tanggalmasuk, now() ) % 12 as month, \
        FLOOR( TIMESTAMPDIFF( DAY, tanggalmasuk, now() ) % 30.4375 ) as day \
        from karyawan a, trello_karyawan tk where a.fullname = tk.fullname and a.divisi in ('SDO') \
                and a.status = 'Active' ;")
        elif(user_role == '2'):
            resultproxy = cur.execute("select user_id,a.fullname,statuspernikahan,nik,identitas,divisi,tanggalmasuk,statuskaryawan,email,phone, alamat, \
        posisi,resource,site,telegram,createdby,createdate,pendidikan,institusi,tempatlahir,tanggallahir,status,role_trello,nikkaryawan, \
        jurusan,trelloid, TIMESTAMPDIFF( YEAR, tanggalmasuk, now() ) year,TIMESTAMPDIFF( MONTH, tanggalmasuk, now() ) % 12 as month, \
        FLOOR( TIMESTAMPDIFF( DAY, tanggalmasuk, now() ) % 30.4375 ) as day \
        from karyawan a, trello_karyawan tk where a.fullname = tk.fullname and a.divisi in ('PMO') \
                and a.status = 'Active' ;")
        else:
            resultproxy = cur.execute("select user_id,fullname, posisi, divisi \
                from karyawan \
                where status = 'Active' \
                and posisi != 'Support Surveillance' \
                order by karyawan.fullname asc;")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'karyawan': a }, 200

    @classmethod
    def return_allnofilter(cls):
        cur = db.session()

        resultproxy = cur.execute("select user_id,a.fullname,statuspernikahan,nik,identitas,divisi,tanggalmasuk,statuskaryawan,email,phone, alamat, \
        posisi,site,telegram,createdby,createdate,pendidikan,institusi,tempatlahir,tanggallahir,status,role_trello,nikkaryawan, \
        jurusan,trelloid, TIMESTAMPDIFF( YEAR, tanggalmasuk, now() ) year,TIMESTAMPDIFF( MONTH, tanggalmasuk, now() ) % 12 as month, \
        FLOOR( TIMESTAMPDIFF( DAY, tanggalmasuk, now() ) % 30.4375 ) as day \
        from karyawan a, trello_karyawan tk where a.fullname = tk.fullname  \
                and a.status = 'Active' ;")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'karyawan': a }, 200

    @classmethod
    def resign(cls, user_role):
        cur = db.session()

        if(user_role == '6'):
            resultproxy = cur.execute("select * from karyawan where status = 'InActive' and divisi = 'SDO';")
        elif(user_role == '2'):

            query = "select user_id,fullname,statuspernikahan,nik,identitas,divisi,tanggalmasuk, \
            statuskaryawan,email,phone, alamat, \
            posisi,site,telegram,createdby,createdate,pendidikan,institusi,tempatlahir,tanggallahir, \
            status,role_trello,nikkaryawan, \
            jurusan, TIMESTAMPDIFF( YEAR, tanggalmasuk, STR_TO_DATE(resigndate , '%Y-%m-%d') ) year, \
            TIMESTAMPDIFF( MONTH, tanggalmasuk, STR_TO_DATE(resigndate , '%Y-%m-%d') ) % 12 as month, \
            FLOOR( TIMESTAMPDIFF( DAY, tanggalmasuk, STR_TO_DATE(resigndate , '%Y-%m-%d') ) % 30.4375 ) as day \
            from karyawan where status = 'InActive' and divisi = 'PMO';"

            query = "select user_id,resigndate,fullname,divisi,tanggalmasuk, \
            statuskaryawan, r.handover,r.tanggalhandover , r.project , \
            posisi,site,telegram,r.createdby,k.createdate,pendidikan,institusi, \
            status,nikkaryawan, \
            jurusan, TIMESTAMPDIFF( YEAR, tanggalmasuk, STR_TO_DATE(resigndate , '%Y-%m-%d') ) year, \
            TIMESTAMPDIFF( MONTH, tanggalmasuk, STR_TO_DATE(resigndate , '%Y-%m-%d') ) % 12 as month, \
            FLOOR( TIMESTAMPDIFF( DAY, tanggalmasuk, STR_TO_DATE(resigndate , '%Y-%m-%d') ) % 30.4375 ) as day \
            from karyawan k, resignkaryawan r  where \
            k.user_id = r.userid \
            and status = 'InActive' and divisi = 'PMO';"

            resultproxy = cur.execute(query)
        else:
            resultproxy = cur.execute("select user_id,fullname, posisi, divisi \
                from karyawan \
                where status = 'Active' \
                and posisi != 'Support Surveillance' \
                order by karyawan.fullname asc;")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'karyawan': a }, 200

    @classmethod
    def return_covidlist(cls):
        cur = db.session()

        resultproxy = cur.execute("select user_id,fullname, posisi, divisi \
            from karyawan \
            where divisi in ('PMO','SDO','RMO','BSO') \
            and status = 'Active' \
            order by karyawan.fullname asc;")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'karyawan': a }, 200



class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    role = db.Column(db.String(10), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()


    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'email': x.email,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)


    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    @classmethod
    def get_role(cls, username):

        print('USERNAME : '+username,flush=True)

        query = "select role,username from users where username='"+username+"'"
        print(query,flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        e = {}
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
                e = value
            a.append(d)

        # if a is not nullable:
        print('USERNAME : '+str(e), flush=True)
        return d

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120))
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)


############### ROLE

class RoleModel(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key = True)
    role_name = db.Column(db.String(20))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select * from role")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Role': a }, 200

class KaryawanMutasiModel(db.Model):
    __tablename__ = 'mutasikaryawan'
    user_id = db.Column(db.String(50), primary_key = True)
    divisi = db.Column(db.String(5), primary_key = True)
    created_by = db.Column(db.String(50))
    created_date = db.Column(db.String(22))
    tanggalmutasi = db.Column(db.String(20))
    keterangan = db.Column(db.String(100))

    def save_to_db(self):
        print(self, flush=True)
        try:
            db.session.add(self)
            db.session.commit()

            db.session.close()

            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : 'Something Wrong' }

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select k.fullname,m.divisi,m.created_by,m.tanggalmutasi tanggalmutasi,k.tanggalmasuk,m.keterangan from karyawan k, mutasikaryawan m where k.user_id = m.user_id")

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Mutasi': a }, 200    

    @classmethod
    def updateDivisi(cls,user_id,divisi):
        print("update karyawan set divisi='"+divisi+"' where user_id = '"+user_id+"'", flush = True)
        try:
            cur = db.session()
            query = "update karyawan set divisi='"+divisi+"' where user_id = '"+user_id+"'"
            print('QUQUQUQU : '+query,flush=True)
            resultproxy = cur.execute(query)
            db.session.commit()

            db.session.close()

            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : ' GAGAGAGA Something Wrong' }


class KaryawanChallengeModel(db.Model):
    __tablename__ = 'challenge_karyawan'
    user_id = db.Column(db.String(50), primary_key = True)
    posisi = db.Column(db.String(50), primary_key = True)
    start = db.Column(db.String(22))
    end = db.Column(db.String(22))
    created_by = db.Column(db.String(50))
    created_date = db.Column(db.String(22))

    def save_to_db(self):
        print(self, flush=True)
        try:
            db.session.add(self)
            db.session.commit()
            db.session.close()

            return { 'Status': 'Success' }, 200
        except:
            return { 'Status' : 'Something Wrong' }

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select k.fullname,m.posisi,m.created_by,m.start,m.end,m.created_date from karyawan k, challenge_karyawan m where k.user_id = m.user_id")

        d, a = {}, []
        for rowproxy in resultproxy:
            for column, value in rowproxy.items():
                d = {**d, **{column: value}}
            a.append(d)

        return { 'Challenge': a }, 200    

class KaryawanSkillModel(db.Model):
    __tablename__ = 'skills'
    employee = db.Column(db.String(100), primary_key = True)
    skill = db.Column(db.String(1000), primary_key = True)
    created_by = db.Column(db.String(25), primary_key = True)
    # timenow = db.Column(db.String(25))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        cur = db.session()
        resultproxy = cur.execute("select s.employee, s.skill, s.created_by,s.timenow, k.user_id  from skills s,karyawan k \
where s.employee = k.fullname")

        d, a = {}, []
        for rowproxy in resultproxy:
            for column, value in rowproxy.items():
                d = {**d, **{column: value}}
            a.append(d)

        return { 'Skills': a }, 200 

    @classmethod
    def skillP(cls, user_id):
        cur = db.session()
        resultproxy = cur.execute("select s.employee, s.skill, s.created_by,s.timenow, k.user_id  from skills s,karyawan k \
where s.employee = k.fullname and k.user_id = '"+user_id+"'")

        d, a = {}, []
        for rowproxy in resultproxy:
            for column, value in rowproxy.items():
                d = {**d, **{column: value}}
            a.append(d)

        return { 'Karyawan': a }, 200

    @classmethod
    def skillUpdate(cls, fullname,skill):
        try:
            cur = db.session()
            query = "Update skills set skill = '"+skill+"' where employee = '"+fullname+"';"
            resultproxy = cur.execute(query)
            db.session.commit()
            db.session.close()

            return { 'Status': 'OK' }, 200
        except:
            return { 'Status' : 'Something Wrong' }


class KaryawanCutiModel(db.Model):
    __tablename__ = 'cutikaryawan'
    fullname = db.Column(db.String(50), primary_key = True)
    tanggal_cuti = db.Column(db.String(10), primary_key = True)
    keterangan = db.Column(db.String(50))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        cur = db.session()
        # resultproxy = cur.execute("select * from cutikaryawan where STR_TO_DATE(tanggal_cuti , '%Y-%m-%d') between CURDATE() - INTERVAL 10 DAY AND CURDATE()")
        resultproxy = cur.execute("select c.fullname, c.tanggal_cuti, c.keterangan, k.user_id   \
from cutikaryawan c, karyawan k where STR_TO_DATE(tanggal_cuti , '%Y-%m-%d') > CURDATE() - INTERVAL 30 DAY \
and k.fullname = c.fullname \
and k.divisi = 'PMO' \
order by tanggal_cuti desc;")
        

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Cuti': a }, 200        

    @classmethod
    def return_all_sdo(cls):
        cur = db.session()
        # resultproxy = cur.execute("select * from cutikaryawan where STR_TO_DATE(tanggal_cuti , '%Y-%m-%d') between CURDATE() - INTERVAL 10 DAY AND CURDATE()")
        resultproxy = cur.execute("select c.fullname, c.tanggal_cuti, c.keterangan, k.user_id   \
from cutikaryawan c, karyawan k where STR_TO_DATE(tanggal_cuti , '%Y-%m-%d') > CURDATE() - INTERVAL 30 DAY \
and k.fullname = c.fullname \
and k.divisi = 'SDO' \
order by tanggal_cuti desc;")
        

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Cuti': a }, 200     

    @classmethod
    def CutiDelete(cls,cutiid):
        try:
            ssplit = cutiid.split("_")
            karyawan = ssplit[0]
            tanggal = ssplit[1]

            cur = db.session()
            resultproxy = cur.execute("delete from cutikaryawan where fullname = '"+karyawan+"' and tanggal_cuti ='"+tanggal+"';")
            db.session.commit()
            db.session.close()
            return { 'Status' : 'Success' } 
        except:
            return { 'Status' : 'Failed' } 


class KaryawanCovidModel(db.Model):
    __tablename__ = 'karyawancovid'
    fullname = db.Column(db.String(50), primary_key = True)
    tanggal_update = db.Column(db.String(10), primary_key = True)
    keterangan = db.Column(db.String(50))
    status = db.Column(db.String(10))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        cur = db.session()
        # resultproxy = cur.execute("select * from cutikaryawan where STR_TO_DATE(tanggal_cuti , '%Y-%m-%d') between CURDATE() - INTERVAL 10 DAY AND CURDATE()")
        resultproxy = cur.execute("select fullname,keterangan,tanggal_update,konfirmasi,hari,status from (SELECT \
            p.fullname, \
            p.keterangan, \
            p.tanggal_update, \
            m.konfirmasi, \
            m.hari, \
            p.status \
            FROM \
            karyawancovid p INNER JOIN ( \
                SELECT \
                fullname, min(tanggal_update) as konfirmasi, \
                MAX(tanggal_update) AS max_date, \
                DATEDIFF(curdate(),min(tanggal_update)) as hari \
                FROM \
                karyawancovid \
                GROUP BY \
                fullname) m \
            ON p.fullname = m.fullname AND p.tanggal_update = m.max_date) a order by konfirmasi asc")
        
  
        
        
        # "select * from karyawancovid where STR_TO_DATE(tanggal_update , '%Y-%m-%d') > CURDATE() - INTERVAL 14 DAY order by tanggal_update desc")
        

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Covid': a }, 200        

class KaryawanAppraisalModel(db.Model):
    __tablename__ = 'appraisal_karyawan'
    appraisalid = db.Column(db.String(100), primary_key = True)
    user_id = db.Column(db.String(20), primary_key = True)
    performance = db.Column(db.String(3))
    potential = db.Column(db.String(3))
    attitude = db.Column(db.String(3))
    pm = db.Column(db.String(100), primary_key = True)
    periode = db.Column(db.String(18), primary_key = True)
    createdate = db.Column(db.String(20))
    

    @classmethod
    def loging(cls, username, desc):
        try:
            query = "INSERT INTO userlog (username, action, tanggal) values ('"+username+"','"+desc+"',CURRENT_TIMESTAMP());"
            cur = db.session()
            resultproxy = cur.execute(query)
            db.session.commit()
            
            return { 'Status' : 'OK' }
        except:
            return { 'Status' : 'Error - Reject data' }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def getdetail(cls,appraisalid):
        cur = db.session()
        # resultproxy = cur.execute("select * from cutikaryawan where STR_TO_DATE(tanggal_cuti , '%Y-%m-%d') between CURDATE() - INTERVAL 10 DAY AND CURDATE()")
        resultproxy = cur.execute("select k.fullname, k.posisi, k.divisi, ak.appraisalid, ak.performance,ak.potential, ak.attitude, \
ak.periode,ak.createdate from appraisal_karyawan ak, karyawan k \
where ak.appraisalid = '"+appraisalid+"' \
and ak.user_id = k.user_id;")
        

        d, a = {}, []
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            a.append(d)

        # if a is not nullable:
        return { 'Appraisal': a }, 200   

    @classmethod
    def deleteAppraisal(cls,appraisalid):
        
        query = "delete from appraisal_karyawan where appraisalid = '"+appraisalid+"';"

        try:

            cur = db.session()
            resultproxy = cur.execute(query)
            db.session.commit()
            db.session.close()
            
            return { 'Status' : 'Success' } 
        except:
            return { 'Status' : 'Failed' } 



class RUserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    role = db.Column(db.String(10), nullable = False)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()


    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'email': x.email,
                'password': x.password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)


    @staticmethod
    def verify_hash(password, hash):
        # print(password,flush=True)
        
        stored_password = hash.decode('ascii')
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                    password.encode('utf-8'), 
                                    salt.encode('ascii'), 
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

        # return sha256.verify(password, hash)

    @classmethod
    def get_role(cls, username):

        print('USERNAME : '+username,flush=True)

        query = "select role,username from users where username='"+username+"'"
        print(query,flush=True)

        cur = db.session()
        resultproxy = cur.execute(query)
        d, a = {}, []
        e = {}
        for rowproxy in resultproxy:
            # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in rowproxy.items():
                # build up the dictionary
                d = {**d, **{column: value}}
                e = value
            a.append(d)

        # if a is not nullable:
        print('USERNAME : '+str(e), flush=True)
        return d
