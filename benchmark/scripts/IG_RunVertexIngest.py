from IG_RunCommon import *
from IG_PropertyFile import *
import IG_Config

propertyFile = IG_PropertyFile("ig.properties")
propertyFile.properties["IG.UseMROWTransactions"] = "false"
propertyFile.properties["IG.Indexing.GraphIndexSensitive"] = "true"
propertyFile.properties["IG.SessionPool.ThreadBasedSessionPool.InitialCacheSizeKb"]=1000
propertyFile.properties["IG.SessionPool.ThreadBasedSessionPool.MaximumCacheSizeKb"]=5000000
propertyFile.properties["IG.SessionPool.ThreadBasedSessionPool.LockWaitTime"]=10
propertyFile.properties["IG.PageSize"]=16384
runner = Runner(IG_Config.Config)
runner.initialize()

page_size = [1024,2048,4096,8192,16384,32768,65536]
sizes = [(20,pow(2,14))]
threads = [1]
index = ["none"]
runner.v_ingest("Vertex Ingest Rate as a function of page size",["page_size"],propertyFile,sizes,index,threads,page_size)

page_size = [16384]
sizes = []
index = ["none","gr"]
threads = [1]
for txsize in range(4,16):
    sizes.append((txsize+4,pow(2,txsize)))
    pass
runner.v_ingest("Vertex Ingest Rate as a function of transaction size",["txsize"],propertyFile,sizes,index,threads,page_size)

page_size = [16384]
threads = [1,2,3,4,5,6,7,8]
sizes = [(20,pow(2,14))]
index = ["none","gr"]
runner.v_ingest("Vertex Ingest Rate as a function of number of threads",["threads"],propertyFile,sizes,index,threads,page_size)


sizes = []
page_size = [16384]
threads = [4]
index = ["none","gr"]
for scale in range(14,20):
    sizes.append((scale,pow(2,14)))
runner.v_ingest("Vertex Ingest Rate as a function of size (time)",["size"],propertyFile,sizes,index,threads,page_size)


