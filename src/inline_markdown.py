import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits TextNodes based on paired delimiters and wraps the content between them in a new TextType.

    This function processes a list of TextNode objects and looks for matching delimiter pairs 
    (e.g., '`' for code or '**' for bold). When such pairs are found within a node's text, the 
    function splits the text into separate nodes and wraps the content between delimiters with the 
    specified TextType.

    Args:
        old_nodes (list of TextNode): The list of nodes to process.
        delimiter (str): The delimiter string marking the start and end of special formatting (e.g., "`", "**").
        text_type (TextType): The type to assign to text found between the delimiter pairs (e.g., TextType.BOLD).

    Returns:
        list of TextNode: A new list of nodes, with matched delimiter content converted to the given text_type.

    Raises:
        ValueError: If a delimiter is opened but not properly closed.
    """

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
      
        sections = old_node.text.split(delimiter)
        print(f"sections: {sections}")
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        inside_delimiter = False  # Start outside delimiters

        for section in sections:
            if inside_delimiter:
                new_nodes.append(TextNode(section, text_type))
            else:
                new_nodes.append(TextNode(section, TextType.TEXT))
                   
            # Flip the flag after processing each section
            inside_delimiter = not inside_delimiter

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)