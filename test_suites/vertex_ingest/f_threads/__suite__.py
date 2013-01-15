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
            }
        },
    ]
