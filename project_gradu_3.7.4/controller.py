# -- coding: utf-8 --
from flask import Flask,request, redirect, render_template, url_for, flash,session,jsonify
from flask_login import LoginManager,login_user, logout_user, current_user, login_required
from flask_restful import Resource,Api,reqparse
from flask import make_response
from flask_objectid_converter import ObjectIDConverter
from form import LoginForm
from flask_wtf.csrf import CSRFProtect


from model import *
import json
from bson import ObjectId
import datetime

import os

from werkzeug.security import check_password_hash


app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get('testDB_develop')
app.config['SECRET_KEY']=os.urandom(24)
app.url_map.converters['ObjectId']=ObjectIDConverter
api = Api(app)
#app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)


class UserForLogin():
    def __init__(self, username):
        self.username = username #user pk

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    qs = UserSchema.objects(pk=user_id).first()
    if not qs:
        return None
    return UserForLogin(qs.pk)


class LoginAPI(Resource):
    def get(self):
        return 'login get api'

    def post(self):
        #form = LoginForm()
        #if form.validate_on_submit():
        user = UserSchema.objects(user_id=request.form['user_id']).first()
        if user and user.user_pw == request.form['user_pw']:
            user_obj = UserForLogin(str(user.pk))
            login_user(user_obj)
            flash("Logged in successfully", category='success')
            return redirect('/farm')
        else:
            flash("Wrong username or password", category='error')
            return redirect('/login')

class LogoutAPI(Resource):
    @login_required
    def post(self):
        logout_user()
        return redirect('/', code=307)

class HomeAPI(Resource):
    def post(self):
        return 'access home successfully'

# class LoginOut(Resource):
#     def post(self):
#     #session.logout('user_id',None)

class FarmAPI(Resource):
    @login_required
    def get(self):
        #temp_user = User.get_by_id('5d77d4d4694d62037a1684e7')
        farm_data = Farm.get_farm_by_user(current_user.get_id())
        position_data = Position.get_position_list(farm_data.pk)
        #url을 farm_id로 바꿔서 get_farm_by_id 로 바꿀 예정..

        #user의 농장정보 + 작물위치(도식화)정보
        data = {
            'id':str(farm_data.pk),
            'name':farm_data.name,
            'manager':farm_data.manager.user_name,
            'position_data' : position_data
        }

        return make_response(json.dumps(data,ensure_ascii=False),200)


parser = reqparse.RequestParser()
parser.add_argument('crop', type=str,default=None)
parser.add_argument('crop_part',type=str,default=None)
parser.add_argument('date',type=str, default=None)

class CropDetailAPI(Resource):
    @login_required
    def get(self,position_num):
        crop_data = Crop.get_crop_by_position('5d77d915acf3296b9e3c1c73',position_num)

        #crop에 해당하는 part 정보도 포함
        for data in crop_data:
            part_name_data = CropPart.get_having_part_name(data['_id'])
            data['crop_part']=part_name_data #crop_part의 이름만 빼오자,, 중복없이?..(가진 crop_part 이름 list)

        return crop_data
        # args = parser.parse_args()
        # crop = args['crop']
        # crop_part = args['crop_part']
        # if args['data'] is None :
        #     date = datetime.datetime.today().strptime('%Y%m%d')
        # return {'crop': crop,'crop_part': crop_part,'date': date}

    def post(self,position_num):
        #구현중
        crop_name = request.form['crop_name']
        part_name = request.form['crop_part_name']
        date = request.form['date']
        data_temp = []

        return data_temp


api.add_resource(HomeAPI, '/')
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
#api.add_resource(FarmAPI,'/<ObjectId:user_pk>')
#api.add_resource(FarmAPI,'/farm/<ObjectId:farm_id>')
api.add_resource(FarmAPI, '/farm')
#api.add_resource(CropDetailAPI,'/farm/crop_detail')
api.add_resource(CropDetailAPI, '/farm/<int:position_num>')

if __name__ == '__main__':
    app.run(debug=True)
