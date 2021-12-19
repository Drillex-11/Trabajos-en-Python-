import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time


class App:
    def __init__(self, master):
        self.master=master
        self.master.title('Detector de rostro')
        self.master.resizable(0,0)
        
        self.idx=tk.IntVar(0)
        self.idx2=tk.IntVar(0)
        self.recent=tk.IntVar(0)
        self.idx2.set(-1)
        self.Recent_photos=[]
        
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
        self.safety = False
        
        self.eye_cascade = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        
        self.cap=cv2.VideoCapture(0)
        self.width=int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height=int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, borderwidth=1, relief=tk.SUNKEN)
        self.canvas.pack()
        
        self.cam_loop()
    
    def cam_loop(self):
            
            ret,frame=self.cap.read()
            self.photo_to_take=frame
            if ret:
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                faces = self.face_cascade.detectMultiScale(gray, 1.2,8,minSize=(70,70))

                cv2.putText(frame,f"Fotos: {self.idx.get()}", (20,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
               
                if len(faces)==0:
                    cv2.putText(frame,"Detectando rostro...", (15,self.height-15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                if self.recent.get()>0:
                    self.recent.set(self.recent.get()-50)
                    cv2.putText(frame,"Guardada!", (self.width-150,self.height-15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
                for x,y,w,h in faces:
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                    cv2.putText(frame,"Rostro detectado", (x-5, y-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)
                    ROI=gray[y:y+h,x:x+h]
                    
                    eyes = self.eye_cascade.detectMultiScale(ROI, 1.105,6,minSize=(25,25))
                    
                    for x2,y2,w2,h2 in eyes:
                        cv2.rectangle(frame, (x+x2,y+y2),(x+x2+w2,y+y2+h2),(0,0,255),2)
                    if len(eyes)==2 and self.safety==False:
                        self.safety=True
                    elif len(eyes)==1 and self.safety:
                        self.safety=False
                        self.idx.set(self.idx.get()+1)
                        self.take_photo()
                        
                        self.show_image()

                        
                        
                for foto in range(len(self.Recent_photos)):
                    pass
                try:
                    photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                    self.canvas.create_image(0,0,image=photo,anchor='nw')
                    self.canvas.image=photo 
                except:
                    pass

            self.master.after(50, self.cam_loop)
            
    def take_photo(self):
        self.dia=int(time.strftime("%Y%m%d", time.localtime()))
        self.hora=int(time.strftime("%H%M%S", time.localtime()))
        self.recent.set(2000)
        self.vez=self.idx.get()
        self.idx2.set(self.idx2.get()+1)
        if self.idx2.get()==4:
            self.idx2.set(0)
        self.Recent_photos.insert(0,cv2.resize(cv2.cvtColor(self.photo_to_take,cv2.COLOR_BGR2RGB),(120,120)))
        if len(self.Recent_photos)>4:
            self.Recent_photos.pop(4)
        cv2.imwrite(f'{self.dia}_{self.hora}_{self.vez}.png', self.photo_to_take)
    
    def close_window(self):
        if self.cap.isOpened():
            self.cap.release()
        self.master.destroy()
        
    def show_image(self):
        pass
        roots=tk.Toplevel()
        Photos(roots,self.dia,self.hora,self.vez)

class Photos:
    def __init__(self,master,dia,hora,vez):
        pass
        self.master=master
        self.master.resizable(0,0)
        self.master.title("Foto capturada")
        self.master.protocol("WM_DELETE_WINDOW", self.close_window)
        width,height=Image.open(f"{dia}_{hora}_{vez}.png").size
        self.master.geometry(f"{width}x{height}")
        self.test=ImageTk.PhotoImage(Image.open(f"{dia}_{hora}_{vez}.png"))
        
        self.label1=tk.Label(master,image=self.test)
        self.label1.image=self.test
        
        self.label1.place(x=0,y=0)
        
        self.master.after(1500, self.close_window)
    def close_window(self):
        self.master.destroy()
        
root=tk.Tk()
app=App(root)
root.mainloop()