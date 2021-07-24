# Import Libraries
from os import name
import cv2 #openCV2 for python
import pandas as pd 
import argparse as arg #library for commandline parse

#Globalas values
click = False
r = g = b = xpos = ypos = 0


#You will have to give path to image in command line after -i command
# $ python3 filename.py -i path_to_image/image.jpg 
# for example 
# $ python3 colors.py -i images.jpeg

ap = arg.ArgumentParser()
ap.add_argument('-i','--input', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Reading image with opencv
img = cv2.imread(img_path)

#Reading CSV file with color dataset
index=["color","color_name","hex","R","G","B"]
color_df = pd.read_csv('colors.csv',names=index, header=None)
#Creating DataFrame pandas format
color_df = pd.DataFrame(color_df)


#Define function to calculate rgb values where you double click on pixel
def rgb_calc(event, x,y,flags,param):

    if event == cv2.EVENT_LBUTTONDBLCLK:

        global b,g,r,xpos,ypos, click
        click = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)


#Define function to calculate color name using minimal distance
def Color_Name(R,G,B):

    min_distance = 10000
    
    for i in range(len(color_df)):

        d = abs(R- int(color_df.loc[i,"R"])) + abs(G- int(color_df.loc[i,"G"]))+ abs(B- int(color_df.loc[i,"B"]))
        if(d<=min_distance):
            min_distance = d
            colorname = color_df.loc[i,"color"]
    return colorname


#Creating input where input will display
cv2.namedWindow('input')

#Setting mouse callback
cv2.setMouseCallback('input',rgb_calc)


while(1):
    cv2.imshow("input",img)
    if (click):

        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        #Dispaly color name and rgb percentage
        text = Color_Name(r,g,b) + ' R='+ str(r) + ' G='+ str(g) + ' B='+ str(b)
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #When colors is light text will be black
        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

        click=False

    #Break the loop when user hits 'esc' key 
    if cv2.waitKey(20) & 0xFF ==27:
        break


cv2.destroyAllWindows()


