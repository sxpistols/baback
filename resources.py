from flask_restful import Resource, reqparse
from models import KaryawanModel, UserModel, RUserModel, RevokedTokenModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import json
import logging
from flask_cors import CORS


parser = reqparse.RequestParser()

# # parser.add_argument('email', help = 'This field cannot be blank', required = True)
# parser.add_argument('password', help = 'This field cannot be blank', required = True)

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

class AddKaryawan(Resource):
    def post(self):
        parser.add_argument('user_id', help = 'This field cannot be blank', required = True)
        parser.add_argument('fullname', help = 'This field cannot be blank', required = True)
        parser.add_argument('statuspernikahan', help = 'This field cannot be blank', required = True)
        parser.add_argument('nik', help = 'This field cannot be blank', required = True)
        parser.add_argument('identitas', help = 'This field cannot be blank', required = True)
        parser.add_argument('divisi', help = 'This field cannot be blank', required = True)
        parser.add_argument('tanggalmasuk', help = 'This field cannot be blank', required = True)
        parser.add_argument('statuskaryawan', help = 'This field cannot be blank', required = True)
        parser.add_argument('email', help = 'This field cannot be blank', required = True)
        parser.add_argument('phone', help = 'This field cannot be blank', required = True)
        parser.add_argument('alamat', help = 'This field cannot be blank', required = True)
        parser.add_argument('posisi', help = 'This field cannot be blank', required = True)
        parser.add_argument('site', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()
        
        if KaryawanModel.find_by_username(data['user_id']):
            return {'message': 'User {} already exists'.format(data['user_id'])}, 500
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}

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
            telegram = data['telegram']
            #username = data['username'],
            #email = data['email'],
            #password = UserModel.generate_hash(data['password'])
        )
   
        new_user = UserModel(
            username = data['user_id'],
            email = data['email'],
            password = UserModel.generate_hash(data['password'])
        )


        
        # try:

        #     new_user.save_to_db()
        #     access_token = create_access_token(identity = data['username'])
        #     refresh_token = create_refresh_token(identity = data['username'])
        #     return {
        #         'message': 'User {} was created'.format(data['username']),
        #         'token': access_token,
        #         'refresh_token': refresh_token
        #         }
        # except:
        #     return {'message': 'Something went wrong'}, 500

        print(addkaryawan, flush=True)
        try:
            addkaryawan.save_to_db()
            new_user.save_to_db()
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

class ListKaryawan(Resource):
    def get(self):
        return KaryawanModel.return_all()


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
        parser.add_argument('user', help = 'This field cannot be blank')
        parser.add_argument('password', help = 'This field cannot be blank')
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['user'])

        print('Current User : '+str(current_user), flush=True)
        # print(current_user.username, flush=True)
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['user'])}
        
        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = data['user'])
            refresh_token = create_refresh_token(identity = data['user'])
            return { 'token': access_token}
                # 'refresh_token': refresh_token
                
        else:
            return {'message': 'Wrong credentials'}
      
      
class RUserLogin(Resource):
    def post(self):
        parser.add_argument('username', help = 'This field cannot be blank')
        parser.add_argument('password', help = 'This field cannot be blank')
        data = parser.parse_args()
        current_user = RUserModel.find_by_username(data['username'])

        # print('Current User : '+str(current_user.password), flush=True)
        # print(current_user.username, flush=True)
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}
        
        if RUserModel.verify_hash(data['password'], current_user.password):
            # access_token = create_access_token(identity = data['user'])
            # refresh_token = create_refresh_token(identity = data['user'])
            return { 'message': 'Success'}
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


class SecretResource2(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        print(current_user,flush=True)
        b = UserModel.get_role(current_user)
        print(b,flush=True)
        return b, 200