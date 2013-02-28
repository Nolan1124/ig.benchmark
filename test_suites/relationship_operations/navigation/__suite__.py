name = "GraphNavigation"
description = "Navigation as a function of graph density"

threads = [1]
page_size = [14]

limit = 1000000
connections = [2,3,4]

cases = []
table_view = [
    [{"sTitle":"Database engine"},{"content":"object.engine()"}],
    [{"sTitle":"Graph Size"},{"content":"'g:%d'%(object.graph_size())"}],
    [{"sTitle":"Connections"},{"content":"object.object_data('connections',0)"}],
    [{"sTitle":"Hops"},{"content":"'%d'%(object.op_size())"}],
    [{"sTitle":"Rate (v/s)"},{"content":"'%.2f'%(object.rate_avg())"}],
    [{"sTitle":"Heap Memory (MB)"},{"content":"'%.3f'%(object.memory_used_avg()*1e-6)"}],
    ]


plot_view = {
    "plot":[
        {"name":"rate","data":("object.rate_avg()","object.object_data('connections',0)"),"xaxis":"Connections"},
        {"name":"memory","data":("object.memory_used_avg()*1e-6","object.object_data('connections',0)"),"xaxis":"Connections"},
        ],
    "ivar":[
        {"name":"Database engine","id":"object.engine_id()","content":"object.engine()"},
        {"name":"Platform","id":"object.platform_id()","content":"object.platform()"},
        ]
    }

cases = [
    {
        "name":"graph_navigation",
        "description":"Graph Navigation",
        "type":"graph_navigate_dense",
        "data":
        {
            "connections":connections,
            "page_size":page_size,
            "engine":["ig3","ig2"],
            "depth":10,
            "limit":limit
            },
        "table_view":table_view,
        "plot_view":plot_view
        }
    ]
   
   
