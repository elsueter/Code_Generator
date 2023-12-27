import tomllib

# Basic Types
#   Integer Types
#       character
#       int (signed/unsignes)
#       enumerated
#   Floating Types
#       real floating
#       complex
# Derived Types
#   array
#   union
#   function
#   pointer

with open("data/types.toml", "rb") as f:
    data = tomllib.load(f)
    print(data['char']['type'])

# Intemediary Reprisentation
