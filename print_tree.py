import sys
import pyconll
import pprint
import re
from collections import defaultdict

# based on https://github.com/tylerneylon/explacy/blob/master/explacy.py

def _print_table(rows):
    col_widths = [max(len(s) for s in col) for col in zip(*rows)]
    fmt = ' '.join('%%-%ds' % width for width in col_widths)
    rows.insert(1, ['─' * width for width in col_widths])
    for row in rows:
        # Uncomment this version to see code points printed out (for debugging).
        # print(list(map(hex, map(ord, list(fmt % tuple(row))))))
        print(fmt % tuple(row))

def _start_end(arrow):
    start, end = arrow['from'], arrow['to']
    mn = min(start, end)
    mx = max(start, end)
    return start, end, mn, mx

def print_tree(conllu_sentence: str):
    _do_print_debug_info = False
    sentence = {}
    conllu_sentence = [token for token in conllu_sentence if not token.is_multiword()]
    for token in conllu_sentence:
        if token.head != '0':
            if int(token.head) - 1 in sentence:
                sentence[int(token.head) - 1].append((int(token.id) - 1, token.deprel))
            else:
                sentence[int(token.head) - 1] = [(int(token.id) - 1, token.deprel)]
    for i in range(0, len(conllu_sentence)):
        if i not in sentence:
            sentence[i] = []
    arrows = [{'from': src, 'to': dst[0],
               'underset': set()}
              for src in sentence
              for dst in sentence[src]]
    arrows_with_deps = defaultdict(set)
    for i, arrow in enumerate(arrows):
        if _do_print_debug_info:
            print('Arrow %d: "%s" -> "%s"' % (i, arrow['from'], arrow['to']))
        num_deps = 0
        start, end, mn, mx = _start_end(arrow)
        for j, other in enumerate(arrows):
            if arrow is other:
                continue
            o_start, o_end, o_mn, o_mx = _start_end(other)
            if ((start == o_start and mn <= o_end <= mx) or
                (start != o_start and mn <= o_start <= mx)):
                num_deps += 1
                if _do_print_debug_info:
                    print('%d is over %d' % (i, j))
                arrow['underset'].add(j)
        arrow['num_deps_left'] = arrow['num_deps'] = num_deps
        arrows_with_deps[num_deps].add(i)
    lines = [[] for token in sentence]
    lines.append([])
    num_arrows_left = len(arrows)

    while num_arrows_left > 0 and arrows_with_deps[0] != set():

        assert len(arrows_with_deps[0])
        arrow_index = arrows_with_deps[0].pop()
        arrow = arrows[arrow_index]
        src, dst, mn, mx = _start_end(arrow)
        height = 3
        if arrow['underset']:
            height = max(arrows[i]['height'] for i in arrow['underset']) + 1
        height = max(height, 3, len(lines[dst]) + 3)
        arrow['height'] = height
        if _do_print_debug_info:
            print('')
            print('Rendering arrow %d: "%s" -> "%s"' % (arrow_index,
                                                        arrow['from'],
                                                        arrow['to']))
            print('  height = %d' % height)
        goes_up = src > dst
        if lines[src] and len(lines[src]) < height:
            lines[src][-1].add('w')
        while len(lines[src]) < height - 1:
            lines[src].append(set(['e', 'w']))
        if len(lines[src]) < height:
            lines[src].append({'e'})
        lines[src][height - 1].add('n' if goes_up else 's')
        # Draw the incoming dst line.
        lines[dst].append(u'►')
        while len(lines[dst]) < height:
            lines[dst].append(set(['e', 'w']))
        lines[dst][-1] = set(['e', 's']) if goes_up else set(['e', 'n'])

        # Draw the adjoining vertical line.
        for i in range(mn + 1, mx):
            while len(lines[i]) < height - 1:
                lines[i].append(' ')
            lines[i].append(set(['n', 's']))

        # Update arrows_with_deps.
        for arr_i, arr in enumerate(arrows):
            if arrow_index in arr['underset']:
                arrows_with_deps[arr['num_deps_left']].remove(arr_i)
                arr['num_deps_left'] -= 1
                arrows_with_deps[arr['num_deps_left']].add(arr_i)
        # at end of loop
        num_arrows_left -= 1
    if num_arrows_left >0 and arrows_with_deps[0] == set():
        non_projective = True
    else:
        non_projective = False

    arr_chars = {'ew'  : '─',
                 'ns'  : '│',
                 'en'  : '└',
                 'es'  : '┌',
                 'enw' : '┴',
                 'ensw': '┼', 'ens':'┤',
                 'esw' : '┬'}
    # Convert the character lists into strings.
    max_len = max(len(line) for line in lines)
    for i in range(len(lines)):
        lines[i] = [arr_chars[''.join(sorted(ch))] if type(ch) is set else ch
                    for ch in lines[i]]
        lines[i] = ''.join(reversed(lines[i]))
        lines[i] = ' ' * (max_len - len(lines[i])) + lines[i]

    # Compile full table to print out.
    rows = [['', '', 'deprel', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head']]
    for i, token in enumerate(sentence):
        ct = conllu_sentence[i]
        rows.append([str(i + 1), lines[i], ct.deprel, ct.form, ct.lemma, ct.upos, ct.xpos, "|".join(f"{f}={','.join(ct.feats[f])}" for f in ct.feats), ct.head])
    return (rows, non_projective)

corpus = pyconll.load_from_file(sys.argv[1])
if len(sys.argv) == 2:
    for sentence in corpus:
        tree, non_projective = print_tree(sentence)
        if non_projective:
            print(f"{sentence.id} is non-projective")
        else:
            print(f"{sentence.id}")
        _print_table(tree)
else:
    for sentence in corpus:
        if re.match(sys.argv[2], sentence.id):
            if len(sys.argv) == 4:
                slice = sentence[0:int(sys.argv[3])]
            else:
                slice = sentence
            tree, non_projective = print_tree(slice)
            if non_projective:
                print(f"{sentence.id} is non-projective")
            else:
                print(f"{sentence.id}")
            _print_table(tree)
            
            
