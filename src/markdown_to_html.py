
from src.block_markdown import *
from src.textnode import *
from src.parentnode import *
from src.leafnode import *
from src.inline_markdown import *
from src.block_markdown import *

def markdown_to_html(doc):


    children = []

    blocks = markdown_to_blocks(doc)

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.Heading:
                children.append(create_heading(block))
            case BlockType.Paragraph:
                children.append(create_paragraph(block))
            case BlockType.Quote:
                children.append(create_quote(block))
            case BlockType.Code:
                children.append(create_codeblock(block))
            case BlockType.Ordered:
                children.append(create_ordered_list(block))
            case BlockType.Unordered:
                children.append(create_unordered_list(block))

            case _:
                raise ValueError(f"Invalid block type:{block_type}")


    root = ParentNode("div", children)
    return root            


def text_to_html_nodes(text):
    html_nodes = []

    text_nodes = text_to_text_nodes(text)

    for node in text_nodes:
        html_nodes.append(node.to_html_node())

    return html_nodes

def create_ordered_list(block):
    lines = block.split("\n")

    children = []


    prev_number = 0
    for line in lines:
        if not line[0].isdigit():
            raise ValueError(f"Invalid ordered-list formatting in block:\n{block}")
        digit = int(line[0])
        if digit <= prev_number:
            raise ValueError(f"Invalid ordered-list formatting - digits are not in ascending order.")
        nodes = text_to_html_nodes(line[line.find(".")+1:].strip())
        list_item_node = ParentNode("li", nodes)
        children.append(list_item_node)

    return ParentNode("ol", children)    

def create_unordered_list(block):
    lines = block.split("\n")

    children = []

    for line in lines:

        if not line.startswith("-"):
            raise ValueError(f"Invalid unordered-list formatting in block:\n{block}")
        nodes = text_to_html_nodes(line.lstrip("-").strip())
        list_item_node = ParentNode("li", nodes)
        children.append(list_item_node)

    return ParentNode("ul", children)

def create_codeblock(block):
    lines = block.split("\n")

    children = []

    for line in lines:
        nodes = text_to_html_nodes(line)
        nodes.append(LeafNode("br", ""))
        for node in nodes:
            children.append(node)

    return ParentNode("code", children)

def create_paragraph(block):
    lines = block.split("\n")

    children = []

    for line in lines:
        nodes = text_to_html_nodes(line)
        nodes.append(LeafNode("br", ""))
        for node in nodes:
            children.append(node)

    return ParentNode("p", children)


def create_quote(block):
    lines = block.split("\n")
    filtered_lines = []

    for line in lines:
        if not line.startswith(">"):
            raise ValueError(f"Invalid quote formatting in text:\n{block}")
        filtered_lines.append(line.lstrip(">").strip())

    children = []

    for line in filtered_lines:
        nodes = text_to_html_nodes(line)
        nodes.append(LeafNode("br", ""))
        for node in nodes:
            children.append(node)

    return ParentNode("blockquote", children)


def create_heading(block):

    header_level = 0
    for char in block:
        if char == "#":
            header_level += 1
            continue
        else:
            break
    
    text = block[header_level:].strip()

    children = text_to_html_nodes(text)
    return ParentNode(f"h{header_level}", children)

