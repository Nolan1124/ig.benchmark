import os
import math
import IG_PropertyFile
import sys
import types
import time
import platform
from collections import deque

import IG_PropertyFile
import IG_Config

class Runner:
    def __init__(self,config):
        self.config = config
        self.sourcePath = os.path.dirname(os.path.abspath(__file__))
        self.jarPath    = os.path.join(os.path.dirname(self.sourcePath),"build")
        self.ig2Jar     = os.path.join(self.jarPath,"benchmark.2.jar")
        self.ig3Jar     = os.path.join(self.jarPath,"benchmark.3.jar")
        self.rootResultsPath = os.path.join(os.path.dirname(self.sourcePath),"results")
        
    def initialize(self):
        if not os.path.exists(self.ig2Jar):
            print >> sys.stderr,"ERROR: Cannot find jar file: ", self.ig2Jar
            return False
        if not os.path.exists(self.ig3Jar):
            print >> sys.stderr,"ERROR: Cannot find jar file: ", self.ig3Jar
            return False
        if not os.path.exists(self.rootResultsPath):
            os.mkdir(self.rootResultsPath)
            pass
        print "IG2 :",self.ig2Jar
        print "IG3 :",self.ig3Jar
        print "Results:",self.rootResultsPath
        if os.system("oocheckls -quiet") != 0:
            print >> sys.stderr,"ERROR: Lock server is not running."
            return False
        else:
            print "Lock server is running on local host"
            pass
        return True

   

    def pow_x(self,base,start,stop,step=1):
        result = []
        current = start
        while current < stop:
            result.append(int(math.ceil(pow(base,current))))
            current += step
            pass
        return result

    def pow_2(self,start,stop,step=1):
        return self.pow_x(2,start,stop,step)


    def createResultsPath(self,name):
        path = os.path.join(self.rootResultsPath,name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def cleanResultsPath(self,name):
        listing = os.listdir(name)
        for i in listing:
            if i.endswith(".profile"):
                os.remove(os.path.join(name,i))
                pass
            pass
        pass

    def ig3_command(self,command):
        if platform.system().lower().startswith("darwin"):
            return "(export DYLD_LIBRARY_PATH=%s;%s)"%(os.path.join(self.config.IG3_Root,"lib"),command)
        return "(export LD_LIBRARY_PATH=%s;%s)"%(os.path.join(self.config.IG3_Root,"lib"),command)
    
    def create_db_ig3(self,propertyFile):
        command = self.ig3_command("java -jar %s -engine ig3 -operation create -property %s"%(self.ig3Jar,propertyFile.fileName))
        return os.system(command)
            

    def run_ig_3(self,operation,scale,propertyFile,threads,vthreads,txsize,index,isNew):
        propertyFile.properties["IG.BootFilePath"]=self.config.BootFilePath
        if isNew:
            if os.path.exists(os.path.join(self.config.BootFilePath,"bench.boot")):
                os.system(self.ig3_command("objy DeleteFd -bootFile %s"%(os.path.join(self.config.BootFilePath,"bench.boot"))))
            locationConfig = IG_PropertyFile.IG_LocationConfigFile(os.path.join(self.config.BootFilePath,"Location.config"))
            locationConfig.generate(self.config.Disks)
            propertyFile.properties["IG.Placement.PreferenceRankFile"] = os.path.join(self.config.BootFilePath,"Location.config")
            propertyFile.generate()
            self.create_db_ig3(propertyFile)
            self.setup_IG3_Location(propertyFile)
            pass
        command = "java -jar %s -engine ig3 -operation %s -scale %d -property %s -t %d -vit %d -tsize %d -index %s"%(self.ig3Jar,
                                                                                                                     operation,scale,
                                                                                                                     propertyFile.fileName,
                                                                                                                     threads,
                                                                                                                     vthreads,txsize,
                                                                                                                     index)  
        command = self.ig3_command(command)
        return os.system(command)

    def setup_IG3_Location(self,propertyFile):
        
        counter = 1
        for disk in self.config.Disks:
            command = self.ig3_command("objy AddStorageLocation -name %s -storageLocation %s::%s -bootfile %s"%(
                disk.name,
                disk.host,
                disk.device,
                os.path.join(self.config.BootFilePath,"bench.boot")))
            os.system(command)
            counter += 1
            pass
        os.system(self.ig3_command("objy ListStorage -bootfile %s"%(os.path.join(self.config.BootFilePath,"bench.boot"))))
        pass
        
    
    def v_ingest_f_tx(self,igPropertyFile,sizes):
        cwd  = os.getcwd()
        path = self.createResultsPath("v_ingest_f_tx")
        self.cleanResultsPath(path)
        os.chdir(path)
        
        for size in sizes:
            scale = size[0]
            txsize = size[1]
            print "running txsize:%d scale:%d"%(txsize,scale)
            self.run_ig_3("standard_ingest",scale,igPropertyFile,1,1,txsize,"none",1)
            pass
        os.chdir(cwd)
        pass
        

def r_mkdir(path,pathList):
    if len(pathList) == 0:
        return path
    else:
        current = str(pathList[0])
        pathList = pathList[1:]
        currentFullPath = os.path.join(path,current)
        if not os.path.exists(currentFullPath):
            os.mkdir(currentFullPath)
        return r_mkdir(currentFullPath,pathList)


def collectFileSize(path):
    pathList = os.listdir(path)
    ADP_ConnectorGroup_Size = 0
    ADP_EdgeGroup_Size = 0
    ADP_VertexGroup_Size = 0
    GraphConfiguration_Size = 0
    IG_ADP_Size = 0
    IG_Init_DB_Size = 0
    IndexDatabase_Size = 0

    sizeMap = {}
    for f in pathList:
        i = os.path.join(path,f)
        if f.lower().endswith(".db"):
            if f.startswith("ADP-ConnectorGroup"):
                ADP_ConnectorGroup_Size += os.stat(i).st_size*1e-6
                pass
            elif f.startswith("ADP-EdgeGroup"):
                ADP_EdgeGroup_Size += os.stat(i).st_size*1e-6
                pass
            elif f.startswith("ADP-VertexGroup"):
                ADP_VertexGroup_Size += os.stat(i).st_size*1e-6
                pass
            elif f.startswith("GraphConfiguration"):
                GraphConfiguration_Size += os.stat(i).st_size*1e-6
                pass
            elif f.startswith("IG-ADP"):
                IG_ADP_Size += os.stat(i).st_size*1e-6
                pass
            elif f.startswith("IG-Init-DB"):
                IG_Init_DB_Size += os.stat(i).st_size*1e-6
                pass
            elif f.startswith("IndexDatabase"):
                IndexDatabase_Size += os.stat(i).st_size*1e-6
                pass
            else:
                print i
                assert(0)
                pass
            pass
        pass
    return {"ADP-ConnectorGroup":ADP_ConnectorGroup_Size,
            "ADP-EdgeGroup":ADP_EdgeGroup_Size,
            "ADP-VertexGroup":ADP_VertexGroup_Size,
            "GraphConfiguration":GraphConfiguration_Size,
            "IG-ADP":IG_ADP_Size,
            "IG-Init-DB":IG_Init_DB_Size,
            "IndexDatabase":IndexDatabase_Size}

def writeFileSize(iteration,path,dataPath):
    sizeMap = collectFileSize(dataPath)
    total = 0
    for name in sizeMap.keys():
        size = sizeMap[name]
        f = file(os.path.join(path,"size-"+name+".dat"),"a")
        print >> f,(str(iteration)+","+str(size))
        f.flush()
        f.close()
        total += size
        pass
    f = file(os.path.join(path,"size-total.dat"),"a")
    print >> f,(str(iteration)+","+str(total))
    f.close()
    pass


def K(i):
    return int(1000*i)

def M(i):
    return int(i*1e6)


def Power(a,points):
    result = []
    if(type(points) == types.ListType):
        for i in points:
            result.append(math.pow(a,i))
    else:
        result.append(math.pow(a,points))
    return result

LUCENE_INDEX="/disk2/data/lucene_index"

def delete_lucene_index(path):
    listing = os.listdir(path)
    for i in listing:
        file = os.path.join(path,i)
        os.remove(file)
        pass
    pass
                            
def run_ingest_task(profile,pageSize,dataSize,txSize,vertices,jarFile,pFileName,type):
    hostname = os.uname()[1]
    propertyFile = IG_PropertyFile.IG_PropertyFile(pFileName)
    propertyFile.properties["IG.BootFilePath"] = "./data"
    propertyFile.properties["IG.LockServerHost"] = hostname
    propertyFile.properties["IG.Placement.Distributed.Location.disk1"] = "%s::/disk1/data"%(hostname)
    propertyFile.properties["IG.Placement.Distributed.Location.disk2"] = "%s::/disk2/data"%(hostname)
    propertyFile.properties["IG.Placement.Distributed.Location.disk3"] = "%s::/disk3/data"%(hostname)

    if (type == "ingest_v_i_lu") or (type == "ingest_v_tx_lu"):
        propertyFile.properties["IG.Indexing.Lucene.Instances"]="luceneIndex"
        propertyFile.properties["IG.Indexing.Lucene.luceneIndex.Path"]=LUCENE_INDEX
        delete_lucene_index(LUCENE_INDEX)
        pass
    
    propertyFile.properties["IG.Placement.Distributed.GroupStorage.GraphData"] = "disk3:Dspec3" #,disk2:Dspec2,disk3:Dspec3"
    propertyFile.properties["IG.Placement.Distributed.GroupPreference.GraphData"]="ANY"
    propertyFile.properties["IG.Placement.Distributed.StorageSpec.Dspec1.ContainerRange"]="2:*"
    propertyFile.properties["IG.Placement.Distributed.StorageSpec.Dspec2.ContainerRange"]="2:*"
    propertyFile.properties["IG.Placement.Distributed.StorageSpec.Dspec3.ContainerRange"]="2:*"
    propertyFile.properties["IG.PageSize"] = int(pageSize)
    propertyFile.generate()
    command = "java -Xms10m -Xmx7000m -jar %s --append --operation=%s --db=test --iteration=1,%d,1 --vsize=%d --size=%d --property=%s --profile=%s"%(jarFile,type,txSize,dataSize,vertices,pFileName,profile)
    os.system(command)


def run_ingest(pPath,pageSizeSet,dataSizeSet,vertexSet,txSize,jarFile,pFileName,type):
    if not os.path.exists(pPath):
        os.mkdir(pPath)
        pass
    
    for page in pageSizeSet:
        page_size = math.pow(2,page)
        pass
        for datasize in dataSizeSet:
            path = ["page.%d"%(page)+"-data.%d"%(datasize)]
            print path
            _pPath = r_mkdir(pPath,path)
            done = False
            for v in vertexSet:
                run_ingest_task(_pPath,page_size,datasize,txSize,v,jarFile,pFileName,type)
                print ".",
                sys.stdout.flush()
        print

def run_ingest_index(pPath,pageSizeSet,dataSizeSet,vertexSet,txSize,jarFile,pFileName):
    if not os.path.exists(pPath):
        os.mkdir(pPath)
        pass
    
    for page in pageSizeSet:
        page_size = math.pow(2,page)
        pass
        for datasize in dataSizeSet:
            path = ["page.%d"%(page)+"-data.%d"%(datasize)]
            _pPath = r_mkdir(pPath,path)
            print path,_pPath
            done = False
            for v in vertexSet:
                print "(.",;sys.stdout.flush()
                #run_ingest_task(_pPath,page_size,datasize,txSize,v,jarFile,pFileName,"ingest_v_i_gr")
                print ".",;sys.stdout.flush()
                #run_ingest_task(_pPath,page_size,datasize,txSize,v,jarFile,pFileName,"ingest_v_i_ge")
                print ".",;sys.stdout.flush()
                delete_lucene_index(LUCENE_INDEX)
                run_ingest_task(_pPath,page_size,datasize,txSize,v,jarFile,pFileName,"ingest_v_i_lu")
                print ")",;sys.stdout.flush()
                sys.stdout.flush()
        print
