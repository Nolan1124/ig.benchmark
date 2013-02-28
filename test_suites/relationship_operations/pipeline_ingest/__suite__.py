name = "Pipeline Ingest"
description = "Pipeline Ingestion as a function of density, graph size and threads"

threads = [1,2,3,4]
txsize  = pow(2,14)
page_size = 14

graph_scale = []
for i in range(18,21):
    graph_scale.append(i)
    pass

cases = []
table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Graph Size"},{"content":"object.graph_size()"}],
    [{"sTitle":"Edge Size"},{"content":"object.op_size()"}],
    [{"sTitle":"Threads"},{"content":"object.threads()"}],
    [{"sTitle":"Index Type"},{"content":"object.index_type()"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    ]


plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","object.object_data('edge_factor',0)"),"xaxis":"Edge Factor"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","object.object_data('edge_factor',0)"),"xaxis":"Edge Factor"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        {"name":"Index Type","id":"object.index_type_id()","content":"object.index_type()"},
        {"name":"Threads","id":"object.threads()","content":"object.threads()"},
        {"name":"Graph Size (M)","id":"object.graph_size()","content":"object.graph_size()*1e-6"},
        ]
    }

plot_view_vs_threads = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","object.threads()"),"xaxis":"Threads"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","object.threads()"),"xaxis":"Edge Factor"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        {"name":"Index Type","id":"object.index_type_id()","content":"object.index_type()"},
        #{"name":"Threads","id":"object.threads()","content":"object.threads()"},
        {"name":"Graph Size (M)","id":"object.graph_size()","content":"object.graph_size()*1e-6"},
        {"name":"Edge Factor","id":"object.object_data('edge_factor',0)","content":"object.object_data('edge_factor',0)"},
        ]
    }



    
cases = [
    {
        "name":"ingest",
        "description":"Edge Ingestion.",
        "type":"graph_e_ingest",
        "data":
        {
            "scale":graph_scale,
            "factor":[2,4,8], #,,16,32,64],
            "page_size":[page_size],
            "threads":threads,
            "index":["none"],
            "txsize":[txsize],
            "engine":["ig3","ig2"],
            },
        "table_view":table_view,
        "plot_view":plot_view_vs_threads
        #"plot_view":plot_view
        }
    ]
   
   
