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

# digit             : 0-9
# digit_list        : <digit_list> <digit> | <digit>
# letter            : a-z | A-Z
# other_char        : |!”%&/()=+-*#><;,^.][\n \t
# character         : <digit> | <letter> | <otherChar>
# character_list    : <character_list> <character> | <character>
# sign              : + | - | <none>
#
# type_specifier    : int
#                   | char
#                   | float
#                   | void
#
# int               : <sign> <digit_list>
# char              : <character_list>
# float             : <sign> <digit_list> . <digit_list> f
#
# type              : <int>
#                   | <char>
#                   | <float>
#
# definition        : <type_specificer> <type>
#
# stmt              : <definition>
# stmt_list         : <stmt_list> <stmt> | <stmt>
#
# exp               :
# exp_list          : <exp_list> <exp> | <exp>
#
# brackets          : ( <exp_list> | <stmt_list> )
# braces            : { <exp_list> | <stmt_list> }
#
# if                : if <brackets <exp_list> > <braces <stmt_list> >
