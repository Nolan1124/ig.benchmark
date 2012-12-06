from IG_RunCommon import *
from IG_PropertyFile import *
import IG_Config

propertyFile = IG_PropertyFile("v_ingest_f_tx.properties")
propertyFile.properties["IG.UseMROWTransactions"] = "false"
propertyFile.properties["IG.Indexing.GraphIndexSensitive"] = "true"
propertyFile.properties["IG.SessionPool.ThreadBasedSessionPool.InitialCacheSizeKb"]=1000
propertyFile.properties["IG.SessionPool.ThreadBasedSessionPool.MaximumCacheSizeKb"]=5000000
propertyFile.properties["IG.SessionPool.ThreadBasedSessionPool.LockWaitTime"]=10
propertyFile.properties["IG.PageSize"]=65536
runner = Runner(IG_Config.Config)
runner.initialize()

sizes = []
for txsize in range(4,8):
    sizes.append((txsize+4,pow(2,txsize)))

runner.v_ingest_f_tx(propertyFile,sizes,"none")
runner.v_ingest_f_tx(propertyFile,sizes,"gr")



