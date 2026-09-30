# OPS 5.12 check of an ops-file edit: prints the changed line ranges, then confirms that every removed line reappears somewhere in the new file (catches moved blocks) and lists genuinely new lines. Run: python3 opscheck.py old.md new.md. Get the old file's EXACT bytes from Drive with download_file_content (read_file_content returns converted text).
import sys, difflib, collections
a = open(sys.argv[1], encoding='utf-8').read().split('\n'); b = open(sys.argv[2], encoding='utf-8').read().split('\n')
rem, add = [], []
for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
    if op != 'equal':
        print(op, f'old {i1+1}-{i2}', f'new {j1+1}-{j2}')
        rem += a[i1:i2]; add += b[j1:j2]
cr, ca = collections.Counter(rem), collections.Counter(add)
print('removed lines not re-added:', [(k[:100], v) for k, v in (cr - ca).items()])
for k, v in (ca - cr).items():
    if k.strip(): print('NEW', v, '|', k[:200])
