import unittest

from src.htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("p", "Hello!", None, { "style": "text-align:right", "color": "navy"})
        self.assertEqual(node.props_to_html(), " style=text-align:right color=navy")

        node = HTMLNode("p", "Hello!", None, [])
        self.assertEqual(node.props_to_html(), "")




if __name__ == "__main__":
    unittest.main()
