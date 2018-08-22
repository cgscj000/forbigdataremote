# A Website in a Container Running CNN

These files can be deploied into a docker container and will establish a website with flask structure, on which users can upload their image about a digit, then the website will use CNN algroithm to indentify the number(not exactly) and report to users. Then the log will be stored into the database of cassandra. 

## catalogue

1,Train the CNN model from mnist<br>
2,Run the cassandra to get access to database<br>
3,Build the docker image<br>
4,Deploy the image into a container<br>
5,Open the browser and go to http:/localhost:4000/upload<br>
6,upload the image and get response of the result<br>
7,Go to cassadra to check the upload log<br>

## configuration required:

1,*Docker* to build image and run container.<br>
2,*Cassandra* to provide database to store log.<br>

### CNN model from mnist datasetu
The websit uses CNN algroithm to recongize images, so there must be a trained model. There is a trained model in *./form*, and if you want to train your own model, execute <br>
`python model.py`<br>
to create your own model. In `saver.save(sess,"./form/model.ckpt")` you can change your path to store your model annd go to `for i in range(5000):` to change times of training.
