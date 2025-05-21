import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_no_props(self):
        """
        test for html node with no props
        """
        node = HTMLNode("a", "This is a text", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_htmlnode_props(self):
        """
        test for html node with with props
        """
        actual_node = HTMLNode("a", "This is a text", None, {"href": "https://www.google.com", "target": "_blank",})
        expected_node = HTMLNode("a", "This is a text", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(actual_node.props_to_html(), expected_node.props_to_html())
    
    def test_multiple_props(self):
        """
        Test HTML node with multiple props
        """
        node = HTMLNode("a", "Click me", None, {
            "href": "https://boot.dev",
            "target": "_blank",
            "class": "link"
        })
        # Check that all properties are present and properly formatted
        props_html = node.props_to_html()
        self.assertIn('href="https://boot.dev"', props_html)
        self.assertIn('target="_blank"', props_html)   
        self.assertIn('class="link"', props_html)
    
    def test_values(self):
        """
        test for html node values if equal
        """
        
        node = HTMLNode("div",
            "I wish I could read",
        )
        
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )
    
      
    def test_repr(self):
        node = HTMLNode("p", "I want to be a software developer", None, {"class": "primary"})
        self.assertEqual(node.__repr__(),"HTMLNode(p, I want to be a software developer, None, {'class': 'primary'})")
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        """
        test for leaf node for <p> tag 
        """
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_b(self):
        """
        test for leaf node for <b> tag
        """
        
        node = LeafNode("b", "I want to be a software engineer")
        self.assertEqual(node.to_html(), "<b>I want to be a software engineer</b>")
        
    def test_leaf_to_html_a(self):
        """
        test for leaf node for <a> tag
        """
        node = LeafNode("a", "This is a link for boot.dev", {"href": "https://boot.dev/", "target": "_blank",})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev/" target="_blank">This is a link for boot.dev</a>')
        
    def test_leaf_to_html_unclose_tag(self):
        """
        test for leaf node with unclose tag
        """
        
        node = LeafNode("p", "I want to become a software engineer")
        self.assertNotEqual(node.to_html(), "<p>I want to become a software engineer</p")
        
    def test_leaf_to_html_opening_tag(self):
        """
        test for leaf node with no opening tag
        """
         
        node = LeafNode("p", "I want to become a software engineer")
        self.assertNotEqual(node.to_html(), "p>I want to become a software engineer</p>")
        
    def test_leaf_to_html_no_tag(self):
        """
        test that LeafNode with no tag returns raw text
        """
        node = LeafNode(None, "I want to become a software engineer")
        self.assertEqual(node.to_html(), "I want to become a software engineer")
        
        
    def test_leaf_to_html_raises_value_error_on_none(self):
        """
        Test that LeafNode raises ValueError when value is None
        """
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()
