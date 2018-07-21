import Bridge
import pandas as pd
import ProtocolReader

bridge = Bridge.Bridge('BRIDGE.xmi')
dataset = pd.read_csv('bridge_map.csv')
bridge.build_dict(dataset)

PR = ProtocolReader.ProtocolReader('0011.pdf')
protocol_list = PR.text.split(".")

# search through protocol
for line in protocol_list:
    fit = bridge.get_fit(line)
    if len(fit)>0:
        print(str(fit) + " : " + line)
