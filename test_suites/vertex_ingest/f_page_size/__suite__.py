name = "ingest_vertex_f_page_size"
description = "Vertex Ingestion as a function of page size."
problem_size = {
    "mini":{"graph_size":[pow(2,16)]},
    "small":{"graph_size":[pow(2,17)]},
    "medium":{"graph_size":[pow(2,18)]},
    "large":{"graph_size":[pow(2,19)]},
    "huge":{"graph_size":[pow(2,20)]},
}

cases = [
    {
        "name":"ingest_vertex_f_page_size",
        "description":"Vertex Ingestion as a function of page size.",
        "type":"graph_v_ingest",
        "data":
        {
            "page_size":[10,11,12,13,14,15,16],
            "threads":[1],
            "index":["none"],
            "txsize":[pow(2,14)],
            "engine":["ig2","ig3"],
            "new":1,
            }
        },
    ]
