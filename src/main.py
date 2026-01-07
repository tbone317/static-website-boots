from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import markdown_to_html_node, extract_title
import os, shutil, sys


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Base path is: {basepath}")
    #text1 = TextNode("Hello, World!", TextType.TEXT)
    #text2 = TextNode("This is bold text.", TextType.BOLD)
    #text3 = TextNode("This is some anchor text.", TextType.IMAGE, url="https://www.boot.dev")
    #print(text1)
    #print(text2)
    #print(text3)
    #print(os.path.exists("static"))


    #files = os.listdir("static")
    #print(files)
    
    #copy_static_files()

    copy_static_to_public()
    
    # Generate the page from content/index.md
    #generate_page("content/index.md", "template.html", "docs/index.html", basepath)
    generate_pages_recursively(basepath)

def generate_pages_recursively(basepath="/", dir_path_content="content", dir_template_path="template.html", dest_dir_path="docs"):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(from_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + ".html")
                print(f"Generating page for {from_path} to {dest_path}")
                generate_page(from_path, dir_template_path, dest_path, basepath)


def copy_recursive(src, dest):
    if os.path.isdir(src):
        if not os.path.exists(dest):
            os.mkdir(dest)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            copy_recursive(s, d)
    else:
        shutil.copy2(src, dest)

def copy_static_to_public(static_dir="static", public_dir="docs"):
    #remove desstination if it exists
    if os.path.exists(public_dir):  
       print(f"Removing existing directory {public_dir}")
       shutil.rmtree(public_dir, ignore_errors=True)   
    
    print(f"Copying static files from {static_dir} to {public_dir}")
    copy_recursive(static_dir, public_dir)

def copy_static_files():
    shutil.rmtree("public", ignore_errors=True)
    if not os.path.exists("public"):
        os.mkdir("public")

    for item in os.listdir("static"):
        s = os.path.join("static", item)
        d = os.path.join("public", item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path: Path to the markdown file to convert
        template_path: Path to the HTML template file
        dest_path: Path where the generated HTML should be written
        basepath: The base path for the site (e.g., "/" for root or "/repo-name/" for GitHub Pages)
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Extract the title
    title = extract_title(markdown_content)
    
    # Replace placeholders in template
    page_content = template_content.replace("{{ Title }}", title)
    page_content = page_content.replace("{{ Content }}", html_content)
    
    # Replace absolute paths with basepath-aware paths
    page_content = page_content.replace('href="/', f'href="{basepath}')
    page_content = page_content.replace('src="/', f'src="{basepath}')
    
    # Create destination directory if needed
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the final HTML file
    with open(dest_path, 'w') as f:
        f.write(page_content)

if __name__ == "__main__":
    main()