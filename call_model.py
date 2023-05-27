import tensorflow as tf
from keras.models import load_model
import numpy as np
import cv2
import tensorflow_text as tf_text



def cnn_model(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE) # load an image
    blur = cv2.medianBlur(img, 5) # apply median filter
    image = tf.image.convert_image_dtype(blur, dtype=tf.float32) #normalize x/255
    image = tf.expand_dims(image, axis=2)  # (x,y,1)
    image = tf.image.resize(image, [428,480])
    image = tf.expand_dims(image, axis=0) # (1,x,y,1)
    
    model = load_model(r'C:\Users\bougu\Documents\GitHub\MyFinalInterface\Model', compile=False)
    
    dict_maladie = {0: 'Rien a signaler', 1: 'Diabtic', 2: 'Occlusion', 3: 'Oedeme papillaire', 4: 'Myopie', 5: 'Maculophatie'}

    pred = model.predict(image) # predict
          
    pred = np.argmax(pred)
    print(pred)
    maladie = dict_maladie[pred]
    return maladie
    
