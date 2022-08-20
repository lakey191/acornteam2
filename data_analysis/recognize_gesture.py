import cv2, pickle
import numpy as np
import tensorflow as tf
import os
#import sqlite3
from keras.models import load_model
import pyautogui
import time
import make_set_hand as mk

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
prediction = None
model = load_model('cnn_model_keras2.h5')

def get_image_size():
	#img = cv2.imread('dataset/0/100.jpg', 0)
	#print(img.shape)
	img=np.zeros([50,50])
	
	return img.shape

image_x, image_y = get_image_size()


def keras_process_image(img):
	img = cv2.resize(img, (image_x, image_y))
	img = np.array(img, dtype=np.float32)
	img = np.reshape(img, (1, image_x, image_y, 1))
	return img

def keras_predict(model, image):
	processed = keras_process_image(image)
	pred_probab = model.predict(processed)[0]
	pred_class = list(pred_probab).index(max(pred_probab))
	return max(pred_probab), pred_class

'''
db에서 갖고오는거
def get_pred_text_from_db2(pred_class):
	conn = sqlite3.connect("gesture_db.db")
	cmd = "SELECT g_name FROM gesture WHERE g_id="+str(pred_class)
	cursor = conn.execute(cmd)
	for row in cursor:
		return row[0]
'''
#db에서 안가져오고 바로
def get_pred_text_from_db(pred_class):
	ges=None
	if pred_class==0:
		ges='up'
	elif pred_class==1:
		ges='down'
	elif pred_class==2:
		ges='right'
	elif pred_class==3:
		ges='left'
	elif pred_class==4:
		ges='stop'
	return ges
	

def split_sentence(text, num_of_words):

	list_words = text.split(" ")
	length = len(list_words)
	splitted_sentence = []
	b_index = 0
	e_index = num_of_words
	while length > 0:
		part = ""
		for word in list_words[b_index:e_index]:
			part = part + " " + word
		splitted_sentence.append(part)
		b_index += num_of_words
		e_index += num_of_words
		length -= num_of_words
	return splitted_sentence

def put_splitted_text_in_blackboard(blackboard, splitted_text):
	y = 200
	for text in splitted_text:
		cv2.putText(blackboard, text, (4, y), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 255, 255))
		y += 50

def get_hand_hist():
	try :
		with open("hist", "rb") as f:
			hist = pickle.load(f)
	except : 
		mk.get_hand_hist()
		with open("hist", "rb") as f:
			hist = pickle.load(f)
	return hist

def recognize(model):
	global prediction
	cam = cv2.VideoCapture(1)
	if cam.read()[0] == False:
		cam = cv2.VideoCapture(0)
	hist = get_hand_hist()
	x, y, w, h = 300, 100, 300, 300
	while True:
		text = ""
		img = cam.read()[1]
		
		img = cv2.flip(img, 1)
		img = cv2.resize(img, (640, 480))
		imgCrop = img[y:y+h, x:x+w]
		imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		dst = cv2.calcBackProject([imgHSV], [0, 1], hist, [0, 180, 0, 256], 1)
		#img(보여질이미지)->blur->thresh로예측
		disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
		cv2.filter2D(dst,-1,disc,dst)
		blur = cv2.GaussianBlur(dst, (11,11), 0)
		blur = cv2.medianBlur(blur, 15)
		thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
		thresh = cv2.merge((thresh,thresh,thresh))
		thresh = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
		thresh = thresh[y:y+h, x:x+w]
		(openCV_ver,_,__) = cv2.__version__.split(".")
		#print(openCV_ver)
		#if openCV_ver=='3':
		contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
		#elif openCV_ver=='4':
		#	contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
		#흑백으로 출력하기
		cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
		resize_img=cv2.resize(img,(350,300))
		img_gray = cv2.cvtColor(resize_img, cv2.COLOR_RGB2GRAY)		
		#이미지 보여주기
		cv2.imshow("Recognizing gesture",img_gray)
		cv2.moveWindow("Recognizing gesture",1200,200)
		if len(contours) > 0:
			contour = max(contours, key = cv2.contourArea)
			#print(cv2.contourArea(contour))
			if cv2.contourArea(contour) > 10000:
				x1, y1, w1, h1 = cv2.boundingRect(contour)
				save_img = thresh[y1:y1+h1, x1:x1+w1]
				
				if w1 > h1:
					save_img = cv2.copyMakeBorder(save_img, int((w1-h1)/2) , int((w1-h1)/2) , 0, 0, cv2.BORDER_CONSTANT, (0, 0, 0))
				elif h1 > w1:
					save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1-w1)/2) , int((h1-w1)/2) , cv2.BORDER_CONSTANT, (0, 0, 0))
				
				pred_probab, pred_class = keras_predict(model, save_img)
				
				

				if pred_probab*100 > 97:
					text = get_pred_text_from_db(pred_class)
					print(text)
					if text=='up':
						pyautogui.press('up',interval=1)
						
					elif text=='down':
						pyautogui.press('down',interval=1)
						
					elif text=='left':
						pyautogui.press('left',interval=1)
						
					elif text=='right':
						pyautogui.press('right',interval=1)
						
					elif text=='stop':
						print('Stopping')
					
				else :
					print('get motion precisely')
					time.sleep(1)

				
		
		
		
		
		
		#blackboard = np.zeros((100, 100, 3), dtype=np.uint8)
		#cv2.putText(blackboard, text, (30, 200), cv2.FONT_HERSHEY_TRIPLEX, 1.3, (255, 255, 255))
		#splitted_text = split_sentence(text, 2)
		#put_splitted_text_in_blackboard(blackboard, splitted_text)
		#res = np.vstack((resize_img, blackboard))
		

		

		# 흑백반전 출력(모델에 들어가는 값)
		# cv2.imshow("thresh", thresh)
		if cv2.waitKey(1) == ord('q'):
			break


