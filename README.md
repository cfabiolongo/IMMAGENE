# IMMAGENE
Intelligent Multi-Modal Agents based on GEnerative Narrative Evaluation.

This is the repository of the Python (3.7+) implementation of IMMAGENE (**I**ntelligent **M**ulti-**M**odal **A**gents based on **Ge**nerative **N**arrative **E**valuation), 
for the evaluation of intelligent agent based on generative multi-modal narrative, presented at the European Conference of Artificial Intelligence (ECAI 2025). 
IMMAGENE is built on top of the framework [PHIDIAS](https://ceur-ws.org/Vol-2502/paper5.pdf).

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

Except for Phidias, all required packages can be installed from the [requierement](requirements.txt) file.

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
* Install a new Mongodb community instance from [here](https://www.mongodb.com/try/download/community) (a GUI Compass installation is also recommended from [here](https://www.mongodb.com/products/tools/compass)), then create a new database named *dipa* containing a collection *annotations_collection* (the easier way is by using Compass). The url of the MongoDB server must be specified by changing the value of HOST (section LKB) in config.ini.

* OPTIONAL (with credentials usage): Create a new mongodb user in the Mongo shell (or Compass shell) as it follows:
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

IMMAGENE can instantiated in mono- and multi-agent setting. In the latter, the meta-reasoning process is fulfilled by a *parallel-local* agent,
acting in another thread than the main agent. The choice between mono- and multi-agent setting ultimately depends on the specific
use-case and domain. Generally, the key advantage of a multi-agent architecture lies in its use of separate threads per agent, each maintaining
an independent KB. This structural separation allows for more accurate control when integrating sensor data that translates external information into
beliefs. Moreover, it is particularly advantageous in scenarios involving multiple Metaval-type agents, where aggregating outputs from multiple tasks
or LLMs is required for self-correction and refinement of results. For both mono- and multi-agent setting, all required parameters must be set in [config.ini](config.ini).

### Mono-agent Meta-reasoning 

After running [immagene.py](immagene.py), to start inference on the images in IMAGES_LIST (group **[INFERENCE]** of config.ini), the command init() must be lanched in the PHIDIAS shell
as follows:

```sh
        PHIDIAS Release 1.3.5 (deepcopy-->clone,micropython,py3)
        Autonomous and Robotic Systems Laboratory
        Department of Mathematics and Informatics
        University of Catania, Italy (santoro@dmi.unict.it)


eShell: main >init()
```

The production rules reported below, after the image's description acquisition, will simulate a Goal/Plan/Action formulation, whereas
actuate_plan(P,A) will be executed only when the *active-belief* ack_plan(D,P) is *True*.

```sh
init() >> [show_line("Achieving img description. Waiting..."), achieve_img_descr()]
+DESCR(D) >> [formulate_goal(D)]
+GOAL(D, G) >> [formulate_plan(D, G)]
+PLAN(D, G, P) >> [formulate_action(D, G, P)]
+ACTUATION(D, G, P, A) / ack_plan(D, P) >> [show_line("No objection."), actuate_plan(P, A)] 
+ACTUATION(D, G, P, A) >> [show_line("The plan cannot be actuated.")]
```


### Multi-agent Meta-reasoning 

---------------
As for multi-agent settings, by running [immagene_mas.py](immagene_mas.py) and *init()* in the shell, two distinct agents types were implemented, both interacting with a
further agent *Metaval* delegated to meta-reasoning:

* Metaval
* Scenario/Plan assessing agents
* Scenario assessing agent

#### *Metaval* agent

---------------

The *Metaval agent*, running in a parallel thread, will receive scenario descriptions and plans for privacy-aware evaluation, for both Related Plan/Non-Related Plan assessment.
In any case, it will send the acknowledgment for plan's execution.

```sh
# Related-Plan assessment
+DESCR(D, P)[{'from': A}] / ack_plan(D, P) >> [-DESCR(D, P), show_line("Received belief DESCR(",D,") from ", A), refuse()]
+DESCR(D, P)[{'from': A}] >> [-DESCR(D, P), show_line("Received belief DESCR(",D,") from ", A), accept()]

# Non-Related-Plan assessment
+DESCR(D)[{'from': A}] / ack_noplan(D) >> [-DESCR(D), show_line("Received belief DESCR(", D, ") from ", A), refuse()]
+DESCR(D)[{'from': A}] >> [-DESCR(D), show_line("Received belief DESCR(", D, ") from ", A), accept()]

accept() >> [show_line(">>>>>>>> Accepting plan <<<<<<<<<<"), +ACK("TRUE")[{'to': 'main'}]]
refuse() >> [show_line(">>>>>>>> Refusing plan <<<<<<<<<<"), +ACK("FALSE")[{'to': 'main'}]]
```

#### Scenario/Plan assessing agents

---------------

In this setting, although the interaction with the agent *Metaval* acting in another thread, the main agent must wait for the plan’s assessment before its
actuation, i.e., there will not be effective parallel meta-reasoning computing.

```sh
init() >> [show_line("\nAchieving img description. Waiting...\n"), achieve_img_descr(), setup()]
setup() / DESCR(D) >> [show_line(">>>>>>>> Communication started <<<<<<<<<"), +DESCR(D)[{'to': "Metaval"}], formulate_goal(D), achieve_plan()]

achieve_plan() / (DESCR(D) & GOAL(G)) >> [show_line("Planning for the goal: ", G, " from the description ", D), formulate_plan(D, G)]

+ACK(X)[{'from': A}] >> [+CONSENT(X), show_line(">>>>>>>> Acknowledgment acquired ", X, " from ", A, " <<<<<<<<"), commit()]

commit() / (PLAN(P) & CONSENT("TRUE")) >> [-CONSENT("TRUE"), show_line(">>>>>>>> No objection for plan actuation <<<<<<<<<"), actuate_plan(P), clear()]
commit() / (PLAN(P) & CONSENT("FALSE")) >> [-CONSENT("FALSE"), show_line(">>>>>>>> The plan cannot be actuated due to privacy issues <<<<<<<<<"), clear()]
commit() / PLAN(P) >> [commit(), show_line(">>>>>>>> WAITING...........")]
clear() / (DESCR(D) & GOAL(G) & PLAN(P)) >> [-DESCR(D), -GOAL(G), -PLAN(P)]
```

#### Scenario assessing agents

---------------

This is the setting involving an effective-parallel scenario assessment achieved with the agent Metaval, but *regardless of the plan*.

```sh
init() >> [show_line("Achieving img description. Waiting..."), achieve_img_descr(), setup()]
setup() / DESCR(D) >> [show_line("Image description achieved: ", D), formulate_goal(D), achieve_plan()]
achieve_plan() / (DESCR(D) & GOAL(G)) >> [show_line("Planning for the goal: ", G, " from the description ", D), formulate_plan(D, G), commit()]
commit() / (DESCR(D) & PLAN(P)) >> [+DESCR(D, P)[{'to': "Metaval"}], show_line(">>>>>>>> Communication started <<<<<<<<<")]

+ACK("TRUE")[{'from': A}] / PLAN(P) >> [show_line(">>>>>>>> No objection for plan actuation <<<<<<<<"), actuate_plan(P), clear()]
+ACK("FALSE")[{'from': A}] / PLAN(P) >> [show_line(">>>>>>>> The plan cannot be actuated due to privacy issues <<<<<<<<"), clear()]

clear() / (DESCR(D) & GOAL(G) & PLAN(P)) >> [-DESCR(D), -GOAL(G), -PLAN(P)]
```

## Images description dataset preparation

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

## Validation replication procedure

This section shows all required steps to replicate the paper validation procedure, by employing a test synthetic dataset generation.

### Synthetic dataset generation

---------------

To generate the DIPA-alike dataset to be used for the validation process, the following preliminary steps must be accomplished:

* Test images selection from DIPA.
* Description files creation with [create_img_descr.py](create_img_descr.py). This work's experiments were conducted with [output_filter.xlsx](validation/inferences/output_filter.xlsx) as results of this computation.
* Synthetic images dataset creation (folder [DIPA_TEST](DIPA_TEST)) with [diffusion_full.py](diffusion_full.py).

### Step-by-Step IMMAGENE inference validation

---------------

To achieve more control over the procedure, the whole inference validation process has been split into the following steps:

* Creation of the DIPA_TEST archive of images descriptions, with [create_img_descr.py](create_img_descr.py).
* Creation of the archive of "best" vectorial matches with the DIPA_TEST, with [inference_vect_db_validation.py](validation/inference_vect_db_validation.py).
* Creation of the inferences outcome archive, with [query_nosql_db_llm.py](validation/query_nosql_db_llm.py). 
* Scores calculation for the above inferences, with [val_counting.py](validation/val_counting.py).

### Direct VLM inference validation

---------------

By leveraging on the above DIPA_TEST images, to compare the IMMAGENE results the following steps must be accomplished:

* Creation of the inference outcome archive for direct VLMs, with [direct_visual_descr.py](validation/direct_visual_descr.py). 
* Scores calculation for the above inferences, for both *pure* zero-shot and DIPA *category-guided* prompts, with [direct_val_counting.py](validation/direct_val_counting.py).