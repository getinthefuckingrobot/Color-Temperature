def alphablend(color, tmpColor, tempStrength):
    return color * (1-tempStrength) + tmpColor * tempStrength

def colorTransform(tmpK):
    tmpK = tmpK/100

    if tmpK <= 66:
        red = 255

        tmpGreen = 99.4708025861 * np.log(tmpK) - 161.1195681661
        green = tmpGreen if tmpGreen <= 255 else 255

        if tmpK <= 19:
            blue = 0
        elif tmpK == 66:
            blue = 255
        else:
            tmpBlue = 138.5177312231 * np.log(tmpK-10) - 305.0447927307
            blue = tmpBlue if tmpBlue <= 255 else 255

    else:
        tmpRed = 329.698727446 * ((tmpK-60) ** -0.1332047592)
        red = tmpRed if tmpRed<= 255 else 255

        tmpGreen = 288.1221695283 * ((tmpK-60) ** -0.0755148492)
        green = tmpGreen if tmpGreen <= 255 else 255

        blue = 255

    return [red, green, blue]

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('train_poor_set/1/1.jpg')
rows, cols, ch = img.shape

tmpColor = colorTransform(1400)

img1 = img.copy()

for i in range(rows):
    for j in range(cols):
        color = np.copy(img[i,j])
        lum = int((int(max(color))+int(min(color)))/2)
        for k in [0,1,2]:
            color[k] = alphablend(color[k], tmpColor[k], 0.5)
        updatedColor = np.array([[color]])
        updatedColor_hls = cv2.cvtColor(updatedColor, cv2.COLOR_RGB2HLS)
        updatedColor_hls[0,0,1] = lum
        updatedColor = cv2.cvtColor(updatedColor_hls, cv2.COLOR_HLS2RGB)

        img1[i,j] = updatedColor


plt.imshow(img),plt.title('Input'), plt.figure(figsize=(6, 6), dpi=100)
plt.imshow(img1),plt.title('Output'), plt.figure(figsize=(6, 6), dpi=100)

plt.show()