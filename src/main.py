from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    text1 = TextNode("Hello, World!", TextType.TEXT)
    text2 = TextNode("This is bold text.", TextType.BOLD)
    text3 = TextNode("This is some anchor text.", TextType.IMAGE, url="https://www.boot.dev")
    print(text1)
    print(text2)
    print(text3)

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes by a delimiter into multiple nodes.
    
    Takes a list of nodes and splits any TEXT type nodes based on the delimiter.
    The delimiter wraps content that should be converted to the specified text_type.
    
    Example:
        split_nodes_delimiter(
            [TextNode("This is text with a `code block` word", TextType.TEXT)],
            "`",
            TextType.CODE
        )
        
        Returns:
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
    """
    new_nodes = []
    
    for node in old_nodes:
        # Only split TEXT type nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Split the text by the delimiter
        parts = node.text.split(delimiter)
        
        # If odd number of parts, closing delimiter is missing
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: unclosed delimiter '{delimiter}'")
        
        # Process the parts
        for i, part in enumerate(parts):
            # Even indices are TEXT type, odd indices are the specified text_type
            if i % 2 == 0:
                # TEXT part
                if part:  # Don't add empty text nodes
                    new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # Delimited part (should be the specified text_type)
                if part:  # Don't add empty nodes
                    new_nodes.append(TextNode(part, text_type))
    
    return new_nodes

if __name__ == "__main__":
    main()