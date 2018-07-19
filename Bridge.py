import xml.etree.ElementTree as ET
import re # regex
import numpy as np


def search(root, term, string=""):
    reg = re.compile(term)
    list = []
    if reg.search(root.tag.lower()):
        print(root.tag + " : " + string + " : " + str(root.attrib))
        list.append(root)

    for i in range(len(root)):
        temp_list = search(root[i], term, string + "[" + str(i) + "]")
        try:
            for item in temp_list:
                list.append(item)
                # print(item)
        except:
            pass

    return list


class Entity():

    def __init__(self, root):
        self.entity = root
        try:
            self.name = root.attrib['name']
        except:
            try:
                self.name = root.attrib['id']
            except:
                self.name = "Unknown"

        try:
            self.type = self.entity.tag[len('omg.org/UML1.3')+2:]
        except:
            self.type = self.entity.tag

        self.tag = self.entity.tag

    def get_term(self, term):
        f = search(self.entity, str(term)+"$")
        childrens = []
        if len(f) > 0:
            childrens = f[0].getchildren()
        return childrens

    def get_features(self):
        return self.get_term("feature")

    def get_attributes(self):
        return self.get_term("attribute")


class Bridge():

    def __init__(self, path):

        self.tree = ET.parse('BRIDGE.xmi')
        self.root = self.tree.getroot()

        self.classes = self.search(self.root, "class$")

    def search(self, root, term):
        reg = re.compile(term)
        list = []
        if reg.search(root.tag.lower()):
            list.append(Entity(root))

        for i in range(len(root)):
            temp_list = self.search(root[i], term)
            try:
                for item in temp_list:
                    list.append(item)
            except:
                pass

        return list

    def get_class(self, name):
        for cls in self.classes:
            if cls.name==name:
                return cls
        return False

    def search_class(self, term):
        reg = re.compile(term)
        list = []
        for cls in self.classes:
            if reg.search(cls.name.lower()):
                list.append(cls)
        return list

bridge = Bridge('BRIDGE.xmi')

for entity in bridge.search_class('bio'):
    print(entity.name)

for feature in bridge.get_class("BiologicEntity").get_features():
    print(feature.attrib["name"])