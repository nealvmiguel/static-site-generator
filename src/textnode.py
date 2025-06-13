from htmlnode import LeafNode
from enum import Enum
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    
class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented  # or return False
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )
       
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    """
    Converts a TextNode instance into a corresponding LeafNode for HTML rendering.

    This function maps specific text types to appropriate HTML tags. For example,
    bold text is converted to a <b> element, links become <a>, and so on.

    Parameters:
        text_node (TextNode): An instance representing a piece of formatted text.

    Returns:
        LeafNode: A leaf HTML node representing the text in HTML.

    Raises:
        ValueError: If the text_type is not recognized or unsupported.

    Supported Mappings:
        - TEXT:    Plain text (no tag)
        - BOLD:    <b>
        - ITALIC:  <i>
        - CODE:    <code>
        - LINK:    <a href="...">...</a>
        - IMAGE:   <img src="..." alt="...">
    """
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

        
        