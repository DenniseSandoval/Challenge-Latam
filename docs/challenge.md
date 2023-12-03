# Execution of the local project

For correct execution, start by installing the following:
pip install --upgrade pip
pip install -r requirements-test.txt

After that in the terminal execute

uvicorn challenge.api:app --reload


# Docker execution

write the commands
docker build -t challenge-latam:latest .
docker run -p 8000 challenge-latam

Test Execution
The UnitTest were executed correctly covering all the test cases established in the project, only in the test_model.py the access path to the file was changed data_path = Path(os.getcwd(),"data/data.csv") in the setUp function

make model-test
make api-test

# Deploy GCP

For the deployment in the cloud, the app.yaml file was configured, and the cd/ci files were also configured with the corresponding branches and the steps for the correct deployment of the application.

GCP server URL: https://latam-challenge-407003.ue.r.appspot.com
# APIS
  get: https://latam-challenge-407003.ue.r.appspot.com/health
  post: https://latam-challenge-407003.ue.r.appspot.com/predict
         body: {
             "flights": [
                 {
                     "OPERA": "Aerolineas Argentinas",
                     "TYPEFLIGHT": "N",
                     "MONTH": 3
                 }
             ]
         }

# Selected Model
Regarding the choice of the model for the final implementation, Logistic Regression was chosen. This decision is based on practical considerations such as time constraints, package dependencies, and ease of use. Selecting Logistic Regression reduces third-party dependency for the component, and the inherent simplicity of this library helps deliver a complete solution efficiently.

This choice aligns with the guidance of the Data Scientist, who indicated that one of the models with Feature Importance and Balance should be selected. Given that both models presented similar results in the classification report, with slight variations in the recall, the choice of Logistic Regression is based on its greater ease of interpretation. This feature will allow you to more clearly understand the impact of each Feature on the model training results. In this case, the ability to understand the reasoning behind the results is valued to improve performance in future iterations of the project.


# APIS
The solution was implemented that allows the model file to be loaded only at the beginning of the execution and thus have it in memory.

In our FastAPI application, we have established an endpoint that leverages the previously generated model to make predictions based on the input data. Users have the ability to send requests to this endpoint, and the model will respond with predictions in an agile manner.