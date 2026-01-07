import re
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

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


def block_to_block_type(block: str) -> str:
    """
    Determine the type of a markdown block.
    
    Returns one of: "heading", "code", "unordered_list", "ordered_list", "quote", "paragraph"
    
    Args:
        block: A single markdown block string
        
    Returns:
        String representing the block type
    """
    lines = block.split("\n")
    
    # Check for heading (starts with # 1-6 times)
    if lines[0].startswith("#"):
        heading_level = 0
        for char in lines[0]:
            if char == "#":
                heading_level += 1
            else:
                break
        if heading_level <= 6 and heading_level > 0 and (len(lines[0]) > heading_level and lines[0][heading_level] == " "):
            return "heading"
    
    # Check for code block (starts and ends with ```)
    if block.startswith("```") and block.endswith("```"):
        return "code"
    
    # Check for unordered list (lines start with - or * followed by space)
    if all(line.startswith("- ") or line.startswith("* ") for line in lines):
        return "unordered_list"
    
    # Check for ordered list (lines start with number. followed by space)
    is_ordered = True
    for i, line in enumerate(lines):
        if not (line.startswith(f"{i + 1}. ")):
            is_ordered = False
            break
    if is_ordered:
        return "ordered_list"
    
    # Check for quote (all lines start with >)
    if all(line.startswith(">") for line in lines):
        return "quote"
    
    return "paragraph"


def text_to_children(text: str) -> list[HTMLNode]:
    """
    Convert inline markdown text to a list of child HTMLNodes.
    
    Processes inline markdown (bold, italic, code, images, links) and
    converts TextNodes to HTMLNodes.
    
    Args:
        text: Text possibly containing inline markdown
        
    Returns:
        List of HTMLNode objects representing the parsed inline content
    """
    from main import text_node_to_html_node
    
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
    """
    Convert a full markdown document to a single parent HTMLNode.
    
    Splits the markdown into blocks, determines the type of each block,
    creates appropriate HTMLNodes, and nests them under a single parent div.
    
    Args:
        markdown: Full markdown document as a string
        
    Returns:
        Parent HTMLNode (div) containing all block content
    """
    from main import text_node_to_html_node
    
    blocks = markdown_to_blocks(markdown)
    children = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == "heading":
            # Extract heading level and content
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else:
                    break
            content = block[level:].strip()
            tag = f"h{level}"
            children_nodes = text_to_children(content)
            html_node = ParentNode(tag, children_nodes)
            children.append(html_node)
            
        elif block_type == "code":
            # Remove the ``` markers and get the content
            lines = block.split("\n")
            code_content = "\n".join(lines[1:-1]) if len(lines) > 2 else ""
            if not code_content and len(lines) >= 2:
                code_content = "\n".join(lines[1:-1])
            # Add newline at end if there's content
            if code_content:
                code_content += "\n"
            code_node = LeafNode("code", code_content)
            pre_node = ParentNode("pre", [code_node])
            children.append(pre_node)
            
        elif block_type == "unordered_list":
            # Split into list items, remove bullet points
            lines = block.split("\n")
            list_items = []
            for line in lines:
                # Remove '- ' or '* ' prefix
                item_text = line[2:] if line.startswith(("- ", "* ")) else line
                children_nodes = text_to_children(item_text)
                li_node = ParentNode("li", children_nodes)
                list_items.append(li_node)
            ul_node = ParentNode("ul", list_items)
            children.append(ul_node)
            
        elif block_type == "ordered_list":
            # Split into list items, remove number prefix
            lines = block.split("\n")
            list_items = []
            for line in lines:
                # Remove number and period prefix (e.g., "1. ")
                dot_index = line.find(". ")
                if dot_index != -1:
                    item_text = line[dot_index + 2:]
                else:
                    item_text = line
                children_nodes = text_to_children(item_text)
                li_node = ParentNode("li", children_nodes)
                list_items.append(li_node)
            ol_node = ParentNode("ol", list_items)
            children.append(ol_node)
            
        elif block_type == "quote":
            # Remove '>' from each line and join
            lines = block.split("\n")
            quote_lines = []
            for line in lines:
                # Remove leading '>' and optional space
                stripped = line[1:].strip() if line.startswith(">") else line
                quote_lines.append(stripped)
            quote_text = " ".join(quote_lines)
            children_nodes = text_to_children(quote_text)
            blockquote_node = ParentNode("blockquote", children_nodes)
            children.append(blockquote_node)
            
        else:  # paragraph
            # Join multi-line paragraphs with spaces
            paragraph_text = " ".join(block.split("\n"))
            children_nodes = text_to_children(paragraph_text)
            p_node = ParentNode("p", children_nodes)
            children.append(p_node)
    
    return ParentNode("div", children)