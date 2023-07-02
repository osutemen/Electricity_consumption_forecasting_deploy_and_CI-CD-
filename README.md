
# Electricity Consumption Forecasting and Deploy and CI/CD

This project has been completed as the final project of VBO's 3rd MLOps bootcamp. A time-series model was built using real-time energy consumption data acquired by EPİAŞ. Based on this model, forecasting are made for a given day and hour.



## 1. Dataset:
For this project, we obtained the electricity consumption data from the "Real-Time Consumption" section of the website https://seffaflik.epias.com.tr/transparency/tuketim/gerceklesen-tuketim/gercek-zamanli-tuketim.xhtml. The dataset provides real-time electricity consumption information, which is continuously updated.

## 2. Modeling:
### 2.1. Daily Consumption Prediction:
Firstly, I developed a Machine Learning model to predict the electricity consumption for the next 5 days. This model was trained using historical consumption data to forecast future daily consumption.

### 2.2. Hourly Consumption Prediction:
Additionally, I created another Machine Learning model to predict the electricity consumption for the next 24 hours. This model was trained using historical hourly consumption data to forecast future hourly consumption.

### 2.3. ML Pipeline:
To automate the process of model development and prediction, I implemented an ML Pipeline. This pipeline incorporates data preprocessing, model training, and prediction steps, allowing for efficient and streamlined model updates and predictions as new data becomes available.

## 3. Deployment:
### 3.1. API Development:
I developed an API with separate endpoints for obtaining daily and hourly consumption predictions. This API enables users to retrieve electricity consumption predictions by providing parameters such as date, number of days, and hour.

### 3.2. Path and Query Parameters:
The API accepts date, number of days, and hour as both path and query parameters. This provides flexibility to users in specifying the desired data range and receiving the corresponding consumption predictions.

### 3.3. FastAPI Results:
The FastAPI returns the predicted electricity consumption for the requested day(s) or hour. This allows users to obtain consumption predictions for specific time intervals and plan their energy usage accordingly.

### 3.4. Model Concept/Data Drift:
To monitor the performance of the model, I implemented a mechanism to detect concept drift and data drift. Concept drift identifies changes in data distribution to determine if the model needs to be updated, while data drift detects differences between the incoming new data and the data the model was trained on. This mechanism ensures the accuracy and reliability of the model.

### 3.5. Model Deployment Automation:
For automating model deployment, I utilized tools such as Jenkins and Gitea. These tools facilitate model updates, automated testing, and integration of the updated model with the API. This ensures fast and secure deployment of the updated model.

### 3.6 Jenkins and Ansible for Server Provisioning:

Jenkins and Ansible enable improved traceability and reproducibility in server provisioning by automating the process and allowing for easy monitoring and reuse of installation and configuration steps. Additionally, they enhance collaboration among teams by providing a unified environment for continuous integration and sharing of configuration code.


## 4. Infrastructure:
### 4.1. Docker Container:
The project leverages Docker containers as the infrastructure. Docker containers provide portability and isolation, allowing the project to run smoothly across different environments.

### 4.2. MySQL Database:
I used MySQL as the database system. MySQL is a relational database system used to store and manage the consumption data for the project. The database stores the prediction results, enabling further analysis and future updates.

### 4.3. Writing Prediction Results to the Database:
The prediction results returned by the FastAPI are written to the MySQL database. This allows the storage of prediction data for future reporting, analysis, or updates.

This project utilizes Machine Learning models to predict electricity consumption and makes them accessible through an FastAPI. It also incorporates a mechanism to track data and model drift and provides an infrastructure for automated model deployment. The project offers a valuable tool for energy consumption analysis and planning.