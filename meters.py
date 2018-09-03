import requests
from config_loader import get_config


def dict_builder(dpid,meter):
    d = {}
    d['dpid'] = dpid
    d.update(meter['meter'])
    return d

def find_meter(meter_config, meter_id):
    for meter in meter_config['meters']:
        if meter['meter']['meter_id'] == int(meter_id):
            return meter
    print ("Error: No meter with that meter_id")
    return None

class MeterHandler(object):
    """docstring for MeterHandler"""
    def __init__(self, app_config):
        super(MeterHandler, self).__init__()
        self.app_config = app_config
        self.meter_config = get_config('meters')
        self.root_url = 'http://%s:%s' % (app_config['hostname'],app_config['port'])
        self.dpid = self.app_config['dpid']

    def meter_operation(self,operation,meter_id):
        meter = find_meter(self.meter_config,meter_id)
        meter_dict = dict_builder(self.dpid, meter)
        self._meter_op(meter_dict,operation)        

    def _meter_op(self,meter_dict,op):
        print(meter_dict)
        url = self.root_url + self.meter_config['urls'][op]
        r = requests.post(url,json=meter_dict)
        print(r)

    def load_all_meters(self):
        for meter in self.meter_config['meters']:
            meter_dict = dict_builder(self.dpid,meter)
            self._meter_op(meter_dict,'add')