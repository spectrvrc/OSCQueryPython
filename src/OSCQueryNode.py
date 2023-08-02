import json
from collections import defaultdict

class OSCQueryNode:
    def __init__(self, fullPath):
        self.FullPath = fullPath
        self.Description = None
        self.Access = None
        self.Contents = None
        self.OscType = None
        self.Value = None

    @property
    def ParentPath(self):
        length = max(1, self.FullPath.rfind('/'))
        return self.FullPath[:length]

    @property
    def Name(self):
        return self.FullPath[self.FullPath.rfind('/')+1:]

    def __str__(self):
        dict_copy = self.__dict__.copy()
        dict_copy.pop('_pathLookup', None)
        return json.dumps(dict_copy, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class OSCQueryRootNode(OSCQueryNode):
    def __init__(self):
        super().__init__('/')
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
            parent = self.AddNode(OSCQueryNode(node.ParentPath))

        if parent.Contents is None:
            parent.Contents = {}

        elif node.Name in parent.Contents:
            print(f"Child node {node.Name} already exists on {self.FullPath}, you need to remove the existing entry first")
            return None

        parent.Contents[node.Name] = node
        self._pathLookup[node.FullPath] = node
        return node

    def RemoveNode(self, path):
        if poath in self._pathLookup:
            node = self._pathLookup[path]
            parent = self.GetNodeWithPath(node.ParentPath)

            if parent and parent.Contents and node.Name in parent.Contents:
                del parent.Contents[node.Name]
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
            self._pathLookup[subNode.FullPath] = subNode
            if subNode.Contents is not None:
                self.AddContents(subNode)

    @staticmethod
    def FromString(json_str):
        tree = json.loads(json_str, object_hook=lambda d: OSCQueryNode(**d))
        tree.RebuildLookup()
        return tree
