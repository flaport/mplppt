""" String and textfile manipulations """


#############
## Imports ##
#############

import string
import random


###############
## Functions ##
###############


def random_name(N=10):
    """ String of N random characters 
    
    Args:
        N: int: the number of random characters

    Returns:
        s: string: the random string with N characters
    """
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(N)
    )


def get_content(filename):
    """ Get content of text file as string 
    
    Args:
        filename: the filename of the textfile to read
    
    Returns:
        s: string: the content of the texfile
    """
    with open(filename, "r") as file:
        content = file.read()
    return content


def parse_xml(filename):
    """ Parse xml file and introduce returns
    
    makes the xml file a bit more readable

    Args:
        filename: str: the filename of the xml file to make more readable
    """
    # check filename
    if not filename.endswith(".xml"):
        filename = filename + ".xml"

    # read content
    with open(filename, "r") as file:
        content = file.read()

    # replace
    content = content.replace("><", ">\n<")

    # overwrite
    with open(filename, "w") as file:
        file.write(content)
