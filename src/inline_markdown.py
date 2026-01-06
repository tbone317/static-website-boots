import re
from textnode import TextNode, TextType

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """
    Extract all markdown images from text.
    
    Returns a list of tuples (alt_text, url) for each image found.
    Markdown image format: ![alt_text](url)
    
    Args:
        text: Raw markdown text containing images
        
    Returns:
        List of tuples with (alt_text, url)
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Extract all markdown links from text.
    
    Returns a list of tuples (anchor_text, url) for each link found.
    Markdown link format: [anchor_text](url)
    
    Args:
        text: Raw markdown text containing links
        
    Returns:
        List of tuples with (anchor_text, url)
    """
    #pattern = r"\[([^\[\]]*)\]\(([^\(\)]*)\)"
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split text nodes by markdown images into multiple nodes.
    
    Takes a list of nodes and splits any TEXT type nodes based on embedded images.
    Images in markdown format ![alt_text](url) are extracted and converted to IMAGE type nodes.
    
    Args:
        old_nodes: List of TextNode objects to process
        
    Returns:
        List of TextNode objects with images extracted as separate IMAGE nodes
        
    Example:
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        # Returns:
        # [
        #     TextNode("This is text with an ", TextType.TEXT),
        #     TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        #     TextNode(" and another ", TextType.TEXT),
        #     TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        # ]
    """
    new_nodes = []
    
    for node in old_nodes:
        # Only split TEXT type nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Extract all images from the text
        images = extract_markdown_images(node.text)
        
        # If no images found, keep the node as is
        if not images:
            new_nodes.append(node)
            continue
        
        # Process the text by splitting on each image
        current_text = node.text
        for alt_text, image_url in images:
            # Create the markdown image pattern to split on
            image_markdown = f"![{alt_text}]({image_url})"
            
            # Split the current text at the image (only split once)
            sections = current_text.split(image_markdown, 1)
            
            # Add the text before the image (if not empty)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
            
            # Update current_text to the text after the image for next iteration
            current_text = sections[1] if len(sections) > 1 else ""
        
        # Add any remaining text after the last image (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split text nodes by markdown links into multiple nodes.
    
    Takes a list of nodes and splits any TEXT type nodes based on embedded links.
    Links in markdown format [anchor_text](url) are extracted and converted to LINK type nodes.
    
    Args:
        old_nodes: List of TextNode objects to process
        
    Returns:
        List of TextNode objects with links extracted as separate LINK nodes
        
    Example:
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        # Returns:
        # [
        #     TextNode("This is text with a link ", TextType.TEXT),
        #     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        #     TextNode(" and ", TextType.TEXT),
        #     TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        # ]
    """
    new_nodes = []
    
    for node in old_nodes:
        # Only split TEXT type nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        # Extract all links from the text
        links = extract_markdown_links(node.text)
        
        # If no links found, keep the node as is
        if not links:
            new_nodes.append(node)
            continue
        
        # Process the text by splitting on each link
        current_text = node.text
        for anchor_text, link_url in links:
            # Create the markdown link pattern to split on
            link_markdown = f"[{anchor_text}]({link_url})"
            
            # Split the current text at the link (only split once)
            sections = current_text.split(link_markdown, 1)
            
            # Add the text before the link (if not empty)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, link_url))
            
            # Update current_text to the text after the link for next iteration
            current_text = sections[1] if len(sections) > 1 else ""
        
        # Add any remaining text after the last link (if not empty)
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Split a markdown document into blocks.
    
    Blocks are separated by blank lines (\n\n) in the markdown.
    Each block is stripped of leading/trailing whitespace.
    Empty blocks are removed.
    
    Args:
        markdown: Raw markdown text representing a full document
        
    Returns:
        List of block strings
    """
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            filtered_blocks.append(stripped)
    return filtered_blocks