import db_benchmark
import os
import base
import time
import sys
import db_objects
import EdgeGenerator

class operation(db_benchmark.operation):
    def __init__(self):
        db_benchmark.operation.__init__(self)
        self.add_argument("connections","eval",2,"number of connections per vertex.")
        self.add_argument("depth","int",10,"depth")
        self.add_argument("limit","int",10000,"limit the number of vertices.")
        self.add_argument("cache","eval",(1000,500000),"cache size given as a set of tuplets (in kB) (init,max) or [(init_1,max_1),(init_2,max_2),.....]")
        self.tag_object = None
        self.case_object = None
        self.cache = None
        self.map_oid = False
        pass

    def run(self,db,suite,case,data,**kwargs):
        self.case_object = case
        self.verbose = kwargs["verbose"]
        self.db = db
        
        self.connections = self.getOption_data(data,"connections")
        self.depth = self.getOption_data(data,"depth")
        self.limit = self.getOption_data(data,"limit")
        
        self.diskmap = self.getOption_data(data,"diskmap")
        self.hostmap = self.getOption_data(data,"hostmap")
        self.engine = self.getOption_data(data,"engine")
        self.page_size = self.getOption_data(data,"page_size")
        self.cache = self.getOption_data(data,"cache")

        self.setup_engine_objects()
        self.setup_page_sizes(self.page_size)
        self.tag_object = self.db.create_unique_object(db_objects.model.tag,"name",kwargs["tag"],
                                                       timestamp=self.db.now_string(True))
        self.run_operation()
        pass

    def run_operation(self):
        for engine in self.engine_objects:
            for _page_size in self.page_size:
                for _connections_ in self.connections:
                    for _cache in self.cache:
                        try:
                            os.remove("object_id.map")
                        except:
                            pass
                        pass
                    
                        edgeFile = "edges_%d.txt"%(_connections_)
                        generator = EdgeGenerator.Generate(edgeFile,_connections_,self.depth,self.limit)
                        generator.run()
                        _s_ =  "\tconnections:%d vertices:%d depth:%d"%(_connections_,generator.getNumber(False),self.depth)
                        print self.output_string(_s_,base.Colors.Blue,True)
                        sys.stdout.flush()
                        
                        self.initialize_property(engine.name)
                        self.propertyFile.setInitCache(_cache[0])
                        self.propertyFile.setMaxCache(_cache[1])
                        self.propertyFile.properties["IG.PageSize"] = _page_size
                        self.ig_setup_placement(engine.name,self.propertyFile)
                        
                        _index = "none"
                        _txsize = 50000
                        _v_size = generator.getNumber(False) + 1
                        _s_ = "\tgraph(%s) create index:%s page_size:%d"%(engine.name,_index,_page_size)
                        print self.output_string(_s_,base.Colors.Blue,True),

                        sys.stdout.flush()
                        start = time.clock()
                        self.ig_run(engine.name,self.propertyFile,"create",_index)
                        elapsed = (time.clock() - start)
                        
                        print self.output_string(str(elapsed),base.Colors.Red,False)
                        self.ig_setup_Location(engine.name,self.propertyFile)
                        
                        _s_ = "\t\tgraph(%s) standard ingest edges index:%s page_size:%d tx_size:%d size:%d diskmap:%s"%(engine.name,_index,_page_size,_txsize,_v_size,str(self.diskmap))
                        print self.output_string(_s_,base.Colors.Blue,True)

                        self.ig_v_ingest(engine.name,self.propertyFile,_index,_v_size,0,1,_txsize,"vprofileName",True)
                        self.ig_e_standard_ingest(engine.name,self.propertyFile,_index,_v_size,1,_txsize,"eprofileName",edgeFile)

                       
                        f = file("search.txt","w")
                        print >> f,"0,1"
                        f.flush()
                        f.close()
                        self.ig_navigate("dfs",engine.name,self.propertyFile,_index,_v_size,1,_txsize,"navigate_profileName","search.txt")
                        try:
                            os.remove("object_id.map")
                        except:
                            pass
                        pass
                    pass
                pass
            pass
        pass
    
    def operate(self):
        if db_benchmark.operation.operate(self):
            self.connections = self.getOption("connections")
            self.depth = self.getSingleOption("depth")
            self.limit = self.getSingleOption("limit")
            self.cache = self.getOption("cache")
            self.run_operation()
        return False

        
