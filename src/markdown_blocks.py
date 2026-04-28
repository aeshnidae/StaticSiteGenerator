from enum import Enum
from htmlnode import ParentNode, HTMLNode, LeafNode
from inline import text_to_textnodes
from textnode import TextNode, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
      

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if len(block) > 0]

def block_to_block_type(block):
    match block[0]:
        case "#":
            return valid_heading(block)
        case "`":
            return valid_code(block)
        case ">":
            return valid_quote(block)
        case "-":
            return valid_unordered_list(block)
        case "1":
            return valid_ordered_list(block)
    return BlockType.PARAGRAPH

def valid_heading(text):
    hashtag_counter = 0
    has_space = False
    has_text = False

    for char in text:
        if char == "#":
            hashtag_counter += 1
        elif char == " ":
            has_space = True
        else:
            has_text = True
            break
    
    if 0 < hashtag_counter < 7 and has_space and has_text:
        return BlockType.HEADING
    else:
        return BlockType.PARAGRAPH
    
def valid_code(text):
    start = text[:4] == "```\n"
    end = text[-4:] == "\n```"
    if start and end:
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH
    
def valid_quote(text):
    if all([True if line[0] == ">" else False for line in text.split("\n")]):
        return BlockType.QUOTE
    else:
        return BlockType.PARAGRAPH
    
def valid_unordered_list(text):
    if all([True if line[:2] == "- " else False for line in text.split("\n")]):
        return BlockType.UNORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def valid_ordered_list(text):
    lines = text.split("\n")
    start_num = 1
    for line in lines:
        if line[:3] == f"{start_num}. ":
            start_num += 1
        else:
            return BlockType.PARAGRAPH
    return BlockType.ORDERED_LIST
    


def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        match block_to_block_type(block):

            case BlockType.PARAGRAPH:
                text_nodes = text_to_textnodes(block.replace("\n", " "))
                leaf_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                new_node = HTMLNode("p", None, leaf_nodes, None)
                html_nodes.append(new_node)

            case BlockType.HEADING:
                parts = block.split(" ",1)
                size = len(parts[0])
                new_node = HTMLNode(f"h{size}", parts[1], None, None)
                html_nodes.append(new_node)

            case BlockType.CODE:
                text = block[4:-3]
                new_node = HTMLNode("pre", None, [LeafNode("code", text)], None)
                html_nodes.append(new_node)

            case BlockType.QUOTE:
                new_node = HTMLNode("blockquote", block.replace("\n", " ").replace("> ","").replace(">",""), None, None)
                html_nodes.append(new_node)

            # These two look spicy
            case BlockType.UNORDERED_LIST:
                items = [ParentNode("li", [text_node_to_html_node(text_node) for text_node in text_to_textnodes(item)]) for item in block.replace("\n","").split("- ") if item != ""]
                new_node = ParentNode("ul", items)
                html_nodes.append(new_node)

            case BlockType.ORDERED_LIST:
                items = [ParentNode("li", [text_node_to_html_node(text_node) for text_node in text_to_textnodes(item[3:])]) for item in block.split("\n") if item != ""]
                new_node = ParentNode("ol",items)
                html_nodes.append(new_node)

    parent_node = ParentNode("div", html_nodes, None)
    return parent_node
