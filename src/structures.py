import tomllib

#Basic Types
#   Integer Types
#       character
#       int (signed/unsignes)
#       enumerated
#   Floating Types
#       real floating
#       complex
#Derived Types
#   array
#   union
#   function
#   pointer

class type:
    def __init__(self) -> None:
        pass


with open("data/types.toml", "rb") as f:
    data = tomllib.load(f)
    print(data['char']['type'])
