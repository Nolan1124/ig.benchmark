from IG_RunCommon import *
from IG_PropertyFile import *
import IG_Config

propertyFile = IG_PropertyFile("ig.properties")
runner = Runner(IG_Config.Config)
runner.initialize()

page_size = [16384]
ingest_threads = [4]
search_threads = [1]
index = ["gr"]
search_size = pow(2,14)
search_seed = 0
scale = 19
size_counter = 100
txsize = pow(2,14)

runner.v_search("Vertex Search Rate as a function of size (search size:%d)"%(txsize),
                ["size"],
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


