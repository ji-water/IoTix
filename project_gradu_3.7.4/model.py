from schema import UserSchema,FarmSchema,CropSchema,CropPartSchema,PositionSchema
from pprint import pprint
from bson import ObjectId
from datetime import datetime

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
                if isinstance(value,datetime):
                    data[key] = str(value)

        return qs_list

    @staticmethod
    def get_crop_part_detail(crop_name,part_name,date):
        crop_qs = CropSchema.objects(crop_name=crop_name,farm='5d77d915acf3296b9e3c1c73').first()
        part_qs = CropPartSchema.objects(crop=crop_qs.pk,crop_part_name=part_name)
        #date 쿼리 추가
        if part_qs.count == 0:
            return None

        qs_list = list(map(lambda part_data: part_data.to_mongo(), part_qs))  # convert to list

        # parse objectid to str
        for data in qs_list:
            for key, value in data.items():
                if isinstance(value, ObjectId):
                    data[key] = str(value)
                if isinstance(value, datetime):
                    data[key] = str(value)

        return qs_list
#
#     #crop_id 로 해당 작물이 가진 part 정보 가져오기
#
#     #part 선택하면 part 정보 가져오기 -> 여기까지 part default정보(default:오늘-6)
#
#     # crop part 날짜 입력시 (queryparam) 정보 계산+반환
#
#     @staticmethod
#     def get_info(crop_id=None,part=None,date=None):
#         if not crop_id:
#             return None
#         qs = CropSchema.objects(id=crop_id)
#
#         if part:
#             qs = CropPartSchema.objects(crop=crop_id, crop_part_name=part)
#
#         if date:
#             qs = qs.filter()

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
    user_dic = {'user_id': "kkkdeon", 'user_pw': "1234", 'user_name': "김도연"}
    #User.create(user_dic)
    farm_dic = {'name': 'farm1', 'manager': User.get_by_id('5d77d4d4694d62037a1684e7'),'phone_num': '01046244619'}
    crop_dic = {'farm': Farm.get_by_id('5d77d915acf3296b9e3c1c73'), 'crop_name':"tomato2", 'crop_type':"tomato", 'position': Position.get_by_id('5d9065696b602e2e595d873e')}
    position_dic = {'farm': Farm.get_by_id('5d77d915acf3296b9e3c1c73'), 'position_num': 2, 'position_abs': "gps주소", 'position_name': "2번 위치 desc"}
    crop_part_dic={'crop': Crop.get_by_id('5d9079e8c54b56aab045d9fb'),'crop_part_name':"stem2",'length':3.88,'speed':0.90,'date': datetime.now()}
    #CropPart.create(crop_part_dic)
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

