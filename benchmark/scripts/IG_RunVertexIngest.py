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

if 0:
    propertyFile.properties["IG.BootFilePath"]="/Users/henocka/IG_data/"
    propertyFile.properties["IG.Placement.ImplClass"]="com.infinitegraph.impl.plugins.adp.DistributedPlacement"
    propertyFile.properties["IG.Placement.Distributed.Location.ig_db_a"]="127.0.0.1::/Users/henocka/IG_Data"
    propertyFile.properties["IG.Placement.Distributed.StorageSpec.SmallData.ContainerRange"]="1:*"
    propertyFile.properties["IG.Placement.Distributed.GroupStorage.GraphData"]="ig_db_a:SmallData"

runner = Runner(IG_Config.Config)
runner.initialize()

sizes = []
for txsize in range(4,8):
    sizes.append((txsize+4,pow(2,txsize)))

runner.v_ingest_f_tx(propertyFile,sizes)



