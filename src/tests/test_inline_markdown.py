import unittest

from src.textnode import TextNode
from src.textnode import TextType
from src.inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_delimiter_code(self):

        node = TextNode("This is a `codeblock` text!", TextType.Text)
        split_nodes = split_textnodes_by_delimiter([node], "`", TextType.Code)

        self.assertEqual(split_nodes, [
            TextNode("This is a ", TextType.Text),
            TextNode("codeblock", TextType.Code),
            TextNode(" text!", TextType.Text),
        ])

    def test_delimiter_bold(self):

        node = TextNode("This is a **bold** text!", TextType.Text)
        split_nodes = split_textnodes_by_delimiter([node], "**", TextType.Bold)

        self.assertEqual(split_nodes, [
            TextNode("This is a ", TextType.Text),
            TextNode("bold", TextType.Bold),
            TextNode(" text!", TextType.Text),
        ])

        
    def test_delimiter_singular(self):

        node = TextNode("**Bold**", TextType.Text)
        split_nodes = split_textnodes_by_delimiter([node], "**", TextType.Bold)

        self.assertEqual(split_nodes, [
            TextNode("Bold", TextType.Bold),
        ])

    def test_delimiter_italic(self):

        node = TextNode("This is an *italic* text!", TextType.Text)
        split_nodes = split_textnodes_by_delimiter([node], "*", TextType.Italic)

        self.assertEqual(split_nodes, [
            TextNode("This is an ", TextType.Text),
            TextNode("italic", TextType.Italic),
            TextNode(" text!", TextType.Text),
        ])

    def test_delimiter_double_word(self):

        node = TextNode("This is **bold**, and so is **this!**", TextType.Text)
        split_nodes = split_textnodes_by_delimiter([node], "**", TextType.Bold)

        self.assertEqual(split_nodes, [
            TextNode("This is ", TextType.Text),
            TextNode("bold", TextType.Bold),
            TextNode(", and so is ", TextType.Text),
            TextNode("this!", TextType.Bold)
        ])

    def test_delimiter_multi_word(self):

        node = TextNode("This is a **multi-word bold!**", TextType.Text)
        split_nodes = split_textnodes_by_delimiter([node], "**", TextType.Bold)

        self.assertEqual(split_nodes, [
            TextNode("This is a ", TextType.Text),
            TextNode("multi-word bold!", TextType.Bold)
        ])

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" \
            + "and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        
        self.assertEqual(extract_markdown_images(text), 
            [
                ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
            ])

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    
    def test_split_text_nodes_with_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        node = TextNode(text, TextType.Text)
        self.assertEqual(split_text_nodes_with_links([node]), 
                         [
                            TextNode("This is text with a ", TextType.Text),
                            TextNode("link", TextType.Link, "https://www.example.com"),
                            TextNode(" and ", TextType.Text),
                            TextNode("another", TextType.Link, "https://www.example.com/another"),
                         ])
        
        text = "Here is a [link](www.example.com), and that's all."
        node = TextNode(text, TextType.Text)
        self.assertEqual(split_text_nodes_with_links([node]), 
                         [
                            TextNode("Here is a ", TextType.Text),
                            TextNode("link", TextType.Link, "www.example.com"),
                            TextNode(", and that's all.", TextType.Text),
                         ])


    def test_split_text_nodes_with_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)" \
            + " and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        node = TextNode(text, TextType.Text)
        self.assertEqual(split_text_nodes_with_images([node]), 
                         [
                            TextNode("This is text with an ", TextType.Text),
                            TextNode("image", TextType.Image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                            TextNode(" and ", TextType.Text),
                            TextNode("another", TextType.Image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
                         ])
        

    def test_text_to_text_nodes(self):
        text = "This is *italic*, this is **bold**, this is `codeblock`, this is [link](www.example.com), and finally this is ![image](www.example.com)"
        nodes = text_to_text_nodes(text)
        self.assertEqual(nodes, 
                         [
                             TextNode("This is ", TextType.Text),
                             TextNode("italic", TextType.Italic),
                             TextNode(", this is ", TextType.Text),
                             TextNode("bold", TextType.Bold),
                             TextNode(", this is ", TextType.Text),
                             TextNode("codeblock", TextType.Code),
                             TextNode(", this is ", TextType.Text),
                             TextNode("link", TextType.Link, "www.example.com"),
                             TextNode(", and finally this is ", TextType.Text),
                             TextNode("image", TextType.Image, "www.example.com"),
                         ])
        

