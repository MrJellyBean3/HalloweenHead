import torch
import serial
import time
import cv2
import ultralytics


def main():
    
    model = torch.hub.load("ultralytics/yolov5", 'custom', path="crowdhuman_yolov5m.pt")
    #model=yolov5.load("crowdhuman_yolov5m.pt")
    cam=cv2.VideoCapture(1)

    ser = serial.Serial('COM6', 2400)  # replace 'COM3' with the port where your Arduino is connected
    time.sleep(2)  # wait for the serial connection to initialize
    
    x_pos=0
    x_dir_val=1
    x_pos_write=1500

    y_pos=0
    y_dir_val=1
    y_pos_write=1500
    while True:
        try:
            ret,frame=cam.read()
            #hide output of model inference
            with torch.no_grad():
                results = model(frame)
                try:
                    #get results and put on cpu
                    result_vals=results.pred[0][0][0:4].cpu().numpy()
                    x_pos=int((result_vals[0]+result_vals[2])/2)-320
                    y_pos=int((result_vals[1]+result_vals[3])/2)-240
                    #print(x_pos,y_pos, x_pos_write, y_pos_write ," hs pred: ",result_vals,end="\r")
                    print(x_pos,y_pos,command,end="\r")
                except:
                    pass

            # X axis
            if x_pos>10:
                x_dir_val=1
            elif x_pos<-10:
                x_dir_val=-1
            else:
                x_dir_val=0
            x_magnitude=int(abs(x_pos**2.5)/1000)
            if x_magnitude>100:
                x_magnitude=100
            x_pos_write +=-x_magnitude*x_dir_val/5
            if x_pos_write<1000:
                x_pos_write=1000
            elif x_pos_write>2000:
                x_pos_write=2000

            # Y axis
            if y_pos>10:
                y_dir_val=1
            elif y_pos<-10:
                y_dir_val=-1
            else:
                y_dir_val=0
            y_magnitude=int(abs(y_pos**2.5)/1000)
            if y_magnitude>100:
                y_magnitude=100
            y_pos_write +=y_magnitude*y_dir_val/5
            if y_pos_write<700:
                y_pos_write=700
            elif y_pos_write>1650:
                y_pos_write=1650
            

            # Send the position to the Arduino
            command = f"{str(int(x_pos_write))},{str(int(y_pos_write))}\n"
            ser.write(command.encode('utf-8'))
            time.sleep(0.01)  # wait for the serial connection to respond


                
        except ValueError:
            print("Please enter a valid number")
        
        except KeyboardInterrupt:
            print("Exiting program")
            ser.close()  # close the serial connection
            break

if __name__ == "__main__":
    main()


