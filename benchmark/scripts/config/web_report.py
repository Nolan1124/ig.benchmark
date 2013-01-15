suite_view = [
    ({"sTitle":"Type"},{"content":"object.object_type()"}),
    ({"sTitle":"TimeStamp"},{"content":"object.timestamp"}),
    #({"sTitle":"Id"},{"content":"object.id"}),
    ({"sTitle":"Name"},{"content":'html_reference(object,object.name)'}),
    ({"sTitle":"Description"},{"content":"object.description"}),
    #({"sTitle":"Path"},{"content":"object.path"}),
    #({"sTitle":"Parent"},{"content":"object.parent"}),

    
    #({"sTitle":"Runs"},{"content":"object.runs"}),
    #({"sTitle":"Adhoc"},{"content":"object.adhoc"})
    ]



__complete_case_view__ = [
    ({"sTitle":"Id"},{"content":"object.id"}),
    ({"sTitle":"Case Id"},{"content":"object.case_id"}),
    ({"sTitle":"Tag"},{"content":"tag_name(object.tag_id).split()[0]"}),
    ({"sTitle":"Simulator"},{"content":"sim_name(object.sim_id)"}),
    ({"sTitle":"Device Type"},{"content":"sim_type_name(object.sim_type_id)"}),
    ({"sTitle":"Template"},{"content":"template_name(object.template_id)"}),
    ({"sTitle":"Timestamp"},{"content":"object.timestamp.split()[1]"}),
    ({"sTitle":"Size"},{"content":"object.size"}),
    ({"sTitle":"Time factor"},{"content":"object.time_factor"}),
    ({"sTitle":"Clock"},{"content":"object.clock_time"}),
    ({"sTitle":"CPU"},{"content":"'%2.3f'%(object.user_time + object.sys_time)"}),
    ({"sTitle":"Sys"},{"content":"object.sys_time"}),
    ({"sTitle":"Max Mem(MB)"},{"content":"'%2.2f'%(float(object.max_memory)*1e-6)"}),
    ({"sTitle":"Status"},{"content":'condition(object.status,"<FONT COLOR=\'green\'>ok</FONT>","<FONT COLOR=\'red\'>fail</FONT>")'}),
    ({"sTitle":"Platform"},{"content":"evaluate(object.data,'result[\"platform\"]','-')"}),
    ({"sTitle":"Internal events"},{"content":"evaluate_with_exception(object.data,'repr(result[\"events\"].keys())')"}),
    ({"sTitle":"Elaborate Time"},{"content":"evaluate_with_exception(object.data,'repr(result[\"events\"][\"elaborate_design\"][\"time\"])')"}),
    ({"sTitle":"Elaborate Memory"},{"content":"evaluate_with_exception(object.data,'repr(result[\"events\"][\"elaborate_design\"][\"mem_delta\"])')"}),
    ({"sTitle":"Data"},{"content":"object.data"}),
    ]


default_case_view = [
    ({"sTitle":"Tag"},{"content":"tag_name(object.tag_id)"}),
    ({"sTitle":"Clock"},{"content":"'%2.3f'%(object.clock_time)"}),
    ({"sTitle":"CPU"},{"content":"'%2.3f'%(object.user_time + object.sys_time)"}),
    ({"sTitle":"Memory(MB)"},{"content":"'%2.3f'%(float(object.max_memory)*1e-6)"}),
    ({"sTitle":"Size"},{"content":"object.size"}),
    ({"sTitle":"Time factor"},{"content":"object.time_factor"})
    ]

simulate_case_view = [
    ({"sTitle":"Tag"},{"content":"tag_name(object.tag_id)"}),
    ({"sTitle":"Clock"},{"content":"'%2.3f'%(object.clock_time)"}),
    ({"sTitle":"CPU"},{"content":"'%2.3f'%(object.user_time + object.sys_time)"}),
    ({"sTitle":"Memory(MB)"},{"content":"'%2.3f'%(float(object.max_memory)*1e-6)"}),
    ({"sTitle":"Time factor"},{"content":"object.time_factor"}),
    ({"sTitle":"Status"},{"content":'condition(object.status,"<FONT COLOR=\'green\'>ok</FONT>","<FONT COLOR=\'red\'>fail</FONT>")'}),
    ]

simulate_pair_case_view = [
    ({"sTitle":"Tag"},{"content":"tag_name(object.tag_id)"}),
    ({"sTitle":"Clock"},{"content":"'%2.3f'%(object.clock_time)"}),
    ({"sTitle":"Device Type"},{"content":"sim_type_name(object.sim_type_id)"}),
    ({"sTitle":"CPU"},{"content":"'%2.3f'%(object.user_time + object.sys_time)"}),
    ({"sTitle":"Memory(MB)"},{"content":"'%2.3f'%(float(object.max_memory)*1e-6)"}),
    ({"sTitle":"Time factor"},{"content":"object.time_factor"}),
    ({"sTitle":"Status"},{"content":'condition(object.status,"<FONT COLOR=\'green\'>ok</FONT>","<FONT COLOR=\'red\'>fail</FONT>")'}),
    ]

benchmark_template_case_view = [
    ({"sTitle":"Tag"},{"content":"tag_name(object.tag_id)"}),
    ({"sTitle":"Clock"},{"content":"'%2.3f'%(object.clock_time)"}),
    ({"sTitle":"CPU"},{"content":"'%2.3f'%(object.user_time + object.sys_time)"}),
    ({"sTitle":"Memory(MB)"},{"content":"'%2.3f'%(float(object.max_memory)*1e-6)"}),
    ({"sTitle":"Size"},{"content":"object.size"}),
    ({"sTitle":"Time factor"},{"content":"object.time_factor"}),
    ]




simulate_plot_view = {
     "plot":[
            {"name":"clock","data":("object.clock_time","(object.tag_id)")},
            {"name":"memory","data":("object.max_memory*1e-6","(object.tag_id)")}
        ],
    "ivar":[]
    }

benchmark_template_plot_view = {
    "plot":[
        {"name":"clock","data":("object.clock_time","object.size")},
        {"name":"memory","data":("object.max_memory","object.size")},
        {"name":"cpu","data":("object.user_time+object.sys_time","object.size")},
        ],
    "ivar":[
        {"name":"Group","id":"object.tag_id","content":"tag_name(object.tag_id)"},
        {"name":"Template","id":"object.template_id","content":"template_name(object.template_id)"},
        {"name":"Simulator","id":"object.sim_id","content":"sim_name(object.sim_id)"},
        {"name":"Device Type","id":"object.sim_type_id","content":"sim_type_name(object.sim_type_id)"},
        {"name":"Stop time factor","id":"object.time_factor","content":"object.time_factor"}
        ]
    }

simulate_pair_plot_view = {
    "plot":[
        {"name":"clock","data":("object.clock_time","object.time_factor")},
        {"name":"memory","data":("object.max_memory","object.time_factor")}
        ],
    "ivar":[
        {"name":"Group","id":"object.tag_id","content":"tag_name(object.tag_id)"},
        {"name":"Simulator","id":"object.sim_id","content":"sim_name(object.sim_id)"},
        {"name":"Device Type","id":"object.sim_type_id","content":"sim_type_name(object.sim_type_id)"},
        ]
    }
    
case_view_map = {
    "__default__":default_case_view,
    "simulate":simulate_case_view,
    "simulate_pair":simulate_pair_case_view,
    "benchmark_template":benchmark_template_case_view
    }

plot_view_map = {
    "__default__":None,
    "simulate":simulate_plot_view,
    "simulate_pair":simulate_pair_plot_view,
    "benchmark_template":benchmark_template_plot_view
    }
