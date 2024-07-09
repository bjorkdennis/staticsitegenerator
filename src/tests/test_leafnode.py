import unittest

from src.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_tohtml(self):
        leaf = LeafNode("p", "Hello!", {"style": "text-align:right", "color": "navy"})
        self.assertEqual(leaf.to_html(), "<p style=text-align:right color=navy>Hello!</p>")

        leaf = LeafNode(None, "Hello!", None)
        self.assertEqual(leaf.to_html(), "Hello!")

    def test_value_none(self):
        with self.assertRaises(ValueError):
            leaf = LeafNode("h1", None, {})