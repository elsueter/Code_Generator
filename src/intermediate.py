# Intermediary Format
# [list]
# <structure>
# => return
# (args)
# {body}

# Intemediary structures
# <file> -> source file
# <function> -> function declaration or reference
# <scope> -> a scope attached to another structure
# <statement> -> generic structure for any line of code
# <expression> -> any code that resolves to a value
# <operator> -> any defined mathematical or logical operator
# <value> -> strucute to hold any given value (variable)
# <cf> -> control flow structures
# <pproc> -> pre-processor instructions
#
# <file> -> <pproc>, <function>, <scope>, <statement>
# <function>([<value>]) => [<value>] -> <scope>
# <scope> -> <scope>, <statement>, <cf>, 

# Example C Function
# int get_largest(int x, int y){
#   if(x > y){
#       return x;
#   }
#   return y;
# }
#
# <function>([<value>]) => <value> {
#   <operator>(
#       <expression(
#           [
#               [<value>],
#               <operator>,
#               [<value>]
#           ],
#           <operator>
#           ))
#           {
#               <statement>
#           }
#   <statement>
#}

# digit          : 0-9
# digit_list     : <digit_list> <digit> | <digit>
# letter         : a-z | A-Z
# otherChar      : |!”%&/()=+-*#><;,^.][\n \t
# character      : <digit> | <letter> | <otherChar>
# character_list : <character_list> <character> | <character>
#
# int            : <sign> <digit_list>
# char           : <character_list>
# float          : <sign> <digit_list> . <digit_list> f
#
# type           : <int>
#                | <char>
#                | <float>
#                | <double>
#
# typeSpec       : int
#                | char
#                | float
#                | double
#                | void
