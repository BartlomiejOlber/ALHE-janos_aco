

def print_hi(name):
    import xml.etree.ElementTree as ET
    root = ET.parse('data/janos-us--D-D-M-N-S-A-N-S/janos-us.xml').getroot()
    print(root)
    for type_tag in root.iter("{http://sndlib.zib.de/network}node"):
        # print(type_tag)
        value = type_tag.get('id')
        print(value)


if __name__ == '__main__':
    print_hi('PyCharm')

