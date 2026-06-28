#!/usr/bin/env python3
"""Scaffold a new numclassify number type."""
import sys
from pathlib import Path

CATEGORIES = [
    'primes', 'digital', 'divisors', 'sequences',
    'powers', 'number_theory', 'combinatorial', 'recreational', 'exam_types',
]

TEMPLATES = {
    '1': ('digit_power_template', 'For types where n equals sum of digit^k (e.g. Armstrong, Narcissistic)'),
    '2': ('divisor_sum_template', 'For types comparing sum of divisors to n (e.g. Perfect, Abundant)'),
    '3': ('sequence_membership_template', 'For sequence membership types (e.g. Fibonacci, Pell)'),
    '4': ('factorization_template', 'For prime factorization property types (e.g. Squarefree, Powerful)'),
    '5': ('bespoke', 'Write a custom explain function'),
    '0': ('none', 'Skip explain= for now'),
}


def prompt(msg, default=None):
    suffix = f" [{default}]" if default else ""
    val = input(f"{msg}{suffix}: ").strip()
    return val if val else default


def main():
    print("\n=== numclassify type scaffolder ===\n")

    name = prompt("Type name (e.g. 'Lucky Number')")
    if not name:
        print("Name required. Exiting.")
        sys.exit(1)

    print(f"\nCategories: {', '.join(CATEGORIES)}")
    category = prompt("Category")

    oeis = prompt("OEIS ID (e.g. A000040, or leave blank)", default="")
    description = prompt("One-line description")
    aliases_raw = prompt("Aliases (comma-separated, or blank)", default="")
    aliases = [a.strip() for a in aliases_raw.split(',') if a.strip()]

    print("\nExplain template:")
    for k, (t, desc) in TEMPLATES.items():
        print(f"  {k}: {t} -- {desc}")
    tmpl_choice = prompt("Choose template", default="0")
    tmpl_name, _ = TEMPLATES.get(tmpl_choice, ('none', ''))

    func_name = "is_" + name.lower().replace(" ", "_").replace("-", "_")
    norm_name = name.lower().replace(" ", "_").replace("-", "_")

    lines = []

    if tmpl_name == 'bespoke':
        lines.append(f"def _explain_{norm_name}(n: int) -> str:")
        lines.append(f'    # TODO: implement explanation for {name}')
        lines.append(f'    result = {func_name}(n)')
        lines.append(f'    return f"{{n}}: {{\'YES\' if result else \'NO\'}}"')
        lines.append("")
    elif tmpl_name == 'digit_power_template':
        lines.append(f"# from numclassify._explain_templates import digit_power_template")
        lines.append(f"_explain_{norm_name} = digit_power_template(")
        lines.append(f"    lambda d: d**3,  # TODO: replace with correct power function")
        lines.append(f'    "3",  # TODO: label')
        lines.append(f")")
        lines.append("")
    elif tmpl_name == 'divisor_sum_template':
        lines.append(f"# from numclassify._explain_templates import divisor_sum_template")
        lines.append(f'_explain_{norm_name} = divisor_sum_template("equal")  # TODO: "equal"/"greater"/"less"')
        lines.append("")
    elif tmpl_name == 'sequence_membership_template':
        lines.append(f"# from numclassify._explain_templates import sequence_membership_template")
        lines.append(f"def _{norm_name}_up_to(n):")
        lines.append(f"    # TODO: generate {name} sequence up to n")
        lines.append(f'    seq = [0, 1]')
        lines.append(f"    while seq[-1] < n: seq.append(seq[-1] + seq[-2])")
        lines.append(f"    return seq")
        lines.append(f"_explain_{norm_name} = sequence_membership_template(_{norm_name}_up_to, '{name}')")
        lines.append("")
    elif tmpl_name == 'factorization_template':
        lines.append(f"# from numclassify._explain_templates import factorization_template")
        lines.append(f"_explain_{norm_name} = factorization_template(")
        lines.append(f"    lambda f: True,  # TODO: condition on factor list")
        lines.append(f'    "TODO: condition description",')
        lines.append(f"    show_exponents=True,")
        lines.append(f")")
        lines.append("")

    aliases_repr = repr(aliases) if aliases else "[]"
    explain_line = f'    explain=_explain_{norm_name},' if tmpl_name not in ('none',) else '    # explain=None,  # add later'

    lines.append("@register(")
    lines.append(f'    name="{name}",')
    lines.append(f'    category="{category}",')
    if oeis:
        lines.append(f'    oeis="{oeis}",')
    lines.append(f'    description="{description}",')
    if aliases:
        lines.append(f'    aliases={aliases_repr},')
    lines.append(f'{explain_line}')
    lines.append(")")
    lines.append(f"def {func_name}(n: int) -> bool:")
    lines.append(f'    """Return True if n is a {name}."""')
    lines.append(f"    # TODO: implement")
    lines.append(f"    raise NotImplementedError")

    output = "\n".join(lines)
    print(f"\n{'='*60}")
    print("Paste this into the appropriate _core/*.py file:")
    print(f"{'='*60}\n")
    print(output)
    print(f"\n{'='*60}")

    out_path = Path("tools/_scaffold_output.py")
    out_path.write_text(output, encoding='utf-8')
    print(f"\nAlso written to: {out_path}")


if __name__ == "__main__":
    main()
