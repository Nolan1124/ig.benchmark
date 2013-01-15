name = "Transaction Size"
description = "Vertex Ingestion as a function of transaction size.",
__problem_size = {
    "mini":{"graph_size":[pow(2,21)]},
    "small":{"graph_size":[pow(2,22)]},
    "medium":{"graph_size":[pow(2,23)]},
    "large":{"graph_size":[pow(2,24)]},
    "huge":{"graph_size":[pow(2,25)]},
}

txsize = []
cases = []
for _txsize in range(1,21):
    tx_size = pow(2,_txsize)
    graph_size = tx_size*5
    cases.append({
            #"name":"f_txsize",
            "description":"Vertex Ingestion as a function of transaction size.",
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
                }
            }
                 )
    
