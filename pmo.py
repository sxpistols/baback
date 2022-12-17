from flask_restful import Resource, reqparse
from models import KaryawanModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import KaryawanModel, RevokedTokenModel,KaryawanShiftModel,KaryawanAssignmentModel, UserModel, Assignment, KaryawanU, RoleModel
from models_pmo import ClientModel, Project, karyawanPMO, ProjectState, ProjectSetting, Appraisal
from flask import json
import logging
import hashlib
from datetime import datetime
from flask import Flask
from flask_mail import Mail, Message
import os
import email_kirim
from flask_cors import CORS

import time


parser = reqparse.RequestParser()

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

class addclient(Resource):
    def post(self):
        parser.add_argument('nama')
        parser.add_argument('alamat')
        parser.add_argument('createdby')

        data = parser.parse_args()


        now = datetime.now()
        sysdatex = now.strftime("%Y-%m-%d %H:%M:%S")


        if ClientModel.find_by_name(data['nama']):
            return {'message': 'Client {} already exists'.format(data['nama'])}, 500

        addclient = ClientModel(
            nama = data['nama'],
            alamat = data['alamat'],
            createdby = data['createdby'],
            createdate = sysdatex
            )

        try:

            addclient.save_to_db()
            # new_user.save_to_db()
            return {
                'message': 'Client {} was created'.format(data['nama']),
                'STATUS' : 'SUCCESS'
                # 'token': access_token,
                # 'refresh_token': refresh_token
            }
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500

class karyawanpmo(Resource):
    def get(self):
        return karyawanPMO.return_all()

class getClient(Resource):
    def get(self):
        return ClientModel.return_all()

class getPM(Resource):
    def get(self):
        return karyawanPMO.find_pm()

class getSA(Resource):
    def get(self):
        return karyawanPMO.find_sa()

class getDev(Resource):
    def get(self):
        return karyawanPMO.find_dev()

class getQC(Resource):
    def get(self):
        return karyawanPMO.find_qc()

class getTW(Resource):
    def get(self):
        return karyawanPMO.find_tw()

class getPA(Resource):
    def get(self):
        return karyawanPMO.find_pa()


class getProject(Resource):
    def get(self):
        return Project.return_all()

class getProjectHist(Resource):
    def get(self):
        return Project.return_all_hist()

class detailProject(Resource):
    def get(self):
        parser.add_argument('id_project')
        data = parser.parse_args()

        return Project.project_detail(data['id_project'])

class projectPM(Resource):
    def get(self):
        parser.add_argument('id_project')
        data = parser.parse_args()

        return Project.project_pm(data['id_project'])

class projectSA(Resource):
    def get(self):
        parser.add_argument('id_project')
        data = parser.parse_args()

        return Project.project_sa(data['id_project'])

class projectDev(Resource):
    def get(self):
        parser.add_argument('id_project')
        data = parser.parse_args()

        return Project.project_dev(data['id_project'])

class projectPA(Resource):
    def get(self):
        parser.add_argument('id_project')
        data = parser.parse_args()

        return Project.project_pa(data['id_project'])

class projectQC(Resource):
    def get(self):
        parser.add_argument('id_project')
        data = parser.parse_args()

        return Project.project_qc(data['id_project'])

class projectTW(Resource):
    def get(self):
        parser.add_argument('id_project')
        data = parser.parse_args()

        return Project.project_tw(data['id_project'])

class projectClose(Resource):
    def post(self):
        parser.add_argument('id_project')
        data = parser.parse_args()

        return Project.project_close(data['id_project'])

class summary(Resource):
    def get(self):
        parser.add_argument('user_role')
        data = parser.parse_args()
        return Project.summary(data['user_role'])

class resourcemandays(Resource):
    def get(self):
        parser.add_argument('user_role')
        parser.add_argument('tahun')
        data = parser.parse_args()
        return Project.resourcemandays(data['user_role'],data['tahun'])

class mandaysProjectFin(Resource):
    def get(self):
        parser.add_argument('user_role')
        parser.add_argument('tahun')
        parser.add_argument('bulan')
        parser.add_argument('board')
        data = parser.parse_args()
        return Project.mandaysProjectFin(data['user_role'],data['tahun'],data['bulan'],data['board'])

class resourcedetailmandays(Resource):
    def get(self):
        parser.add_argument('fullname')
        parser.add_argument('start')
        parser.add_argument('end')
        data = parser.parse_args()
        return Project.resourcedetailmandays(data['fullname'], data['start'], data['end'])
#
class resource_summary(Resource):
    def get(self):
        return Project.resource_summary()

class dashboard_summary(Resource):
    def get(self):
        return Project.dashboard_summary()

class dashboard_pmo(Resource):
    def get(self):
        return Project.dashboard_pmo()

class dashboard_pmopercent(Resource):
    def get(self):
        return Project.dashboard_pmopercent()

class dashboard_pmochart(Resource):
    def get(self):
        return Project.dashboard_pmochart()

class dashboard_pmosharing(Resource):
    def get(self):
        return Project.dashboard_pmosharing()

class dashboard_sdodipmo(Resource):
    def get(self):
        return Project.dashboard_sdodipmo()

class dashboard_pmosdoother(Resource):
    def get(self):
        return Project.dashboard_pmosdoother()

class dashboard_pmoforsdo(Resource):
    def get(self):
        return Project.dashboard_pmoforsdo()

class dashboard_pmoposisi(Resource):
    def get(self):
        return Project.dashboard_pmoposisi()

class dashboard_pmostatusk(Resource):
    def get(self):
        return Project.dashboard_pmostatusk()

class dashboard_sdo(Resource):
    def get(self):
        return Project.dashboard_sdo()

class dashboard_qc(Resource):
    def get(self):
        return Project.dashboard_qc()

class setmandays(Resource):
    def post(self):
        parser.add_argument('jumlah')
        parser.add_argument('boardid')
        parser.add_argument('createdby')
        data = parser.parse_args()
        return Project.setmandays(data['jumlah'],data['boardid'],data['createdby'])

class resourceactive(Resource):
    def get(self):
        return Project.resourceactive()

class resourceidle(Resource):
    def get(self):
        
        return Project.resourceidle()

class resourceidledaily(Resource):
    def get(self):
        parser.add_argument('tanggal')
        data = parser.parse_args()

        return Project.resourceidledaily(data['tanggal'])

class resourceidledailyD(Resource):
    def get(self):
        parser.add_argument('tanggal')
        data = parser.parse_args()

        return Project.resourceidledailyD(data['tanggal'])        

class delResourceproject(Resource):
    def post(self):
        parser.add_argument('id_project')
        parser.add_argument('resource_name')
        data = parser.parse_args()

        return Project.delResource(data['id_project'],data['resource_name'])


class updateTanggal(Resource):
    def post(self):
        parser.add_argument('id_project')
        parser.add_argument('selesai')
        data = parser.parse_args()

        return Project.updateTanggal(data['id_project'],data['selesai'])




class settingproject(Resource):
    def post(self):
        parser.add_argument('board')
        parser.add_argument('pm')
        parser.add_argument('client')
        parser.add_argument('projecttype')
        parser.add_argument('nilai_project')
        parser.add_argument('mandays')
        parser.add_argument('dateassignment')
        parser.add_argument('endassignment')
        parser.add_argument('projectdiv')
        parser.add_argument('created_by')
        data = parser.parse_args()
        parser.add_argument('noproject')
        parser.add_argument('namaproject')
        parser.add_argument('no_po')
        parser.add_argument('nama_po')
        parser.add_argument('invoice1')
        parser.add_argument('invoice2')

        now = datetime.now()
        date_time = now.strftime("%m%d%Y%H:%M:%S")
        timenow = now.strftime("%Y-%m-%d %H:%M:%S")

        addProjectSetting = ProjectSetting(
            board = data['board'],
            pm = data['pm'],
            client = data['client'],
            project_type = data['projecttype'],
            nilai_project = data['nilai_project'],
            mandays = data['mandays'],
            start_date = data['dateassignment'],
            end_date = data['endassignment'],
            projectdiv = data['projectdiv'],
            created_by = data['created_by'],
            timenow = timenow,
            noproject = data['noproject'],
            namaproject = data['namaproject'],
            no_po = data['no_po'],
            nama_po = data['nama_po'],
            invoice1 = data['invoice1'],
            invoice2 = data['invoice2']
        )

        try:

            addProjectSetting.save_to_db()


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


class addProject(Resource):
    def post(self):
        parser.add_argument('project')
        parser.add_argument('client')
        parser.add_argument('po')
        parser.add_argument('cr')
        parser.add_argument('jenispekerjaan')
        parser.add_argument('mulai')
        parser.add_argument('selesai')
        parser.add_argument('posisi')
        parser.add_argument('resource_name')
        parser.add_argument('createdby')
        data = parser.parse_args()
        now = datetime.now()
        sysdatex = now.strftime("%Y-%m-%d %H:%M:%S")

        hash_string = data['project']+'_'+data['client']


        addproject = Project(
            id_project = hash_string.replace("-","").replace(" ",""),
            project = data['project'],
            client = data['client'],
            po_name = data['po'],
            cr_name = data['cr'],
            jenis = data['jenispekerjaan'],
            mulai = data['mulai'],
            selesai = data['selesai'],
            posisi = data['posisi'],
            resource_name = data['resource_name'],
            createdby = data['createdby'],
            createdate = sysdatex,
            status = 'Active'
            )

        addprojectstate = ProjectState(
            id_project = hash_string.replace("-","").replace(" ",""),
            status = 'Active'
            )

        print(addproject, flush=True)

        try:
            if Project.find_by_resource(hash_string.replace("-","").replace(" ",""),data['resource_name']):
                print('Sudah ADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', flush=True)
                Project.update_resource(hash_string.replace("-","").replace(" ",""),data['resource_name'])
            else:
                addproject.save_to_db()
                addprojectstate.save_to_db()

            return {'message': 'Project {} was created'.format(data['project']),'STATUS' : 'Success Add Project'}

        except Exception as e:
            print(e.message , flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500


class activityByDate(Resource):
    def get(self):
        parser.add_argument('karyawan')
        parser.add_argument('dateassignment')
        parser.add_argument('endassignment')
        data = parser.parse_args()

        return Project.activityByDate(data['karyawan'],data['dateassignment'],data['endassignment'])

class appraisalteam(Resource):
    def get(self):
        parser.add_argument('userid')
        data = parser.parse_args()

        return Project.appraisalteam(data['userid'])

class jadwalappraisal(Resource):
    def post(self):
        parser.add_argument('tahun')
        parser.add_argument('semester')
        parser.add_argument('status')
        parser.add_argument('createdby')
        data = parser.parse_args()
        
        now = datetime.now()
        sysdatex = now.strftime("%Y-%m-%d %H:%M:%S")

        addjadwalappraisal = Appraisal(
            tahun = data['tahun'],
            semester = data['semester'],
            status = data['status'],
            createdby = data['createdby'],
            createdate = sysdatex
        )


        try:

            addjadwalappraisal.save_to_db()

            return {
                'message': 'Success insert jadwal appraisal',
                'STATUS' : 'SUCCESS'
                # 'token': access_token,
                # 'refresh_token': refresh_token
                }
        except (ValueError, KeyError, TypeError) as error:
            print(error, flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500

class listjadwalappraisal(Resource):
    def get(self):
        return Appraisal.listjadwalappraisal()