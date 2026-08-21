import cv2 as cv
import numpy as np 
import sys 


def create_bar(height, width, color ):
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    return bar, (red, green, blue)

img = cv.imread("images/HeroQuestMap.jpg")

if img is None:
    sys.exit("could not read the image.")

height, width, _ = np.shape(img)

data = np.reshape(img, (height * width,3))
data = np.float32(data)

number_k = 10

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
flags = cv.KMEANS_RANDOM_CENTERS

compactness, labels, centers = cv.kmeans(data, number_k, None, criteria, 10, flags) # type: ignore

font = cv.FONT_HERSHEY_COMPLEX
bars = []
rgb_values = []

for index, row in enumerate(centers):
    bar, rgb = create_bar(200,200, row)
    bars.append(bar)
    rgb_values.append(rgb)
    
img_bar = np.hstack(bars)



for index, row in enumerate(rgb_values):
    image = cv.putText(img_bar, f'{index + 1}. RGB: {row}', (5 + 200 * index, 200 - 10),
                        font, 0.5, (255, 0, 0), 1, cv.LINE_AA)
    print(f'{index + 1}.RGB{row}')
    
cv.imshow('Image', img)
cv.imshow('dominant Colors', img_bar)    
cv.waitKey(0)


