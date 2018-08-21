#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 09:06:23 2018

@author: van
"""

import logging
import sys
import datetime

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)
#from cassandra.cluster import Cluster
#from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
#from cassandra.query import SimpleStatement

KEYSPACE = "spaceforcnn"

cluster = Cluster(contact_points=['172.17.0.2'],port=9042)#NOT the 127.0.0.1
session = cluster.connect()

def createKeySpace():
    """
    To create the space
    """

    log.info("Creating keyspace...")
    try:
        session.execute("""
            CREATE KEYSPACE %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ % KEYSPACE)

        log.info("setting keyspace...")
        session.set_keyspace(KEYSPACE)

        log.info("creating table...")
        session.execute("""
            CREATE TABLE IF NOT EXISTS cnntable (
                time text,
                filename text,
                recongnized_number text,
                PRIMARY KEY (time, filename)
            )
            """)
    except Exception as e:
        log.error("Unable to create keyspace")
        log.error(e)

def append(argv):
    """
    To append data into the table
    """
    log.info("append new data about uploaded image")
    upload_time=datetime.datetime.now().strftime('%Y-%m-%d')
    try:
        session.execute(
				"INSERT INTO spaceforcnn.cnntable (time, filename, recongnized_number) VALUES (%s, %s, %s)" , [upload_time,argv[1],argv[2]]#Claim the space that contains table
                )
    except Exception as e:
        log.error("Unable to append new data")
        log.error(e)

def main(argv):
    createKeySpace();
    append(argv);
    
if __name__=="__main__":
    main(sys.argv)
