import cv2
import numpy as np
import pickle

def build_squares(img):
	x, y, w, h = 420, 140, 10, 10
	d = 10
	imgCrop = None
	crop = None
	for i in range(10):
		for j in range(5):
			if np.any(imgCrop == None): #np.any는 조건에 맞는값있으면 True 반환
				imgCrop = img[y:y+h, x:x+w]
			else:
				imgCrop = np.hstack((imgCrop, img[y:y+h, x:x+w]))
			#print(imgCrop.shape)
			cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 1)#영상에 사각형 그리기(img,시작점좌표,종료점좌표,색상,두께)
			x+=w+d
		if np.any(crop == None):
			crop = imgCrop
		else:
			crop = np.vstack((crop, imgCrop)) 
		imgCrop = None
		x = 420
		y+=h+d
	return crop

def get_hand_hist():
	cam = cv2.VideoCapture(1)
	if cam.read()[0]==False:
		cam = cv2.VideoCapture(0)
	x, y, w, h = 300, 100, 300, 300
	flagPressedC, flagPressedS = False, False
	imgCrop = None
	while True:
		img = cam.read()[1]
		img = cv2.flip(img, 1)
		img = cv2.resize(img, (640, 480))
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #이미지 변환, HSV로
		
		keypress = cv2.waitKey(1) #1초뒤에 다음 소스 실행
		if keypress == ord('c'):		#아스키코드값으로 변경
			hsvCrop = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2HSV) 
			flagPressedC = True
			hist = cv2.calcHist([hsvCrop], [0, 1], None, [180, 256], [0, 180, 0, 256])#(이미지, 채널수, 마스크, 히스트사이즈, 히스트 빈 경계값 배열)
			cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX) #정규화 분포 시켜주는거임, 이미지가 자연스럽게 연결되도록
		elif keypress == ord('s'):
			flagPressedS = True	
			break
		if flagPressedC:	
			dst = cv2.calcBackProject([hsv], [0, 1], hist, [0, 180, 0, 256], 1) #역투영(입력영상,채널번호리스트,히스토그램,(히스토그램최대,최소),추가곱할값
			dst1 = dst.copy()
			disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))#이미지 형태 변환, 타원형
			cv2.filter2D(dst,-1,disc,dst)#이미지 부드럽게 사용, 가우시안과 미디언블러 같이 사용
			blur = cv2.GaussianBlur(dst, (11,11), 0)
			blur = cv2.medianBlur(blur, 15)
			ret,thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
			thresh = cv2.merge((thresh,thresh,thresh))
			#cv2.imshow("res", res)
			cv2.imshow("Thresh", thresh)
		if not flagPressedS:
			imgCrop = build_squares(img)
		#cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
		cv2.imshow("Set hand histogram", img)
	cam.release()
	cv2.destroyAllWindows()#열린창 모두 닫기
	with open("hist", "wb") as f:
		pickle.dump(hist, f)

