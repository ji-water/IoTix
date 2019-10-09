# -- coding: utf-8 --
from flask import Flask,request, redirect, render_template, url_for, flash,session,jsonify
from flask_login import LoginManager,login_user, logout_user, current_user, login_required
from flask_restful import Resource,Api,reqparse
from flask import make_response,Response
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
        return

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
        return make_response(render_template('login.html'))

    def post(self):
        #form = LoginForm()
        #if form.validate_on_submit():
        user = UserSchema.objects(user_id=request.form['user_id']).first()
        if user and user.user_pw == request.form['user_pw']:
            user_obj = UserForLogin(str(user.pk))
            login_user(user_obj)
            flash("Logged in successfully", category='success')
            session['logged_in']=True
            return redirect('/')
        else:
            flash("Wrong username or password", category='error')
            return redirect('/login')

class LogoutAPI(Resource):
    @login_required
    def get(self):
        session['logged_in']=False
        logout_user()
        return redirect('/')

class HomeAPI(Resource):
    def get(self):
        if not session.get('logged_in'):
            return redirect('/login')
        else:
            return make_response(render_template('index.html'))

class FarmAPI(Resource):
    @login_required
    def get(self):
        if not session.get('logged_in'):
            return redirect('/login')
        else:
            farm_data = Farm.get_farm_by_user(current_user.get_id())
            position_data = Position.get_position_list(farm_data.pk)

            #user의 농장정보 + 작물위치(도식화)정보
            data = {
                'id':str(farm_data.pk),
                'name':farm_data.name,
                'manager':farm_data.manager.user_name,
                'position_data' : position_data
            }
            p_list = [0]*9
            for x in data['position_data']:
                p_list[x['position_num']-1]=1
            data['position_list'] = p_list

            #return make_response(json.dumps(data,ensure_ascii=False),200)
            return make_response(render_template('farm.html',id=data['id'],name=data['name'],manager=data['manager'],position_data=data['position_data']))

parser = reqparse.RequestParser()
parser.add_argument('crop', type=str,default=None)
parser.add_argument('crop_part',type=str,default=None)
parser.add_argument('date',type=str, default=None)

class CropAPI(Resource):
    @login_required
    def get(self,position_num,crop_name):
        farm_data = Farm.get_farm_by_user(current_user.get_id())
        crop_data = Crop.get_crop_by_name(farm_data.pk, position_num,crop_name)
        part_name_data = CropPart.get_having_part_name(crop_data['_id'])

        return part_name_data

class CropDetailAPI(Resource):
    @login_required
    def get(self,position_num):
        farm_data = Farm.get_farm_by_user(current_user.get_id()) #farm_id받아올수있으면 필요없는 과정
        crop_data = Crop.get_crop_by_position(farm_data.pk, position_num)

        #crop에 해당하는 part 정보도 포함
        for data in crop_data:
            part_name_data = CropPart.get_having_part_name(data['_id'])
            data['crop_part']=part_name_data #중복없이 crop_part_name list만 추가

        return crop_data

    @login_required
    def post(self,position_num):
        #구현중
        farm_data = Farm.get_farm_by_user(current_user.get_id()) #farm_id받아올수있으면 필요없는 과정
        crop_name = request.form['crop_name']
        part_name = request.form['crop_part_name']
        if request.form['date'] :
            date_temp = request.form['date'] #format : 20191005
        else :
            date_temp = datetime.datetime.now().strftime("%Y%m%d")

        date_obj = datetime.datetime.strptime(date_temp, "%Y%m%d")

        today = datetime.datetime.today().strftime("%Y%m%d")
        today_obj = datetime.datetime.strptime(today, "%Y%m%d")

        gap = (today_obj-date_obj).days #오늘날짜-입력된날짜

        result_list = list()
        list_for_graph = list() #7일의 delta만 담음

        for i in range(gap+1) :
            temp_qs = CropPart.get_crop_part_day_detail(farm_data.pk,crop_name,part_name,date_obj+timedelta(days=i))
            yes_qs  = CropPart.get_crop_part_day_detail(farm_data.pk,crop_name,part_name,date_obj+timedelta(days=i-1))
            temp_qs['delta']= temp_qs['length']-yes_qs['length'] #변화량 추가

            list_for_graph.append(temp_qs['delta'])
            result_list.append(temp_qs)

        for i in range(7-(gap+1)):
            tp_dict = dict()
            tp_dict['date'] = str(today_obj+timedelta(days=i+1))

            list_for_graph.append(float(0))
            result_list.append(tp_dict)

        print(list_for_graph)

        return result_list

api.add_resource(HomeAPI, '/')
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
#api.add_resource(FarmAPI,'/<ObjectId:user_pk>')
#api.add_resource(FarmAPI,'/farm/<ObjectId:farm_id>')
api.add_resource(FarmAPI, '/farm')
#api.add_resource(CropDetailAPI,'/farm/crop_detail')
api.add_resource(CropDetailAPI, '/farm/<int:position_num>')
api.add_resource(CropAPI, '/farm/<int:position_num>/<string:crop_name>')

if __name__ == '__main__':
    app.run(debug=True)
