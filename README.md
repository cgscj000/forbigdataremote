# A Website in a Container Running CNN

These files can be deploied into a docker container and will establish a website with flask structure, on which users can upload their image about a digit, then the website will use CNN algroithm to indentify the number(not exactly) and report to users. Then the log will be stored into the database of cassandra. 

## catalogue

1,Train the CNN model from mnist<br>
2,Build the docker image<br>
3,Run the cassandra to get access to database<br>
4,Deploy the image into a container<br>
5,Open the browser and go to http:/localhost:4000/upload<br>
6,upload the image and get response of the result<br>
7,Go to cassadra to check the upload log<br>

## configuration required:

1,*Docker* to build image and run container.<br>
2,*Cassandra* to provide database to store log.<br>

### CNN model from mnist datasetu
The websit uses CNN algroithm to recongize images, so there must be a trained model. There is a trained model in *./form*, and if you want to train your own model, execute <br>
* FILE: ./model.py <br>
`python model.py`<br>

to create your own model. In `saver.save(sess,"./form/model.ckpt")` you can change your path to store your model and go to `for i in range(5000):` to change times of training.

If you just want to recongnize your local image, just drag your file into the current catalogue, then execute<br>
* FILE: ./show.py xxx.png/jpg/jpeg<br>
`python show.py xxx.png/jpg/jpeg`<br>

to get the result. You can use image of any size and color, but only jpg,png,jpeg form are accepted. If you have created your own model, go to `saver=tf.train.import_meta_graph('./form/model.ckpt.meta')` and `
saver.restore(sess, tf.train.latest_checkpoint('./form'))` and change the path into yours. 

### build docker image from these files
We will build a docker image from these files, preparing to deploy it into a container. Make sure that you have installed docker. 
then execute<br>
`docker build -t name .`<br>
in current catalogue. The `-t name` means adding a tag to the docker image, so you can type your tag  on the position of `name`.
Wait for a few minutes, the docker iamge will be created. Use<br>
`docker image ls`<br>
to check all the docker image that you have created.<br>

#### Toubleshooting
* The dot`.`in the first commad is NOT a type mistake, this dot means you create your docker image from the current path. If you miss the dot, the building will fail. <br>
* In the `Dokcerfile`, the docker will install modules that the image need from `pypi.python.org`. Becasue I am in USA, I can install them successfully, but if you are in China, you minght be affected by the GFW and cannot install them from this source. Then you should change the `pypi.python.org` into some mirror in China, such as `pypi.tuna.tsinghua.edu.cn/simple`.<br>

### run cassandra and connect to database
We use cassandra to provide a database to store the log data. Make sure that you have installed cassandra. Then execute<br>
`docker run --name yourname-cassandra -p 9042:9042 -d cassandra:latest`<br>
to start the cassandra service. You can use your ownrun name to replace `yourname`. Then execute<br>
`docker run -it --link yourname-cassandra:cassandra --rm cassandra cqlsh cassandra`<br>
to cqlsh, in which you can create the keyspace and table, then you can insert your log data. If you want to test the cqlsh only, run<br>
* FILE: ./communicate_with_cassandra.py<br>
`python communicate_with_cassandra.py xxx.png/jpg/jpeg '0'`<br>
to create a keyspace named `spaceforcnn` and a table named `cnntable` then insert a row into the table.


