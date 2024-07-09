from enum import Enum

from src.parentnode import ParentNode
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from functools import reduce

class TextType(Enum):
    Text = "text",
    Bold = "bold",
    Italic = "italic",
    Image = "image",
    Code = "code",
    Link = "link"

class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
    def to_html_node(self):
        match(self.text_type):
            case TextType.Text:
                return LeafNode(None, self.text, None)
            case TextType.Bold:
                return LeafNode("b", self.text, None)
            case TextType.Italic:
                return LeafNode("i", self.text, None)
            case TextType.Code:
                return LeafNode("code", self.text, None)
            case TextType.Link:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.Image:
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            

