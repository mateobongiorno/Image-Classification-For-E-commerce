<h1>Image Classification For E-commerce</h1>

  <h2>Project Overview</h2>
  <p>Welcome to the Image Classification For E-commerce project! In this project, we will be building an image classification system for an online retail company. The goal of this system is to classify the contents of uploaded images to ensure that inappropriate or unacceptable images are not displayed on the website.</p>

  <h2>Problem Statement</h2>
  <p>The retail company allows customers to upload photos when submitting product reviews. However, they discovered that many of the uploaded photos were not suitable and should not be visible on the website. The challenge is to develop an image classification system that can automatically predict and classify the content of each uploaded photo.</p>

  <h2>Solution Overview</h2>
  <p>To address the problem, we will build an image classification model that can predict the content of each uploaded photo. We will design a web service architecture that includes a web server, API endpoint, image classification service, and a database. The web service will provide an API that can be easily integrated into the existing e-commerce website.</p>

  <h2>Getting Started</h2>
  <ol>
    <li>Install Docker: Make sure you have Docker installed on your machine.</li>
    <li>Clone the Repository: Clone the project repository from GitHub.</li>
    <li>Build and Run the Services: Use Docker Compose to build and run the web service containers.</li>
    <li>Access the Web Interface: Open your web browser and navigate to the provided URL to access the e-commerce website.</li>
  </ol>

  <h2>Project Structure</h2>
  <p>Here is the structure of the Image-Classification-For-E-commerce project:</p>
  
  <pre>
  .
  ├── api
  │   ├── Dockerfile
  │   ├── app.py
  │   ├── middleware.py
  │   ├── views.py
  │   ├── settings.py
  │   ├── utils.py
  │   ├── templates
  │   │   └── index.html
  │   └── tests
  │       ├── test_api.py
  │       └── test_utils.py
  ├── model
  │   ├── Dockerfile
  │   ├── ml_service.py
  │   ├── settings.py
  │   └── tests
  │       └── test_model.py
  ├── stress_test
  │   └── locustfile.py
  ├── docker-compose.yml
  ├── README.html
  └── tests
      └── test_integration.py
  </pre>
  
  <p>The project is organized into several modules:</p>
  
Let's take a quick overview on each module:

- api: It has all the needed code to implement the communication interface between the users and our service. It uses Flask and Redis to queue tasks to be processed by our machine learning model.
    - `api/app.py`: Setup and launch our Flask API.
    - `api/views.py`: Contains the API endpoints. You must implement the following endpoints:
        - *upload_image*: Displays a frontend in which the user can upload an image and get a prediction from our model.
        - *predict*: POST method which receives an image and sends back the model prediction. This endpoint is useful for integrating other services and platforms because we can access it from any other programming language.
        - *feedback*: Endpoint used to get feedback from users when the prediction from our model is incorrect.
    - `api/utils.py`: Implements some extra functions used internally by our API.
    - `api/settings.py`: It has all the API settings.
    - `api/templates`: Here we put the .html files used in the front.
    - `api/tests`: Test suite.
- model: Implements the logic to get jobs from Redis and process them with our Machine Learning model. When we get the predicted value from our model, we must encode it on Redis again so it can be delivered to the user.
    - `model/ml_service.py`: Runs a thread in which it gets jobs from Redis, processes them with the model, and returns the answers.
    - `model/settings.py`: Settings for our ML model.
    - `model/tests`: Test suite.
- tests: This module contains integration tests so we can properly check our system's end-to-end behavior is expected.

You can also take a look at the file `System_architecture_diagram.png` to have a graphical description of the microservices and how the communication is performed.

  <h2>Testing</h2>
  <p>We have provided both integration and unit tests to ensure the correctness and functionality of the image classification system. Please follow the instructions I've included to run the tests and verify the system's behavior.</p>

  <h2>Stress Testing with Locust</h2>
  <p>For stress testing, we provide a Locust file that allows you to simulate multiple users accessing the system concurrently. You can easily launch more instances for a particular service using `--scale SERVICE=NUM` when running `docker-compose up` command (https://docs.docker.com/compose/reference/up/). Scale `model` service to 2 or even more instances and check the performance with locust. </p> 
  <pre> docker-compose up --scale model=5 </pre>

  <h2>User Feedback</h2>
  <p> The users can report using the service UI when a model prediction is wrong. Store the reported image path and the model prediction in a `.csv` file inside the folder `/src/feedback` so we can access it later to check those cases in which our Machine Learning model failed according to users.</p>

  <h2></h2>
  <p>By this, we have come to the end of this project.

Thanks for trying to understand it, I hope you like it, Mateo.</p>
