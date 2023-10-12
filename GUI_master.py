from tkinter import * 
import tkinter as tk
from tkinter import ttk, LEFT, END
import time
import numpy as np
import cv2
import os
from PIL import Image , ImageTk     
from PIL import Image # For face recognition we will the the LBPH Face Recognizer 
import pandas as pd
import openpyxl
import xlwrite,firebase.firebase_ini as fire
##############################################+=============================================================

root = tk.Tk()
root.configure(background="seashell2")
#root.geometry("1300x700")
import sqlite3
my_conn = sqlite3.connect('face.db')

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Face Attendance System")


#++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 =Image.open('a.png')
image2 =image2.resize((w,h), Image.ANTIALIAS)

background_image=ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) #, relwidth=1, relheight=1)


lbl = tk.Label(root, text="Facial Attendance System", font=('times', 40,' bold '), height=1, width=25,bg="white",fg="black")
lbl.place(x=370, y=25)

frame_alpr = tk.LabelFrame(root, text=" ----------------------------Process----------------------------- ", width=480, height=500, bd=5, font=('times', 15, ' bold '),bg="white")
frame_alpr.grid(row=0, column=0, sticky='nw')
frame_alpr.place(x=170, y=157)




################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 


def Create_database():
        
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    cap = cv2.VideoCapture(0)
    
#    id = input('enter user id')
    id=entry2.get()
    
    sampleN=0;
    
    while 1:
    
        ret, img = cap.read()
    
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
        for (x,y,w,h) in faces:
    
            sampleN=sampleN+1;
    
            cv2.imwrite("facesData/User."+str(id)+ "." +str(sampleN)+ ".jpg", gray[y:y+h, x:x+w])
    
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
            cv2.waitKey(100)
    
        cv2.imshow('img',img)
    
        cv2.waitKey(1)
    
        if sampleN > 40:
    
            break
    
    cap.release()
    entry2.delete(0,'end')
    cv2.destroyAllWindows()
def mail():
    print("Mail Sending")
    from subprocess import call
    call(["python", "mail.py"])
def update_label(str_T):
    #clear_img()
    result_label = tk.Label(root, text=str_T, width=40, font=("bold", 25), bg='bisque2', fg='black')
    result_label.place(x=300, y=400)

def Train_database():
           
    recognizer =cv2.face.LBPHFaceRecognizer_create();
    
    path="facesData"
    
    def getImagesWithID(path):
    
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]   
    
     # print image_path   
    
     #getImagesWithID(path)
    
        faces = []
    
        IDs = []
    
        for imagePath in imagePaths:      
    
      # Read the image and convert to grayscale
    
            facesImg = Image.open(imagePath).convert('L')
    
            faceNP = np.array(facesImg, 'uint8')
    
            # Get the label of the image
            
    
            ID= int(os.path.split(imagePath)[-1].split(".")[1])
    
             # Detect the face in the image
    
            faces.append(faceNP)
    
            IDs.append(ID)
    
            cv2.imshow("Adding faces for traning",faceNP)
    
            cv2.waitKey(10)
    
        return np.array(IDs), faces
    
    Ids,faces  = getImagesWithID(path)
    
    recognizer.train(faces,Ids)
    
    recognizer.save("trainingdata.yml")
    
    cv2.destroyAllWindows()

def Test_database():
    flag=0
    recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8, 100)
#    recognizer = cv2.face.FisherFaceRecognizer(0, 3000);
    
    recognizer.read('trainingdata.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    #iniciate id counter
    id = 0
    # names related to ids: example ==> Marcelo: id=1,  etc
    #names = ['None', 'Criminal person identified', 'Missing person', 'Criminal person identified', 'Criminal person identified', 'Missing person','Missing person'] 
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    while True:
        ret, img =cam.read()
#        img = cv2.flip(img, -1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray,1.3,8,minSize = (int(minW), int(minH)))
#        faces = faceCascade.detectMultiScale( 
#            gray,
#            scaleFactor = 1.2,
#            minNeighbors = 5,
#            minSize = (int(minW), int(minH)),
#           )
       # sample = 0
        filename='pandas_to_excel.xlsx'
        dict = {
            'item1': 1
            }
        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            # If confidence is less them 100 ==> "0" : perfect match
           
            if confidence < 50:
               
                #print(id)
                #name = names[id]
                id = id
                
                print(type(id))
                
                #
                #id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                
                         
                cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
                cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)
                cv2.putText(img, 'Number of Faces : ' + str(len(faces)), (40, 40), font, 1, (255, 0, 0), 2)
              
                if(id==1):
                    id='Aniruddha'
                    if((str(id)) not in dict):
                         filename=xlwrite.output('pandas_to_excel.xls','class1',1,id,'yes')
                         dict[str(id)]=str(id) 
                       
                elif (id==2):
                    id='Mrunalini'
                    if((str(id)) not in dict):
                          filename=xlwrite.output('pandas_to_excel.xls','class1',2,id,'yes')
                          dict[str(id)]=str(id)
                elif (id==3):
                    id='Audumber'
                    if((str(id)) not in dict):
                          filename=xlwrite.output('pandas_to_excel.xls','class1',3,id,'yes')
                          dict[str(id)]=str(id)
                elif (id==16):
                    id='Shreyash'
                    if((str(id)) not in dict):
                          filename=xlwrite.output('pandas_to_excel.xls','class1',16,id,'yes')
                          dict[str(id)]=str(id)
                elif (id==14):
                    id='Hrutik'
                    if((str(id)) not in dict):
                          filename=xlwrite.output('pandas_to_excel.xls','class1',14,id,'yes')
                          dict[str(id)]=str(id)
                elif (id==15):
                     id='kunal'
                     if((str(id)) not in dict):
                           filename=xlwrite.output('pandas_to_excel.xls','class1',15,id,'yes')
                           dict[str(id)]=str(id)         
                
                #cam.release()  
                #l = Label(frame_display1, text = "Authenticated User...Locker Successfully Open..") 
                #l.config(font =("Courier", 20, "bold"),fg= 'green') 
                #l.place(x=330,y=400)
                #l.pack()
                mail()
      
            else:
#                print(confidence)
                id = "unknown Person Identified"
                confidence = "  {0}%".format(round(100 - confidence))
                
                cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
                cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)  
                
               # l = Label(frame_display1, text = "Ooops!!!!!....Unauthenticated User..") 
               # l.config(font =("Courier", 25,"bold"),fg= 'red4') 
                #l.place(x=330,y=400)
                #l.pack() 
                update_label('Ooops!!!!!....Unauthenticated User..')
        
        
#        time.sleep(0.2)
        cv2.imshow('camera',img) 
#        print(flag)
        if flag==10:
            flag=0
            cam.release()
            cv2.destroyAllWindows()
            from subprocess import call
     
           
                    
        # k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
#        if k == 27:
#            break
        if cv2.waitKey(1) == ord('Q'):
            break

    # Do a bit of cleanup
#    print("\n [INFO] Exiting Program and cleanup stuff")
#    cam.release()
#    cv2.destroyAllWindows()
#  
    
    
def registration():
    
##### tkinter window ######
    
    print("Registration")
    from subprocess import call
    call(["python", "registration.py"]) 



def display():
    
##### tkinter window ######
    
    print("Display")
    from subprocess import call
    call(["python", "display.py"]) 


    

# def Test_database1():
    
#     face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#     cap = cv2.VideoCapture(0)
#     rec = cv2.face.LBPHFaceRecognizer_create(1,8,8,8);
#     rec.read("trainingdata.yml")
#     id=0
    
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     while 1:
#         ret, img = cap.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#         for (x,y,w,h) in faces:
#             cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#             id,conf=rec.predict(gray[y:y+h,x:x+w])
#             print(id,conf)
            
#             if(id==0):
#                 id="alok"
#             if id==3:
#                 id="Alka"
#             if id==1:
#                 id="Manju"
#             if id==6:
#                 id="Neha"
#             if id==2:
#                 id='Mamta'
                
                
#             if conf < 60:
#                 cv2.putText(img,str(id),(x,y+h),font,4,(255,255,255),2,cv2.LINE_AA)
#             else:
#                 cv2.putText(img,"No Match",(x,y+h),font,4,(255,255,255),2,cv2.LINE_AA)
                
            
    
# #            cv2.putText(img,str(id),(x,y+h),font,4,(255,255,255),2,cv2.LINE_AA)
#         cv2.imshow('img',img)
        
#         if cv2.waitKey(1) == ord('q'):
#             break
#         cap.release()
#         cv2.destroyAllWindows()
        
        
        
def ID():     
    my_conn = sqlite3.connect('face.db')
    r_set=my_conn.execute("SELECT * FROM User")
    i=0 # row value inside the loop 
    for student in r_set: 
        for j in range(len(student)):
            e =tk.Entry(frame_display, width=10, fg='blue') 
            e.grid(row=i, column=j) 
            e.insert(END, student[j])
        i=i+1
        
        
        
            
    



#################################################################################################################
def window():
    root.destroy()


button1 = tk.Button(frame_alpr, text="Registration Of User", command=registration,width=20, height=1, font=('times', 15, ' bold '),bg="purple",fg="white")
button1.place(x=100, y=40)

button1 = tk.Button(frame_alpr, text="Create Face Data", command=Create_database,width=15, height=1, font=('times', 15, ' bold '),bg="purple",fg="white")
button1.place(x=100, y=100)

button2 = tk.Button(frame_alpr, text="Train Face Data", command=Train_database, width=20, height=1, font=('times', 15, ' bold '),bg="purple",fg="white")
button2.place(x=100, y=160)

button3 = tk.Button(frame_alpr, text="Face Attendance", command=Test_database, width=20, height=1, font=('times', 15, ' bold '),bg="purple",fg="white")
button3.place(x=100, y=220)


entry2=tk.Entry(frame_alpr,bd=2,width=7)
entry2.place(x=310, y=110)


##
#
#button5 = tk.Button(frame_alpr, text="button5", command=window,width=20, height=1, font=('times', 15, ' bold '),bg="yellow4",fg="white")
#button5.place(x=10, y=280)


exit = tk.Button(frame_alpr, text="Exit", command=window, width=12, height=1, font=('times', 15, ' bold '),bg="red",fg="black")
exit.place(x=150, y=340)



root.mainloop()