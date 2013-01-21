name = "Disk"
description = "Vertex Ingestion as a function of number of disks used."


table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Disks"},{"content":"object.object_data('diskmap','n/a')"}],
    [{"sTitle":"Threads"},{"content":"object.threads()"}],
    [{"sTitle":"Index Type"},{"content":"object.index_type()"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    ]

plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","object.threads()"),"xaxis":"Threads"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","object.threads()"),"xaxis":"Threads"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        {"name":"Index Type","id":"object.index_type_id()","content":"object.index_type()"},
        {"name":"Disks","id":"object.object_data('diskmap',0)","content":"object.object_data('diskmap','n/a')"},
        ]
    }



search_table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Disks"},{"content":"object.object_data('diskmap','n/a')"}],
    [{"sTitle":"Threads"},{"content":"object.threads()"}],
    [{"sTitle":"Search Size"},{"content":"object.op_size()"}],
    [{"sTitle":"Index Type"},{"content":"object.index_type()"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    ]

search_plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","object.threads()"),"xaxis":"Threads"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","object.threads()"),"xaxis":"Threads"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        {"name":"Index Type","id":"object.index_type_id()","content":"object.index_type()"},
        {"name":"Disks","id":"object.object_data('diskmap',0)","content":"object.object_data('diskmap','n/a')"},
        {"name":"Search Size","id":"object.op_size()","content":"object.op_size()"},
        {"name":"Cache (initial,max) (MB)","id":"object.cache_max()","content":"'(%.0f,%.0f)'%(object.cache_init()*1e-3,object.cache_max()*1e-3)"},
        ]
    }

cases = []


for diskmap in [1,2,3,4]:
    for engine in ["ig3","ig2"]:
        cases.append(
            {
                "name":"ingest",
                "description":"Vertex Ingestion as a function of number of disks threads.",
                "type":"graph_v_ingest",
                "data":
                {
                    "page_size":[14],
                    "threads":[1],
                    "index":["gr"],
                    "txsize":[pow(2,14)],
                    "engine":[engine],
                    "new":1,
                    "diskmap":diskmap,
                    "graph_size":[pow(2,20)]
                    },
                "table_view":table_view,
                "plot_view":plot_view
                }
            )
        for t in [1,2,3,4,5,6,7,8]:
            cases.append(
                {
                    "name":"search",
                    "description":"Vertex Search as a function of number of disks/threads.",
                    "type":"graph_v_search",
                    "data":
                    {
                        "page_size":[14],
                        "search_size":[[pow(2,14)*t,pow(2,20)]],
                        "threads":[t],
                        "index":["gr"],
                        "txsize":[pow(2,14)],
                        "engine":[engine],
                        "diskmap":diskmap,
                        "graph_size":[pow(2,20)]
                        },
                    "table_view":search_table_view,
                    "plot_view":search_plot_view
                    }
                )
            pass
        pass
    pass
            
            
for diskmap in [1,2,3,4]:
    cases.append(
        {
            "name":"ingest",
            "description":"Vertex Ingestion as a function of number of disks threads.",
            "type":"graph_v_ingest",
            "data":
            {
                "page_size":[14],
                "threads":[1,2,3,4,5,6,7,8],
                "index":["none","gr"],
                "txsize":[pow(2,14)],
                "engine":["ig2","ig3"],
                "new":1,
                "diskmap":diskmap,
                "graph_size":[pow(2,20)]
                },
            "table_view":table_view,
            "plot_view":plot_view
            }
        )
    pass
