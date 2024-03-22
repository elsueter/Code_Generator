# Imports

import argparse, tree_structure as tree
parser=argparse.ArgumentParser(description="sample argument parser")
parser.add_argument('-v', action='store_true')
args = parser.parse_args()

# -------------------------------------- EXECUTION --------------------------------------------

from timeit import default_timer as timer
start = timer()

tree_string = """
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

new_tree = tree.tree(tree.process_string(tree_string))

if args.v:
    print("input string for generating tree:\n")
    print(tree.process_string(tree_string))
    print("\ngenerated tree:\n")
    tree.print_tree(new_tree.root)
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

