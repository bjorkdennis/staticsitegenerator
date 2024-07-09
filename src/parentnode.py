from src.htmlnode import HTMLNode

from functools import reduce

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):

        if children == None:
            raise ValueError("Children cannot be None")
        if len(children) == 0:
            raise ValueError("Children cannot be empty")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag cannot be None")
        if len(self.children) == 0:
            raise ValueError("Children cannot be empty")
        
        result = reduce(lambda curr, child: curr + child.to_html(), self.children, "")
        return f"<{self.tag}>{result}</{self.tag}>"