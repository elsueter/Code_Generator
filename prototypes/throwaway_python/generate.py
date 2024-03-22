# Python 3

# Full version would load a spec file for the generation.
# Here we just hard-code a data structure.

# Findings from this throwaway prototype:
# * A DSL is a must, these are unwieldy structures
# * Some kind of debug output for the internal structure will be essential
# * The end result of the initial build will be some kind of tree, you'll need a way
#   to say to the search, what it's allowed to change and where e.g. add another
#   statement, replace an expr with another of the same type (bigger, smaller size
#   expr), remove a statement, move something from one file to a separate included
#   file, turn a statement into a function call to a function that does that thing,
#   inline a function call, etc etc
# * I've not looked at how you might embed information to help calculate the
#   corresponding test cases to run on the code to achieve whatever you want to
#   achieve.
# * We probably want to have small pre-defined builds that you can combine, similar
#   with finds. Needs to be part of the DSL. We might need to run multiple finds
#   in sequence eventually. Or even in parallel?
# * We definitely want to be able to turn the results from a "find" into a "build"
#   so it would be best if internally everything turns into a build spec that
#   we can apply.
# * We could do with some "where this came from" information, perhaps even to be
#   able to round-trip an edit of the output into a change to the build spec.
# * There are optional things like expression parens, component naming,
#   whitespace layout, single-statement block that aren't directly functional but 
#   can affect how we parse or instrument. So we'll need to be able to control,
#   search, or fuzz those areas.
gen_spec={
    "build": [],
    "find": [],
}

structdb = {
    "declare_variable": {
            "params": [
                { "name": "vartype", "type": "type" },
                { "name": "varname", "type": "identifier" },
                { "name": "varinit", "type": "expr" },
            ],
            "content": [
                { "type": "varinst", "var": "vartype" },
                " ",
                { "type": "varinst", "var": "varname" },
                " = ",
                { "type": "varinst", "var": "varinit" },
                ";"
            ],
            "provides": {
                "type": "statement",
                "declaration": {
                    "type": "var",
                    "vartype":
                        { "type": "varinst", "var": "vartype" },
                    "varname":
                    { "name": "varname", "type": "identifier" },
                }
            },
        },
    "cast_init": {
            "params": [
                { "name": "vartype", "type": "type" },
                { "name": "varinit", "type": "expr" },
            ],
            "content": [
                "(",
                { "type": "varinst", "var": "vartype" },
                ")",
                { "type": "varinst", "var": "varinit" },
            ],
        },
    }

def instantiate(spec):
    built=""
    tn=spec["template_name"]
    t=structdb[tn]
    for part in t["content"]:
        resolved_part=None
        if isinstance(part, dict):
            n=part["var"]
            resolved_part=spec["params"][n]
        else:
            resolved_part=part
        if isinstance(resolved_part, dict):
            resolved_part=instantiate(resolved_part) # note: you'll probably need to capture and pass parameters through from layer to layer?
        built+=resolved_part
    return built

def create_initial_model(spec):
    b=spec["build"]
    model={
            "files": [
                ],
            "info": []
    }

    model["files"].append( main :=
            {
                "name": "main.c",
                "content": []
            }
    )

    initializer = "int x = 0;"

# note: currently this makes a string to feed forward, but eventually we'll keep it "live"
# until we generate the final output. This lets us use the characterizing data to run
# searches for extra things.

    initializer_1 = instantiate(
            {
                "type": "template",
                "template_name": "declare_variable",
                "params":
                {
                    "vartype": "int",
                    "varname": "y",
                    "varinit": "200",
                }
            }
            )
    initializer_2 = instantiate(
            {
                "type": "template",
                "template_name": "declare_variable",
                "params":
                {
                    "vartype": "char *",
                    "varname": "x",
                    "varinit": {
                        "type": "template",
                        "template_name": "cast_init",
                        "params": {
                            "vartype": "char *",
                            "varinit": "0",
                        }
                    }
                }
            }
            )

    main["content"].append(
            {
                "tags": [ "statement", "declaration", "definition" ],
                "role": [ "statement" ],
                "node": "leaf",
                "provides": [],
                "text": initializer_1,
            }
    )
    main["content"].append(
            {
                "tags": [ "statement", "declaration", "definition" ],
                "role": [ "statement" ],
                "node": "leaf",
                "provides": [],
                "text": initializer_2,
            }
    )
    main["content"].append(
            {
                "tags": [ "subprogram", "declaration", "definition" ],
                "role": [ "subprogram" ],
                "node": "node",
                "provides": [],
                "content": [
                    "int main(void) { return 0; }"
                ]
            }
    )
    return model

def extend_model(model, spec):
    pass

def write_model_file_content(handle, model, structure):
    for c in structure:
        if "content" in c:
            for part in c["content"]:
                handle.write(part)
        else:
            handle.write(c["text"])

def write_model(model):
    for file in model["files"]:
        with open(file["name"], "w") as ofh:
            write_model_file_content(ofh, model, file["content"])


def get_diagnostic(model):
    return "0 OK; 0:1"

# Start with the imperative part first.

model=create_initial_model(gen_spec)

# Then extend it to meet the search criteria. Use blackboard architecture?

extend_model(model, gen_spec)

# Now write the model

write_model(model)

# We might want to write some debug as well

diag=get_diagnostic(model)
print(diag)
