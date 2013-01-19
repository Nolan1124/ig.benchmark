name = "Graph Size"
description = "Vertex Ingestion as a function of graph size."

threads = 1
txsize  = pow(2,14)
page_size = 14


counter = pow(2,20)
increment = counter
graph_size = []
for i in range(1,21):
    graph_size.append(counter)
    counter += increment
    pass

cases = []
table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Graph Size"},{"content":"object.graph_size()"}],
    [{"sTitle":"Index Type"},{"content":"object.index_type()"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    ]

plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","object.graph_size()*1e-6"),"xaxis":"Graph Size (million)"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","object.graph_size()*1e-6"),"xaxis":"Graph Size (million)"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        {"name":"Index Type","id":"object.index_type_id()","content":"object.index_type()"},
        ]
    }

search_table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Graph Size"},{"content":"object.graph_size()"}],
    [{"sTitle":"Search Size"},{"content":"object.op_size()"}],
    [{"sTitle":"Cache Max(MB)"},{"content":"'%.0f'%(1e-3*object.cache_max())"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    ]

search_plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","object.graph_size()*1e-6"),"xaxis":"Graph Size (million)"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","object.graph_size()*1e-6"),"xaxis":"Graph Size (million)"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        {"name":"Threads","id":"object.threads()","content":"object.threads()"},
        {"name":"Search Size","id":"object.op_size()","content":"object.op_size()"},
        {"name":"Cache (initial,max) (MB)","id":"object.cache_max()","content":"'(%.0f,%.0f)'%(object.cache_init()*1e-3,object.cache_max()*1e-3)"},
        ]
    }

def MB(value):
    return value*1000

search_size = [pow(2,14),2*pow(2,14)]
search_cache = [
    [MB(1),MB(1)],
    [MB(1),MB(10)],
    [MB(1),MB(100)],
    [MB(1),MB(1000)],
    ]
    
for g in graph_size:
    if 1:
        cases.append({
            "name":"ingest",
            "description":"Vertex Ingestion as a function of graph size (threads=%d,txsize=%d,page_size=%d)."%(threads,txsize,pow(2,page_size)),
            "type":"graph_v_ingest",
            "data":
            {
                "graph_size":[g],
                    "page_size":[page_size],
                "threads":[threads],
                "index":["none"],
                "txsize":[txsize],
                "engine":["ig2","ig3"],
                "new":1,
                },
            "table_view":table_view,
            "plot_view":plot_view
            })
    cases.append({
        "name":"ingest",
        "description":"Vertex Ingestion as a function of graph size (threads=%d,txsize=%d,page_size=%d)"%(threads,txsize,pow(2,page_size)),
        "type":"graph_v_ingest",
        "data":
        {
            "graph_size":[g],
            "page_size":[page_size],
            "threads":[threads],
            "index":["gr"],
            "txsize":[txsize],
            "engine":["ig2"],
            "new":1,
            },
        "table_view":table_view,
        "plot_view":plot_view
        })
   
    cases.append({
        "name":"search",
        "description":"Indexed Vertex Search as a function of graph size (txsize=%d,page_size=%d)"%(txsize,pow(2,page_size)),
        "type":"graph_v_search",
        "data":
        {
            "graph_size":[g],
            "search_size":search_size,
            "page_size":[page_size],
            "threads":[1,2,3,4],
            "index":["gr"],
            "txsize":[txsize],
            "engine":["ig2"],
            "cache":search_cache,
            },
        "table_view":search_table_view,
        "plot_view":search_plot_view
        })
    cases.append({
        "name":"ingest",
        "description":"Vertex Ingestion as a function of graph size (threads=%d,txsize=%d,page_size=%d)"%(threads,txsize,pow(2,page_size)),
        "type":"graph_v_ingest",
        "data":
        {
            "graph_size":[g],
            "page_size":[page_size],
            "threads":[threads],
            "index":["gr"],
            "txsize":[txsize],
            "engine":["ig3"],
            "new":1,
            },
        "table_view":table_view,
        "plot_view":plot_view
        })
    cases.append({
        "name":"search",
        "description":"Indexed Vertex Search as a function of graph size (txsize=%d,page_size=%d)"%(txsize,pow(2,page_size)),
        "type":"graph_v_search",
        "data":
        {
            "graph_size":[g],
            "search_size":search_size,
            "page_size":[page_size],
            "threads":[1,2,3,4],
            "index":["gr"],
            "txsize":[txsize],
            "engine":["ig3"],
            "cache":search_cache,
            },
        "table_view":search_table_view,
        "plot_view":search_plot_view
        })
    
    
