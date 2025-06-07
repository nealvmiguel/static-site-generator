import unittest
from markdown_to_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownParser(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        
        markdown_blocks = markdown_to_blocks(markdown)
        
        self.assertEqual(markdown_blocks, [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ])
        
    def test_markdown_two_consecutive_newlines(self):
        markdown = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
- with items
        """
        
        markdown_blocks = markdown_to_blocks(markdown)
        self.assertEqual([
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items\n- with items"
            
        ],
        markdown_blocks)

    def test_markdown_one_block(self):
        markdown = """
This is **bolded** paragraph
    """
    
        blocks = markdown_to_blocks(markdown)
        
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph"
            ]
        )
    
    def test_markdown_empty(self):
        markdown = ""
        
        blocks = markdown_to_blocks(markdown)
        
        self.assertEqual(
            blocks,
            []
        )
        
        
    def test_markdown_internal_newlines(self):
        markdown = """
This is a paragraph that
spans multiple lines. Even though there's a newline character
after "that" and "lines.", it's still just one paragraph block
because there are no blank lines between them.

This is a new paragraph block because there's a blank line above it.
    """
        
        blocks = markdown_to_blocks(markdown)
        
        self.assertEqual(
            blocks,
            [
                "This is a paragraph that\nspans multiple lines. Even though there's a newline character\nafter \"that\" and \"lines.\", it's still just one paragraph block\nbecause there are no blank lines between them.",
                "This is a new paragraph block because there's a blank line above it."
            ]
        )
        
        
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)        
        
if __name__ == '__main__':
    unittest.main()