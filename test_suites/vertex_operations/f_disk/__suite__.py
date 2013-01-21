name = "Disk"
description = "Vertex Ingestion as a function of number of disks used."


table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
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
        ]
    }

cases = []

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
        cases.append(
            {
                "name":"search",
                "description":"Vertex Search as a function of number of disks/threads.",
                "type":"graph_v_search",
                "data":
                {
                    "page_size":[14],
                    "search_size":[[pow(2,14),pow(2,14)],[pow(2,15),pow(2,15)]],
                    "threads":[1,2,3,4,5,6,7,8],
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
