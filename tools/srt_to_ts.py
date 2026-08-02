import re
import sys

def parse_srt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'\n\n+', content.strip())
    out = []
    
    def time_to_sec(tstr):
        h, m, s = tstr.split(':')
        s, ms = s.split(',')
        return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000.0

    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            id_ = lines[0]
            times = lines[1].split(' --> ')
            start = time_to_sec(times[0])
            end = time_to_sec(times[1])
            text = ' '.join(lines[2:]).replace('"', '\\"')
            out.append(f'    {{ id: {id_}, start: {start:.3f}, end: {end:.3f}, text: "{text}" }},')
    
    return '\n'.join(out)

print(parse_srt(sys.argv[1]))
