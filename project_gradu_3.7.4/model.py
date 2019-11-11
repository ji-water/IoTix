from schema import UserSchema,FarmSchema,CropSchema,CropPartSchema,PositionSchema
from pprint import pprint
from bson import ObjectId
from datetime import datetime,timedelta

class ModelErrorBase(Exception):
    def __init__(self,msg):
        self.message = msg

class ValueError(ModelErrorBase):pass


class User():
    @staticmethod
    def create(data):
        user_schema = UserSchema(**data).save()
        return user_schema

    @staticmethod
    def get_by_id(user_id):
        qs = UserSchema.objects(pk=user_id)
        if qs.count == 0:
            return None
        return qs.first()

class Farm():
    @staticmethod
    def create(data):
        farm_schema = FarmSchema(**data).save()
        return farm_schema

    @staticmethod
    def get_farm_by_user(current_user):
        qs = FarmSchema.objects(manager=current_user)
        if qs.count == 0:
            raise ValueError("There is no such user")
        return qs.first()

    @staticmethod
    def get_by_id(farm_id):
        qs = FarmSchema.objects(pk=farm_id)
        if qs.count == 0:
            return None
        return qs.first()

    @staticmethod
    def get_positions(farm_id):
        qs = PositionSchema.objects(farm=farm_id)
        if qs.count == 0:
            raise ValueError("There is no position by farm id")
        return qs.first() #list 반환으로 변경


class Crop():
    @staticmethod
    def create(data):
        crop_schema = CropSchema(**data).save()
        return crop_schema

    @staticmethod
    def get_by_id(crop_id):
        qs = CropSchema.objects(pk=crop_id)
        if qs.count == 0:
            return None
        return qs.first()

    @staticmethod
    def get_crop_by_farm(farm_id):
        qs = CropSchema.objects(farm=farm_id)
        if qs.count == 0:
            return None
        return list(map(lambda crop: crop.to_mongo(), qs))

    @staticmethod
    def get_crop_by_name(farm_id, position_num, crop_name):
        position_qs = PositionSchema.objects(farm=farm_id, position_num=position_num).first()
        qs = CropSchema.objects(farm=farm_id, position=position_qs.id, crop_name=crop_name)
        if qs.count == 0:
            return None
        qs_list = list(map(lambda crop: crop.to_mongo(), qs))  # convert to list

        # parse objectid to str
        for data in qs_list:
            for key, value in data.items():
                if isinstance(value, ObjectId):
                    data[key] = str(value)

        return qs_list[0]

    @staticmethod
    def get_crop_by_position(farm_id, position_num):
        position_qs = PositionSchema.objects(farm=farm_id,position_num=position_num).first()
        qs = CropSchema.objects(farm=farm_id,position=position_qs.id)
        if qs.count == 0:
            return None
        qs_list = list(map(lambda crop: crop.to_mongo(), qs)) #convert to list

        #parse objectid to str
        for data in qs_list:
            for key, value in data.items():
                if isinstance(value,ObjectId):
                    data[key] = str(value)

        return qs_list

class CropPart():
    @staticmethod
    def create(data):
        crop_part_schema = CropPartSchema(**data).save()
        return crop_part_schema

    @staticmethod
    def get_having_part_name(crop_id):
        part_name_list = []
        qs = CropPartSchema.objects(crop=crop_id).only('crop_part_name')
        if qs.count == 0:
            return None
        qs_list = list(map(lambda crop: crop.to_mongo()['crop_part_name'], qs))
        non_dup_list = list(set(qs_list))

        return sorted(non_dup_list)


    @staticmethod
    def get_crop_part_list(crop_id):
        qs = CropPartSchema.objects(crop=crop_id)
        if qs.count == 0:
            return None

        qs_list = list(map(lambda crop: crop.to_mongo(), qs))  # convert to list

        # parse objectid to str
        for data in qs_list:
            for key, value in data.items():
                if isinstance(value, ObjectId):
                    data[key] = str(value)
                if isinstance(value, datetime):
                    data[key] = str(value)

        return qs_list

    @staticmethod
    def get_crop_part_detail(farm_id, crop_name, part_name, date_obj):
        #date_obj = datetime.strptime(date, "%Y%m%d")
        date_obj2 = date_obj+timedelta(days=1)
        print(date_obj2)

        crop_qs = CropSchema.objects(crop_name=crop_name,farm=farm_id).first()
        part_qs = CropPartSchema.objects.filter(crop=crop_qs.pk,crop_part_name=part_name)
        date_qs = part_qs.filter(__raw__={"date": {"$gte": date_obj, "$lt": date_obj2}})

        #date 쿼리 추가
        if part_qs.count == 0:
            return None

        qs_list = list(map(lambda part_data: part_data.to_mongo(), date_qs))  # convert to list


        # parse objectid to str
        for data in qs_list:
            for key, value in data.items():
                if isinstance(value, ObjectId):
                    data[key] = str(value)
                if isinstance(value, datetime):
                    data[key] = str(value)

        return qs_list

    @staticmethod
    def get_crop_part_day_detail(farm_id,crop_name, part_name, date_obj):
        #date_obj = datetime.strptime(date, "%Y%m%d")
        date_obj2 = date_obj+timedelta(days=1)
        #print(date_obj2)

        crop_qs = CropSchema.objects(crop_name=crop_name,farm=farm_id).first()
        part_qs = CropPartSchema.objects.filter(crop=crop_qs.pk,crop_part_name=part_name)

        part_list = list(map(lambda part_data: part_data.to_mongo(), part_qs))  # convert to list
        speed_list = list()
        for data in part_list:
            speed_list.append(data['speed'])

        date_qs = part_qs.filter(__raw__={"date": {"$gte": date_obj, "$lt": date_obj2}})
        #print(date_qs)

        if date_qs.count()==0:
            print("---None---")
            return None
        data = date_qs.order_by('-id').first().to_mongo()

        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            if isinstance(value, datetime):
                data[key] = str(value)


        return data

    @staticmethod
    def get_crop_part_speed_list(farm_id,crop_name, part_name):
        crop_qs = CropSchema.objects(crop_name=crop_name, farm=farm_id).first()
        part_qs = CropPartSchema.objects.filter(crop=crop_qs.pk, crop_part_name=part_name,tag=0)

        part_list = list(map(lambda part_data: part_data.to_mongo(), part_qs))  # convert to list

        ##speed_list 삭제해야함
        speed_list = list()
        for data in part_list:
            speed_list.append(data['speed'])

        return part_list

class Position():
    @staticmethod
    def create(data):
        position_schema = PositionSchema(**data).save()
        return position_schema

    @staticmethod
    def get_by_id(position_id):
        qs = PositionSchema.objects(pk=position_id)
        if qs.count == 0:
            return None
        return qs.first()

    @staticmethod
    def get_by_position_num(farm_id,position_num):
        qs = PositionSchema.objects(farm=farm_id,position_num=position_num)
        if qs.count == 0:
            return None
        return qs.first()

    @staticmethod
    def get_position_list(farm_id):
        qs = PositionSchema.objects(farm=farm_id)
        if qs.count==0:
            return None

        qs_list = list(map(lambda crop: crop.to_mongo(), qs))  # convert to list

        # parse objectid to str
        for data in qs_list:
            for key, value in data.items():
                if isinstance(value, ObjectId):
                    data[key] = str(value)

        return qs_list



if __name__ == '__main__':
    ##지수 user id '5d943df97689541378a2540f'
    ##지수 farm id '5d95c39e0d93ac9e7b820ce2'
    ##지수 position id _1 '5d998f78e179752adb6b880f'
    ##      position id 2 '5d998f86d07e9dbd486b78bd'
    ##지수 crop id tomato1 '5d999068dbc2308bb0794aab'
    ##              tomato2 '5d99907a612afe8a0bf55b2e'


    #user_dic = {'user_id': "kkkdeon", 'user_pw': "1234", 'user_name': "김도연"}
    #User.create(user_dic)

    #farm_dic = {'name': 'farm1', 'manager': User.get_by_id('5d77d4d4694d62037a1684e7'),'phone_num': '01046244619'}
    #crop_dic = {'farm': Farm.get_by_id('5d95c39e0d93ac9e7b820ce2'), 'crop_name':"tomato2", 'crop_type':"tomato", 'position': Position.get_by_id('5d998f78e179752adb6b880f')}
    position_dic = {'farm': Farm.get_by_id('5d77d915acf3296b9e3c1c73'), 'position_num': 3, 'position_abs': "gps주소", 'position_name': "3번 위치 desc"}

    str1 = "20191111 3:02:02"
    date_obj1 = datetime.strptime(str1, "%Y%m%d %H:%M:%S")
    crop_part_dic={'crop': Crop.get_by_id('5d9079e8c54b56aab045d9fb'),'crop_part_name':"stem1",'length':17.9,'speed':2.1,'date': date_obj1,'tag':0}
    CropPart.create(crop_part_dic)


    #farm_dic = {'name': 'farm1', 'manager': User.get_by_id('5d943df97689541378a2540f'),'phone_num': '01046244619'}
    # crop_dic = {'farm': Farm.get_by_id('5d95c39e0d93ac9e7b820ce2'), 'crop_name':"tomato2", 'crop_type':"tomato", 'position': Position.get_by_id('5d95c3f7cd8c9473a8840692')}
    #position_dic = {'farm': Farm.get_by_id('5d95c39e0d93ac9e7b820ce2'), 'position_num': 2, 'position_abs': "gps주소", 'position_name': "2번 위치 desc"}
    #crop_part_dic={'crop': Crop.get_by_id('5d95c445451de46928d16d85'),'crop_part_name':"stem2",'length':3.88,'speed':0.90,'date': datetime.now()}

    #Farm.create(farm_dic)
    #Position.create(position_dic)
    #Crop.create(crop_dic)
    #print(Farm.get_farm_by_user('5d77d4d4694d62037a1684e7').to_mongo())
    #print(User.get_by_id('5d77d4d4694d62037a1684e7').pk)

    #qs=PositionSchema.objects(farm='5d77d915acf3296b9e3c1c73', position_num=1).first()
    #print(CropSchema.objects(farm='5d77d915acf3296b9e3c1c73',position=qs.id).first().to_mongo())
    #pprint(Crop.get_crop_by_position('5d77d915acf3296b9e3c1c73', 1))
    #pprint(Position.get_position_list('5d77d915acf3296b9e3c1c73'))
    #pprint(Crop.get_crop_by_farm('5d77d915acf3296b9e3c1c73'))

    str_date = "20191005"
    str_date2="20191006"
    tp_date = datetime.now()
    date = datetime.strptime(str_date, "%Y%m%d")
    date2 = datetime.strptime(str_date2, "%Y%m%d")

    #pprint(CropPart.get_crop_part_detail("tomato1","stem1","20191005"))

    #date_obj = datetime.strptime("20191005", "%Y%m%d")
    #pprint(CropPart.get_crop_part_day_detail("tomato1", "stem1", date_obj))
