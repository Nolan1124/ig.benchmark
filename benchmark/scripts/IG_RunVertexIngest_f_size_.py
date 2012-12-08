from IG_RunCommon import *
from IG_PropertyFile import *
import IG_Config

propertyFile = IG_PropertyFile("ig.properties")
runner = Runner(IG_Config.Config)
runner.initialize()

sizes = []
page_size = [16384]
threads = [4]
index = ["none","gr"]
for scale in range(14,20):
    sizes.append((scale,pow(2,14)))
runner.v_ingest("Vertex Ingest Rate as a function of size (time)",["size"],propertyFile,sizes,index,threads,page_size)


