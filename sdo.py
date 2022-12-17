from flask_restful import Resource, reqparse
from models import KaryawanModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import KaryawanModel, RevokedTokenModel,KaryawanShiftModel,KaryawanAssignmentModel, UserModel, Assignment, KaryawanU, RoleModel
from models_sdo import ClientModelSDO, ProjectSDO, karyawanSDO, ProjectStateSDO
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
        parser.add_argument('start')
        parser.add_argument('end')
        data = parser.parse_args()
        return Project.resourcemandays(data['start'],data['end'])

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

        
class setmandays(Resource):
    def post(self):
        parser.add_argument('jumlah')
        parser.add_argument('boardid')
        parser.add_argument('createdby')
        data = parser.parse_args()
        return ProjectSDO.setmandays(data['jumlah'],data['boardid'],data['createdby'])

class resourceactive(Resource):
    def get(self):
        return ProjectSDO.resourceactive()

class resourceidlesdo(Resource):
    def get(self):
        
        return ProjectSDO.resourceidlesdo()

class resourceidledailysdo(Resource):
    def get(self):
        parser.add_argument('tanggal')
        data = parser.parse_args()

        return ProjectSDO.resourceidledailysdo(data['tanggal'])

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
            # print('error : '+e , flush=True)
            print(e.message , flush=True)
            return {'message': 'Something went wrong', 'STATUS': 'Gagal Ditambahkan'}, 500


