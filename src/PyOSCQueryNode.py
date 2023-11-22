import json
from collections import defaultdict
from .PyOSCQueryNodeTypes import AccessValues, osc_type_for
class PyOSCQueryNode:
    def __init__(self, FULL_PATH: str,  access: AccessValues, description: str =None, contents: dict =None, oscType: str =None, value=None):
        self.FULL_PATH = FULL_PATH
        self.DESCRIPTION = description
        self.ACCESS = access
        self.CONTENTS = contents
        #self.OscType = oscType
        #self.Value = value

    @property
    def ParentPath(self):
        length = max(1, self.FULL_PATH.rfind('/'))
        return self.FULL_PATH[:length]

    @property
    def Name(self):
        return self.FULL_PATH[self.FULL_PATH.rfind('/')+1:]

    def __str__(self):
        dict_copy = self.__dict__.copy()
        dict_copy.pop('_pathLookup', None)
        output = json.dumps(dict_copy, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        # Remove any null CONTENTS entries
        output = output.replace('"CONTENTS": null,', '')
        return output


class PyOSCQueryRootNode(PyOSCQueryNode):
    def __init__(self):
        super().__init__('/', AccessValues.ReadWrite, "Root Node")
        self._pathLookup = {"/": self}

    def GetNodeWithPath(self, path):
        if self._pathLookup is None:
            self.RebuildLookup()

        if path in self._pathLookup:
            return self._pathLookup[path]
        
        return None
    
    def AddNode(self, node):
        parent = self.GetNodeWithPath(node.ParentPath)
        if parent is None:
            try:
                parent = self.AddNode(PyOSCQueryNode(node.ParentPath, 
                                                node.ACCESS, 
                                                node.DESCRIPTION, 
                                                node.CONTENTS))
            except AttributeError:
                parent = self.AddNode(PyOSCQueryNode(node.ParentPath, 
                                                    node.ACCESS, 
                                                    node.DESCRIPTION, 
                                                    node.CONTENTS))
                                               #node.OscType, 
                                               #node.Value))

        if parent.CONTENTS is None:
            parent.CONTENTS = {}

        elif node.Name in parent.CONTENTS:
            print(f"Child node {node.Name} already exists on {self.FULL_PATH}, you need to remove the existing entry first")
            return None

        parent.CONTENTS[node.Name] = node
        self._pathLookup[node.FULL_PATH] = node
        return node

    def RemoveNode(self, path):
        if path in self._pathLookup:
            node = self._pathLookup[path]
            parent = self.GetNodeWithPath(node.ParentPath)

            if parent and parent.CONTENTS and node.Name in parent.CONTENTS:
                del parent.CONTENTS[node.Name]
                del self._pathLookup[path]
                return True

        return False

    def RebuildLookup(self):
        self._pathLookup = {"/": self}
        self.AddContents(self)

    def AddContents(self, node):
        if node.Contents is None:
            return
        
        for subNode in node.Contents.values():
            self._pathLookup[subNode.FULL_PATH] = subNode
            if subNode.Contents is not None:
                self.AddContents(subNode)

    @staticmethod
    def FromString(json_str):
        tree = json.loads(json_str, object_hook=lambda d: PyOSCQueryNode(**d))
        tree.RebuildLookup()
        return tree
