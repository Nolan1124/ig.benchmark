import IG_Config

class __Defaults__:
    Defaults = {
        "IG.BootFilePath":".",
        "IG.LockServerHost":"127.0.0.1"
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


class IG_LocationConfigFile:
    def __init__(self,fileName):
        self.fileName = fileName
        pass

    def generate(self,disks):
        f = file(self.fileName,"w")
        print >> f,'<?xml version="1.0" encoding="UTF-8"?>'
        print >> f,'<InfiniteGraph>'
        print >> f,'<LocationPreferences allowNonPreferredLocations="true">'
        print >> f,'<LocationPreferenceRank>'
        for disk in disks:
            print >> f,'<StorageLocation value="%s"/>'%(disk.name)
            pass
        print >> f,'</LocationPreferenceRank>'
        print >> f,'</LocationPreferences>'
        print >> f,'</InfiniteGraph>'

        f.flush()
        f.close()
        pass
    pass

#p = IG_PropertyFile()
#p.generate()


        
