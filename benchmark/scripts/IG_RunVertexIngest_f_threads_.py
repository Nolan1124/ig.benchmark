from IG_RunCommon import *
from IG_PropertyFile import *
import IG_Config

propertyFile = IG_PropertyFile("ig.properties")
runner = Runner(IG_Config.Config)
runner.initialize()

page_size = [16384]
threads = [1,2,3,4,5,6,7,8]
sizes = [(20,pow(2,14))]
index = ["none","gr"]
runner.v_ingest("Vertex Ingest Rate as a function of number of threads",["threads"],propertyFile,sizes,index,threads,page_size)


