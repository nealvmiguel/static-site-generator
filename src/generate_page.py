import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    
    for line in lines:
        if line.startswith("#"):
            return line[2:].strip()    
    
    raise ValueError("No title found")
   
   
   
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Step 5.2 - Read markdown file
    with open(from_path, "r") as file:
        markdown = file.read()
    
    # Step 5.3 - Read template file  
    with open(template_path, "r") as file:
        template = file.read()
    
    # Step 5.4 - Convert markdown to HTML (goes here, outside the with blocks)
    html = markdown_to_html_node(markdown).to_html()
    
    # step 5.5 
    title = extract_title(markdown)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    dest_dir_path = os.path.dirname(dest_path)
    
    os.makedirs(dest_dir_path, exist_ok=True)
        
        
    with open(dest_path, "w") as file:
        file.write(template)