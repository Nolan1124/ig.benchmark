name = "Cache"
description = "Vertex Ingestion as a function of search size set and cache size."

threads = 1
txsize  = pow(2,14)
page_size = 14

def MB(value):
    return value*1000
counter = pow(2,20)
graph_size = [counter]
search_size = []


search_cache = []
for i in range(1,5,1):
    search_cache.append([MB(1),MB(i)])
    pass
search_cache.append([MB(1),MB(500)])

max_size = 17
for i in range(10,max_size+1):
    search_size.append([pow(2,max_size),pow(2,i)])
    pass

table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Graph Size"},{"content":"object.graph_size()"}],
    [{"sTitle":"Index Type"},{"content":"'index:%s'%(object.index_type())"}],
    [{"sTitle":"Threads"},{"content":"'%dT'%(object.threads())"}],
    [{"sTitle":"Cache Max(MB)"},{"content":"'%.0fMB'%(1e-3*object.cache_max())"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    ]

plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","math.log(object.cache_max()*1e-3,10)"),"xaxis":"Cache Size max = pow(10,x)"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","math.log(object.cache_max()*1e-3,10)"),"xaxis":"Cache Size max = pow(10,x)"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        {"name":"Index Type","id":"object.index_type_id()","content":"object.index_type()"},
        {"name":"Graph size","id":"object.graph_size()","content":"'%dM'%(int(1.0*object.graph_size()/pow(2,20)))"},
        {"name":"Threads","id":"object.threads()","content":"object.threads()"},
        ]
    }

search_table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Graph Size"},{"content":"object.graph_size()"}],
    [{"sTitle":"Threads"},{"content":"'%dT'%(object.threads())"}],
    [{"sTitle":"Search Size"},{"content":"object.op_size()"}],
    [{"sTitle":"Sample Size"},{"content":"object.object_data('search_set_size',object.graph_size())"}],
    [{"sTitle":"Cache Max(MB)"},{"content":"'%.0fMB'%(1e-3*object.cache_max())"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    
    ]

search_plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","math.log(1.0*object.op_size()/object.object_data('search_set_size',object.graph_size()),2)"),"xaxis":"(Search size)/(Sample Size) = pow(2,x)"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","math.log(1.0*object.op_size()/object.object_data('search_set_size',object.graph_size()),2)"),"xaxis":"(Search size)/(Sample Size) = pow(2,x)"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        {"name":"Threads","id":"object.threads()","content":"object.threads()"},
        {"name":"Search Size","id":"object.op_size()","content":"object.op_size()"},
        {"name":"Cache (initial,max) (MB)","id":"object.cache_max()","content":"'(%.0f,%.0f)'%(object.cache_init()*1e-3,object.cache_max()*1e-3)"},
        ]
    }

cases = []
for engine in ["ig3","ig2"]:
    cases.append({
        "name":"ingest",
        "description":"Vertex Ingestion vs. cache size (txsize=%d,page_size=%d)"%(txsize,pow(2,page_size)),
        "type":"graph_v_ingest",
        "data":
        {
            "graph_size":graph_size,
            "page_size":[page_size],
            "threads":[threads],
            "index":["gr"],
            "txsize":[txsize],
            "engine":[engine],
            "new":1,
            },
        "table_view":table_view,
        "plot_view":plot_view
        })
    cases.append({
        "name":"search",
        "description":"Indexed Vertex Search as a function of cache size and search size set (graph_size=%d,txsize=%d,page_size=%d)"%(graph_size[0],txsize,pow(2,page_size)),
        "type":"graph_v_search",
        "data":
        {
            "graph_size":graph_size,
            "search_size":search_size,
            "page_size":[page_size],
            "threads":[1,2,3,4],
            "index":["gr"],
            "txsize":[txsize],
            "engine":[engine],
            "cache":search_cache,
            },
        "table_view":search_table_view,
        "plot_view":search_plot_view
        })
    pass
    
ingest_cache = []
ingest_cache.append([MB(1),MB(1)])
ingest_cache.append([MB(1),MB(10)])
ingest_cache.append([MB(1),MB(100)])
ingest_cache.append([MB(1),MB(1000)])

for engine in ["ig3","ig2"]:
    cases.append({
        "name":"ingest",
        "description":"Vertex Ingestion vs. cache size (txsize=%d,page_size=%d)"%(txsize,pow(2,page_size)),
        "type":"graph_v_ingest",
        "data":
        {
            "graph_size":[pow(2,20),pow(2,21),pow(2,22),pow(2,23),pow(2,24)],
            "page_size":[page_size],
            "threads":[1,2,3,4],
            "index":["none","gr"],
            "txsize":[txsize],
            "engine":[engine],
            "new":1,
            "cache":ingest_cache,
            },
        "table_view":table_view,        
        "plot_view":plot_view
        })    
