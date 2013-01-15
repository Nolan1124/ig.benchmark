import os
import math


import sys
import types
import time
import platform
import random
import string
import subprocess
from collections import deque

import ig_property
import config
import runnable
import db_objects

class operation(runnable.operation):
    def __init__(self):
        runnable.operation.__init__(self)
        self.add_argument("engine","str","ig","engine (ig)")
        self.add_argument("page_size","eval",14,"page size page_size=pow(2,value) valid_values=[10,11,12,13,14,15,16]")
        self.config     = config.ig.Config
        self.rootResultsPath = os.path.abspath("results")
        self.version = None
        self.engine  = "ig"
        self.propertyFile = ig_property.PropertyFile("ig.properties")
        self.db_access = db_objects.db()
        self.db_access.create_database()
        pass
    
    def initialize(self):
        if not os.path.exists(self.config.ig.IG2_Jar):
            print >> sys.stderr,"ERROR: Cannot find jar file: ", self.config.ig.IG2_Jar
            return False
        if not os.path.exists(self.config.ig.IG3_Jar):
            print >> sys.stderr,"ERROR: Cannot find jar file: ", self.config.ig.IG3_Jar
            return False
        if not os.path.exists(self.rootResultsPath):
            self.mkdir(self.rootResultsPath)
            pass
        return True

    def createResultsPath(self,name):
        path = os.path.join(self.rootResultsPath,name)
        if not os.path.exists(path):
            self.mkdir(path)
        return path

    def cleanResultsPath(self,name):
        listing = os.listdir(name)
        for i in listing:
            if i.endswith(".profile"):
                os.remove(os.path.join(name,i))
                pass
            pass
        pass

    def run_ig_command(self,config,version,binary,arguments):
        _command = None
        env  = os.environ.copy()
        lib_path_list = [os.path.join(self.config.Root[version],"lib")]
        lib  = string.join(lib_path_list,":")
        env["DYLD_LIBRARY_PATH"] = lib
        env["LD_LIBRARY_PATH"] = lib
        path_list = env["PATH"]
        env["PATH"] = os.path.join(self.config.Root[version],"bin") + ":" + path_list
        _arguments = [binary]
        _arguments += arguments
        p = subprocess.Popen(_arguments,stdout=sys.stdout,stderr=sys.stderr,env=env)
        p.wait()
        return  p.returncode
        

    def makedirs(self,path):
        if not os.path.exists(path):
            os.makedirs(path)
            pass
        pass
        

    def ig_setup_placement(self,version,propertyObject):
        counter = 1
        if version == "ig2":
            propertyObject.properties["IG.Placement.ImplClass"]="com.infinitegraph.impl.plugins.adp.DistributedPlacement"
            pass
        disks = self.config.Disks[version]
        self.makedirs(self.config.BootFilePath[version])
        for disk in disks:
            self.makedirs(disk.device)
            if version == "ig2":
                storageName  = "storage_%d"%(counter)
                propertyObject.properties["IG.Placement.Distributed.Location.%s"%(disk.name)]  = "%s::%s"%(disk.host,disk.device)
                propertyObject.properties["IG.Placement.Distributed.StorageSpec.%s.ContainerRange"%(storageName)]="1:*"
                propertyObject.properties["IG.Placement.Distributed.GroupStorage.GraphData"]="%s:%s"%(disk.name,storageName)
                counter += 1
                pass
            pass
        pass        


    def ig_setup_Location(self,version,propertyObject):
        if version == "ig3":
            locationConfig = ig_property.LocationConfigFile(os.path.join(self.config.BootFilePath[version],"Location.config"))
            locationConfig.generate(self.config.Disks[version])
            propertyObject.properties["IG.Placement.PreferenceRankFile"] = os.path.join(self.config.BootFilePath[version],"Location.config")
            counter = 1
            disks = self.config.Disks[version]
            for disk in disks:
                arguments = ["AddStorageLocation",
                             "-noTitle",
                             "-name",disk.name,
                             "-storageLocation","%s::%s"%(disk.host,disk.device),
                             "-bootfile",os.path.join(self.config.BootFilePath[version],"bench.boot")
                             ]
                
                if self.verbose == 0:
                    arguments.append("-quiet")
                    pass
                self.run_ig_command(self.config,version,"objy",arguments)
                counter += 1
            pass
        pass
    
    def ig_run(self,version,propertyObject,operation,index):
        env  = os.environ.copy()
        engine = None
        jarFile = None
        propertyObject.properties["IG.BootFilePath"] = self.config.BootFilePath[version]
        propertyObject.fileName = os.path.join(os.getcwd(),"%s.properties"%(version))
        propertyObject.generate()
        lib_path_list = [os.path.join(self.config.Root[version],"lib")]
        lib = string.join(lib_path_list,":")
        env["DYLD_LIBRARY_PATH"] = lib
        env["LD_LIBRARY_PATH"] = lib
        path_list = env["PATH"]
        env["PATH"] = os.path.join(self.config.Root[version],"bin") + ":" + path_list
        engine = version
        jarFile = self.config.BenchmarkJar[version]
        binary = "java"
        arguments = [binary,"-jar",jarFile,"-engine",engine,"-operation",operation,"-property",propertyObject.fileName,"-index",index,"-verbose",str(0)]
        p = subprocess.Popen(arguments,stdout=sys.stdout,stderr=sys.stderr,env=env)
        p.wait()
        
        return  p.returncode


    def ig_v_ingest(self,version,propertyObject,index,size,block,threads,txsize,profileName):
        env  = os.environ.copy()
        engine = None
        jarFile = None
        propertyObject.properties["IG.BootFilePath"] = self.config.BootFilePath[version]
        propertyObject.fileName = os.path.join(os.getcwd(),"%s.properties"%(version))
        propertyObject.generate()
        lib_path_list = [os.path.join(self.config.Root[version],"lib")]
        lib = string.join(lib_path_list,":")
        env["DYLD_LIBRARY_PATH"] = lib
        env["LD_LIBRARY_PATH"] = lib
        path_list = env["PATH"]
        env["PATH"] = os.path.join(self.config.Root[version],"bin") + ":" + path_list
        engine = version
        jarFile = self.config.BenchmarkJar[version]
        binary = "java"
        arguments = [binary,"-jar",jarFile,"-engine",engine,"-operation","standard_ingest","-property",propertyObject.fileName,"-index",index,"-verbose",str(0),
                     "-size",str(size),
                     "-block",str(block),
                     "-vit",str(threads),
                     "-tsize",str(txsize),
                     "-profile",profileName
                     ]
        #print arguments
        #raw_input()
        p = subprocess.Popen(arguments,stdout=sys.stdout,stderr=sys.stderr,env=env)
        p.wait()
        #print string.join(arguments," ")
        return  p.returncode

    Known_Engines = {"ig2":"InfiniteGraph version 2.1","ig3":"InfiniteGraph version 3.0"}
    
    def is_known_engine(self,name):
        name = name.lower()
        return self.Known_Engines.has_key(name)
    
    def get_engine_object(self,name):
        name = name.lower()
        engine = None
        if self.is_known_engine(name):
            engine = self.db_access.create_unique_object(db_objects.model.engine,"name",name,description=self.Known_Engines[name])
            pass
        return engine

    def setup_engine_objects(self):
        self.engine_objects = []
        for i in self.engine:
            e = self.get_engine_object(i)
            if e != None:
                self.engine_objects.append(e)
            else:
                self.error("Unknown database engine '%s'."%(i))
                self.error("Known engines are %s."%(self.Known_Engines.keys()))
                return False
            pass
        return True

    def setup_page_sizes(self,_page_size):
        self.page_size = []
        for i in _page_size:
            if i < 10:
                self.warn("Invalid page_size (%d) given must be between [10,16], setting to 10"%(i))
                i = 10
            elif i > 16:
                self.warn("Invalid page_size (%d) given must be between [10,16], setting to 16"%(i))
                i = 16
                pass
            self.page_size.append(pow(2,i))
            pass
        pass
    
    def operate(self):
        if runnable.operation.operate(self):
            self.engine = self.getOption("engine")
            _page_size = self.getOption("page_size")
            self.setup_page_sizes()
            return self.setup_engine_objects()
        return False
