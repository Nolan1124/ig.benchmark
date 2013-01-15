import sys
import getopt
import os
import shutil
import model
import datetime
import types
import json
import imp
import db
from db_types import *



def tag_name(i):
    if db_report.TAG_MAP.has_key(i):
        return db_report.TAG_MAP[i]
    return None

def sim_name(i):
    if db_report.SIM_MAP.has_key(i):
        return db_report.SIM_MAP[i]
    return None

def sim_type_name(i):
    if db_report.SIM_TYPE_MAP.has_key(i):
        return db_report.SIM_TYPE_MAP[i]
    return None

def template_name(i):
    if db_report.TEMPLATE_MAP.has_key(i):
        return db_report.TEMPLATE_MAP[i]
    return None

def case_type_name_to_object(i):
    if db_report.CASE_TYPE_ID_MAP.has_key(i):
        return db_report.CASE_TYPE_ID_MAP[i]
    return None
            
def html_reference(o,name):
    return "<a href=javascript:tda_datatable_populate_using_name('%s','%d');>%s</a>"%(o.object_type(),o.id,name)
    
def condition(value,pass_value,fail_value):
    if(value):
        return pass_value
    return fail_value

def evaluate_with_exception(data,expression):
    result = None
    try:
        result = eval(data)
        result = eval(expression)
    except Exception,e:
        result = str(e)
        pass
    return result

def evaluate(data,expression,failure):
    result = None
    try:
        result = eval(data)
        result = eval(expression)
    except Exception,e:
        result = failure
        pass
    return result



class PlotView:
    def __init__(self):
        self.module = None
        self.default_plot_view = None
        self.plot_view_map = {}
        self.data_map = {}
        pass


    def __read_plot_view__(self,handler):
        try:
            view_map = self.module.plot_view_map
            self.plot_view_map = {}
            for name in view_map:
                if name == "__default__":
                    self.plot_view_map[None] = self.default_plot_view = view_map[name]
                else:
                    case_type_object = case_type_name_to_object(name)
                    if case_type_object == None:
                        handler.warn("Unable to find case type '%s' when defining plot views."%(name))
                    else:
                        self.plot_view_map[case_type_object.id] = view_map[case_type_object.name]
                        pass
                    pass
                pass
            pass
        except Exception, e:
            print e
            pass
        pass
    
    def initialize(self,handler,module,config_filename):
        self.module = module
        try:
            self.__read_plot_view__(handler)
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            message  = "\n\tFile:%s\n"%(exc_tb.tb_frame.f_code.co_filename)
            message += "\tLine number:%d\n"%(exc_tb.tb_lineno)
            message += "\t%s\n"%(str(exc_obj))
            handler.error(message)
            return False
        return True
    
    def __generate_key_list__(self,iVarView):
        key_list = []
        for i in iVarView:
            key_list.append({})
            pass
        return key_list
    
    def get_key(self,iVarView,key_list,object):
        counter = 0
        key = ""
        for i in iVarView:
            e_content = eval(i["content"])
            e_key = eval(i["id"])
            key_list[counter][e_key] = e_content
            key += "%s."%(str(e_key))
            counter += 1
            pass
        return key
    
    def add(self,key_list,data_map,iVarView,dataView,case_data):
        key = self.get_key(iVarView,key_list,case_data)
        if data_map.has_key(key):
            data_map[key].append(case_data)
        else:
            data_map[key] = [case_data]
            pass
        pass

    def write_data(self,location,case_object,case_data_list):
        print ".",
        sys.stdout.flush()
        plot_view = None
        if self.plot_view_map.has_key(case_object.case_type_id):
            plot_view = self.plot_view_map[case_object.case_type_id]
        else:
            plot_view = self.plot_view_map[None]
            pass
        description_structure = None
        if plot_view == None:
            print "No plot view for type:",case_object.case_type_id

        else:
            iVar = []
            iVarView = plot_view["ivar"]
            dataView = plot_view["plot"]
            key_list = self.__generate_key_list__(iVarView)
            data_map = {}
            for case_data in case_data_list:
                self.add(key_list,data_map,iVarView,dataView,case_data)
                pass
            
            #print key_list
            counter = 0
            dVar = []
            for view in dataView:
                dVar.append({"name":view["name"]})
            for i in iVarView:
                data = []
                keys = key_list[counter]
                for _id in keys:
                    data.append({"id":_id,"name":keys[_id]})
                    pass
                iVar.append({"name":i["name"],"data":data})
                counter += 1
                pass
            
            description_structure = {
                "name":case_object.name,
                "description":case_object.description,
                "ivar":iVar,
                "dvar":dVar
                }
            plot_content_map = {}
            for view in dataView:
                name = view["name"]
                y_axis = view["data"][0]
                x_axis = view["data"][1]
                
                for data_key in data_map:
                    data = []
                    for object in data_map[data_key]:
                        data.append([eval(x_axis),eval(y_axis)])
                        pass
                    K = data_key.split(".")
                    label = ""
                    counter = 0
                    for _k in K:
                        if len(_k):
                            ivalue = int(_k)
                            label += "%s,"%(key_list[counter][ivalue])
                            counter += 1
                            pass
                        pass
                    label = label[:len(label)-1]
                    structure = {"data":data,"label":label}
                    f = file(os.path.join(location,"data","case.%s.%d.%sjson"%(name,case_object.id,data_key)),"w")
                    print >> f,json.dumps(structure,indent=1)
                    f.close()
                    pass
            pass
        f = file(os.path.join(location,"data","case.description.%d.json"%(case_object.id)),"w")
        print >> f,json.dumps(description_structure,indent=1)
        f.close()
        return
    
    pass

class ObjectView:
    COUNTER = 1
    def __init__(self):
        self.module = None
        self.suite_view = None
        self.default_case_view = None
        self.case_view_map = None
        self.suite_description = None
        self.case_description_map = {}
        pass

    def __read_suite_view__(self,handler,module):
        try:
            view = module.suite_view
            self.suite_view = view
        except Exception, e:
            print e
            pass
        pass

    def __read_default_case_view__(self,handler,module):
        try:
            view = module.default_case_view
            self.default_case_view = view
        except Exception, e:
            print e  
            pass
        pass

    def __read_case_view__(self,handler,module):
        try:
           view_map = module.case_view_map
           self.case_view_map = {}
           for name in view_map:
               if name == "__default__":
                   self.case_view_map[None] = self.default_case_view = view_map[name]
               else:
                   case_type_object = case_type_name_to_object(name)
                   if case_type_object == None:
                       handler.warn("Unable to find case type '%s' when defining case views."%(name))
                   else:
                       self.case_view_map[case_type_object.id] = view_map[case_type_object.name]
               pass
           pass
        except Exception, e:
            print e
            pass
        pass

    def get_suite_description(self):
        if  self.suite_description == None:
            self.suite_description = []
            for i in self.suite_view:
                description = i[0]
                self.suite_description.append(description)
                pass
            pass
        return self.suite_description

    def get_case_description(self,case_type):
        if self.case_description_map.has_key(case_type):
            return self.case_description_map[case_type]
        case_description = []
        case_view = self.default_case_view
        if self.case_view_map.has_key(case_type):
            case_view = self.case_view_map[case_type]
            pass
        for i in case_view:
            description = i[0]
            case_description.append(description)
            pass
        self.case_description_map[case_type] = case_description
        return case_description

    def get_suite_content(self,object_list):
        data = []
        for object in object_list:
            row_data = []
            for i in self.suite_view:
                content = i[1]
                row_data.append(eval(content["content"]))
                pass
            data.append(row_data)
        return data

    def get_case_content(self,object_list,case_type):
        data = []
        case_view = self.default_case_view
        if self.case_view_map.has_key(case_type):
            case_view = self.case_view_map[case_type]
            pass
        for object in object_list:
            row_data = []
            for i in case_view:
                content = i[1]
                row_data.append(eval(content["content"]))
                pass
            data.append(row_data)
        return data

    def initialize(self,handler,config_filename):
        module = None
        if not os.path.exists(config_filename):
            handler.error("Unable to find file '%s'."%(config_filename))
            return module
        try:
            module = imp.load_source("_temp_%d"%(ObjectView.COUNTER),config_filename)
            ObjectView.COUNTER += 1
            self.__read_suite_view__(handler,module)
            self.__read_default_case_view__(handler,module)
            self. __read_case_view__(handler,module)
        except Exception, e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            message  = "\n\tFile:%s\n"%(config_filename)
            message += "\tLine number:%d\n"%(exc_tb.tb_lineno)
            message += "\t%s\n"%(str(exc_obj))
            handler.error(message)
            pass
        return module


default_location = "benchmark_web_report"
class db_report:
    

    TAG_MAP = {}
    SIM_MAP = {}
    SIM_TYPE_MAP = {}
    TEMPLATE_MAP = {}
    CASE_TYPE_ID_MAP = {}
    
    def __init__(self,db):
        self.db = db
        pass
    
    def copy_web_template(self,location):
        source = os.path.abspath(os.path.dirname(__file__))
        source = os.path.dirname(source)
        try:
            shutil.rmtree(location)
        except:
            pass
        shutil.copytree(os.path.join(source,"web_template"), location)
        pass


    def traverse_case_tree(self,tree_structure,parent_id):
        cases = self.db.fetch_using(model.case,"parent",parent_id)
        for i in cases:
            item_map = {"name":i.name,"ref":"javascript:tda_datatable_populate_using_name('case','%d');"%(i.id)}
            item_structure = []
            item_map["data"] = item_structure
            item_map["strong"] = 0
            tree_structure.append(item_map)
            pass            

    def traverse_suite_tree(self,tree_structure,parent_id):
        suites = self.db.fetch_using(model.suite,"parent",parent_id)
        for i in suites:
            item_map = {"name":i.name,"ref":"javascript:tda_datatable_populate_using_name('suite','%d');"%(i.id)}
            item_structure = []
            self.traverse_suite_tree(item_structure,i.id)
            self.traverse_case_tree(item_structure,i.id)
            item_map["data"] = item_structure
            item_map["strong"] = 1
            tree_structure.append(item_map)
            pass
        pass

    def generate_treeview_data(self,location):
        structure = []
        self.traverse_suite_tree(structure,-1)
        f = file(os.path.join(location,"data","tree.json"),"w")
        print >> f,json.dumps(structure)
        f.close()
        pass

    def save_json_data(self,data,location,file_name):
        f = file(os.path.join(location,"data",file_name),"w")
        print >> f,json.dumps(data)
        f.close()
        pass
        
    class PData:
        def __init__(self):
            self.data_map = {}
            self.tags = {}
            self.templates = {}
            self.sim = {}
            self.sim_type = {}
            self.time_factor = {}
            self.description_structure = None
            pass

        def get_key(self,case_data):
            self.tags[case_data.tag_id] = 1
            self.templates[case_data.template_id] = 1
            self.sim[case_data.sim_id] = 1
            self.sim_type[case_data.sim_type_id] = 1
            self.time_factor[case_data.time_factor] = 1
            return "%s.%s.%s.%s.%s"%(str(case_data.tag_id),str(case_data.template_id),str(case_data.sim_id),str(case_data.sim_type_id),str(case_data.time_factor))

        def add(self,case_data):
            key = self.get_key(case_data)
            if self.data_map.has_key(key):
                self.data_map[key].append(case_data)
            else:
                self.data_map[key] = [case_data]
            pass

        def add_list(self,case_object,case_data_list):
            for i in case_data_list:
                self.add(i)
            
            tag_structure = []
            for i in self.tags.keys():
                tag_structure.append({"id":i,"name":tag_name(i)})
                pass
            template_structure = []
            for i in self.templates.keys():
                template_structure.append({"id":i,"name":template_name(i)})
                pass
            sim_structure = []
            for i in self.sim.keys():
                sim_structure.append({"id":i,"name":sim_name(i)})
                pass
            sim_type_structure = []
            for i in self.sim_type.keys():
                sim_type_structure.append({"id":i,"name":sim_type_name(i)})
                pass
            time_factor_structure = []
            for i in self.time_factor.keys():
                time_factor_structure.append({"id":i,"name":"%sx"%(str(i))})
                pass
            self.description_structure = {
                "name":case_object.name,
                "description":case_object.description,
                "ivar":
                [
                    {"name":"Group","data":tag_structure},
                    {"name":"Template","data":template_structure},
                    {"name":"Simulator","data":sim_structure},
                    {"name":"Device Type","data":sim_type_structure},
                    {"name":"Time Factor","data":time_factor_structure}
                    ]
                }
            pass

        def to_int(self,value):
            try:
                value = int(value)
            except:
                value = None
            return value


        def get_data(self,key):
            data = self.data_map[key]
            size = {}
            for i in data:
                size[i.size] = i
                pass
            size_key = size.keys()
            size_key.sort()
            time_data = []
            mem_data  = []
            for i in size_key:
                time_data.append([i,size[i].clock_time])
                mem_data.append([i,size[i].max_memory])
                pass
            key_items = key.split(".")
            label = "%s.%s.%s.%s.time_factor:%sx"%(tag_name(self.to_int(key_items[0])),
                                                   template_name(self.to_int(key_items[1])),
                                                   sim_name(self.to_int(key_items[2])),
                                                   sim_type_name(self.to_int(key_items[3])),
                                                   key_items[4])
            return ({"label":"time.%s"%(label),"data":time_data},{"label":"memory.%s"%(label),"data":mem_data})
        pass
    
    def report_case_data(self,location,case,object_view,plot_view):
        f = file(os.path.join(location,"data","case.%d.json"%(case.id)),"w")
        case_data_list = self.db.fetch_using(model.case_data,"case_id",case.id)
        case_data_structure = object_view.get_case_content(case_data_list,case.case_type_id)
        structure = {
            "name":"Case: %s"%(case.name),
            "description":case.description,
            "column_description":object_view.get_case_description(case.case_type_id),
            "data":case_data_structure
            }
        print >> f,json.dumps(structure,indent=1)
        f.close()
        #pData = db_report.PData()
        #pData.add_list(case,case_data_list)
        #f = file(os.path.join(location,"data","case.description.%d.json"%(case.id)),"w")
        #print >> f,json.dumps(pData.description_structure,indent=1)
        #f.close()

        plot_view.write_data(location,case,case_data_list)
               
        if 0:
            for key in pData.data_map:
                (time,memory) = pData.get_data(key)
                f = file(os.path.join(location,"data","case.time.%d.%s.json"%(case.id,key)),"w")
                print >> f,json.dumps(time)
                f.close()
                f = file(os.path.join(location,"data","case.memory.%d.%s.json"%(case.id,key)),"w")
                print >> f,json.dumps(memory)
                f.close()
                pass
            pass
        pass
    
    def report_suite_data(self,location,parent_id,object_view,plot_view):
        suites = self.db.fetch_using(model.suite,"parent",parent_id)
        for suite in suites:
            f = file(os.path.join(location,"data","suite.%d.json"%(suite.id)),"w")
            case_structure = []
            cases = self.db.fetch_using(model.case,"parent",suite.id)
            sub_suites = self.db.fetch_using(model.suite,"parent",suite.id)
            suite_data = object_view.get_suite_content(cases)
            suite_data = suite_data + object_view.get_suite_content(sub_suites)
            structure = {
                "name":"Suite: %s"%(suite.name),
                "description":suite.description,
                "column_description":object_view.get_suite_description(),
                "data":suite_data
                }
            print >> f,json.dumps(structure,indent=1)
            f.close()
            
            for case in cases:
                self.report_case_data(location,case,object_view,plot_view)
                pass
            self.report_suite_data(location,suite.id,object_view,plot_view)
            pass
        pass

    def map_constants(self):
        tags = self.db.fetch_using_generic(model.tag)
        sims  = self.db.fetch_using_generic(model.simulator)
        sim_types = self.db.fetch_using_generic(model.simtype)
        templates = self.db.fetch_using_generic(model.template)
        __case_types__ = self.db.fetch_using_generic(model.case_type)
        for i in tags:
            self.TAG_MAP[i.id] = i.name
            pass
        for i in sims:
            self.SIM_MAP[i.id] = i.name
            pass
        for i in sim_types:
            self.SIM_TYPE_MAP[i.id] = i.name
            pass
        for i in templates:
            self.TEMPLATE_MAP[i.id] = i.name
            pass
        for i in __case_types__:
            self.CASE_TYPE_ID_MAP[i.name] = i
            pass
        pass


    
    def report(self,handler,location):
        self.copy_web_template(location)
        if self.db.connection == None:
            self.db.create_database()
            pass
        self.map_constants()
        object_view = ObjectView()
        config_name = os.path.join(os.path.dirname(os.path.dirname(__file__)),"report_config.py")
        module = object_view.initialize(handler,config_name)

        if module:
            plot_view  = PlotView()
            plot_view.initialize(handler,module,config_name)
            self.generate_treeview_data(location)
            self.report_suite_data(location,-1,object_view,plot_view)
            pass
        pass
    pass

   
