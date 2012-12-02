class __Defaults__:
    Defaults = {
        "IG.BootFilePath":".",
        "IG.LockServerHost":"127.0.0.1",
        "IG.InstanceId":"5551",
        "IG.Placement.ImplClass":"com.infinitegraph.impl.plugins.adp.DistributedPlacement",
        }
    
class IG_PropertyFile:
    def __init__(self,fileName="IG.properties",defaults=__Defaults__.Defaults):
        self.properties = defaults.copy()
        self.defaults = defaults.copy()
        self.fileName = fileName
        pass

    def initialize(self):
        self.properties = self.defaults.copy()
        pass

    def generate(self):
        f = file(self.fileName,"w")
        for key in self.properties.keys():
            value = self.properties[key]
            print >> f,str(key)+"="+str(value)
        f.flush()
        f.close()


#p = IG_PropertyFile()
#p.generate()


        
