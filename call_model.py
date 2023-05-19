import tensorflow as tf
from keras.models import load_model
import numpy as np
import cv2
import tensorflow_text as tf_text



def cnn_model(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE) # load an image
    blur = cv2.medianBlur(img, 5) # apply median filter
    cv2.imwrite(path, blur) #Orignal
    image = tf.io.read_file(path)
    image = tf.image.decode_image(image,1)#creat image into pixels
    image = tf.image.convert_image_dtype(image, dtype=tf.float32) #normalize x/255
    image = tf.image.resize(image, [428,480]) # (60,60,1)
    image = tf.expand_dims(image, axis=0) # (1,60,60,1)
    model = load_model(r'C:\Users\bougu\Documents\GitHub\MyFinalInterface\Model', compile=False)
    
    dict_maladie = {0: 'Rien a signaler', 1: 'Diabtic', 2: 'Occlusion', 3: 'Oedeme papillaire', 4: 'Myopie', 5: 'Maculophatie'}

    pred = model.predict(image) # predict
          
    pred = np.argmax(pred)
    print(pred)
    maladie = dict_maladie[pred]
    return maladie
    


def cnn_test(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_image(image,1)#creat image into pixels
    image = tf.image.convert_image_dtype(image, dtype=tf.float32) #normalize x/255
    image = tf.image.resize(image, [60,60]) # (60,60,3)
    image = tf.expand_dims(image, axis=0) # (1,60,60,3)
    model = load_model('C:/Users/bougu/Desktop/STUDY/CODING/DL-Diabetic/model ver2' , compile=False)
    pred = model.predict(image) # [0.005, 0.00003, 0.99, 0.00 ....]
    print(pred)
    if pred<0.5:
        return "Normal"
    else:
        return "Diabetic"
