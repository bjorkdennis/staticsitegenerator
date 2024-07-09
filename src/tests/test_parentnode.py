import unittest

from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_tohtml(self):

        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

        node = ParentNode(
        "p",
        [
            ParentNode("h1", [LeafNode("p", "Hello!", {"Color": "Navy"})]),
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])

        self.assertEqual(node.to_html(), "<p><h1><p Color=Navy>Hello!</p></h1><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_no_children(self):
        
        with self.assertRaises(ValueError):
            node = ParentNode("p", [], None)

        with self.assertRaises(ValueError):
            node = ParentNode("p", None, None)

    def test_no_tag(self):

        with self.assertRaises(ValueError):
            node = ParentNode(None, None, None)

        
        
