import re

from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

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
    """
    Extracts all image markdown elements from the given text.

    Markdown image syntax looks like: ![alt text](image_url)

    Args:
        text (str): The input string that may contain markdown image syntax.

    Returns:
        list of tuples: Each tuple contains (alt_text, image_url) for each image found.
                        Example: [('cat picture', 'https://example.com/cat.png')]
    """
   

    return re.findall(r"!\[((?:[^\[\]]|(?:\[[^\[\]]*\]))*)\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)", text)


def extract_markdown_links(text):
    """
    Extracts all standard markdown links from the given text, excluding images.

    Markdown link syntax looks like: [link text](url)

    Args:
        text (str): The input string that may contain markdown link syntax.

    Returns:
        list of tuples: Each tuple contains (link_text, url) for each link found.
                        Example: [('OpenAI', 'https://openai.com')]
    """
    
    
    return re.findall(r"(?<!!)\[((?:[^\[\]]|(?:\[[^\[\]]*\]))*)\]\(([^()]*(?:\([^()]*\)[^()]*)*)\)", text)



def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        for image in images:  
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        original_text = old_node.text
        
        links = extract_markdown_links(original_text)

        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        for link in links:  
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
          
            
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            
            original_text = sections[1]
            
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    
 
    return new_nodes
            


        
