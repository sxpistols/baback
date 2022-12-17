from flask_restful import Resource, reqparse
from models import KaryawanModel
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import KaryawanModel, RevokedTokenModel,KaryawanShiftModel,KaryawanAssignmentModel, UserModel, Assignment, KaryawanU, RoleModel
from models_trello import Report
# from models_board import Boards
from flask import json
import logging
import hashlib
from datetime import datetime
from flask import Flask
from flask_mail import Mail, Message
import os
import email_kirim
from flask_cors import CORS
import requests
import json
from datetime import datetime
from dateutil import tz
import time

from_zone = tz.tzutc()
to_zone = tz.tzlocal()


headers = {
           "Accept": "application/json"
           }

query = {
           'key': '1b33653f71a909d49832d7353c390575',
              'token': 'bf38564da7697e5577104399bd765a4e427502bdae7fa81f58c6b62668043471'
              }

parser = reqparse.RequestParser()

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

# select distinct name from boards b2 ;
class getBoardsBackup(Resource):
    def get(self):
      url = "https://api.trello.com/1/members/dolants/boards"
      response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
      )

      y = json.loads(response.text)
      # print(y[11]['name'])
      a = []

      i=0

      while i < len(y):
        a.append({'board' : y[i]['name'], 'boardid': y[i]['id'], 'url': y[i]['url']})
        # print(y[i]['name'])
        i = i+1


      return { 'Boards' : a }, 200

class getBoards(Resource):
    def get(self):
      parser.add_argument('tahun')
      parser.add_argument('bulan')
      parser.add_argument('tanggal')
      parser.add_argument('user_role')
      data = parser.parse_args()
      return Report.getBoards(data['tahun'],data['bulan'],data['tanggal'],data['user_role'])

class allBoards(Resource):
    def get(self):
      parser.add_argument('user_role')
      data = parser.parse_args()
      return Report.allBoards(data['user_role'])

class getBoardsNot(Resource):
    def get(self):
      parser.add_argument('tahun')
      parser.add_argument('user_role')
      data = parser.parse_args()
      return Report.getBoardsNot(data['tahun'],data['user_role'])

class getDailyActivity(Resource):
    def get(self):
      parser.add_argument('tanggal')
      parser.add_argument('role')
      data = parser.parse_args()
      return Report.getDailyActivity(data['tanggal'], data['role'])

class getBoardDetailBackup(Resource):
    def get(self):
      # from_zone = tz.gettz('UTC')
      # to_zone = tz.gettz('Asia/Jakarta')

      # METHOD 2: Auto-detect zones:
     

      parser.add_argument('boardid')
      parser.add_argument('tanggal')
      data = parser.parse_args()

      # return Project.project_detail(data['id_project'])
      url = "https://api.trello.com/1/boards/"+data['boardid']+"/actions"
      response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
      )

      y = json.loads(response.text)
      # print(y[11]['name'])
      a = []

      i=0
      # while i < len(y):
      #   a.append({'board' : y[i]['name'], 'boardid': y[i]['id'], 'url': y[i]['url']})
      #   # print(y[i]['name'])
      #   i = i+1

      while i < len(y):
        try:
          if y[i]['type'] == 'commentCard':
            # # dd = str(y[i]['date'])
            utc = datetime.strptime(y[i]['date'], '%Y-%m-%dT%H:%M:%S.%fZ')

            # # Tell the datetime object that it's in UTC time zone since 
            # # datetime objects are 'naive' by default
            utc = utc.replace(tzinfo=from_zone)

            # # Convert time zone
            central = utc.astimezone(to_zone)
            print(central,flush=True)

            print(type(y[i]['date']),flush =True)
            # print(datss=y[i]['date'],flush=True)
            # datex='2020-10-08 03:20:34.000Z'
            # utc = datetime.strptime(datex, '%Y-%m-%dT%H:%M:%S.%fZ')
            # central = utc.astimezone(to_zone)
            # print(d.strftime('%Y-%m-%d %H-%M-%S'))  #==> '09/26/2008'
            a.append({'list' : y[i]['data']['list']['name'], \
                'card' : y[i]['data']['card']['name'], 'type' : y[i]['type'], \
                'date' : central.strftime("%d-%m-%Y %H:%M:%S"), 'fullname' : y[i]['memberCreator']['fullName'], \
                   'text' : y[i]['data']['text'], 'shortlink' : y[i]['data']['card']['shortLink'] })

          if y[i]['type'] == 'addAttachmentToCard':
            # # dd = str(y[i]['date'])
            utc = datetime.strptime(y[i]['date'], '%Y-%m-%dT%H:%M:%S.%fZ')

            # # Tell the datetime object that it's in UTC time zone since 
            # # datetime objects are 'naive' by default
            utc = utc.replace(tzinfo=from_zone)

            # # Convert time zone
            central = utc.astimezone(to_zone)
            a.append({'list' : y[i]['data']['list']['name'], \
                'card' : y[i]['data']['card']['name'], 'type' : y[i]['type'], \
                'date' : central.strftime("%d-%m-%Y %H:%M:%S"), 'fullname' : y[i]['memberCreator']['fullName'], \
                'text' : 'tidak ada', 'shortlink' : y[i]['data']['card']['shortLink']  })

        except:
          print('GA ADA')

        i = i+1

      return { 'Boards' : a }, 200


class getBoardDetail(Resource):
    def get(self):
      # from_zone = tz.gettz('UTC')
      # to_zone = tz.gettz('Asia/Jakarta')

      # METHOD 2: Auto-detect zones:
     

      parser.add_argument('boardid')
      parser.add_argument('tanggal')
      data = parser.parse_args()

      return Report.getDetail(data['boardid'],data['tanggal'])

class getBoardDetailD(Resource):
    def get(self):
      # from_zone = tz.gettz('UTC')
      # to_zone = tz.gettz('Asia/Jakarta')

      # METHOD 2: Auto-detect zones:
     

      parser.add_argument('boardid')
      parser.add_argument('tanggal')
      data = parser.parse_args()

      return Report.getDetailD(data['boardid'],data['tanggal'])

class getBoardDetailM(Resource):
    def get(self):
      # from_zone = tz.gettz('UTC')
      # to_zone = tz.gettz('Asia/Jakarta')

      # METHOD 2: Auto-detect zones:
     

      parser.add_argument('boardid')
      parser.add_argument('tanggal')
      data = parser.parse_args()

      return Report.getDetailM(data['boardid'],data['tanggal'])

class getBoardName(Resource):
    def get(self):
      # from_zone = tz.gettz('UTC')
      # to_zone = tz.gettz('Asia/Jakarta')

      # METHOD 2: Auto-detect zones:
     

      parser.add_argument('boardid')
      data = parser.parse_args()

      return Report.getBoardName(data['boardid'])


class getBoardMembersMandays(Resource):
    def get(self):
      parser.add_argument('boardid')
      data = parser.parse_args()

      return Report.getBoardMembersMandays(data['boardid'])

class getBoardMembers(Resource):
    def get(self):
      parser.add_argument('boardid')
      data = parser.parse_args()

      # return Project.project_detail(data['id_project'])
      url = "https://api.trello.com/1/boards/"+data['boardid']+"/members"
      response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
      )

      y = json.loads(response.text)
      # print(y[11]['name'])
      a = []

      i=0
      # while i < len(y):
      #   a.append({'board' : y[i]['name'], 'boardid': y[i]['id'], 'url': y[i]['url']})
      #   # print(y[i]['name'])
      #   i = i+1

      while i < len(y):
        try:
          a.append({'fullname' : y[i]['fullName'] })

        except:
          print('GA ADA')

        i = i+1

      return { 'Members' : a }, 200



class getReport(Resource):
    def get(self):
        parser.add_argument('tanggal')
        parser.add_argument('user_role')
        data = parser.parse_args()

        return Report.getReport(data['tanggal'], data['user_role'])

class getBoardDaily(Resource):
    def get(self):
        parser.add_argument('tanggal')
        data = parser.parse_args()

        return Report.getBoardDaily(data['tanggal'])

class projectmdetail(Resource):
    def get(self):
        parser.add_argument('project_id')
        data = parser.parse_args()

        return Report.projectmdetail(data['project_id'])

#{'board': '5fb1ee36f2aa301bd7407737', 'startd': '2021-09-29', 'endd': '2021-10-22', 'mandays': '231', 'nilai': '2003828127', 'status': 'ACTIVE'}
class pmndaysupdate(Resource):
    def post(self):
        parser.add_argument('board')
        parser.add_argument('startd')
        parser.add_argument('endd')
        parser.add_argument('mandays')
        parser.add_argument('nilai')
        parser.add_argument('status')
        parser.add_argument('no_po')
        parser.add_argument('nama_po')
        parser.add_argument('project_type')
        parser.add_argument('noproject')
        parser.add_argument('namaproject')
        parser.add_argument('invoice1')
        parser.add_argument('invoice2')
        data = parser.parse_args()

        return Report.pmndaysupdate(data['board'],data['startd'],data['endd'],data['mandays'],data['nilai'],data['status'],data['no_po'],data['nama_po'],data['project_type'],data['noproject'],data['namaproject'],data['invoice1'],data['invoice2'])

        
class projectMandays(Resource):
    def get(self):
        parser.add_argument('tahun')
        data = parser.parse_args()

        return Report.projectMandays(data['tahun'])        

class getBoardMonthly(Resource):
    def get(self):
        parser.add_argument('tanggal')
        data = parser.parse_args()

        return Report.getBoardMonthly(data['tanggal'])

class getRepDailyAct(Resource):
    def get(self):
        parser.add_argument('tanggal')
        data = parser.parse_args()

        return Report.getRepDailyAct(data['tanggal'])

class getRepMonthlyAct(Resource):
    def get(self):
        parser.add_argument('tanggal')
        data = parser.parse_args()

        return Report.getRepMonthlyAct(data['tanggal'])

class getlastten(Resource):
    def get(self):
        parser.add_argument('user_role')
        data = parser.parse_args()
        return Report.getlastten(data['user_role'])


class getAddBoardList(Resource):
    def get(self):
        parser.add_argument('tahun')
        parser.add_argument('bulan')
        data = parser.parse_args()

        return Report.getAddBoardList(data['tahun'],data['bulan'])

class getAddBoardMember(Resource):
    def get(self):
        parser.add_argument('tahun')
        parser.add_argument('bulan')
        data = parser.parse_args()

        return Report.getAddBoardMember(data['tahun'],data['bulan'])
        
        
class monthlyactkaryawanlist(Resource):
    def get(self):
        parser.add_argument('tahun')
        parser.add_argument('user_role')
        data = parser.parse_args()
        return Report.monthlyactkaryawanlist(data['tahun'],data['user_role'])

class monthlyact(Resource):
    def get(self):

        parser.add_argument('trelloid')
        parser.add_argument('bulan')
        data = parser.parse_args()

        return Report.monthlyact(data['trelloid'],data['bulan'])

class monthlyactd(Resource):
    def get(self):

        parser.add_argument('trelloid')
        parser.add_argument('bulan')
        data = parser.parse_args()

        return Report.monthlyactd(data['trelloid'],data['bulan'])