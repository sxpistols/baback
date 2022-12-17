from flask_restful import Resource, reqparse
from models import KaryawanModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import KaryawanModel, RevokedTokenModel,KaryawanShiftModel,KaryawanAssignmentModel, UserModel, Assignment, KaryawanU, RoleModel
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



class role_list(Resource):
    def get(self):
        return RoleModel.return_all()
