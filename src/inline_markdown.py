from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
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
        # If the delimiter isn't present, keep the node as is
        if delimiter not in node.text:
            new_nodes.append(node)
            continue

        # Split the text by the delimiter
        parts = node.text.split(delimiter)

        # If even number of parts, closing delimiter is missing
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