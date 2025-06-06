# IMMAGENE
Intelligent Multi-Modal Agents based on GEnerative Narrative Evaluation.

This is the repository of the Python (3.7+) implementation of IMMAGENE (**I**ntelligent **M**ulti-**M**odal **A**gents based on **Ge**nerative **N**arrative **E**valuation), 
for the evaluation of intelligent agent based on generative multi-modal narrative. IMMAGENE is built on top of the framework [PHIDIAS](https://ceur-ws.org/Vol-2502/paper5.pdf).

![Image 1](images/schema.jpg)


### Requirements

---------------

This repository has been tested on Python 3.10 64bit (Windows 10/PopOs linux), with the following packages versions:

* [PHIDIAS](https://github.com/corradosantoro/phidias) (release 1.3.4.alpha) 
* pillow (11.2.1)
* opencv_python (4.11.0.86)
* pandas (2.2.3)
* openpyxl (3.1.5)
* pymongo (4.12.0)

### PHIDIAS installation

---------------

```sh
> git clone https://github.com/corradosantoro/phidias
> cd phidias
> pip install -r requirements.txt
> pip install .
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
In the case MongoDB container, Mongo Express can be accessed by the link: http://localhost:8087/ (admin/tribes).

```sh
> docker-compose -f mongo.yaml up
```

## Framework setup

Immagene can implemented in mono- and multi-agent setting. In the latter, the meta-reasoning process is fulfilled by a parallel-local agent,
acting in another thread than respect to the main agent. The choice between mono- and multi-agent setting ultimately depends on the specific
use case and domain. Generally, the key advantage of a multi-agent architecture lies in its use of separate threads per agent, each maintaining
an independent KB. This structural separation allows for more accurate control when integrating sensor data that translates external information into
beliefs. Moreover, it is particularly advantageous in scenarios involving multiple Metaval-type agents, where aggregating outputs from multiple tasks
or LLMs is required for self-correction and refinement of results. For both mono- and multi-agent setting, all required parameters must be set in [config.ini](config.ini).

### Mono-agent Meta-reasoning 

After running immagene.py, to start inference on the images in IMAGES_LIST (group [INFERENCE] of config.ini), the command init() must be lanched in the PHIDIAS
as follows:

```sh
        PHIDIAS Release 1.3.5 (deepcopy-->clone,micropython,py3)
        Autonomous and Robotic Systems Laboratory
        Department of Mathematics and Informatics
        University of Catania, Italy (santoro@dmi.unict.it)


eShell: main >init()
```

The production rules reported below, after the image's descriptiion acquisition, will simulate a Goal/Plan/Action formulation, whereas
actuate_plan(P,A) will be executed only when the active-belief ack_plan(D,P) is *True*.

```sh
init() >> [show_line("Achieving img description. Waiting...\n"), achieve_img_descr()]
+DESCR(D) >> [show_line("\nImage description achieved: ", D), formulate_goal(D)]
+GOAL(D, G) >> [show_line("No objection.", D), formulate_plan(D, G)]
+PLAN(D, G, P) >> [formulate_action(D, G, P)]
+ACTUATION(D, G, P, A) / ack_plan(D, P) >> [show_line("No objection."), actuate_plan(P, A)] 
+ACTUATION(D, G, P, A) >> [show_line("The plan cannot be actuated.")]
```


### Multi-agent Meta-reasoning 

---------------
bla bla bla



### Images description dataset preparation

---------------
This framework's meta-reasoning relies on the annotated images dataset [DIPA](https://dl.acm.org/doi/abs/10.1145/3581754.3584176).

* Download the dataset from this [link](https://dl.acm.org/doi/suppl/10.1145/3581754.3584176/suppl_file/dataset.zip)
* Set the proper variables in the file [create_img_descr.py](create_img_descr.py)
* Run the above create_img_descr.py and build the images dataset descriptions in excel (output_excel).


### Vect DB building

---------------
* Set the proper variables in the file [create_vect_db.py](create_vect_db.py).
* Run the above create_vect_db.py to build the sqlite3 vectorial database. 
* Run [inference_vect_db.py](inferece_vect_db.py) to test the Vect DB with a text.


### Privacy features NoSql DB building

---------------
* Set the proper variables im the file [create_nosql_db.py](create_nosql_db.py)
* Run the above create_nosql_db.py to build the NoSql database.
* Run [query_nosql_db.py](query_nosql_db.py) to test the NoSql database (e.g 00b4064b073e51f3) 


## Running IMMAGENE

bla bla bla
