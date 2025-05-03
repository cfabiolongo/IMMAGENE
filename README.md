# IMMAGENE
Intelligent Multi-Modal Agents based on GEnerative Narrative Evaluation.

This is the repository of the Python (3.7+) implementation of IMMAGENE (**I**ntelligent **M**ulti-**M**odal **A**gents based on **Ge**nerative **N**arrative **E**valuation), 
for the evaluation of intelligente agent based on generative multi-modal narrative. IMMAGENE is built on top of the framework [PHIDIAS](https://ceur-ws.org/Vol-2502/paper5.pdf).


# Installation

---------------

This repository has been tested on Python 3.10 64bit (Windows 10/PopOs linux), with the following packages versions:

* [PHIDIAS](https://github.com/corradosantoro/phidias) (release 1.3.4.alpha) 
* [Owlready2](https://pypi.org/project/Owlready2/) (ver. 0.26) 


### PHIDIAS

---------------

```sh
> git clone https://github.com/corradosantoro/phidias
> cd phidias
> pip install -r requirements.txt
> pip install .
```


### pillow

---------------

```sh
> pip install pillow
```

### opencv

---------------

```sh
> pip install opencv-python
```


### Pandas (for clauses exporting from mongodb to excel)


```sh
> pip install pandas
> pip install openpyxl
```


### pymongo

---------------

```sh
> pip install pymongo
```


### MongoDB

---------------
* Install a new Mongodb community instance from [here](https://www.mongodb.com/try/download/community) (a GUI Compass installation is also recommended from [here](https://www.mongodb.com/products/tools/compass)), then create a new database named *ad-caspar* containing a collection *clauses* (the easier way is by using Compass). The url of the MongoDB server must be specified by changing the value of HOST (section LKB) in config.ini.

* Create a new mongodb user in the Mongo shell (or Compass shell) as it follows:
```sh
> use dipa
> db.createUser({
  user: "root",
  pwd: "example",
  roles: [
    { role: "readWrite", db: "dipa" }
  ]
})
```


### MongoDB (Docker use case)

---------------
In the case of using a mongoDB container, the latter can be accessed by the link: http://localhost:8087/ (user/password are set in config.ini).

```sh
> docker-compose -f mongo.yaml up
```

### Pandas (for clauses exporting from mongodb to excel)


```sh
> pip install pandas
> pip install openpyxl
```

