from flask_restful import Resource, reqparse
from models import KaryawanModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import KaryawanModel,KaryawanAppraisalModel,KaryawanModelTrello, RevokedTokenModel,KaryawanShiftModel,KaryawanAssignmentModel, UserModel, Assignment, KaryawanU, KaryawanCutiModel, KaryawanCovidModel, KaryawanAssignment, KaryawanMutasiModel, KaryawanChallengeModel, KaryawanSkillModel
from flask import json
import logging
import hashlib
from datetime import datetime
from flask import Flask
from flask_mail import Mail, Message
import os
import email_kirim
from flask_cors import CORS
import secrets
import time
# import mail

# app = Flask(__name__)


parser = reqparse.RequestParser()

# # parser.add_argument('email')
# parser.add_argument('password')

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


def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature


class KaryawanCuti(Resource):
    def post(self):
        parser.add_argument('resource_name')
        parser.add_argument('tanggal')
        parser.add_argument('keterangan')
        data = parser.parse_args()

        print(data['resource_name'], flush=True)
        print(data['tanggal'], flush=True)
        print(data['keterangan'], flush=True)

        addkaryawanCuti = KaryawanCutiModel( fullname = data['resource_name'], tanggal_cuti = data['tanggal'], keterangan = data['keterangan'] )
        # if KaryawanModel.find_by_userid(data['user_id']):
        try:
            addkaryawanCuti.save_to_db()
            return {
                'message': 'User {} was created'.format(data['resource_name']),
                'STATUS' : 'SUCCESS'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }            
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500

class KaryawanMutasi(Resource):
    def post(self):
        parser.add_argument('karyawan')
        parser.add_argument('divisi')
        parser.add_argument('createdby')
        parser.add_argument('tanggalmutasi')
        parser.add_argument('ket')
        now = datetime.now()
        datenow = datetime.now()
        createddate = now.strftime("%Y-%m-%d %H:%M:%S")
        data = parser.parse_args()

        print('DIVISI ' +data['divisi'], flush=True)
        addkaryawanMutasi = KaryawanMutasiModel( user_id = data['karyawan'], divisi = data['divisi'], created_by = data['createdby'], created_date = createddate, tanggalmutasi = data['tanggalmutasi'], keterangan = data['ket']  )
        # if KaryawanModel.find_by_userid(data['user_id']):
        try:
            addkaryawanMutasi.save_to_db()
            print(data['karyawan'], flush=True)
            print("KESINI SAMPE?", flush=True)

            KaryawanMutasiModel.updateDivisi(data['karyawan'],data['divisi'])
            return {
                'message': 'Berhasil menambah daftar mutasi karyawan {} '.format(data['karyawan']),
                'STATUS' : 'SUCCESS'
                }            
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': ' INI YA? Gagal Ditambahkan'}, 500


class AddChallenge(Resource):
    def post(self):
        parser.add_argument('karyawan')
        parser.add_argument('posisi')
        parser.add_argument('createdby')
        parser.add_argument('start')
        parser.add_argument('end')
        now = datetime.now()
        datenow = datetime.now()
        createddate = now.strftime("%Y-%m-%d %H:%M:%S")
        data = parser.parse_args()

        addkaryawanChallenge = KaryawanChallengeModel( user_id = data['karyawan'], posisi = data['posisi'], start = data['start'], end = data['end'] ,created_by = data['createdby'], created_date = createddate  )
        # if KaryawanModel.find_by_userid(data['user_id']):
        try:
            addkaryawanChallenge.save_to_db()
            return {
                'message': 'Berhasil menambah daftar mutasi karyawan {} '.format(data['karyawan']),
                'STATUS' : 'SUCCESS'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }            
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500


class KaryawanCovid(Resource):
    def post(self):
        parser.add_argument('resource_name')
        parser.add_argument('tanggal')
        parser.add_argument('keterangan')
        parser.add_argument('status')
        data = parser.parse_args()

        print(data['resource_name'], flush=True)
        print(data['tanggal'], flush=True)
        print(data['keterangan'], flush=True)
        print(data['status'], flush=True)

        addkaryawanCovid = KaryawanCovidModel( fullname = data['resource_name'], tanggal_update = data['tanggal'], keterangan = data['keterangan'], status = data['status'] )
        # if KaryawanModel.find_by_userid(data['user_id']):
        try:
            addkaryawanCovid.save_to_db()
            return {
                'message': 'User {} was created'.format(data['resource_name']),
                'STATUS' : 'SUCCESS'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }            
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500

class AddKaryawan(Resource):
    def post(self):
        parser.add_argument('user_id')
        parser.add_argument('fullname')
        parser.add_argument('statuspernikahan')
        parser.add_argument('nik')
        parser.add_argument('identitas')
        parser.add_argument('divisi')
        parser.add_argument('tanggalmasuk')
        parser.add_argument('statuskaryawan')
        parser.add_argument('email')
        parser.add_argument('phone')
        parser.add_argument('alamat')
        parser.add_argument('posisi')
        parser.add_argument('site')
        parser.add_argument('telegram')
        parser.add_argument('createdby')
        parser.add_argument('pendidikan')
        parser.add_argument('institusi')
        parser.add_argument('nikkaryawan')
        parser.add_argument('jurusan')
        parser.add_argument('tempatlahir')
        parser.add_argument('tanggallahir')
        data = parser.parse_args()
        

        now = datetime.now()
        sysdatex = now.strftime("%Y-%m-%d %H:%M:%S")


        if KaryawanModel.find_by_username(data['user_id']):
            return {'message': 'User {} already exists'.format(data['user_id'])}, 500
        
        addkaryawan = KaryawanModel(
            user_id = data['user_id'],
            fullname = data['fullname'],
            statuspernikahan = data['statuspernikahan'],
            nik = data['nik'],
            identitas = data['identitas'],
            divisi = data['divisi'],
            tanggalmasuk = data['tanggalmasuk'],
            statuskaryawan = data['statuskaryawan'],
            email = data['email'],
            phone = data['phone'],
            alamat = data['alamat'],
            posisi = data['posisi'],
            site = data['site'],
            telegram = data['telegram'],
            createdby = data['createdby'],
            createdate = sysdatex,
            tempatlahir = data['tempatlahir'],
            tanggallahir = data['tanggallahir'],
            pendidikan = data['pendidikan'],
            institusi = data['institusi'],
            nikkaryawan = data['nikkaryawan'],
            jurusan = data['jurusan']
        )

        addtrellokaryawan = KaryawanModelTrello(
            fullname = data['fullname'],
            trelloid = 'trelloid'
        )

        try:

            addkaryawan.save_to_db()
            addtrellokaryawan.save_to_db()
            # new_user.save_to_db()
            access_token = create_access_token(identity = data['user_id'])
            refresh_token = create_refresh_token(identity = data['user_id'])
            # access_token = create_access_token(identity = data['username'])
            # refresh_token = create_refresh_token(identity = data['username'])

            return {
                'message': 'User {} was created'.format(data['user_id']),
                'STATUS' : 'SUCCESS'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500


class AddShiftKaryawan(Resource):
    def post(self):
        parser.add_argument('user_id')
        parser.add_argument('startdate', help = 'This field cannot be blank')
        parser.add_argument('enddate', help = 'This field cannot be blank')
        parser.add_argument('shifttype', help = 'This field cannot be blank')
        data = parser.parse_args()
        
        addshift = KaryawanShiftModel(
            user_id = data['user_id'],
            startdate = data['startdate'],
            enddate = data['enddate'],
            shifttype = data['shifttype']
            #username = data['username'],
            #email = data['email'],
            #password = UserModel.generate_hash(data['password'])
        )

        print(addshift, flush=True)
        try:

            addshift.save_to_db()
            # access_token = create_access_token(identity = data['username'])
            # refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['user_id']),
                'STATUS' : 'Success Add Shift'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500

class Karyawan(Resource):
    def get(self):
        parser.add_argument('user_id')
        data = parser.parse_args()
        
        # if KaryawanModel.find_by_userid(data['user_id']):
        return KaryawanU.getuserid(data['user_id'])
        

        # print(addkaryawan, flush=True)
        # try:

        #     addkaryawan.save_to_db()
        #     # access_token = create_access_token(identity = data['username'])
        #     # refresh_token = create_refresh_token(identity = data['username'])
        #     return {
        #         'message': 'User {} was created'.format(data['user_id']),
        #         'STATUS' : 'SUCCESS'
        #         # 'token': access_token,
        #         # 'refresh_token': refresh_token
        #         }
        # except (ValueError, KeyError, TypeError) as error:
        #     print(error, flush=True)
        #     return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500





class ListKaryawan(Resource):
    def get(self):
        parser.add_argument('user_role')
        data = parser.parse_args()
        return KaryawanModel.return_all(data['user_role'])

class ListKaryawanAll(Resource):
    def get(self):
        return KaryawanModel.return_allnofilter()

class ListKaryawanResign(Resource):
    def get(self):
        parser.add_argument('user_role')
        data = parser.parse_args()
        return KaryawanModel.resign(data['user_role'])

class ListKaryawanUCovid(Resource):
    def get(self):
        return KaryawanModel.return_covidlist()

class ShiftKaryawan(Resource):
    def get(self):
        return KaryawanShiftModel.return_all()

class Skills(Resource):
    def get(self):
        return KaryawanSkillModel.return_all()

class Skill(Resource):
    def get(self):
        parser.add_argument('user_id')
        data = parser.parse_args()
        return KaryawanSkillModel.skillP(data['user_id'])

class SkillUpdate(Resource):
    def post(self):
        parser.add_argument('fullname')
        parser.add_argument('skill')
        data = parser.parse_args()
        return KaryawanSkillModel.skillUpdate(data['fullname'],data['skill'])
        
class BayaranShift(Resource):
    def get(self):
        return KaryawanShiftModel.bayaran_shift()

class ListSupervisor(Resource):
    def get(self):
        return KaryawanShiftModel.list_supervisor()

class DetailAssignment(Resource):
    def get(self):
        parser.add_argument('assignment_id')
        data = parser.parse_args()
        return KaryawanAssignmentModel.return_detail(data['assignment_id'])

class DeleteAssignment(Resource):
    def get(self):
        parser.add_argument('assignment_id')
        data = parser.parse_args()
        return KaryawanAssignmentModel.deleteAssignment(data['assignment_id'])

class AddAssignment(Resource):
    def post(self):
        time.sleep(1)
        parser.add_argument('karyawan', help = 'This field cannot be blank')
        parser.add_argument('board', help = 'This field cannot be blank')
        parser.add_argument('pm', help = 'This field cannot be blank')
        parser.add_argument('assignmenttype', help = 'This field cannot be blank')
        parser.add_argument('dateassignment', help = 'This field cannot be blank')
        parser.add_argument('endassignment', help = 'This field cannot be blank')


        data = parser.parse_args()

        now = datetime.now()
        date_time = now.strftime("%m%d%Y%H:%M:%S")
        sysdatex = now.strftime("%Y-%m-%d %H:%M:%S")
        print(sysdatex,flush=True)
        # print(sha_signature)

        # return { 'message': aa }, 200

        addAssignment = KaryawanAssignmentModel(
            user_id = data['user_id'],
            tanggal = data['tanggal'],
            starttime = data['startt'],
            endtime = data['endt'],
            detail = data['detail'],
            reff = data['reff'],
            status = data['status'],
            applicationname = data['applicationname'],
            assignmenttype = data['assignmenttype'],
            dateassignment = data['dateassignment'],
            supervisor = data['supervisor'],
            site = data['site'],
            onsite = data['onsite'],
            approval = 'PENDING',
            id_assignment = hash_string.replace("-","").replace(" ",""),
            timenow = sysdatex
            #username = data['username'],
            #email = data['email'],
            #password = UserModel.generate_hash(data['password'])
        )

        try:

            addAssignment.save_to_db()


            # access_token = create_access_token(identity = data['username'])
            # refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Assignment {} was created'.format(data['user_id']),
                'STATUS' : 'Success Add Shift'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }
        except:
            print('error', flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500

class AddAssignmentKaryawan(Resource):
    def post(self):
        time.sleep(1)
        parser.add_argument('karyawan', help = 'This field cannot be blank')
        parser.add_argument('board', help = 'This field cannot be blank')
        parser.add_argument('pm', help = 'This field cannot be blank')
        parser.add_argument('assignmenttype', help = 'This field cannot be blank')
        parser.add_argument('dateassignment', help = 'This field cannot be blank')
        parser.add_argument('endassignment', help = 'This field cannot be blank')
        parser.add_argument('crname')
        parser.add_argument('created_by', help = 'This field cannot be blank')
        data = parser.parse_args()


        now = datetime.now()
        assignment_id_tmp = secrets.token_hex(20)
        date_time = now.strftime("%m%d%Y%H:%M:%S")
        sysdatex = now.strftime("%Y-%m-%d %H:%M:%S")

        # print(sha_signature)

        # return { 'message': aa }, 200

        addAssignment = KaryawanAssignment(
            assignment_id = assignment_id_tmp,
            user_id = data['karyawan'],
            board = data['board'],
            pm = data['pm'],
            assignmenttype = data['assignmenttype'],
            dateassignment = data['dateassignment'],
            endassignment = data['endassignment'],
            crname = data['crname'],
            created_by = data['created_by'],
            timenow = sysdatex
        )

        try:

            addAssignment.save_to_db()


            # access_token = create_access_token(identity = data['username'])
            # refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Assignment was created',
                'STATUS' : 'Success'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }, 200
        except Exception as e:
            print('ERROR APA SIH?', flush=True)
            print(e, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'ERROR'}, 500

class assignmentupdate(Resource):
    def post(self):
        parser.add_argument('assignmentid')
        parser.add_argument('startd')
        parser.add_argument('endd')
        parser.add_argument('typex')
        parser.add_argument('status')
        parser.add_argument('extendd')
        parser.add_argument('crname')
        data = parser.parse_args()

        return KaryawanAssignment.assignmentupdate(data['assignmentid'],data['startd'],data['endd'],data['typex'],data['status'],data['extendd'],data['crname'])


class ListAssignment(Resource):
    def get(self):
        return KaryawanAssignment.return_all()

class ListKaryawanCuti(Resource):
    def get(self):
        return KaryawanCutiModel.return_all()

class CutiDelete(Resource):
    def get(self):
        parser.add_argument('cutiid')
        data = parser.parse_args()
        return KaryawanCutiModel.CutiDelete(data['cutiid'])

class ListKaryawanMutasi(Resource):
    def get(self):
        return KaryawanMutasiModel.return_all()

class ListChallenge(Resource):
    def get(self):
        return KaryawanChallengeModel.return_all()

class ListKaryawanCutiSDO(Resource):
    def get(self):
        return KaryawanCutiModel.return_all_sdo()

class ListKaryawanCovid(Resource):
    def get(self):
        return KaryawanCovidModel.return_all()

class resignK(Resource):
    def post(self):
        parser.add_argument('username')
        data = parser.parse_args()

        return KaryawanU.resignK(data['username'])

class addresign(Resource):
    def post(self):
        parser.add_argument('createdby')
        parser.add_argument('karyawan')
        parser.add_argument('tanggal')
        parser.add_argument('handover')
        parser.add_argument('ket')
        parser.add_argument('ket2')
        data = parser.parse_args()

        return KaryawanU.addresign(data['createdby'],data['karyawan'],data['tanggal'],data['handover'],data['ket'],data['ket2'])

class loging(Resource):
    def post(self):
        parser.add_argument('username')
        parser.add_argument('desc')
        data = parser.parse_args()
        return KaryawanModel.loging(data['username'],data['desc'])

class updateK(Resource):
    def post(self):
        parser.add_argument('username')
        parser.add_argument('email')
        parser.add_argument('fullname')
        parser.add_argument('telegram')
        parser.add_argument('divisi')
        parser.add_argument('posisi')
        parser.add_argument('alamat')
        parser.add_argument('telepon')
        parser.add_argument('tanggalmasuk')
        parser.add_argument('statuskaryawan')
        parser.add_argument('identitas')
        parser.add_argument('noidentitas')
        parser.add_argument('statuspernikahan')
        parser.add_argument('id_assignment')
        parser.add_argument('pendidikan')
        parser.add_argument('trelloid')
        parser.add_argument('institusi')
        parser.add_argument('nikkaryawan')
        parser.add_argument('jurusan')
        parser.add_argument('resource')
        data = parser.parse_args()
        
        # if KaryawanModel.find_by_userid(data['user_id']):
        return KaryawanU.updateK(data['username'],data['email'],data['fullname'],data['telegram'],data['divisi'],data['posisi'],data['alamat'],data['telepon'],data['tanggalmasuk'],data['statuskaryawan'],data['identitas'],data['statuspernikahan'], data['pendidikan'], data['trelloid'], data['institusi'], data['nikkaryawan'], data['jurusan'], data['resource'])


class ApproveAssignment(Resource):
    def post(self):
        parser.add_argument('id_assignment')
        data = parser.parse_args()
        
        # if KaryawanModel.find_by_userid(data['user_id']):
        return KaryawanAssignmentModel.approveAssignment(data['id_assignment'])

class HistoryAssignment(Resource):
    def get(self):
        return KaryawanAssignmentModel.return_done()

class AssignmentUser(Resource):
    def get(self):
        parser.add_argument('id_assignment')
        data = parser.parse_args()
        
        # if KaryawanModel.find_by_userid(data['user_id']):
        return Assignment.find_by_id_assignment(data['id_assignment'])

class AssignmentReportKaryawan(Resource):
    def get(self):        
        # if KaryawanModel.find_by_userid(data['user_id']):
        now = datetime.now()
        monthday = now.strftime("%Y-%m")
        print(monthday, flush=True)
        return Assignment.getall()

# class AssignmentReport(Resource):
#     def post(self):
#         parser.add_argument('startdate', help = 'This field cannot be blank')
#         parser.add_argument('enddate', help = 'This field cannot be blank')
#         data = parser.parse_args()
#         startdate = data['startdate']
#         enddate = data['enddate']

#         # if KaryawanModel.find_by_userid(data['user_id']):
#         # now = datetime.now()
#         # monthday = now.strftime("%Y-%m")
#         # print(monthday, flush=True)
#         return Assignment.find_pars_monthly(startdate,enddate)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}
        
        new_user = UserModel(
            username = data['username'],
            email = data['email'],
            password = UserModel.generate_hash(data['password'])
        )

        print(new_user)

        
        try:

            new_user.save_to_db()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'token': access_token,
                'refresh_token': refresh_token
                }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return { 'token': access_token }
                # 'refresh_token': refresh_token
                
        else:
            return {'message': 'Wrong credentials'}
      
      

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
      
      
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
      
      
class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()
    
    def delete(self):
        return UserModel.delete_all()
      

class User(Resource):
    def get(self):
        return UserModel.return_all()
      
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'username': 'cshutoff'
        }

class cobaEmail(Resource):
    def get(self):
        # if __name__ == '__main__':
        #     with app.app_context():
        parser.add_argument('tanggal', help = 'This field cannot be blank')
        parser.add_argument('user_id', help = 'This field cannot be blank')
        parser.add_argument('time', help = 'This field cannot be blank')
        parser.add_argument('detail', help = 'This field cannot be blank')
        parser.add_argument('reff', help = 'This field cannot be blank')
        parser.add_argument('status', help = 'This field cannot be blank')
        parser.add_argument('applicationname', help = 'This field cannot be blank')
        parser.add_argument('assignmenttype', help = 'This field cannot be blank')
        parser.add_argument('dateassignment', help = 'This field cannot be blank')
        parser.add_argument('site', help = 'This field cannot be blank')
        parser.add_argument('onsite', help = 'This field cannot be blank')
        parser.add_argument('supervisor', help = 'This field cannot be blank')
        
        data = parser.parse_args()

        email_kirim.sendM(data)
        return { 'Status' : 'OK'}

class sendEmail(Resource):
    def post(self):
        # parser.add_argument('tanggal', help = 'This field cannot be blank')
        parser.add_argument('user_id', help = 'This field cannot be blank')
        parser.add_argument('applicationname', help = 'This field cannot be blank')
        parser.add_argument('assignmenttype', help = 'This field cannot be blank')
        parser.add_argument('dateassignment', help = 'This field cannot be blank')
        # parser.add_argument('site', help = 'This field cannot be blank')
        # parser.add_argument('onsite', help = 'This field cannot be blank')
        parser.add_argument('supervisor', help = 'This field cannot be blank')

        data = parser.parse_args()
        hash_string = str(data['user_id'])+'_'+str(data['applicationname'])+'_'+str(data['dateassignment'])+'_'+str(data['supervisor'])+'_'+str(data['assignmenttype'])
        hash_string = hash_string.replace("-","").replace(" ","")
        # print(hash_string, flush=True)
        find_by_id_assignment = KaryawanAssignmentModel.email_data(hash_string)
        email_address = KaryawanAssignmentModel.email_address(hash_string)

        print('email_address')
        print(email_address[0]['email'])
        # print(find_by_id_assignment[1], flush = True)
        # print(str(len(find_by_id_assignment)), flush=True)
        fullname = KaryawanAssignmentModel.getfullname(str(data['user_id']))[0]
        # print(fullname,flush=True)
        # a = []
        data.update(fullname)
        # data.update(email_address[0])
        email_kirim.sendM(find_by_id_assignment,data,email_address[0]['email'])
        # a.append(fullname)
        # print(data, flush=True)
        # return KaryawanAssignmentModel.find_by_id_assignment(hash_string), 200
        return { 'OK' : 'Robot' }

class userReg(Resource):
    def post(self):
        # parser.add_argument('tanggal', help = 'This field cannot be blank')
        parser.add_argument('user_id')
        parser.add_argument('password')
        parser.add_argument('fullname')
        parser.add_argument('email')

        data = parser.parse_args()
        
        email_kirim.userReg(data)
        # a.append(fullname)
        # print(data, flush=True)
        # return KaryawanAssignmentModel.find_by_id_assignment(hash_string), 200
        return { 'OK' : 'Robot' }

class AddSkills(Resource):
    def post(self):
        parser.add_argument('karyawan')
        parser.add_argument('skills')
        parser.add_argument('createdby')
        data = parser.parse_args()

        print(data['karyawan'], flush=True)
        print(data['skills'], flush=True)
        print(data['createdby'], flush=True)

        # addkaryawanCuti = KaryawanCutiModel( fullname = data['resource_name'], tanggal_cuti = data['tanggal'], keterangan = data['keterangan'] )
        addSkills = KaryawanSkillModel( employee = data['karyawan'], skill = data['skills'], created_by = data['createdby'] )
        # if KaryawanModel.find_by_userid(data['user_id']):
        try:
            addSkills.save_to_db()
            return {
                'message': 'User {} was created'.format(data['resource_name']),
                'STATUS' : 'SUCCESS'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }            
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500


class AddKaryawanAppraisal(Resource):
    def post(self):
        parser.add_argument('user_id')
        parser.add_argument('performance')
        parser.add_argument('potential')
        parser.add_argument('attitude')
        parser.add_argument('pm')
        parser.add_argument('periode')
        data = parser.parse_args()
        
        appraisalid = data['user_id']+data['pm']+data['periode']

        now = datetime.now()
        sysdatex = now.strftime("%Y-%m-%d %H:%M:%S")
        
        addkaryawanappraisal = KaryawanAppraisalModel(
            appraisalid = appraisalid.replace(" ","").replace(".","").replace("-",""),
            user_id = data['user_id'],
            performance = data['performance'],
            potential = data['potential'],
            attitude = data['attitude'],
            pm = data['pm'],
            periode = data['periode'],
            createdate = sysdatex
        )


        try:

            addkaryawanappraisal.save_to_db()

            return {
                'message': 'User {} appraisal was created'.format(data['user_id']),
                'STATUS' : 'SUCCESS'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500

class AppraisalDetail(Resource):
    def get(self):
        parser.add_argument('appraisalid')
        data = parser.parse_args()
        return KaryawanAppraisalModel.getdetail(data['appraisalid'])

class AppraisalDelete(Resource):
    def post(self):
        parser.add_argument('appraisalid')
        data = parser.parse_args()
        return KaryawanAppraisalModel.deleteAppraisal(data['appraisalid'])
        