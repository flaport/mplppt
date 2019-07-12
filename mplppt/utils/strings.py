#############
## Imports ##
#############

import string
import random


###############
## Functions ##
###############


def random_name(N=10):
    """ String of N random characters """
    return "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(N)
    )


def get_content(filename):
    """ Get content of text file as string """
    with open(filename, "r") as file:
        content = file.read()
    return content


def parse_xml(filename):
    """ Parse xml file and introduce enters """
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
