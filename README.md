# Bottle Classifier App

### Setting Up Procedure

### Prerequisites :

* Python3.10
* MongoDB

### Cloning or Downloading the Zip :

* Clone the repository in your local machine - ``` git clone https://github.com/SyedAnas26/bottle_classifier_app.git```
* Or Download the repository as Zip and extract the files
* Change Directory to project - ```cd bottle_classifier_app```

### MongoDB Database set up :

* Make sure the database service is running at port **"mongodb://localhost:27017"**
* Create a database named **"bottle_classifier_db"** - ``` use bottle_classifier_db;```
* Create a collection to store bottle data **"bottles"** - ``` db.createCollection("bottles");```
* Import bottle data from the csv provided in dataset directory <br/>
  ```mongoimport -d bottle_classifier_db -c bottles --type csv --file your_path_to_repo\dataset\bottle_database.csv --headerline```

### Python Environment :

* Create a python environment of version 3.10 - ```python -m venv classifier_env```
* Activate the environment - ```classifier_env\Scripts\activate```
* Install the dependencies of the project - ```pip install -r requirements.txt```

Now you can run the python script - ``` python Main.py ```

**"Slide Deck"** and **"screenshot images"** of the GUI Application is available in the project folder.
