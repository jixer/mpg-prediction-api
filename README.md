# Miles per Gallon Prediction API
This POC was built in Python and runs in two docker containers.

The POC was mainly built in order to demonstrate how to wrap a trained model with a JSON API and then use a secondary training service (container) to continously update the trained model used by the API as new datasets are available.

> NOTE: The predictions made by this API will be inacurate as the data used for training is outdated (see [DISCLAIMER on the Dataset section](#DISCLAIMER-on-the-Dataset))


# The Docker Containers
One of the docker containers monitors a docker volume (/usr/input) for the mpg datasets.  When it detects a new file it creates the trained model from the data using multi-linear regression via scikit-learn.  It then serializes the model and vehicle make categories to the /usr/output volume.

The second container hosts a uses the model created by the file watcher to run predictions.  It is hosted as an API that recieves JSON data through HTTP POST via Flask.


# Running the POC
To run the POC, first clone the github repo to a local director.  Once that is complete, navigate to the root `mpg-prediction-api`:
```sh
cd ./mpg-prediction-api
```

Create two directories there named "output" and "input" which will are used as volume mount points within the docker-compose.yaml file.
```sh
mkdir output && mkdir input
```

Then navigate to the `src` directory:
```sh
cd ./src
```

Then use the `build` command within `docker-compose` to buid the containers:
```sh
docker-compose build
```

Lastly, run the containers using the `up` command in `docker-compose` along with `-d` to run the containers and background daemons:
```sh
docker-compose up -d
```

If it's successful, you should see output similar to the following:
```sh
Creating src_watcher_1 ... done
Creating src_api_1     ... done
```

From there, you can also run `docker ps` to show the running containers
```sh
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
4dee769519bf        src_api             "python3 -m api.app"     2 minutes ago       Up 2 minutes        0.0.0.0:5000->5000/tcp   src_api_1
14d417b0781b        src_watcher         "python3 -m watcher.…"   2 minutes ago       Up 2 minutes                                 src_watcher_1
```

Also, `docker-compose logs` will show you the output for the containers 
```sh
$ docker-compose logs
Attaching to src_api_1, src_watcher_1
api_1      |  * Serving Flask app "app" (lazy loading)
api_1      |  * Environment: production
api_1      |    WARNING: Do not use the development server in a production environment.
api_1      |    Use a production WSGI server instead.
api_1      |  * Debug mode: off
api_1      |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

As shown above, the logs reflect that the API is running on port 5000.  This is accessible via [http://localhost:5000](http://localhost:5000).  See next section for info on communicating with the API.


# Testing the POC
Perform these steps only after you have followed through the [Running the POC](#Running-the-POC) section and confirmed the containers started successfully.

To test things out, you'll first need to force the watcher to pick up the dataset and use it to train the model that is then saved to the output folder (volume).  Copy the file named 'auto-mpg.data' from the datasets directory within root github directory.  Paste it into the input folder that we created in the previous section (github_root/input).

After a few moments, the file should disappear.  If you browse the output folder, you should eventually see to files appear: 
- output/makes.output
- output/model.output

The next step is to call the API with some input data.  I recommend using a tool like PostMan to send the data.  Alternatively, `curl` will work as well, but I find the graphical interface of PostMan to be more intuitive.

Below are examples of a JSON payload, HTTP request body, and HTTP response body.


## Example JSON Request
Here is a formated JSON payload that meets the schema requirements of the API:
```json
{
	"mpg": 26.0,
	"cylinders": 4,
	"displacement": 97.00,
	"horsepower": 46.00,
	"weight": 1835.0,
	"acceleration": 20.5,
	"model_year": 70,
	"origin": 2,
	"car_name": "volkswagen 1131 deluxe sedan"
}
```
> NOTE: `mpg` is not required, but if you have the data and provide it, the response will preserve the value in addition to the `predicted_mpg`.  This is helpful for seeing the accuracy of the prediction within the scikit-learn's trained model.


## Example JSON Response
Below is an example of the response.  Note that it preserves all the input fields but also provides the `predicted_mpg`.
```json
{
    "acceleration": 20.5,
    "car_name": "volkswagen 1131 deluxe sedan",
    "cylinders": 4,
    "displacement": 97,
    "horsepower": 46,
    "model_year": 70,
    "mpg": 26,
    "origin": 2,
    "predicted_mpg": 27.679311963033157,
    "weight": 1835
}
```

## Example HTTP Request
```
POST  HTTP/1.1
Host: 127.0.0.1:5000
Content-Type: application/json
Cache-Control: no-cache
Postman-Token: 3cb08c82-c313-763b-cc3e-f8df2ce47da7

{
	"mpg": 26.0,
	"cylinders": 4,
	"displacement": 97.00,
	"horsepower": 46.00,
	"weight": 1835.0,
	"acceleration": 20.5,
	"model_year": 70,
	"origin": 2,
	"car_name": "volkswagen 1131 deluxe sedan"
}
```

## Example HTTP Response
```
Content-Length: 205
Content-Type: application/json
Date: Wed, 01 May 2019 16:40:50 GMT
Server: Werkzeug/0.15.2 Python/3.7.3

{
    "acceleration": 20.5,
    "car_name": "volkswagen 1131 deluxe sedan",
    "cylinders": 4,
    "displacement": 97,
    "horsepower": 46,
    "model_year": 70,
    "mpg": 26,
    "origin": 2,
    "predicted_mpg": 27.679311963033157,
    "weight": 1835
}
```


# The MPG Dataset
The auto-mpg.data dataset came from the [UCI Machine Learning Repository](https://archive.ics.uci.edu).  The data set was found [here](https://archive.ics.uci.edu/ml/datasets/Auto+MPG), within their [datasets repository](https://archive.ics.uci.edu/ml/datasets.php).

## DISCLAIMER on the Dataset
The data set was submitted back in 1993, is fairly small, and only contains older makes of vehicles.  This dataset was used for this POC due to its smaller file size and the simplicity of the data (limited amount of categorical data).

Since this project was really only for POC / demonstration purposes, the dataset was sufficient.  However, please note that the predictions will not be as accurate for newer vehicle.  In addition, they seem to have a large margin of error for older vehicles as well due to the smaller size of the dataset.  You would not want to use this POC for making any real predictions regarding Miles per Gallon.
