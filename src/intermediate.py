# Intermediary Format
# [list]
# <structure>
# => return
# (args)
# {body}

# Intemediary Reprisentation Components
# <file>
# <function>
# <scope>
# >

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
