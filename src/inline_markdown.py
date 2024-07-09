from functools import reduce

from src.textnode import TextNode
from src.textnode import TextType

def split_textnodes_by_delimiter(old_nodes, delimiter, text_type):

    def split_and_map(text_node):
        if text_node.text_type != TextType.Text:
            return [text_node]
        
        chunks = text_node.text.split(delimiter)

        if len(chunks) == 0 or len(chunks) % 2 == 0:
            raise Exception(f"Improper opening/closing delimiter found in text:'{text_node.text}'. Delimiter:{delimiter}")
        
        return list(
            map(
                lambda tpl: TextNode(tpl[1], text_type if tpl[0] % 2 else TextType.Text),
                filter(lambda chunk: chunk[1], enumerate(chunks))
            )
        )

    return reduce(lambda acc, x: acc + x, map(split_and_map, old_nodes), [])


def text_to_text_nodes(text):
    node = TextNode(text, TextType.Text)
    nodes = [node]

    nodes = split_text_nodes_with_images(nodes)
    nodes = split_text_nodes_with_links(nodes)
    nodes = split_textnodes_by_delimiter(nodes, "**", TextType.Bold)
    nodes = split_textnodes_by_delimiter(nodes, "*", TextType.Italic)
    nodes = split_textnodes_by_delimiter(nodes, "`", TextType.Code)

    return nodes



def split_text_nodes_with_images(old_nodes):
        
    def get_new_nodes(text_node):
        images = extract_markdown_images(text_node.text)
        if len(images) == 0:
            return [text_node]
        
        def split(acc, image):
            txt, num_remaining_images, new_nodes = acc
            splits = txt.split(f"![{image[0]}]({image[1]})")

            new_nodes.append(TextNode(splits[0], TextType.Text))
            new_nodes.append(TextNode(image[0], TextType.Image, image[1]))

            if num_remaining_images == 0:
                if len(splits[1]) > 0:
                    new_nodes.append(TextNode(splits[1], TextType.Text))
                    return ("", num_remaining_images - 1, new_nodes)

            return (splits[1], num_remaining_images - 1, new_nodes)

        _, _, new_nodes = list(reduce(split, images, (text_node.text, len(images)-1, [])))
        return new_nodes
    
    return list(reduce(lambda acc, x: acc + x, list(map(get_new_nodes, old_nodes)), []))
    


def split_text_nodes_with_links(old_nodes):

    def get_new_nodes(text_node):
        links = extract_markdown_links(text_node.text)
        if len(links) == 0:
            return [text_node]
        
        def split(acc, link):
            txt, num_remaining_links, new_nodes = acc
            splits = txt.split(f"[{link[0]}]({link[1]})")

            new_nodes.append(TextNode(splits[0], TextType.Text))
            new_nodes.append(TextNode(link[0], TextType.Link, link[1]))

            if num_remaining_links == 0:
                if len(splits[1]) > 0:
                    new_nodes.append(TextNode(splits[1], TextType.Text))
                    return ("", num_remaining_links - 1, new_nodes)

            return (splits[1], num_remaining_links - 1, new_nodes)

        _, _, new_nodes = list(reduce(split, links, (text_node.text, len(links)-1, [])))
        return new_nodes
    
    return list(reduce(lambda acc, x: acc + x, list(map(get_new_nodes, old_nodes)), []))


def extract_markdown_links(text):
    import re
    return re.findall(r"\[(.*?)\]\((.*?)\)", text, re.MULTILINE)

def extract_markdown_images(text):
    import re
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text, re.MULTILINE)
