from enum import Enum

from functools import reduce

class BlockType(Enum):
    Paragraph = "paragraph",
    Heading = "heading",
    Code = "code",
    Quote = "quote",
    Unordered = "unordered-list",
    Ordered = "ordered-list"


def markdown_to_blocks(doc):

    lines = doc.split("\n")

    def accumulate_blocks(acc, line):
        current_block, blocks = acc

        if len(line.strip()) == 0:
            if len(current_block.strip()) > 0:
                blocks.append(current_block.strip())
                return ("", blocks)
            return (current_block, blocks)

        current_block += line + "\n"
        return (current_block, blocks)
        

    initial_acc = ("", [])
    final_current_block, final_blocks = reduce(accumulate_blocks, lines, initial_acc)

    if final_current_block.strip():
        final_blocks.append(final_current_block.strip())

    return final_blocks

def block_to_block_type(text_block) -> BlockType:

    import re

    num_lines = len(text_block.split("\n"))

    if re.search("^#{1,} ", text_block):
        return BlockType.Heading
    
    if re.search("^\`{3}.+\`{3}$", text_block,):
        return BlockType.Code
    
    if len(re.findall("^(> [^>]*?)$", text_block, re.MULTILINE)) == num_lines:
        return BlockType.Quote
    
    if len(re.findall("^(\- [^*]*?)$", text_block, re.MULTILINE)) == num_lines:
        return BlockType.Unordered

    ordered_list_matches = re.findall("^\d+\. [^\n]*$", text_block, re.MULTILINE)
    if len(ordered_list_matches) == num_lines:

        # Extract the list-indices into a list
        def extract_into_list(acc, str):
            acc.append(int(str[0]))
            return acc
        
        index_list = reduce(extract_into_list, ordered_list_matches, [])

        # Make sure numbers are in ascending order
        def check_ascending(acc, num):
            is_ascending, last_num = acc
            
            if num - last_num != 1:
                return (False, num)
            return (is_ascending, num)
            
        is_ascending, _ = reduce(check_ascending, index_list, (True, 0))

        if not is_ascending:
            raise ValueError(f"Ordered-list is not in ascending order. Text-block:\n{text_block}")
        
        return BlockType.Ordered
    
    return BlockType.Paragraph



