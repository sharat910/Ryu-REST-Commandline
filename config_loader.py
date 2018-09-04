from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


config_type = 'hqos'

def get_config(filename):
    with open("configs/%s/%s.yml" % (config_type,filename)) as f:
        config = load(f,Loader=Loader)
    return config
