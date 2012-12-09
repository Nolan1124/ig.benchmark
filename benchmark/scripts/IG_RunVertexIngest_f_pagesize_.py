from IG_RunCommon import *
from IG_PropertyFile import *
import IG_Config

propertyFile = IG_PropertyFile("ig.properties")
runner = Runner(IG_Config.Config)
runner.initialize()

page_size = [1024,2048,4096,8192,16384,32768,65536]
sizes = [(23,pow(2,14))]
threads = [1]
index = ["none"]
runner.v_ingest("Vertex Ingest Rate as a function of page size",["page_size"],propertyFile,sizes,index,threads,page_size)

