from enum import Enum

from htmlnode import ParentNode, HTMLNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
        

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks 

def block_to_block_type(block):
    # check for heading
    if block.startswith(('#', '##', '###', '####', '#####', '######')):
        return BlockType.HEADING
    
    # check for code 
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")
    

    # check for quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # check for unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    # check for ordered list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown) 

    children = []
    
    for block in blocks:
       html_node = block_to_html_node(block)
       children.append(html_node)
    return ParentNode("div", children, None)
    
def block_to_html_node(block):
    block_type = block_to_block_type(block)
    
    match block_type:
        case BlockType.HEADING:
            return heading_to_html(block)
        case BlockType.PARAGRAPH:
            return paragraph_to_html(block)
        case BlockType.CODE:
            return code_to_html(block)
        case BlockType.QUOTE:
            return quote_to_html(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html(block)
        case _:
            raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
  
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
        
    return children
    
def heading_to_html(block):
    """
    Convert a heading block to HTML heading tag.
    """
    # Count the number of # characters at the start
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    
    # HTML only supports h1-h6, so cap at level 6
    if level > 6:
        raise ValueError("Invalid Heading Level")
     
    # Extract the heading text (everything after the #s and any following spaces)
    heading_text = block[level:].strip() 
    children = text_to_children(heading_text)
    
    return ParentNode(f"h{level}", children)

def paragraph_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def code_to_html(block):
    if not block.startswith("```") and not block.endswith("```"):
        raise ValueError("Invalid Code Block")
    
    
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

    
def quote_to_html(block):
    lines = block.split("\n")
    new_lines = []
    
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")

        new_lines.append(line.lstrip(">").strip())
        
    quote_text = " ".join(new_lines)
    children = text_to_children(quote_text)
    return ParentNode("blockquote", children)
    
def unordered_list_to_html(block):
    items = block.split("\n")
    new_items = []
    
    for item in items:
        item_text = item.lstrip("-").strip()
        children = text_to_children(item_text)
        li_text = ParentNode("li" ,children)
        new_items.append(li_text)
        
    
    return ParentNode("ul", new_items)

def ordered_list_to_html(block):
    items = block.split("\n")
    new_items = []
    for item in items:
        text = item[2:].strip()
        children = text_to_children(text)
        li_text = ParentNode("li", children)        
        new_items.append(li_text)
        
    return ParentNode("ol", new_items)
   
    



# markdown_to_html_node("""
# # This is a heading of oten oten

# This is a paragraph of text. It has some **bold** and _italic_ words inside of it.
# This is also in the paragraph
# This is paragraph with `code` block

# ```let ben = cute```

# > "Growth doesn’t come from knowing the path, but from walking it with curiosity, courage, and consistency.  
# > We don’t become better by avoiding mistakes—we evolve by embracing them, learning from their sharp edges, and continuing forward with clearer eyes.  
# > The most powerful tools you have are not just your skills, but your willingness to keep asking questions, to keep showing up, and to build something meaningful even when the outcome is uncertain.  
# > Progress is rarely loud or glamorous—it’s quiet, persistent, and often invisible until suddenly, it’s undeniable."


# - This is the first list item in a list block
# - This is a list item with **bold** text
# - This is another list item with *italic* text        

# 1. list number one
# 2. List number two
# 3. List number three
         
# """)