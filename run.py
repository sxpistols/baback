from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mysqldb import MySQL
import os
from flask_mail import Mail, Message

config = {
  'ORIGINS': [
    'http://localhost:3000',  # React
    'http://127.0.0.1:3000',
    'http://127.0.0.1:3000',
    'http://localhost:9001'  # React
  ],
  'SECRET_KEY': 'fuck-you!'
}

app = Flask(__name__)
#CORS(app,supports_credentials=True)
cors = CORS(app, support_credentials=True)
api = Api(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://employee:Syabian247#@127.0.0.1/employee'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'fuck-you!'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'employee'
app.config['MYSQL_PASSWORD'] = 'Syabian247#'
app.config['MYSQL_DB'] = 'employee'

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

mail_settings = {
          "MAIL_SERVER": 'smtp.gmail.com',
          "MAIL_PORT": 465,
          "MAIL_USE_TLS": False,
          "MAIL_USE_SSL": True,
          "MAIL_USERNAME": os.environ['EMAIL_USER'],
          "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
          }

        #ztgpjzxupdibpizw
app.config.update(mail_settings)
mail = Mail(app)

#app.config['SECRET_KEY'] = 'fuck you!'
jwt = JWTManager(app)
# mysql = MySQL(app)
# db = MySQL(app)
db = SQLAlchemy(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


@app.before_first_request
def create_tables():
    db.create_all()


import views, models, resources, karyawan, Role, pmo, trello, sdo

api.add_resource(resources.UserRegistration, '/api/registration')
api.add_resource(resources.UserLogin, '/api/auth/login')
api.add_resource(resources.RUserLogin, '/api/auth/rlogin')
api.add_resource(resources.UserLogoutAccess, '/api/auth/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/api/auth/logout/refresh')
api.add_resource(resources.User, '/api/auth/user')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/api/auth/secret')
api.add_resource(resources.SecretResource2, '/api/auth/secret2')
api.add_resource(karyawan.AddKaryawan, '/api/karyawan/add')
api.add_resource(karyawan.AddKaryawanAppraisal, '/api/karyawan/addappraisal')
api.add_resource(karyawan.AppraisalDetail, '/api/karyawan/appraisaldetail')
api.add_resource(karyawan.AppraisalDelete, '/api/karyawan/deleteappraisal')
api.add_resource(karyawan.ListKaryawan, '/api/karyawan/list')
api.add_resource(karyawan.ListKaryawanAll, '/api/karyawan/listall')
api.add_resource(karyawan.ListKaryawanResign, '/api/karyawanresign/list')
api.add_resource(karyawan.ListKaryawanUCovid, '/api/karyawan/listucovid')
api.add_resource(karyawan.AddShiftKaryawan, '/api/karyawan/addshift')
api.add_resource(karyawan.Karyawan, '/api/karyawan')
api.add_resource(karyawan.KaryawanCuti, '/api/karyawan/cuti')
api.add_resource(karyawan.ListKaryawanCuti, '/api/karyawan/listcuti')
api.add_resource(karyawan.CutiDelete, '/api/karyawan/cutidelete')
api.add_resource(karyawan.ListKaryawanCutiSDO, '/api/karyawan/sdolistcuti')
api.add_resource(karyawan.updateK, '/api/karyawan/update')
api.add_resource(karyawan.resignK, '/api/karyawan/resign')
api.add_resource(karyawan.addresign, '/api/karyawan/addresign')
api.add_resource(karyawan.KaryawanMutasi, '/api/karyawan/mutasi')
api.add_resource(karyawan.ListKaryawanMutasi, '/api/karyawan/listmutasi')
api.add_resource(karyawan.ShiftKaryawan, '/api/karyawan/shift')
api.add_resource(karyawan.BayaranShift, '/api/karyawan/bayaranshift')
api.add_resource(karyawan.ListSupervisor, '/api/karyawan/listsupervisor')
api.add_resource(karyawan.AddAssignment, '/api/karyawan/addassignment')
api.add_resource(karyawan.AddAssignmentKaryawan, '/api/karyawan/addassignmentkaryawan')
api.add_resource(karyawan.ListAssignment, '/api/karyawan/listassignment')
api.add_resource(karyawan.ApproveAssignment, '/api/karyawan/approve')
api.add_resource(karyawan.HistoryAssignment, '/api/karyawan/historyassignment')
api.add_resource(karyawan.AssignmentUser, '/api/karyawan/assignmentuser')
api.add_resource(karyawan.AssignmentReportKaryawan, '/api/karyawan/reportassignmentkaryawan')
api.add_resource(karyawan.DetailAssignment, '/api/karyawan/detailassignment')
api.add_resource(karyawan.DeleteAssignment, '/api/karyawan/assignment_delete')
# api.add_resource(karyawan.AssignmentReport, '/api/karyawan/reportassignment')
api.add_resource(karyawan.cobaEmail, '/api/karyawan/cobaEmail')
api.add_resource(karyawan.sendEmail, '/api/karyawan/sendemail')
api.add_resource(karyawan.userReg, '/api/karyawan/mailreg')
api.add_resource(Role.role_list, '/api/role')
api.add_resource(karyawan.KaryawanCovid, '/api/karyawan/covid')
api.add_resource(karyawan.ListKaryawanCovid, '/api/karyawan/listcovid')
api.add_resource(karyawan.loging, '/api/karyawan/userlog')
api.add_resource(karyawan.AddChallenge, '/api/karyawan/addchallenge')
api.add_resource(karyawan.ListChallenge, '/api/karyawan/listchallenge')
api.add_resource(karyawan.assignmentupdate,'/api/karyawan/assignmentupdate')
api.add_resource(karyawan.AddSkills, '/api/karyawan/addskills')
api.add_resource(karyawan.Skills, '/api/karyawan/skills')
api.add_resource(karyawan.Skill, '/api/karyawan/skill')
api.add_resource(karyawan.SkillUpdate, '/api/karyawan/skillupdate')

###PMO

api.add_resource(pmo.karyawanpmo, '/api/pmo/karyawan')
api.add_resource(pmo.addclient, '/api/pmo/addclient')
api.add_resource(pmo.getClient, '/api/pmo/client')
api.add_resource(pmo.getPM, '/api/pmo/listpm')
api.add_resource(pmo.getSA, '/api/pmo/listsa')
api.add_resource(pmo.getDev, '/api/pmo/listdev')
api.add_resource(pmo.getQC, '/api/pmo/listqc')
api.add_resource(pmo.getTW, '/api/pmo/listtw')
api.add_resource(pmo.getPA, '/api/pmo/listpa')
api.add_resource(pmo.addProject, '/api/pmo/project/add')
api.add_resource(pmo.getProject, '/api/pmo/projects')
api.add_resource(pmo.detailProject, '/api/pmo/project')
api.add_resource(pmo.projectPM, '/api/pmo/project/pm')
api.add_resource(pmo.projectSA, '/api/pmo/project/sa')
api.add_resource(pmo.projectDev, '/api/pmo/project/dev')
api.add_resource(pmo.projectPA, '/api/pmo/project/pa')
api.add_resource(pmo.projectQC, '/api/pmo/project/qc')
api.add_resource(pmo.projectTW, '/api/pmo/project/tw')
api.add_resource(pmo.projectClose, '/api/pmo/project/close')
api.add_resource(pmo.getProjectHist, '/api/pmo/projectshist')
api.add_resource(pmo.delResourceproject, '/api/pmo/project/delres')
api.add_resource(pmo.updateTanggal, '/api/pmo/project/updtgl')
api.add_resource(pmo.summary, '/api/pmo/summary')
api.add_resource(pmo.resourceactive, '/api/pmo/resourceactive')
api.add_resource(pmo.resourceidle, '/api/pmo/resourceidle')
api.add_resource(pmo.resourceidledaily, '/api/pmo/resourceidledaily')
api.add_resource(pmo.resourceidledailyD, '/api/pmo/resourceidledailyD')
api.add_resource(pmo.resource_summary, '/api/pmo/ressum')
api.add_resource(pmo.dashboard_summary, '/api/pmo/dashsum')
api.add_resource(pmo.dashboard_pmo, '/api/pmo/dashpmo')
api.add_resource(pmo.dashboard_pmopercent, '/api/pmo/dashpmopercent')
api.add_resource(pmo.dashboard_pmochart, '/api/pmo/dashpmochart')
api.add_resource(pmo.dashboard_pmosharing, '/api/pmo/dashpmosharing')
api.add_resource(pmo.dashboard_pmostatusk, '/api/pmo/pmostatusk')
api.add_resource(pmo.dashboard_sdodipmo, '/api/pmo/sdodipmo')
api.add_resource(pmo.dashboard_pmosdoother, '/api/pmo/pmosdoother')
api.add_resource(pmo.dashboard_pmoforsdo, '/api/pmo/pmoforsdo')
api.add_resource(pmo.dashboard_pmoposisi, '/api/pmo/pmoposisi')
api.add_resource(pmo.dashboard_sdo, '/api/pmo/dashsdo')
api.add_resource(pmo.dashboard_qc, '/api/pmo/dashqc')
api.add_resource(pmo.setmandays, '/api/pmo/setmandays')
api.add_resource(pmo.resourcemandays, '/api/pmo/resourcemandays')
api.add_resource(pmo.resourcedetailmandays, '/api/pmo/resourcedetailmandays')
api.add_resource(pmo.settingproject, '/api/pmo/settingproject')
api.add_resource(pmo.mandaysProjectFin, '/api/pmo/mandaysProjectFin')
api.add_resource(pmo.activityByDate, '/api/pmo/activityByDate')
api.add_resource(pmo.appraisalteam, '/api/pmo/appraisalteam')
api.add_resource(pmo.jadwalappraisal, '/api/pmo/jadwalappraisal')
api.add_resource(pmo.listjadwalappraisal, '/api/pmo/listjadwalappraisal')




#PMOTRELLO
api.add_resource(trello.getBoards, '/api/trello/boards')
api.add_resource(trello.allBoards, '/api/trello/allboards')
api.add_resource(trello.getBoardsNot, '/api/trello/boardsnot')
api.add_resource(trello.getBoardName, '/api/trello/boardname')
api.add_resource(trello.getBoardMembers, '/api/trello/boardmembers')
api.add_resource(trello.getBoardMembersMandays, '/api/trello/boardmembersmandays')
api.add_resource(trello.getBoardDetail, '/api/trello/boarddetail')
api.add_resource(trello.getBoardDetailD, '/api/trello/boarddetaildaily')
api.add_resource(trello.getBoardDetailM, '/api/trello/boarddetailmonthly')
api.add_resource(trello.getReport, '/api/trello/reporttimesheet')
api.add_resource(trello.getBoardDaily, '/api/trello/boarddaily')
api.add_resource(trello.getBoardMonthly, '/api/trello/boardmonthly')
api.add_resource(trello.getDailyActivity, '/api/trello/dailyactivity')
api.add_resource(trello.getRepDailyAct, '/api/trello/actdetaildaily')
api.add_resource(trello.getRepMonthlyAct, '/api/trello/actdetailmonthly')
api.add_resource(trello.getlastten, '/api/trello/getlastten')
api.add_resource(trello.projectMandays, '/api/trello/projectmandays')
api.add_resource(trello.monthlyactkaryawanlist, '/api/trello/monthlyactkaryawanlist')
api.add_resource(trello.monthlyact, '/api/trello/monthlyact')
api.add_resource(trello.monthlyactd, '/api/trello/monthlyactd')
api.add_resource(trello.projectmdetail, '/api/trello/projectmdetail')
api.add_resource(trello.pmndaysupdate, '/api/trello/pmndaysupdate')


#ADMIN SUPERMAN
api.add_resource(trello.getAddBoardList, '/api/trello/addboardlist')
api.add_resource(trello.getAddBoardMember, '/api/trello/addboardmember')

###SDO
api.add_resource(sdo.resourceidlesdo, '/api/sdo/resourceidlesdo')
api.add_resource(sdo.resourceidledailysdo, '/api/sdo/resourceidledailysdo')

#Update 10Juni2021



if __name__ == '__main__':
    app.run(port=9966,threaded=True, host='0.0.0.0', debug=True)
