import cv2
import numpy as np
import matplotlib.pyplot as plt

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

def colorTemperature(img, temperature):
    tmpColor = np.array(colorTransform(temperature))

    img_hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)

    updatedColor = np.array(alphablend(img, tmpColor, 0.5), dtype='uint8')

    updatedColor_hls = cv2.cvtColor(updatedColor, cv2.COLOR_RGB2HLS)
    updatedColor_hls[:,:,1] = img_hls[:,:,1]
    updatedColor = cv2.cvtColor(updatedColor_hls, cv2.COLOR_HLS2RGB)

    return updatedColor