import logging
import copy


logger_ = logging.getLogger()


class BodypartTree(object):
    CONNECTION_TYPE_CENTER = 0
    CONNECTION_TYPE_ATTACHED = 1
    CONNECTION_TYPE_INSERTED = 2

    def __init__(self, central_body_part):
        self.nodes = [BodypartTreeNode(central_body_part, self.CONNECTION_TYPE_CENTER)]

    def copy(self):
        return copy.deepcopy(self)

    def attach(self, parent, children):
        self._bind_new_child_to_parent(parent, children, self.CONNECTION_TYPE_ATTACHED)

    def insert(self, parent, children):
        self._bind_new_child_to_parent(parent, children, self.CONNECTION_TYPE_INSERTED)

    def _bind_new_child_to_parent(self, parent_node, children_body_part, connection_type):
        child_bodypart_node = BodypartTreeNode(children_body_part, connection_type)
        parent_node.add_child_node(child_bodypart_node)
        self.nodes.append(child_bodypart_node)


class BodypartTreeNode(object):
    def __init__(self, body_part, connection_type):
        self.body_part = body_part
        self.connection_type = connection_type
        self.children_nodes = []

    def add_child_node(self, child_node):
        self.children_nodes.append(child_node)

    @property
    def name(self):
        return self.body_part.name
