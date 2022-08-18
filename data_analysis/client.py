import numpy as np
import recognize_gesture as recog
from keras.models import load_model
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#손 색상 인식(c:프로그램창 오픈 / s:저장)(hist 파일 없으면 새로생성됨)
#인식하기(c)
model = load_model('cnn_model_keras2.h5')



def recog_():
    recog.recognize(model)

if __name__ == '__main__':
    recog_()

    



