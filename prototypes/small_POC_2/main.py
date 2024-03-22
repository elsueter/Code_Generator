
# Imports

import argparse
parser=argparse.ArgumentParser(description="sample argument parser")
parser.add_argument('-v', action='store_true')
args = parser.parse_args()

# --- Description ---
# A quick working example demonstratinc MC/DC coverage expectations on a function call in a condition in C 
#
# Example C code:
#
# int main(int a)
# {
#   int y = 0;
#
#   if( ( x && y ) || a )
#   {
#       return 1;
#   }
#   else
#   {
#       printf("%i", a);
#   }
#   return 0;
# }
#
# s-exp
#
# here this tree is not sticking to the <cons> <atom> style
# of s-exp like in lisp. here () denotes going deeper into
# the tree and . is adding a node at the same level.
# this has been done to allow a non-binary tree to be described
#
# nl on "." where a <cons> cell has 2nd item for complex obj
# maintain "()" for empty value -> returns "NIL"
# if brackets are opened for specifically not a scope or body
# the first element "names" the node
#
# ( <label> . <node> . <node> . ( <node> ) )
#
#
# 
#

code_string = """
( 
    include . <stdio.h>
) .
(
    func . int . test_func . 
    (
        int . a
    ) .
    (
        (
            int . x . 0
        )
        (
            int . y . 0
        )
        (
            if . ( || . ( && . x . y ) . a ) .
            (
                return . (1)
            )
        )
        (
            if . ( && . ( || . x . y ) . a ) .
            (
                return . (1)
            )
        )
        (
            else .
            (
                printf("a:%i", a)
            )
        )
        (
            return . (0)
        )
    )
) .
(
    func . int . main . () .
    (
        test_func( 0 )
    )
)"""

# -------------------------------------- TREE --------------------------------------------

structure_keywords = {"int", "body", "params", "if", "else", "func", "file"}
conditionals = {"if"}
operators = {"||", "&&"}
types = {"int"}


# subsets of node classes
class node(object):
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []
        self.value = False

    def add_child(self, obj):
        self.children.append(obj)
        obj.add_parent(self)

    def add_parent(self, obj):
        self.parent = obj


    #lookup MC/DC calculations - not what out tooling does
    def resolve(self):
        if self.data in operators:
            match self.data:
                case "||":
                    return self.children[0].resolve() or self.children[1].resolve()
                case "&&":
                    return self.children[0].resolve() and self.children[1].resolve()
        else:
            return self.value

    def parse_vectors(self, in_conditional, test_vectors):
        return_arr = [];
        if in_conditional:
            if self.data not in operators:
                test_vectors.append(self)
            for c in self.children:
                c.parse_vectors(in_conditional, test_vectors)
        elif self.data in conditionals:
            #get the vector variables
            self.children[0].parse_vectors(True, test_vectors)
            current_string = f"Test vector: {self.render().split('{')[0]}\n"
            for tv in test_vectors:
                current_string += f"{tv.data} "
            current_string += "R\n"
            for i in range(pow(2, len(test_vectors))):
                for j, tv in enumerate(test_vectors):
                    bin_val = bin(i)[-(j+1)]
                    if bin_val == '1':
                        tv.value = True
                    else:
                        tv.value = False
                for tv in test_vectors:
                    current_string += f"{+(tv.value)} "
                current_string += f"{self.children[0].resolve()}\n"
            return_arr.append(current_string)
            # TODO case of a conditional in the body of a conditional is not handled currently
        else:
            for c in self.children:
                test_vectors = []
                return_arr += c.parse_vectors(in_conditional, [])
        return return_arr
    
    def render(self):
        return_string = ""
        # TODO this feels quite specific and relies on the input "intermediary" string to be of the correct
        # "format" - more brain power to make this generic will be worthwhile
        match self.data:
            case "func":
                return_string += self.children[0].data + " " + self.children[1].data + "(" + self.children[2].render() + "){" + self.children[3].render() + "}\n"
            case "if":
                return_string += self.data + self.children[0].render() + "{" + self.children[1].render() + "}"
            case "else":
                return_string += self.data + "{" + self.children[0].render() + "}"
            case "return":
                return_string += self.data + " " + self.children[0].data + ";"
            case "include":
                return_string += "#" + self.data + self.children[0].render() + "\n"
            case "none":
                next
            case _:
                # TODO update this to case match syntax - this is currently horrible but does work
                # case data.type if data.type in types works for example but this is also not great
                # rust enums or cpp structs/enums would be a better fit here?
                if self.data in types:
                    return_string += self.data + " " + self.children[0].data
                    if len(self.children) > 1:
                        return_string += "=" + self.children[1].data + ";"
                elif self.data in operators:
                    return_string += "(" + self.children[0].render() + self.data + self.children[1].render() + ")"
                elif self.data in structure_keywords:
                    for c in self.children:
                        return_string += c.render()
                else:
                    if len(self.children) > 0:
                        return_string += self.data + "("
                        for c in self.children:
                            return_string += c.data
                        return_string += ");" 
                    else:
                        return_string += self.data
        return return_string

class tree(object):
    def __init__(self, db):
        # TODO more brain power on this area when not prototyping to get a less messy system
        self.root = node("file")
        current_node = self.root
        buff = ""
        mk_node = False
        in_string = False
        for c in db:
            match c:
                case "(":
                    #create new node and set current node to it
                    if(buff != ""):
                        new_node = node(buff)
                        current_node.add_child(new_node)
                        current_node = new_node
                        mk_node = False
                    if mk_node:
                        new_node = node("body")
                        current_node.add_child(new_node)
                        current_node = new_node
                    mk_node = True
                    buff = ""
                case ")":
                    #exit current node and back to parent of node
                    if(buff != ""):
                        current_node.add_child(node(buff))
                    elif mk_node:
                        current_node.add_child(node("none"))
                    if current_node.parent != None and not mk_node:
                        current_node = current_node.parent
                    buff = ""
                    mk_node = False
                case ".":
                    if not in_string:
                        #add current buffer as a child to current node
                        if(mk_node):
                            new_node = node(buff)
                            current_node.add_child(new_node)
                            current_node = new_node
                            mk_node = False
                        elif(buff != ""):
                            current_node.add_child(node(buff))
                        buff = ""
                    else:
                        buff += c
                case "<":
                    in_string = True
                    buff += c
                case ">":
                    in_string = False
                    buff += c
                case _:
                    buff += c

    def parse_vectors(self):
        return self.root.parse_vectors(False, []) 

    def render(self):
        return self.root.render()

# -------------------------------------- TEMP UTILS --------------------------------------------

# cuts newlines and spaces from the string so
# it may be written in a more human readable form

def process_string(string):
    new_string = string.replace(" ", "")
    return new_string.replace("\n", "")

# makeshift print file to make terminal printing of the resultant
# tree easier to see

def print_tree(p: node, last=True, header=''):
    elbow = "└──"
    pipe = "│  "
    tee = "├──"
    blank = "   "
    print(header + (elbow if last else tee) + "%s" % p.data)
    children = list(p.children)
    for i, c in enumerate(children):
        print_tree(c, header=header + (blank if last else pipe), last=i == len(children) - 1)

# -------------------------------------- EXECUTION --------------------------------------------

from timeit import default_timer as timer
start = timer()

new_tree = tree(process_string(code_string))

if args.v:
    print("input string for generating tree:\n")
    print(process_string(code_string))
    print("\ngenerated tree:\n")
    print_tree(new_tree.root)
    print("\ngenerated code:\n")
    print(new_tree.render())
    for vec in new_tree.parse_vectors():
        print(vec)
else:
    with open("main.c", "w") as file:
        file.write(new_tree.render())
    with open("test_vectors.txt", "w") as file:
        for vec in new_tree.parse_vectors():
            file.write(vec)
            file.write("\n")

end = timer()
print(end-start)

