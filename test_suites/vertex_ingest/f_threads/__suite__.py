name = "Threads"
description = "Vertex Ingestion as a function of number of threads."
problem_size = {
    "mini":{"graph_size":[pow(2,20)]},
    "small":{"graph_size":[pow(2,21)]},
    "medium":{"graph_size":[pow(2,22)]},
    "large":{"graph_size":[pow(2,23)]},
    "huge":{"graph_size":[pow(2,24)]},
}

cases = [
    {
        #"name":"f_threads",
        "description":"Vertex Ingestion as a function of number of threads.",
        "type":"graph_v_ingest",
        "data":
        {
            "page_size":[14],
            "threads":[1,2,3,4,5,6,7,8],
            "index":["none","gr"],
            "txsize":[pow(2,14)],
            "engine":["ig2","ig3"],
            "new":1,
            },
        "table_view":[
            [{"sTitle":"Database engine"},{"content":"object.engine()"}],
           # [{"sTitle":"Platform"},{"content":"object.platform()"}],
            [{"sTitle":"Threads"},{"content":"object.threads()"}],
            [{"sTitle":"Index Type"},{"content":"object.index_type()"}],
            [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
        #    [{"sTitle":"Time (ms)"},{"content":"object.time_avg()"}],
            [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
            ],
        "plot_view":{
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
        },
    ]
