import sys
import argparse
from config_loader import get_config
from flows import FlowHandler
from meters import MeterHandler
from groups import GroupHandler
# from stats_collector import collect_stats

def usage():
    print("Error in command")
    print("=============USAGE===================")
    print("python main.py (loadallconfig | loadallflows | loadallgroups |\
     loadallmeters | deleteallflows | deleteallgroups )")
    print("or")
    print("python main.py (add | mod | delete) (flow | group | meter) (flow_name | meter_id)")
    print("or")
    print("python main.py attach (flow_name) (meter | queue) (meter_id | queue_id)")

if __name__ == '__main__':
    app_config = get_config('app')
    flow_handler = FlowHandler(app_config)
    meter_handler = MeterHandler(app_config)
    group_handler = GroupHandler(app_config)

    #parser = argparse.ArgumentParser(description='Ryu REST API interactor for QoS Experiments')

    if len(sys.argv) == 2:
        command = sys.argv[1]
        if command == "loadallconfig":
            group_handler.load_all_groups()
            flow_handler.load_all_flows()
            meter_handler.load_all_meters()
        elif command == "loadallflows":
            group_handler.load_all_groups()
            flow_handler.load_all_flows()
        elif command == "loadallgroups":
            group_handler.load_all_groups()
        elif command == "deleteallgroups":
            group_handler.delete_all_groups()
        elif command == "deleteallflows":
            flow_handler.delete_all_flows()
        elif command == "loadallmeters":
            meter_handler.load_all_meters()
        else:
            usage()

    elif len(sys.argv) == 4 or len(sys.argv) == 3:
        operation = sys.argv[1]
        if operation == 'add' or operation == 'mod' or operation == 'delete':
            entity = sys.argv[2]
            if entity == "flow":
                flow_name = sys.argv[3]
                flow_handler.flow_operation(operation,flow_name)
            elif entity == "meter":
                meter_id = sys.argv[3]
                meter_handler.meter_operation(operation,meter_id)
            elif entity == "group":
                group_name = sys.argv[3]
                group_handler.group_operation(operation,group_name)
            else:
                usage()
        else:
            usage()


    elif len(sys.argv) == 5:
        command = sys.argv[1]
        if command == "attach":
            try:
                flow_name = sys.argv[2]
                m_or_q = sys.argv[3]
                if m_or_q == "meter":
                    meter_id = sys.argv[4]
                    flow_handler.attach_meter(flow_name,meter_id)
                elif m_or_q == "queue":
                    queue_id = sys.argv[4]
                    flow_handler.attach_queue(flow_name,queue_id)
            except Exception as e:
                print(e)
                usage()
        else:
            usage()
    else:
        usage()
