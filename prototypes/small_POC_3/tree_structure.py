# -------------------------------------- TREE --------------------------------------------

structure_keywords = {"int", "body", "params", "if", "else", "func", "file"}
conditionals = {"if"}
operators = {"||", "&&"}
types = {"int"}


# temp function to create the sub-node types dynamically. This function is only called
# during the creation of the tree - the case/match/if combination is a bit of a mess
# due to using some dicts for matching which does cut down the overall size of this...
# lots of repitition in here but at least it follows KISS - improvements to come
def node_factory(node_name):
    match node_name:
        case "func":
            return func_node(node_name)
        case "if":
            return if_node(node_name)
        case "else":
            return else_node(node_name)
        case "return":
            return return_node(node_name)
        case "include":
            return include_node(node_name)
        case "none":
            next
        case _:
            if node_name in types:
                return type_node(node_name)
            elif node_name in operators:
                return operator_node(node_name)
            elif node_name in structure_keywords:
                return structure_node(node_name)
    return node(node_name)

# subsets of node classes
class node:
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
        else:
            for c in self.children:
                test_vectors = []
                return_arr += c.parse_vectors(in_conditional, [])
        return return_arr

    def render(self):
        return_string = ""
        if len(self.children) > 0:
            return_string += self.data + "("
            for c in self.children:
                return_string += c.data
            return_string += ");" 
        else:
            return_string += self.data
        return return_string

# ---- Sub_Nodes ----
# these sub classes are mainly split out for the sake of "rendering" the code.
# at this current point it is just generating C code but could be allowed to generate
# other languages - though the structures are very C - like in mapping even at this
# abstraction level so this may not be possible for some Ada features or other languages

class func_node(node):
    def render(self):
        return self.children[0].data + " " + self.children[1].data + "(" + self.children[2].render() + "){" + self.children[3].render() + "}\n"

# split out the parse_vectors into a sub node with sub-classes to make the vector parsing
# recursive base case cleaner
class conditional_node(node):
    def parse_vectors(self, in_conditional, test_vectors):
        return_arr = [];
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
        return return_arr

class if_node(conditional_node):
    def render(self):
        return self.data + self.children[0].render() + "{" + self.children[1].render() + "}"

class else_node(node):
    def render(self):
        return self.data + "{" + self.children[0].render() + "}"

class return_node(node):
    def render(self):
        return self.data + " " + self.children[0].data + ";"

class include_node(node):
    def render(self):
        return "#" + self.data + self.children[0].render() + "\n"

class type_node(node):
    def render(self):
        return_string = self.data + " " + self.children[0].data
        if len(self.children) > 1:
            return_string += "=" + self.children[1].data + ";"
        return return_string

class operator_node(node):
    def render(self):
        return "(" + self.children[0].render() + self.data + self.children[1].render() + ")"

class structure_node(node):
    def render(self):
        return_string = ""
        for c in self.children:
            return_string += c.render()
        return return_string

# ---- Tree ----

class tree(object):
    def __init__(self, db):
        # TODO more brain power on this area when not prototyping to get a less messy system
        self.root = node_factory("file")
        current_node = self.root
        buff = ""
        mk_node = False
        in_string = False
        for c in db:
            match c:
                case "(":
                    #create new node and set current node to it
                    if(buff != ""):
                        new_node = node_factory(buff)
                        current_node.add_child(new_node)
                        current_node = new_node
                        mk_node = False
                    if mk_node:
                        new_node = node_factory("body")
                        current_node.add_child(new_node)
                        current_node = new_node
                    mk_node = True
                    buff = ""
                case ")":
                    #exit current node and back to parent of node
                    if(buff != ""):
                        current_node.add_child(node_factory(buff))
                    elif mk_node:
                        current_node.add_child(node_factory("none"))
                    if current_node.parent != None and not mk_node:
                        current_node = current_node.parent
                    buff = ""
                    mk_node = False
                case ".":
                    if not in_string:
                        #add current buffer as a child to current node
                        if(mk_node):
                            new_node = node_factory(buff)
                            current_node.add_child(new_node)
                            current_node = new_node
                            mk_node = False
                        elif(buff != ""):
                            current_node.add_child(node_factory(buff))
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


# -------------------------------------- Tree Intermediary Reprisentation --------------------------------------------

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
# here this tree is not sticking to the <cons> <atom> style
# of s-exp like in lisp. here () denotes going deeper into
# the tree and . is adding a node at the same level.
# this has been done to allow a rose tree to be described
#
# nl on "." where a <cons> cell has 2nd item for complex obj
# maintain "()" for empty value -> returns "NIL"
# if brackets are opened for specifically not a scope or body
# the first element "names" the node
#
# ( <label> . <node> . <node> . ( <node> ) )
#
# Example tree string:
# """
# ( 
#     include . <stdio.h>
# ) .
# (
#     func . int . test_func . 
#     (
#         int . a
#     ) .
#     (
#         (
#             int . x . 0
#         )
#         (
#             int . y . 0
#         )
#         (
#             if . ( || . ( && . x . y ) . a ) .
#             (
#                 return . (1)
#             )
#         )
#         (
#             else .
#             (
#                 printf("a:%i", a)
#             )
#         )
#         (
#             return . (0)
#         )
#     )
# ) .
# (
#     func . int . main . () .
#     (
#         test_func( 0 )
#     )
# )"""
#
# This intermediary reprisentation here is very simple but just matches 1:1 with a tree
# 

# -------------------------------------- TEMP UTILS --------------------------------------------

# cuts newlines and spaces from the string so
# it may be written in a more human readable form

def process_string(string):
    new_string = string.replace(" ", "")
    return new_string.replace("\n", "")

# makeshift print tree to make terminal printing of the resultant
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


