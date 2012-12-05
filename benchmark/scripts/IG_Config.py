import os

class Disk:
    def __init__(self,name,host,device):
        self.name = name
        self.host = host
        self.device = device
        
        
class LocalConfig:
    BootFilePath = "/Users/henocka/IG_data/boot/"
    Disks = [
        Disk("disk1","127.0.0.1","/Users/henocka/IG_data/data/")
        ]
    IG2_Root = "/opt/local/InfiniteGraph-2.1.0_rc2/mac86_64/"
    IG3_Root = "/Applications/InfiniteGraph/3.0"
    Host = "127.0.0.1"
    pass

Config = LocalConfig
def Setup():
    os.system("mkdir -p %s"%(Config.BootFilePath))
    for i in Config.Disks:
        os.system("mkdir -p %s"%(i.device))
        pass
    pass

Setup()
