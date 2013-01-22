name = "Page size"
description = "Vertex Ingestion as a function of page size."

table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Page size"},{"content":"object.page_size()"}],
    [{"sTitle":"Index Type"},{"content":"'index:%s'%(object.index_type())"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    ]

plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","math.log(object.page_size(),2)"),"xaxis":"page size = pow(2,x)"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","math.log(object.page_size(),2)"),"xaxis":"page size = pow(2,x)"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        {"name":"Index Type","id":"object.index_type_id()","content":"object.index_type()"},
        ]
    }

search_table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Page Size"},{"content":"object.page_size()"}],
    #   [{"sTitle":"Threads"},{"content":"'%dT'%(object.threads())"}],
   # [{"sTitle":"Search Size"},{"content":"object.op_size()"}],
   # [{"sTitle":"Sample Size"},{"content":"object.object_data('search_set_size',object.graph_size())"}],
    [{"sTitle":"Cache Max(MB)"},{"content":"'%.0fMB'%(1e-3*object.cache_max())"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    
    ]

search_plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","math.log(1.0*object.page_size(),2)"),"xaxis":"Page Size = pow(2,x)"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","math.log(1.0*object.page_size(),2)"),"xaxis":"Page Size = pow(2,x)"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        ]
    }

txsize = pow(2,14)
graph_size = pow(2,20)
def MB(value):
    return value*1000
cases = []
for page_size in [16,15,14,13,12,11,10]:
    cases.append(
        {
            "name":"ingest",
            "description":"Vertex Ingestion as a function of page size (transaction_size=%d graph_size=%d)."%(txsize,graph_size),
                    "type":"graph_v_ingest",
            "data":
            {
                "page_size":[page_size],
                "threads":[1],
                "index":["none"],
                "txsize":[txsize],
                "engine":["ig2","ig3"],
                "new":1,
                "graph_size":[graph_size]
                },
            "table_view":table_view,
            "plot_view":plot_view
            }
        )
    for engine in ["ig2","ig3"]:
        cases.append(
            {
                "name":"ingest",
                "description":"Vertex Ingestion as a function of page size (transaction_size=%d graph_size=%d)."%(txsize,graph_size),
                "type":"graph_v_ingest",
                "data":
                {
                    "page_size":[page_size],
                    "threads":[1],
                    "index":["gr"],
                    "txsize":[txsize],
                    "engine":[engine],
                    "new":1,
                    "graph_size":[graph_size]
                    },
                "table_view":table_view,
                "plot_view":plot_view
                }
            )
        cases.append(
            {
                "name":"search",
                "description":"Indexed Vertex Search as a function of page size (transaction_size=%d graph_size=%d)."%(txsize,graph_size),
                "type":"graph_v_search",
                "data":
                {
                    "graph_size":[graph_size],
                    "search_size":[txsize],
                    "page_size":[page_size],
                    "threads":[1],
                    "index":["gr"],
                    "txsize":[txsize],
                    "engine":[engine],
                    },
                "table_view":search_table_view,
                "plot_view":search_plot_view
                }
            )
        pass
    pass
