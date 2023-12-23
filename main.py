#import os, sys
#path = os.path.abspath("src")
#sys.path.append(path)
#
#import structures
import xml.etree.ElementTree as ET

def parse_cppcheck_result(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    results = root.findall(".//error")

    return results

def generate_graph(errors, output_file='graph'):

    for error in errors:
        function_name = error.get('verbose')
        print (function_name)


if __name__ == "__main__":
    cppcheck_result_path = 'cppcheck_result.xml'
    cppcheck_errors = parse_cppcheck_result(cppcheck_result_path)
    generate_graph(cppcheck_errors)
