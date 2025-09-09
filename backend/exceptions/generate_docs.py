from backend import exceptions


def create_subtree(tree: dict, version: bool = True) -> dict | None:
    subtree = {}
    for sub_err_name, sub_err_dict in tree.items():
        if sub_err_name == "object":
            continue
        if str(sub_err_dict["object"].internal_code).endswith("0"):
            subtree[sub_err_name] = sub_err_dict
            continue
        elif version:
            subtree[sub_err_name] = sub_err_dict
    return subtree


def create_subtree_2(tree: dict) -> dict | None:
    subtree = {}
    for sub_err_name, sub_err_dict in tree.items():
        if sub_err_name == "object":
            continue
        subtree[sub_err_name] = sub_err_dict
    return subtree


def prepare_table_of_contents(toc: list, tree: dict, level: int = 0) -> None:
    for err_name, value in tree.items():
        lean_err_name = err_name.replace("Error", "")
        err_code_x: str = str(value["object"].internal_code).replace("0", "x")
        indent = "  " * level
        half_1: str = f"[{err_code_x} {lean_err_name} Codes]"
        half_2: str = f"(#{err_code_x}-{lean_err_name.lower()}-codes)"
        toc_point = f"{indent}- {half_1}{half_2}"
        toc.append(toc_point)
        subtree = create_subtree(tree=value, version=False)
        if subtree:
            prepare_table_of_contents(toc=toc, tree=subtree, level=level + 1)


def prepare_codes_description(
    sections: list, tree: dict, level: int = 1
) -> None:
    for err_name, value in tree.items():
        lean_err_name = err_name.replace("Error", "")
        int_err_code: str = str(value["object"].internal_code)
        int_err_code_x: str = int_err_code.replace("0", "x")
        http_err_code: str = str(value["object"].http_code)
        if level == 1:
            header: str = f"## {int_err_code_x} {lean_err_name} Codes"
            sections.append(header)
        indent = "  " * level
        if level == 1:
            tst = (
                f"{indent}- `{int_err_code}` {lean_err_name} Base Code | "
                f"HTTP {http_err_code} | "
                f"[Details](#code-{int_err_code})"
            )
            sections.append(tst)
        subtree = create_subtree(tree=value)
        indent = "  " * (level + 1)
        if subtree and level != 1:
            x = f"{indent}- {'#'*(level+1)} {int_err_code_x} {lean_err_name} Codes"
            sections.append(x)
        else:
            indent = "  " * level
        x = f"{indent}- `{int_err_code}` {lean_err_name} | HTTP {http_err_code} | [Details](#code-{int_err_code})]"
        if level != 1:
            sections.append(x)
        if subtree:
            prepare_codes_description(
                sections=sections,
                tree=subtree,
                level=level + 1,
            )


def prepare_codes_explanation(explanations: list, tree: dict, indent: int = 3):
    for key, err_cls in tree.items():
        if key == "object":
            explanations.append(
                f"{'#' * indent} <a id='code-{err_cls.internal_code}'></a> `{err_cls.internal_code}` {err_cls.__name__}"
            )
            explanations.append(f"General {err_cls.__name__} Base Error.<br>")
            explanations.append(f"_Probable cause: Unexpected and Uncaught base exception_")
        else:
            if isinstance(err_cls, dict) and set(err_cls.keys()) == {"object"}:
                explanations.append(
                    f"{'#' * indent} <a id='code-{err_cls['object'].internal_code}'></a> `{err_cls['object'].internal_code}` {key}"
                )
                explanations.append(f"External message: {err_cls['object'].external_message}<br>")
                explanations.append(
                    f"_Probable cause: {err_cls['object'].internal_message}_"
                )
            else:
                explanations.append(f"{'#' * indent} {key.replace('Error', '')} Codes")
                if isinstance(err_cls, dict):
                    prepare_codes_explanation(
                        explanations=explanations,
                        tree=err_cls,
                        indent=4,
                    )


def build_readme():
    tree = exceptions.BaseCustomError._tree
    toc: list = []
    prepare_table_of_contents(toc=toc, tree=tree)
    sections: list = []
    prepare_codes_description(sections=sections, tree=tree)
    explanations: list = []
    prepare_codes_explanation(explanations=explanations, tree=tree)

    readme = [
        "# Internal Error Code Documentation",
        "",
        "## 📘 Table of Contents",
        "",
        "\n".join(toc),
        "\n",
        "- [📄 Code Explanations](#-code-explanations)",
        "---",
        "\n".join(sections),
        "\n",
        "---",
        "\n",
        "# 📄 Code Explanations",
        "",
        "\n".join(explanations),
    ]

    return "\n".join(readme)


if __name__ == "__main__":
    markdown = build_readme()
    with open("README_internal_codes.md", "w") as f:
        f.write(markdown)
