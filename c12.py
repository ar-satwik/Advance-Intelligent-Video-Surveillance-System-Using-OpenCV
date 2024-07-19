import cv2
import time
import datetime
cap=cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
detection = False

detection_stopped_time = None

timer_started = False

SECONDS_AFTER_DETECTION=5
f_size = (int(cap.get(3)), int(cap.get(4)))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# loop over the frames from the video stream
while True:
    
    # Capture frame by frame
    _,frame = cap.read()
    
    # Converting frames to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # detect faces in the input frame using haar cascade face detector
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) + len(bodies) > 0:
        
        if detection:
            timer_started = False
        
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, f_size)
            print("Started Recording!")
   
    elif detection:
        
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print("Recording Stopped!")
                
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)
        
    #display the resulting frame
    
    cv2.imshow("Lucky Camera", frame)
    
    #if the 'q' key was pressed,break from the loop 
    if cv2.waitKey(1) == ord('q'):
                            break

out.release()
cap.release()
cv2.destroyAllWindows()
