from OSCQueryHttpServer import PyOSCQuery, OSCQueryNode
from OSCQueryNodeTypes import AccessValues

app = PyOSCQuery()


new_node = OSCQueryNode("/foo/bar", AccessValues.ReadWrite, "A node with a value", oscType="i", value="42")
app.root_node.AddNode(new_node)

app.run()