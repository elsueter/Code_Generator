from collections import OrderedDict

# A quick working example demonstratinc MC/DC coverage expectations on a function call in a condition in C

# Example C code:
#
# int main()
# {
#   int x = 1;
#   int y = 0;
#
#   if( x || Y )
#   {
#       return 1;
#   }
#   else
#   {
#       return 2;
#   }
#   return 0;
# }
#
# broken down into an intermediate form (WIP):
# <func_def
#   [main]
#       {
#           <var_def [x] {1}>
#           <var_def [y] {1}>
#
#           < if [0] ( <or_op [0] (x, y) > )
#               {
#                   <return [0] {1}>
#               }
#           >
#           < else [0]
#               {
#                   <return [1] {2}>
#               }
#           >
#           <return [2] {0}>
#       }
# >
#
# where:
# <> is a defined type
# [] is the tag for the type
# () is the input (parameters) for the type
# {} anything 'within' or returned by the type


# example "DB" of data above once parsed. This is just being used as an example
# in real use cases a tree structure that is far less verbose would be faster
db = {
    "main":
    {
        "type": "func_def",
        "body": 
        [
            "x",
            "y",
            "if_0",
            "else_0",
            "return_2"
        ],
    },
    "x":
    {
        "type": "var_def",
        "body": 
        [
            "1"
        ]
    },
    "y":
    {
        "type": "var_def",
        "body": 
        [
            "0"
        ]
    },
    "if_0":
    {
        "type": "if",
        "params": 
        [
            "or_op_0"
        ],
        "body": 
        [
            "return_0"
        ]
    },
    "else_0": 
    {
        "type": "else",
        "body": 
        [
            "return_1"
        ]
    },
    "or_op_0": 
    {
        "type": "or_op",
        "params":
        [
            "x",
            "y"
        ],
        "body": 
        [
            "return_2"
        ]
    },
    "return_0": 
    {
        "type": "return",
        "body": 
        [
            "1"
        ]
    },
    "return_1": 
    {
        "type": "return",
        "body": 
        [
            "2"
        ]
    },
    "return_2": 
    {
        "type": "return",
        "body": 
        [
            "0"
        ]
    },
}

# parsing the above to translate into a tree structure (using a dict with keys - not ideal...)
# rust enums are nice for this use case - or c/cpp?

tree = {}

class node:
    def __init__( self, kind, tag, params, parent, children):
        self.kind = kind
        self.tag = tag
        self.params = params
        self.parent = parent
        self.children = children

    def __init__( self, string, tag ):
        self.kind = ""
        self.tag = tag
        self.params = ""
        self.parent = ""
        self.children = ""
        for item in string:
            if item == "type":
                self.kind = string[item]
            elif item == "params":
                self.params = string[item]
            elif item == "body":
                self.children = string[item]

    def prnt( self ):
        print((self.children))


    # TODO this is all very rough and a bit fudget currently.
    # this will take any parameter from an or statement and declare it needs to
    # be set to true/false and that any given return statement must be hit.
    # It should be doable to derrive if a return is hit given a statement with the
    # current data (I think...) but this is not implemented
    def calc_MCDC(self):
        ret_val = "";
        
        if self.kind == "if":
            for param in self.params:
                ret_val += tree[param].calc_MCDC()
        elif self.kind == "or_op":
            for parameter in self.params:
                ret_val += "Parameter: " + parameter + " is true or false\n"
            return ret_val
        elif self.kind == "return":
            ret_val += "Parameter: " + self.tag + " is reached\n"
            return ret_val

        for child in self.children:
            if not child.isnumeric():
                ret_val += tree[child].calc_MCDC()

        return ret_val

    # TODO improve this and pass more data through so the current "node" knows more
    # about the state of the current part of the program in relation to its parent.

    def render(self):
        program_string = ""

        if self.kind == "func_def":
            program_string += "int " + self.tag + "(" + self.params + ") {\n"
        elif self.kind == "var_def":
            program_string += "int " + self.tag + " = " + self.children[0] + ";\n"
            return program_string
        elif self.kind == "if":
            program_string += "if("
            for param in self.params:
                program_string += tree[param].render()
            program_string += ")"
            program_string += "{\n"
            for child in self.children:
                program_string += tree[child].render()
            program_string += "}"
            return program_string
        elif self.kind == "else":
            program_string += "else{\n"
            for child in self.children:
                program_string += tree[child].render()
            program_string += "}\n"
            return program_string
        elif self.kind == "or_op":
            for param in self.params:
                program_string += param
                program_string += "||"
            program_string = program_string[:-2]
            return program_string
        elif self.kind == "return":
            program_string += "return " + self.children[0] + ";\n"
            return program_string

        for child in self.children:
            if not child.isnumeric():
                program_string += tree[child].render()

        if self.kind == "func_def":
            program_string += "}\n"

        return program_string

for item in db:
    tree[item] = node(db[item], item)

#for node in tree:
#    tree[node].prnt()

print(tree["main"].calc_MCDC())
print(tree["main"].render())
