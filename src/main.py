from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
import os, shutil


def main():
    text1 = TextNode("Hello, World!", TextType.TEXT)
    text2 = TextNode("This is bold text.", TextType.BOLD)
    text3 = TextNode("This is some anchor text.", TextType.IMAGE, url="https://www.boot.dev")
    print(text1)
    print(text2)
    print(text3)
    print(os.path.exists("static"))


    files = os.listdir("static")
    print(files)
    #copy_static_files()
    copy_static_to_public()

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

def copy_static_to_public(static_dir="static", public_dir="public"):
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

if __name__ == "__main__":
    main()