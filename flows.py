import requests
from config_loader import get_config
from meters import find_meter

def dict_builder(dpid,table_id,flow):
    d = {}
    d['dpid'] = dpid
    d['table_id'] = table_id
    d.update(flow['flow'])
    return d

def find_flow(flow_config, flow_name):
    for flow in flow_config['flows']:
        if flow['flow']['name'] == flow_name:
            return flow
    print ("Error: No flow with that name")
    return None

class FlowHandler(object):
    """docstring for FlowHandler"""
    def __init__(self, app_config):
        super(FlowHandler, self).__init__()
        self.app_config = app_config
        self.flow_config = get_config('flows')
        self.root_url = 'http://%s:%s' % (app_config['hostname'],app_config['port'])
        self.dpid = self.app_config['dpid']
        self.table_id = self.flow_config['table_id']

    def flow_operation(self,operation,flow_name):
        flow = find_flow(self.flow_config,flow_name)
        flow_dict = dict_builder(self.dpid, self.flow_config['table_id'],flow)
        self._flow_op(flow_dict,operation)

    def _flow_op(self,flow_dict,op):
        print(op,flow_dict)
        url = self.root_url + self.flow_config['urls'][op]
        r = requests.post(url,json=flow_dict)
        print(r)

    def delete_all_flows(self):
        print("Deleting all flows...")
        url = self.root_url + self.flow_config['urls']['delete_all']
        url = url.replace('<dpid>',str(self.dpid))
        r = requests.delete(url)
        print(r)

    def load_all_flows(self):
        for flow in self.flow_config['flows']:
            # print(flow)
            flow_dict = dict_builder(self.dpid,self.table_id,flow)
            self._flow_op(flow_dict,'add')    

    def attach_meter(self,flow_name,meter_id):
        flow = find_flow(self.flow_config,flow_name)       
        meter = find_meter(get_config('meters'),meter_id)
        if flow != None and meter != None:        
            flow_dict = dict_builder(self.dpid,self.table_id,flow)
            meter_action = {"type": "METER", "meter_id": meter_id}
            flow_dict['actions'].insert(0,meter_action)
            self._flow_op(flow_dict,'mod')
        else:
            print("Unable to attach meter | Flow %s | Meter %s" % (flow,meter))


    def attach_queue(self,flow_name,queue_id):
        flow = find_flow(self.flow_config,flow_name)
        if flow != None:        
            flow_dict = dict_builder(self.dpid,self.table_id,flow)
            queue_action = {"type": "SET_QUEUE", "queue_id": queue_id}
            n_actions = len(flow_dict['actions'])
            flow_dict['actions'].insert(n_actions -1 ,queue_action)
            self._flow_op(flow_dict,'mod')
        else:
            print("Unable to attach queue | Flow %s | Queue %s" % (flow,queue_id))