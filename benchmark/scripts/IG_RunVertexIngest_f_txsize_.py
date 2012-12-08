from IG_RunCommon import *
from IG_PropertyFile import *
import IG_Config

propertyFile = IG_PropertyFile("ig.properties")
runner = Runner(IG_Config.Config)
runner.initialize()

page_size = [16384]
sizes = []
index = ["none","gr"]
threads = [1]
for txsize in range(4,16):
    sizes.append((txsize+4,pow(2,txsize)))
    pass
runner.v_ingest("Vertex Ingest Rate as a function of transaction size",["txsize"],propertyFile,sizes,index,threads,page_size)

