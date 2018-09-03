import requests
from config_loader import get_config

def dict_builder(dpid,group):
    d = {}
    d['dpid'] = dpid
    d.update(group['group'])
    return d

def find_group(group_config, group_name):
    for group in group_config['groups']:
        if group['group']['name'] == group_name:
            return group
    print ("Error: No group with that name")
    return None

class GroupHandler(object):
    """docstring for GroupHandler"""
    def __init__(self, app_config):
        super(GroupHandler, self).__init__()
        self.app_config = app_config
        self.group_config = get_config('groups')
        self.root_url = 'http://%s:%s' % (app_config['hostname'],app_config['port'])
        self.dpid = self.app_config['dpid']

    def group_operation(self,operation,group_name):
        group = find_group(self.group_config,group_name)
        group_dict = dict_builder(self.dpid,group)
        self._group_op(group_dict,operation)

    def _group_op(self,group_dict,op):
        print(op,group_dict)
        url = self.root_url + self.group_config['urls'][op]
        r = requests.post(url,json=group_dict)
        print(r)

    def load_all_groups(self):
        for group in self.group_config['groups']:
            group_dict = dict_builder(self.dpid,group)
            self._group_op(group_dict,'add')