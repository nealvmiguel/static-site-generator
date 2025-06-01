import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_equal_nodes_are_equal(self):
        """
        Test for equal both text and text type
        """
        actual_node = TextNode("This is a text node", TextType.BOLD)
        expected_node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(actual_node, expected_node)
        
    def test_text_type_not_equal(self):
        """
        Test for not equal text type
        """
        actual_node = TextNode("This is a text node", TextType.BOLD)
        expected_node = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(actual_node, expected_node)

    def test_text_not_equal(self):
        """
        Test for not equal Text
        """
        actual_node = TextNode("This is a text node", TextType.BOLD)
        expected_node = TextNode("This is a different node", TextType.BOLD)
        self.assertNotEqual(actual_node, expected_node)
    
    
    def test_link_is_none(self):
        """
        Test for link is None
        """
        actual_node = TextNode("This is a text node", TextType.LINK, "https://boot.dev/")
        expected_node = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(actual_node, expected_node)
        
    def test_link_equal(self):
        """
        Test for link is equal
        """
        actual_node = TextNode("This is a text node", TextType.LINK, "https://boot.dev/")
        expected_node = TextNode("This is a text node", TextType.LINK, "https://boot.dev/")
        self.assertEqual(actual_node, expected_node)
        
    def test_link_not_equal(self):
        """
        test for link not equal
        """
        actual_node = TextNode("This is a text node", TextType.LINK, "https://boot.dev/")
        expected_node = TextNode("This is a text node", TextType.LINK, "https://scrimba.com/home")
        self.assertNotEqual(actual_node, expected_node)
        
        
    class TestTextNodeToHTMLNode(unittest.TestCase):
        def test_text_no_tag(self):
            """
            test for text_node_to_html no tag
            """
            node = TextNode("This is a text node", TextType.TEXT)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, None)
            self.assertEqual(html_node.value, "This is a text node")
        
        def test_text_no_value(self):
            """
            test for text_node_to_html no value
            """              
            node = TextNode("this is a text", TextType.TEXT)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, None)
            self.assertEqual(html_node.value, "")
            
        def test_bold(self):
            """
            test for text_node_to_html bold tag
            """
            node = TextNode("This is bold", TextType.BOLD)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "b")
            self.assertEqual(html_node.value, "This is bold")
        
        def test_italic(self):
            """
            test for text_node_to_html italic tag
            """
            node = TextNode("This is italic", TextType.ITALIC)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "i")
            self.assertEqual(html_node.value, "This is italic")
            
        def test_image(self):
            """
            test for text_node_to_html image tag
            """
            node = TextNode("", TextType.IMAGE)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "img")
            self.assertEqual(html_node.value, "")
            self.assertEqual(
                html_node.props,
                {"src": "https://www.boot.dev", "alt": "This is an image"},
                )            
            
        def test_link(self):
            """
            test for text_node_to_html image tag
            """
            node = TextNode("This is a link", TextType.LINK)
            html_node = text_node_to_html_node(node)
            self.assertEqual(html_node.tag, "a")
            self.assertEqual(html_node.value, "This is a link")
            self.assertEqual(
                html_node.props,
                {"href": "https://www.google.com", "target": "_blank",},
                )            
        
if __name__ == "__main__":
    unittest.main()