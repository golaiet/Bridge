import xml.etree.ElementTree as ET
import re # regex
# import numpy as np
import pandas as pd


def search(root, term):
    reg = re.compile(term)
    list = []
    if reg.search(root.tag.lower()):
        list.append(root)

    for i in range(len(root)):
        temp_list = search(root[i], term)
        try:
            for item in temp_list:
                list.append(item)
        except:
            pass

    return list


class Entity():
    """" An entity is a class in bridge represent entity, features or attributes """
    def __init__(self, root):
        self.entity = root
        self.dict = []
        self.children = []

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

    def build_children(self, term):
        for child in self.get_term(term):
            child_entity = Entity(child)
            self.children.append(child_entity)
            self.dict.append(child_entity.name)

    def get_term(self, term):
        f = search(self.entity, str(term)+"$")
        children = []
        if len(f) > 0:
            children = f[0].getchildren()
        return children

    def get_features(self):
        return self.get_term("feature")

    def get_attributes(self):
        return self.get_term("attribute")

    def is_fit(self, term, case_sensitive = False):
        # try:
        #     term = re.compile(str(term).lower())
        # except:
        #     return False
        for word in self.dict:
            if term.strip().find(word.strip()) > -1:
            # if term.search(word):
            #     print(word + " : " + term)
                return True
        return False


class Bridge():
    """ A python instantiation of bridge (as a collection of entities (features and attributes)"""
    def __init__(self, path):

        self.tree = ET.parse('BRIDGE.xmi')
        self.root = self.tree.getroot()

        self.classes = self.search(self.root, "class$")

    def search(self, root, term):
        reg = re.compile(term)
        list = []
        if reg.search(root.tag.lower()):
            list.append(Entity(root))

        for index in range(len(root)):
            temp_list = self.search(root[index], term)
            try:
                for item in temp_list:
                    list.append(item)
            except:
                pass

        return list

    def build_dict(self, dataset):
        for index in range(len(dataset)):
            entity = dataset.iloc[index][0]
            bag_of_words = dataset.iloc[index][1]
            cls = self.get_class(entity)
            for word in bag_of_words.split(','):
                cls.dict.append(word)

    def get_fit(self, term, case_sensitive = False):
        list = []
        for cls in self.classes:
            for word in term.split(" "):
                try:
                    # print(term + " : " + word)
                    if cls.is_fit(word, case_sensitive):
                        list.append(cls.name)
                        # print(cls.name)
                except:
                    pass
        return list

    def get_class(self, name, case_sensitive = False):
        for cls in self.classes:
            if case_sensitive:
                if cls.name==name:
                    return cls
            else:
                if cls.name.lower() == str(name).lower():
                    return cls
        return False

    def search_class(self, term, case_sensitive = False):
        reg = re.compile(term)
        list = []
        for cls in self.classes:
            if case_sensitive:
                if reg.search(cls.name):
                    list.append(cls)
            else:
                if reg.search(cls.name.lower()):
                    list.append(cls)
        return list

# bridge = Bridge('BRIDGE.xmi')
# dataset = pd.read_csv('bridge_map.csv')
# bridge.build_dict(dataset)
#
# # examples
#
# # how to search a class in bridge
# for entity in bridge.search_class('bio'):
#     print(entity.name)
#
# # how to print class features by name
# for feature in bridge.get_class("BiologicEntity").get_features():
#     print(feature.attrib["name"])
#
# # find an entities that related to 'terribly patient death'
# bridge.get_fit('the terribly patient death')
