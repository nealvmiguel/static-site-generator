import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
)
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_delim_bold(self):
        """
        test for split nodes delimiter bold Text node
        """
        
        node = TextNode("This is a text with a **bolded** word", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_node
        )
    
    def test_delim_italic(self):
        """
        test for split nodes delimiter italic Text node
        """
        
        node = TextNode("This is a text with a *italic* word", TextType.TEXT)
        
        new_node = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        self.assertEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT)   
            ],
            new_node
        )
        
    def test_delim_code(self):
        """
        test for split nodes delimiter code Text node
        """
        
        node = TextNode("This is a text with a `coded` word", TextType.TEXT)
        
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("coded", TextType.CODE),
                TextNode(" word", TextType.TEXT)

            ],
            new_node
        )
    
    def test_delim_beginning_bold(self):
        """
        Test for delimiter in the beginning
        """
        
        node = TextNode("**bolded** text in the beginning", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [   
                TextNode("", TextType.TEXT), 
                TextNode("bolded", TextType.BOLD),
                TextNode(" text in the beginning", TextType.TEXT),
            ],
            new_node
        )
        
    def test_delim_beginning_italic(self):
        """
        Test for delimiter italic in the beginning
        """
        
        node = TextNode("*italic* text in the beginning", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            [   
                TextNode("", TextType.TEXT), 
                TextNode("italic", TextType.ITALIC),
                TextNode(" text in the beginning", TextType.TEXT),
            ],
            new_node
        )
        
    def test_delim_beginning_code(self):
        """
        Test for delimiter code in the beginning
        """
        
        node = TextNode("`code` text in the beginning", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [   
                TextNode("", TextType.TEXT), 
                TextNode("code", TextType.CODE),
                TextNode(" text in the beginning", TextType.TEXT),
            ],
            new_node
        )
    
    def test_delim_end_bold(self):
        """
        Test for delimiter bold at the end
        """
        
        node = TextNode("Delimiter at the end of text **bolded**", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [
                TextNode("Delimiter at the end of text ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode("", TextType.TEXT)
            ],
            new_node
            
        )
        
    def test_delim_end_italic(self):
        """
        Test for delimiter italic at the end
        """
        
        node = TextNode("Delimiter at the end of text *italic*", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("Delimiter at the end of text ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode("", TextType.TEXT)
            ],
            new_node
            
        )
    
    def test_delim_end_code(self):
        """
        Test for delimiter code at the end
        """
        
        node = TextNode("Delimiter at the end of text `code`", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [
                TextNode("Delimiter at the end of text ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode("", TextType.TEXT)
            ],
            new_node
        )
    
    def test_delim_no_closing_bold(self):
        """
        Test for bold delimiter with no closing bold delimiter
        """
        
        with self.assertRaises(ValueError):
            node = TextNode("This is a **bolded text", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)
            
    def test_delim_no_closing_italic(self):
        """
        Test for italic delimiter with no closing italic delimiter
        """
        
        with self.assertRaises(ValueError):
            node = TextNode("This is a *italic text", TextType.TEXT)
            split_nodes_delimiter([node], "*", TextType.ITALIC)
    
    def test_delim_no_closing_code(self):
        """
        Test for code delimiter with no closing code delimiter
        """
        
        with self.assertRaises(ValueError):
            node = TextNode("This is a `code text", TextType.TEXT)
            split_nodes_delimiter([node], "`", TextType.CODE)       
    
        
    def test_no_delim(self):
        """
        test with no delimiter
        """
        
        node = TextNode("This is a just a plain text", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "**", TextType.TEXT)
        
        self.assertEqual(
            [
                TextNode("This is a just a plain text", TextType.TEXT),

            ], 
            new_node)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )  
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches
        )
        