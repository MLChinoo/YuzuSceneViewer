import json
import re

def scnchartdata_tjs_to_json(src: str) -> str:
    src_no_comment = re.sub(r'//.*', '', src)

    tmp = (src_no_comment
           .replace('(const) %[', '{')
           .replace('(const) [', '[')
           .replace('=>', ':'))

    out = []
    stack = []

    i = 0
    in_str = False

    while i < len(tmp):
        ch = tmp[i]

        if ch == '"':
            in_str = not in_str
            out.append(ch)
            i += 1
            continue

        if not in_str and tmp.startswith('void', i):
            before = tmp[i - 1] if i > 0 else ' '
            after = tmp[i + 4] if i + 4 < len(tmp) else ' '
            if not before.isalnum() and not after.isalnum() and after != '_':
                out.append('null')
                i += 4
                continue

        if ch == '{':
            stack.append('object')
            out.append('{')
            i += 1

        elif ch == '[':
            stack.append('array')
            out.append('[')
            i += 1

        elif ch == ']':
            if not stack:
                raise ValueError('Unmatched ] at pos %d' % i)
            t = stack.pop()
            out.append('}' if t == 'object' else ']')
            i += 1

        else:
            out.append(ch)
            i += 1

    if stack:
        raise ValueError('Unclosed bracket(s): %s' % stack)

    json_text = ''.join(out)
    return json_text


if __name__ == "__main__":
    with open(r"C:\Users\MLChinoo\Desktop\senren_dumps\data\main\scnchartdata.tjs", mode="r", encoding="UTF-16") as file:
        raw = file.read()
    converted = scnchartdata_tjs_to_json(raw)
    # print(converted)
    test = json.loads(converted)
    pass
    print(f"var flags = {json.dumps(test["flags"])};")