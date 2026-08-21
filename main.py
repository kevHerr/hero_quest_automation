import cv2 as cv
import numpy as np 
import sys



img = cv.imread("images/Board.jpg")


if img is None:
    sys.exit("Could not read the file")



height, width, size = np.shape(img)

columns_size = height // 19 # number of vertical rows
rows_size = width // 26 #number of horizontal rows 


image_array =  np.arange(1,495).reshape(19,26)

array_text = np.array2string(image_array)
lines = array_text.split('\n')


start_y = 30
line_height = 20


for i, line in enumerate(lines):
    y_position = start_y + (i * line_height)
    cv.putText(img,line, (50,y_position),cv.FONT_HERSHEY_COMPLEX, (1.0),(0,255,0), 3)
    
    
    
print(image_array)

#for px in range(0, height, columns_size):
#    cv.line(img,(0,0+px),(width,0+px),(0,255,0), 10 )

#for px in range(0,width,rows_size):
#    cv.line(img,(0+px,0),(0+px,height),(255,0,0),10)


print(img.shape)
cv.imshow("board", img)
cv.waitKey(0)

