name = "Standard Ingest"
description = "Standard Ingestion as a function of density and graph size"

threads = [1]
txsize  = pow(2,14)
page_size = 14

graph_scale = []
for i in range(16,20):
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

cases = [
    {
        "name":"ingest",
        "description":"Edge Ingestion.",
        "type":"graph_e_standard_ingest",
        "data":
        {
            "scale":graph_scale,
            "factor":[2,3,4,5,6,7,8,9,10]
            "page_size":[page_size],
            "threads":threads,
            "index":["gr"],
            "txsize":[txsize],
            "engine":["ig3","ig2"],
            },
        "table_view":table_view,
        "plot_view":plot_view
        }
    ]
   
   
