name = "Page size"
description = "Vertex Ingestion as a function of page size."

problem_size = {
    "mini":{"graph_size":[pow(2,16)]},
    "small":{"graph_size":[pow(2,17)]},
    "medium":{"graph_size":[pow(2,18)]},
    "large":{"graph_size":[pow(2,19)]},
    "huge":{"graph_size":[pow(2,20)]},
}


txsize = pow(2,14)
cases = [
    {
        "description":"Vertex Ingestion as a function of page size (transaction_size=%d)."%(txsize),
        "type":"graph_v_ingest",
        "data":
        {
            "page_size":[10,11,12,13,14,15,16],
            "threads":[1],
            "index":["none"],
            "txsize":[txsize],
            "engine":["ig2","ig3"],
            "new":1,
            },
        "table_view":[
            [{"sTitle":"Database engine"},{"content":"object.engine()"}],
            [{"sTitle":"Page size"},{"content":"object.page_size()"}],
            [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
            [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
            ],
        "plot_view":{
            "plot":[
                {"name":"rate","data":("object.rate_avg()","math.log(object.page_size(),2)"),"xaxis":"page size [log2]"},
                {"name":"memory","data":("object.memory_used_avg()*1e-6","math.log(object.page_size(),2)"),"xaxis":"page size [log2]"},
                ],
            "ivar":[
                {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
                {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
                ]
            }
        },
    ]

