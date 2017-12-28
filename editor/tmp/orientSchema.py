from pyorient.ogm.declarative import declarative_node, declarative_relationship
from pyorient.ogm.property import Integer, String
from graphID import IDConverter

Node = declarative_node()
Relationship = declarative_relationship()


class User(Node):
    element_type = 'user'
    element_plural = 'users'
    id = Integer()

    def graphID(self):
        return IDConverter().getGraphID(self.id, 'user')

class Repo(Node):
    element_type = 'repo'
    element_plural = 'repos'

    id = Integer()
    type = String()

    def graphID(self):
        return IDConverter().getGraphID(self.id, 'repo')

class Contribution(Relationship):
    label = "contribution"

class ThemeRoot(Node):
    element_type="themeroot"
    element_plural="themeroot"

    name = String()