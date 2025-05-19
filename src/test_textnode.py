import unittest

from textnode import TextNode, TextType


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
        
if __name__ == "__main__":
    unittest.main()