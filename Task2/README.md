# Task2: Search Engine

A simple search engine that performs a search for entered search queries 
on a beforehand established index of the whoosh library. The search engine
can be used with the help of a flask app. To use the search engine the 
following link can be opend. Be aware, that a connection to the wifi of 
University of Osnabrueck has to be established.

Link: http://vm150.rz.uni-osnabrueck.de/u015/searchengine.wsgi

## Description
The files are orderd the following way:

Task 2   
├── indexdir  
│   ├── MAIN_WRITELOCK  
│   ├── MAIN_kefjsq64mdi79vd9.seg  
│   ├──_MAIN_1.toc  
├── static  
│   ├── styles  
│   │   └──styling.css  
│   └── logo.jpg  
├── templates  
│   ├── index.html  
│   ├── layout.html  
│   └── results.html  
├── README.md    
├── crawler.py  
├── requirements.txt  
├── searchengine.py          
└── searchengine.wsgi  

The *indexdir* directory contains the beforehand established index of the whoosh library.

The styles of our webpage are enhanced with the css file contained in the *static* folder,
as well as with the logo contained in there.

The directory *templates* containes our html files that determine the layout and functionalities
of our web page the users can interact with. We have the *index.html* start page as well as the 
*results.html* file, where our users are redirected to after entering a search query.

Additionally to these directories, there are also the README.md file, our crawler,the searchangine 
pyhon file and the searchengine.wsgi file, that is used by the server to deploy our webpage. 
The crawler.py and searchengine.py can be run directly without using the url from above. This will
be explained in the following part. 

To run our implementations you need to install the libraries from the *requirements.txt* file. 
You can do so by using the following command:

```console
pip install -r requirements.txt
```

## Run the Crawler
To simply run the crawler, without starting the whole searchengine, you can just run the 
python script crawler.py, e.g. the following way:

```console
python crawler.py 
```

this will create a new index directory.

## Start the Flask App
To simply run the flask app we developed, without using the url we provided at the beginning, 
you can use the following command:

```console
flask --app searchengine.py run 
```

You can then access the resulting web page at your local machine.

## Authors

Brüggemann, Lena 	lenbrueggema@uni-osnabrueck.de 

Döring, Luna 	    ldoering@uni-osnabrueck.de 

Guillou, Emily      eguillou@uni-osnabrueck.de 

