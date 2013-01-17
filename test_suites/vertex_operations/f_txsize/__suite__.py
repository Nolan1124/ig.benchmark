name = "Transaction Size"
description = "Vertex Ingestion as a function of transaction size."

problem_size = {
    "mini":{"graph_size":[pow(2,20)]},
    "small":{"graph_size":[pow(2,21)]},
    "medium":{"graph_size":[pow(2,22)]},
    "large":{"graph_size":[pow(2,23)]},
    "huge":{"graph_size":[pow(2,24)]},
}

txsize = []
cases = []
for _txsize in range(8,18):
    tx_size = pow(2,_txsize)
    graph_size = tx_size*5
    cases.append({
        "name":"ingest",
        "description":"Vertex Ingestion as a function of transaction size (page_size=%d)."%(pow(2,14)),
        "type":"graph_v_ingest",
        "data":
        {
            "graph_size":[graph_size],
            "page_size":[14],
            "threads":[1],
            "index":["none","gr"],
            "txsize":[tx_size],
            "engine":["ig2","ig3"],
            "new":1,
            },
        "table_view":[
            [{"sTitle":"Database engine"},{"content":"object.engine()"}],
            [{"sTitle":"Transaction size"},{"content":"object.tx_size()"}],
            [{"sTitle":"Index Type"},{"content":"object.index_type()"}],
            [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
            [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
            ],
        "plot_view":{
            "plot":[
                {"name":"rate","data":("object.rate_avg()","math.log(object.tx_size(),2)"),"xaxis":"pow(2,Transaction size)"},
                {"name":"memory","data":("object.memory_used_avg()*1e-6","math.log(object.tx_size(),2)"),"xaxis":"pow(2,Transaction size)"},
                ],
            "ivar":[
                {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
                {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
                {"name":"Index Type","id":"object.index_type_id()","content":"object.index_type()"},
                ]
            }
        })
    
    
