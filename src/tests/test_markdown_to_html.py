import unittest

from src.markdown_to_html import *

class TestMarkdownToHtml(unittest.TestCase):

    def test_markdown_to_html(self):
          with open("src/tests/MarkdownTest.md") as file:
            content = file.read()
            root = markdown_to_html(content)
            print(f"HTML:\n{root.to_html()}")

