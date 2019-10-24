0. 버전
	python 3.6.8
	tensorflow 1.11.0
	keras 2.2.4

1. 파일 설명
	-IOTIX_length_L2.py 
		100일간 토마토 길이 변화량을 임의 생성한 sample191020_5.json file 읽고 모델 학습하는 코드
		Lookback3, output1 -> 반복 output 출력하여 총 '7일'간 예측 데이터 출력
		LSTM16 DENSE1 LR0.05 EPOCH500
	-IOTIX_predict.py 
		3일간 길이 변화량을 json 파일 형태로 불러와 총 7일간 예측 데이터 출력하는 예측 코드
		저장된 mnist_mlp_model_2.h5 모델을 불러와서 총 '7일'간 예측 데이터 출력

2. 예측 코드 사용법
	1) IOTIX_predict.py 이 존재하는 폴더에 3일 간 길이 변화량 데이터 json 파일이 존재해야함
		* 쿼리 결과 json 파일 생성이 번거롭다면 코드 내에서 입력받는 형식으로 변경해도 됨
		** 파일 저장 형태 유의할 것 {"test":[]} 가 무조건 존재해야하고 [ ] 안에 3일 간 데이터 있어야함 
	2) 데이터를 무사히 불러온다면 '7일'간 예측 데이터를 print 함
		* print한 것을 return으로 바꿔야할 수도 있음
		** predictY 형태 유의 해야함....