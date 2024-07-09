import unittest

from src.textnode import TextNode
from src.textnode import TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertEqual(node, node2)

        node = TextNode("This is a text node", "bold", "www.google.com")
        node2 = TextNode("This is a text node", "bold", "www.google.com")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.Italic)
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.Bold, "www.google.com")
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.Code, "www.google.com")
        node2 = TextNode("This is another text node", TextType.Code, "www.google.com")
        self.assertNotEqual(node, node2)

        node = TextNode("This is a text node", TextType.Link, "www.youtube.com")
        node2 = TextNode("This is a text node", TextType.Bold, "www.google.com")
        self.assertNotEqual(node, node2)


  



if __name__ == "__main__":
    unittest.main()
