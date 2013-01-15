import os

class Disk:
    def __init__(self,name,host,device):
        self.name = name
        self.host = host
        self.device = device
        pass
    pass

class LocalConfig:
    BootFilePath = {
        "ig2":os.path.expanduser("~/IG2_data/boot/"),
        "ig3":os.path.expanduser("~/IG3_data/boot/"),
        }
    
    Disks = {
        "ig2":[Disk("disk1","127.0.0.1",os.path.expanduser("~/IG2_data/data/"))],
        "ig3":[Disk("disk1","127.0.0.1",os.path.expanduser("~/IG3_data/data/"))],
        }
    Root = {
        "ig2":"/opt/local/InfiniteGraph-2.1.0_rc2/mac86_64/",
        "ig3":"/Applications/InfiniteGraph/3.0"
        }
    Host = {
        "ig2":"127.0.0.1",
        "ig3":"127.0.0.1"
        }
    SourcePath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    BuildPath = os.path.join(SourcePath,"build")
    BenchmarkJar = {
        "ig2":os.path.join(BuildPath,"benchmark.2.jar"),
        "ig3":os.path.join(BuildPath,"benchmark.3.jar"),
        }
    pass

class FrakConfig:
    BootFilePath = "/disk1/IG_data/"
    Disks = [
        Disk("disk1","frak08-b11.objy.com","/disk1/IG_data/")
        ]
    IG2_Root = "/disk1/InfiniteGraph-2.1.0/linux86_64/"
    IG3_Root = "/disk1/InfiniteGraph/3.0/"
    Host = "127.0.0.1"
    pass






Config = LocalConfig
#Config = FrakConfig

def Setup():
    os.system("mkdir -p %s"%(Config.BootFilePath))
    for i in Config.Disks:
        os.system("mkdir -p %s"%(i.device))
        pass
    pass

