import os, sys

# Fail PR if no docs/roadmap/step-XX.md referenced

ref_ok = False
pr_body_path = os.environ.get('PR_BODY_FILE', '')
if pr_body_path and os.path.exists(pr_body_path):
    body = open(pr_body_path, 'r', encoding='ascii', errors='ignore').read()
    if 'Ref: docs/roadmap/step-' in body:
        ref_ok = True
if not ref_ok:
    print('Missing roadmap Ref in PR body')
    sys.exit(1)
print('Roadmap guard OK')
