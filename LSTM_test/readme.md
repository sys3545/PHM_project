# LSTM model test
시계열 데이터를 활용한 LSTM 모델 활용 테스트
tensorflow 기반, google colab 사용


### create_model.ipynb - 모델을 생성
모델은 tensorflow.keras 의 LSTM을 사용합니다
sensor_data.csv 파일의 humidity column을 dataset으로 설정합니다
lstm past_set 을 10개로 설정합니다
전체 데이터 셋의 80% 학습 데이터, 20%를 테스트 데이터로 사용합니다
rmse = 0.195296


### saved_model.h5 - create_model에서 생성한 모델을 h5 형태로 저장
향후 학습 과정 없이 모델을 사용하기 위해 모델을 따로 분리하여 파일로 저장합니다


### test_saved_model.ipynb - 생성된 모델을 사용하여 새로운 데이터셋을 적용
새로운 데이터셋을 받아 예측이 잘 되는지 테스트합니다
분리된 model 파일을 사용하여 모델 학습 부분이 없습니다.
rmse = 0.07456


### sensor_data.csv - 모델 학습에 사용한 데이터 파일입니다

### sensor_date1.csv - 학습한 모델을 테스팅하기 위한 데이터 파일입니다

