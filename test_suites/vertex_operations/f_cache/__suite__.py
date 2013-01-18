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

search_cache = [[MB(1),MB(1)]]
for i in range(5,20,5):
    search_cache.append([MB(1),MB(i)])
    pass

max_size = 17
for i in range(10,max_size+1):
    search_size.append([pow(2,max_size),pow(2,i)])
    pass

search_table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Graph Size"},{"content":"object.graph_size()"}],
    [{"sTitle":"Search Size"},{"content":"object.op_size()"}],
    [{"sTitle":"Sample Size"},{"content":"object.object_data('search_set_size',object.graph_size())"}],
    [{"sTitle":"Cache Max(MB)"},{"content":"'%.0f'%(1e-3*object.cache_max())"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    ]

search_plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","1.0*object.op_size()/object.object_data('search_set_size',object.graph_size())"),"xaxis":"Average number of repeats"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","1.0*object.op_size()/object.object_data('search_set_size',object.graph_size())"),"xaxis":"Average number of repeats"},
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
for engine in ["ig2","ig3"]:
    cases.append({
        "name":"ingest",
        "description":"Vertex Ingestion for search purposes (threads=%d,txsize=%d,page_size=%d)"%(threads,txsize,pow(2,page_size)),
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
            }
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
            "threads":[1],
            "index":["gr"],
            "txsize":[txsize],
            "engine":[engine],
            "cache":search_cache,
            },
        "table_view":search_table_view,
        "plot_view":search_plot_view
        })
    
    
    
