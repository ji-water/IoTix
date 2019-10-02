from mongoengine import *

connect('testDB_develop')

class UserSchema(Document):
    user_id = StringField(required=True,unique=True)
    user_pw = StringField(required=True)
    user_name = StringField(required=True)

class FarmSchema(Document):
    name = StringField(required=True) #farm name
    manager = ReferenceField('UserSchema',reverse_delete_rule=CASCADE)
    phone_num = StringField()

#농장 별 작물 위치 정보
class PositionSchema(Document):
    farm = ReferenceField('FarmSchema',reverse_delete_rule=CASCADE)
    position_num = IntField(required=True) #상대 위치(사용자 식별용) 1~9
    position_name = StringField() #사용자 식별 이름(고민중)
    position_abs = StringField() #절대 위치

#특정 작물
class CropSchema(Document):
    farm = ReferenceField('FarmSchema',reverse_delete_rule=CASCADE)
    crop_name = StringField(required=True) #ex.tomato1
    crop_type = StringField(required=True) #tomato
    position = ReferenceField('PositionSchema', reverse_delete_rule=CASCADE)


#특정 작물 부위 정보
class CropPartSchema(Document):
    meta = {'collection': 'crop_part_schema'}
    crop = ReferenceField('CropSchema',reverse_delete_rule=CASCADE)
    crop_part_name = StringField(required=True) #stem1, crop별로 unique(예외처리하기)
    length = FloatField() #current len
    speed = FloatField()
    date = DateTimeField() #측정시간
