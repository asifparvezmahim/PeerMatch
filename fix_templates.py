import re

files = [
    r"e:\My Django Project\Research Partner\research_platform\peermatch\core\templates\idea_form.html",
    r"e:\My Django Project\Research Partner\research_platform\peermatch\core\templates\edit_profile.html",
    r"e:\My Django Project\Research Partner\research_platform\peermatch\core\templates\researchers.html",
]

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Fix all cases of ==variablename without spaces (e.g. ==f, ==field)
    fixed = re.sub(r'==(\w)', r'== \1', content)
    # Also fix variablename== without spaces (e.g. field==)
    fixed = re.sub(r'(\w)==', r'\1 ==', fixed)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(fixed)

    # Verify
    with open(path, 'r', encoding='utf-8') as f:
        verify = f.read()

    remaining = re.findall(r'\w==\w', verify)
    if remaining:
        print(f"STILL HAS ISSUES in {path}: {remaining}")
    else:
        print(f"FIXED OK: {path}")
