import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
)
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Show full diffs in assertion failures
        
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
        1
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
        
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )    
    
    def test_split_image(self):       
        node = TextNode(
            "This is a cool setup ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        
        new_node = split_nodes_image([node])       
        self.assertListEqual(
            [
                TextNode("This is a cool setup ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_node
        )
    
    def test_split_image_single(self):        
        node = TextNode(
            "![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )      
        new_node = split_nodes_image([node])       
        self.assertEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_node
        )
        
    def test_split_links(self):      
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )      
        new_node = split_nodes_link([node])      
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ",  TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_node
        )
    
    def test_split_link(self):      
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT
        )
        new_node = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_node
        )
        
    def test_split_nodes_image_empty_list(self):
        self.assertEqual([], split_nodes_image([]))

    def test_split_nodes_link_empty_list(self):
        self.assertEqual([], split_nodes_link([]))
      
    def test_split_nodes_image_no_images(self):
        node = TextNode("Just plain text with no images", TextType.TEXT)
        self.assertEqual([node], split_nodes_image([node]))

    def test_split_nodes_link_no_links(self):
        node = TextNode("Just plain text with no links", TextType.TEXT)
        self.assertEqual([node], split_nodes_link([node]))
            
    def test_image_with_link_text(self):
        node = TextNode("![image with [link]](https://example.com/img.png)", TextType.TEXT)
        expected = [
            TextNode("image with [link]", TextType.IMAGE, "https://example.com/img.png")
        ]
        self.assertEqual(expected, split_nodes_image([node]))
        
    def test_link_with_image_text(self):
        node = TextNode("[link with ![image]](https://example.com)", TextType.TEXT)
        expected = [
            TextNode("link with ![image]", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(expected, split_nodes_link([node]))
        
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )