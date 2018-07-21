import Bridge
import ProtocolReader
import pandas as pd


bridge = Bridge.Bridge('BRIDGE.xmi')
dataset = pd.read_csv('bridge_map_stem.csv')
bridge.build_dict(dataset)

PR = ProtocolReader.ProtocolReader('0011.pdf')
protocol_list = PR.clean_text_list
protocol_text = PR.text_list

# build bridge children
for index in range(len(bridge.classes)):
    try:
        bridge.classes[index].build_children('features')
    except:
        pass
    try:
        bridge.classes[index].build_children('attribute')
    except:
        pass

# search through protocol
print("##### start labeling")
for (index, line) in enumerate(protocol_list):
    fit = bridge.get_fit(line)
    if len(fit) > 0:
        print(str(fit) + " : " + protocol_text[index].replace("\n", ""))