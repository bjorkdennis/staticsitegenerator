import unittest

from src.block_markdown import markdown_to_blocks
from src.block_markdown import block_to_block_type
from src.block_markdown import BlockType

class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):

        test_md = "This is **bolded** paragraph\n\n" \
                    + "This is another paragraph with *italic* text and `code` here\n" \
                    + "This is the same paragraph on a new line\n\n" \
                    + "- This is a list\n" \
                    + "- with items"


        self.assertEqual(markdown_to_blocks(test_md),
                            [
                            "This is **bolded** paragraph",
                            "This is another paragraph with *italic* text and `code` here\n" +
                            "This is the same paragraph on a new line",
                            "- This is a list\n- with items"

                            ])
        

    def test_block_to_block_type(self):

        self.assertEqual(block_to_block_type("> I am a quote\n> That spans\n> Multiple lines!"), BlockType.Quote)
        self.assertEqual(block_to_block_type("- I am an unordered-list\n- That spans\n- Multiple lines!"), BlockType.Unordered)
        self.assertEqual(block_to_block_type("1. I am an ordered list\n2. That spans\n3. Multiple lines!"), BlockType.Ordered)
        self.assertEqual(block_to_block_type("```I am a code block```"), BlockType.Code)
        self.assertEqual(block_to_block_type("### I am a header!"), BlockType.Heading)
        self.assertEqual(block_to_block_type("I am just a simple  \multi-line paragraph!"), BlockType.Paragraph)

