from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from django.shortcuts import render
import cv2
import numpy as np  
import cvzone
import pickle
from django.views import View
from . forms import CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings


# Create your views here.

def home(request):
    return render(request, 'home.html',locals())

def contact(request):   
    return render(request, 'contact.html',locals())

def video_feed(request):
    
    cap = cv2.VideoCapture('http://192.168.0.196:8080/video')

    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)

    width, height = (250-50), (300-192)
    
    new_width, new_height = 5000, 2500

    def checkParkingSpace(img, imgPro):  
        spaceCounter = 0
        for pos in posList:
            x, y = pos

            imgCrop = imgPro[y:y+height, x:x+width]
            count = cv2.countNonZero(imgCrop)
            cvzone.putTextRect(img, str(count), (x, y+height-2), scale=1, thickness=2, offset=0, colorR=(0, 0, 255))

            if count < 500:
                color = (0, 255, 0)  
                thickness = 5
                spaceCounter += 1
            else:
                color = (0, 0, 255)
                thickness = 2
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        
        cvzone.putTextRect(img, f'FREE {str(spaceCounter)}/{len(posList)}', (450, 50), scale=2, thickness=5, offset=20, colorR=(0, 200, 0))

    def generate_frames():
        while True:
            success, img = cap.read()

            if not success:
                print("Error: Failed to capture frame from the camera.")
                break
            
            img = cv2.resize(img,(1200,800))
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
            imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY_INV, 25, 16)

            imgMedian = cv2.medianBlur(imgThreshold, 5)
            kernel = np.zeros((3, 3), np.uint8)
            imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

            checkParkingSpace(img, imgDilate)  

            _, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')



class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()       
        return render(request, 'customerregistration.html',locals())
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'customerregistration.html',locals())
    
    
