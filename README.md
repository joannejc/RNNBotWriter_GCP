# RNN Bot Writer App (deployed on Google Cloud Platform)
See live action [here](https://app191114.appspot.com/).
### To set up GCP:
* [Github Demo](https://github.com/GoogleCloudPlatform/serverless-store-demo)
* [Python3 GCP App Engine](https://cloud.google.com/appengine/docs/standard/python3/quickstart?fbclid=IwAR31gptmZIIA0xDj5dumgkQ-7mNiDfLq5wJel5i00enhqer8gyeKJy6kg_Q)

### To test webapp locally:
1. navigate to the app root directory
2. activate the conda environment with Python3
3. build docker image:
    ```
    docker build -t rnnbot . && docker run --rm -it -p 8080:8080 rnnbot
    ```
4. go to http://localhost:8080
<br/>
(Note: make sure to use port 8080 on GCP)

### To deploy the app on GCP:
1. navigate to the app root directory
2. set the gcloud configuration and deploy the app:
    ```
    gcloud config set project YOUR-PROJECT-ID
    gcloud app deploy
    ```
3. once it's deployed, you can open the webapp by running this in the terminal:
    ```
    gcloud app browse
    ```
    or on https://[YOUR-PROJECT-NAME].appspot.com

### Other good resources:
* FastAI Python Live [Example](https://fastai-v3.onrender.com/)/ [Github](https://github.com/render-examples/fastai-v3/blob/master/app) (deployed on Render)
