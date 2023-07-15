import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array, load_img


# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    port = settings.REDIS_PORT,
    db = settings.REDIS_DB_ID,
    host = settings.REDIS_IP
)

# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = ResNet50(include_top = True, weights = 'imagenet')

def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    class_name = None
    pred_probability = None

    
    img = image.load_img(
        os.path.join(settings.UPLOAD_FOLDER, image_name),
        target_size = (224, 224)
    )
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis = 0)
    img_batch = preprocess_input(img_batch)

    preds = model.predict(img_batch)
    prob = decode_predictions(preds, top = 1)
    
    class_name = prob[0][0][1]
    pred_probability = prob[0][0][2]

    return class_name, round(pred_probability, 4)

def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        #   2. Run your ML model on the given data
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        
        _, msg = db.brpop(settings.REDIS_QUEUE)
        print(msg)
        msg = json.loads(msg.decode('utf-8'))
        image_name = msg['image_name']
        pred, score = predict(image_name)

        preddict = {
            'prediction' : pred,
            'score' : str(score)
        }

        output = json.dumps(preddict)

        db.set(msg['id'], output)
        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)

if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()