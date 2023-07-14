import json
import time
from uuid import uuid4

import redis
import settings


# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    port = settings.REDIS_PORT,
    db = settings.REDIS_DB_ID,
    host = settings.REDIS_IP
)

def model_predict(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    # Assign an unique ID for this job and add it to the queue.
    # We need to assing this ID because we must be able to keep track
    # of this particular job across all the services
    job_id = str(uuid4())

    # Create a dict with the job data we will send through Redis having the
    # following shape:
    # {
    #    "id": str,
    #    "image_name": str,
    # }
    job_dict =     {
        "id": job_id,
        "image_name": str(image_name)
    }

    job_data = json.dumps(job_dict)

    # Send the job to the model service using Redis
    # Hint: Using Redis `lpush()` function should be enough to accomplish this.
    db.lpush(settings.REDIS_QUEUE, job_data)

    # Loop until we received the response from our ML model
    while True:
        # Attempt to get model predictions using job_id
        # Hint: Investigate how can we get a value using a key from Redis
        
        rpse = db.get(job_id)
        if rpse is None:
            time.sleep(settings.API_SLEEP)
            continue
        rpse_dict = json.loads(rpse)
        prediction = rpse_dict['prediction']
        score = rpse_dict['score']
        # Don't forget to delete the job from Redis after we get the results!
        # Then exit the loop
        
        db.delete(job_id)
        break
        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)
    return prediction, score
