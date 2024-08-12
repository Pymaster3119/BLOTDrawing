from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve
import math
import tqdm
from multiprocessing import Pool
import time

def process(minx):
    image = Image.open('image.png').convert("L")
    image_array = np.array(image)
    maxx = minx + 16
    array_slice = np.zeros((256, image_array.shape[0] * 16))
    for x in range(minx, maxx): 
        try:
            for y in range(image_array.shape[1]):
                #Get intensity
                intensity = image_array[x][y].item()/16
                #Draw circle with appropriate radius
                for i in range(int(-intensity), int(intensity) + 1):
                    for j in range(int(-intensity), int(intensity) + 1):
                        if math.sqrt(i**2 + j**2) <= intensity:
                            array_slice[i * 16][16 * y + j] = 1
        except Exception as e:
            print(e)
    print("DONE")
    return minx, array_slice

global image_array, big_array


if __name__ == "__main__":
    
    #Load image
    image = Image.open('image.png').convert("L")
    image_array = np.array(image)
    plt.imshow(image_array, cmap='gray')
    plt.axis('off')
    plt.show()

    #Converting it to a bigger Numpy array
    big_array = np.zeros((0, image_array.shape[1] * 16))
    print(big_array.shape)
    with Pool() as p:
        results = p.map(process, range(0, image_array.shape[0], 16))
    for minx, array_slice in results:
        big_array = np.append(big_array, array_slice, axis=0)
        print(big_array.shape)

    plt.imshow(big_array, cmap='gray')
    plt.axis('off')
    plt.show()

    #Blot code generation
    with open("Blotcode.js", "w") as txt:
        txt.write("//Produced by Aditya Anand's Blotinator, not human-written\n")
        txt.write(f"setDocDimensions({big_array.shape[0]}, {big_array.shape[1]});\n")
        txt.write("const finalLines = [];\n")
        for x in tqdm.tqdm(range(big_array.shape[0])):
            for y in range(big_array.shape[1]):
                if big_array[x][y] == 1:
                    #Find line if applicable - along x axis
                    maxx = 0
                    for i in range(big_array.shape[0]):
                        try:
                            if big_array[x + i][y] == 1:
                                maxx = x + i
                                big_array[maxx][y] = 0
                            else:
                                break
                        except:
                            break
                    txt.write(f"finalLines.push([[{y}, {x}], [{y}, {maxx}]]);\n")
        txt.write("drawLines(finalLines);")