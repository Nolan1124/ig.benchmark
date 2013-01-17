import db_benchmark
import os
import base
import time
import sys
import db_objects
import random

class operation(db_benchmark.operation):
    def __init__(self):
        db_benchmark.operation.__init__(self)
        self.add_argument("index","str","none","index type")
        self.add_argument("size","eval",pow(2,12),"number of vertices.")
        self.add_argument("search_size","eval",None,"The number of vertices to search for.")
        self.add_argument("seed","int",0,"Random seed used in generating search list.")
        self.add_argument("threads","eval",1,"number of threads")
        self.add_argument("txsize","eval",10000,"transaction size")
        self.add_argument("cache","eval",(1000,500000),"cache size given as a set of tuplets (in kB) (init,max) or [(init_1,max_1),(init_2,max_2),.....]")
        self.tag_object = None
        self.case_object = None
        self.cache = None
        pass

    def generate_random_searchlist(self,fileName,randomGenerator,size,graphSize):
        searchListFile = file(fileName,"w")
        for i in xrange(size):
            print >> searchListFile,randomGenerator.randint(1,graphSize)
            pass
        searchListFile.flush()
        searchListFile.close()
        pass
    
    def run(self,db,suite,case,data,**kwargs):
        self.case_object = case
        self.verbose = kwargs["verbose"]
        self.db = db
        suite_problem_size = suite.get_problem_size()
        problem_size = kwargs["problem_size"]
        if suite_problem_size:
            current_problem_size = suite_problem_size[problem_size]
            if current_problem_size:
                for i in current_problem_size:
                    data[str(i)] = current_problem_size[str(i)]
                    pass
                pass
            pass
        
        self.engine = self.getOption_data(data,"engine")
        self.index = self.getOption_data(data,"index")
        self.page_size = self.getOption_data(data,"page_size")
        self.txsize = self.getOption_data(data,"txsize")
        self.threads = self.getOption_data(data,"threads")
        self.graph_size = self.getOption_data(data,"graph_size")[0]
        self.cache = self.getOption_data(data,"cache")
        self.search_size = self.getOption_data(data,"search_size")
        self.seed = self.getOption_data(data,"seed")
        self.setup_engine_objects()
        self.setup_page_sizes(self.page_size)
        self.tag_object = self.db.create_unique_object(db_objects.model.tag,"name",kwargs["tag"],
                                                       timestamp=self.db.now_string(True))
        self.run_operation()
        pass

    def run_operation(self):
        random.seed(self.seed)
        for _index in self.index: 
            for _page_size in self.page_size:
                for _v_size in self.search_size:
                    for _threads in self.threads:
                        for _txsize in self.txsize:
                            for _cache in self.cache:
                                for engine in self.engine_objects:
                                    boot_file_path = self.config.BootFilePath[engine.name]
                                    boot_file_name = os.path.join(boot_file_path,"bench.boot")
                                    search_file_name = "searchlist.data"
                                    self.generate_random_searchlist(search_file_name,random,_v_size,self.graph_size)
                                    print 
                                    self.propertyFile.initialize()
                                    self.propertyFile.setInitCache(_cache[0])
                                    self.propertyFile.setMaxCache(_cache[1])
                                    self.propertyFile.properties["IG.PageSize"] = _page_size
                                    _s_ = "\tgraph(%s) search vertices index:%s page_size:%d tx_size:%d size:%d search_size:%d cache_init:%d cache_max:%d"%(engine.name,_index,_page_size,_txsize,_v_size,self.graph_size,_cache[0],_cache[1])
                                    print self.output_string(_s_,base.Colors.Blue,True)
                                    profileName = "search.profile"
                                    if self.tag_object:
                                        profileName = self.tag_object.name +"_"+ self.db.now_string(True)  +"_"+ ".profile"
                                        profileName = profileName.replace(" ","_")
                                        pass

                                    run_counter = 0
                                    done = False
                                    while not done:
                                        if run_counter > 0:
                                            print self.output_string("Retrying search (%d)"%(run_counter),base.Colors.Red,True)
                                        self.ig_v_search(search_file_name,engine.name,self.propertyFile,_index,_v_size,self.graph_size,_threads,_txsize,profileName)
                                        f = file(profileName,"r")
                                        line = f.read()
                                        data = eval(line)
                                        f.close()
                                        if(_v_size == data["opsize"]):
                                            done = True
                                        elif run_counter >= 3:
                                            done = True
                                        else:
                                            os.remove(profileName)
                                        run_counter += 1
                                        
                                    if self.case_object:
                                        f = file(profileName,"r")
                                        line = f.read()
                                        data = eval(line)
                                        platform_object = self.db.create_unique_object(db_objects.model.platform,"name",data["os"])
                                        index_object = self.db.create_unique_object(db_objects.model.index_type,"name",_index)

                                        assert(_v_size == data["opsize"])
                                        case_data_object = self.db.create_object(db_objects.model.case_data,
                                                                                 timestamp=self.db.now_string(True),
                                                                                 case_id=self.case_object.id,
                                                                                 tag_id=self.tag_object.id,
                                                                                 engine_id=engine.id,
                                                                                 size=data["size"],
                                                                                 time=data["time"],
                                                                                 memory_init=data["mem_init"],
                                                                                 memory_used=data["mem_used"],
                                                                                 memory_committed=data["mem_committed"],
                                                                                 memory_max=data["mem_max"],
                                                                                 op_size=data["opsize"],
                                                                                 rate=data["rate"],
                                                                                 page_size=_page_size,
                                                                                 cache_init=self.propertyFile.getInitCache(),
                                                                                 cache_max=self.propertyFile.getMaxCache(),
                                                                                 tx_size=_txsize,
                                                                                 platform_id=platform_object.id,
                                                                                 threads=_threads,
                                                                                 index_id=index_object.id,
                                                                                 status=1
                                                                                 )
                                        case_data_key = case_data_object.generateKey()
                                        case_data_stat_object = self.db.fetch_using_generic(db_objects.model.case_data_stat,
                                                                                            key=case_data_key,
                                                                                            case_id=self.case_object.id
                                                                                            )
                                        if (len(case_data_stat_object) == 0):
                                            case_data_stat_object = self.db.create_unique_object(db_objects.model.case_data_stat,
                                                                                                 "key",case_data_key,
                                                                                                 case_id=self.case_object.id
                                                                                                 )
                                        else:
                                            case_data_stat_object = case_data_stat_object[0]
                                            pass
                                        case_data_stat_object.addCounter()
                                        case_data_stat_object.setRateStat(data["rate"])
                                        case_data_stat_object.setTimeStat(data["time"])
                                        case_data_stat_object.setMemInitStat(data["mem_init"])
                                        case_data_stat_object.setMemUsedStat(data["mem_used"])
                                        case_data_stat_object.setMemCommittedStat(data["mem_committed"])
                                        case_data_stat_object.setMemMaxStat(data["mem_max"])
                                        self.db.update(case_data_stat_object)
                                        f.close()
                                        os.remove(profileName)
                                        pass
                                    pass
                                pass
                            pass
                        pass
                    pass
                pass
            pass
        pass
    
    def operate(self):
        if db_benchmark.operation.operate(self):
            self.index = self.getOption("index")
            self.graph_size = self.getSingleOption("size")
            self.threads = self.getOption("threads")
            self.txsize = self.getOption("txsize")
            self.cache = self.getOption("cache")
            self.search_size = self.getOption("search_size")
            self.seed = self.getSingleOption("seed")
            self.seed = self.getSingleOption("seed")
            self.run_operation()
        return False

        
