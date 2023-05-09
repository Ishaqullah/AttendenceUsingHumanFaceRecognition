import cv2
import numpy as np
import face_recognition as fr
import dlib
import datetime
import os
import csv

path = 'Image DataSet'
images = [] 
ClassNames = []
imgList = os.listdir(path)
print('Extracting the Images from the Data Set folder! ',imgList) 

for cl in imgList: 
    CurrentImage = cv2.imread(f'{path}/{cl}')
    images.append(CurrentImage)
    ClassNames.append(os.path.splitext(cl)[0])
print('The Names of the Images in the Data Set Folder are: ',ClassNames)



def GenerateEncodings(images):
    Encodelist = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        Encodelist.append(encode)
    return Encodelist

KnownEncodeList=GenerateEncodings(images)
print('Encodings of the Images have been completed!')





attendance_dict = {}

def mark_attendance(name):
    today = datetime.date.today()
    date_str = today.strftime('%Y-%m-%d')
    filename = f'{date_str}.csv'

    if not os.path.isfile(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'Attendance'])
            writer.writerow([name, 'Present'])
    else:
        with open(filename, mode='r', newline='') as input_file:
            reader = csv.reader(input_file)
            header = next(reader)

            name_col = header.index('name')
            attendance_col = header.index('Attendance')

            name_present = False
            name_absent = False

            for row in reader:
                if row[name_col] == name:
                    if row[attendance_col] == 'Present':
                        name_present = True
                    elif row[attendance_col] == 'Absent':
                        name_absent = True

            if not name_present and not name_absent:
                with open(filename, mode='a', newline='') as output_file:
                    writer = csv.writer(output_file)
                    writer.writerow([ name, 'Present'])


cam = cv2.VideoCapture(0)


while True:
    Success, img = cam.read()
    ImageScale = cv2.resize(img,(0,0),None,0.25,0.25)
    ImageScale = cv2.cvtColor(ImageScale,cv2.COLOR_BGR2RGB)

    CurrentFrame = fr.face_locations(ImageScale)
    EncodeCurrentFrame = fr.face_encodings(ImageScale,CurrentFrame)


    for EncodeFace, FaceLoc in zip(EncodeCurrentFrame,CurrentFrame):
        matches = fr.compare_faces(KnownEncodeList,EncodeFace)
        Facedis = fr.face_distance(KnownEncodeList,EncodeFace)
        print('Minimal Face Distances: ', Facedis)
        matchIndex = np.argmin(Facedis)

        if matches[matchIndex]:
            Name = ClassNames[matchIndex].upper()
            print('Name: ',Name)
            mark_attendance(Name)
            y1,x2,y2,x1 = FaceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,Name,(x1+6,y2-6),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
    cv2.imshow('WebCam',img)
    cv2.waitKey(1)

































