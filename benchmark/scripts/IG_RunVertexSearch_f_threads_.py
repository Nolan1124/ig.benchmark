from IG_RunCommon import *
from IG_PropertyFile import *
import IG_Config

propertyFile = IG_PropertyFile("ig.properties")
runner = Runner(IG_Config.Config)
runner.initialize()

page_size = [16384]
ingest_threads = [4]
search_threads = [1,2,3,4,5,6,7,8,9,10]
index = ["gr"]
search_size = pow(2,14)
search_seed = 0
scale = 24
size_counter = 1
txsize = pow(2,14)

runner.v_search("Vertex Search Rate as a function of threads (search size:%d)"%(search_size),
                ["threads"],
                propertyFile,
                scale,
                size_counter,
                txsize,
                index,
                ingest_threads,
                search_threads,
                page_size,
                search_size,
                search_seed
                )


