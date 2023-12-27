import os, sys
path = os.path.abspath("src")
sys.path.append(path)

import structures

# Intermediary Format
# [list]
# <structure>
# => return
# (args)
# {body}

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
