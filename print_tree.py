"""based on https://github.com/tylerneylon/explacy/blob/master/explacy.py"""

import sys
import re
from collections import defaultdict
import pyconll

def print_table(rows):
    """Pretty-prints the table"""
    col_widths = [max(len(s) for s in col) for col in zip(*rows)]
    fmt = ' '.join('%%-%ds' % width for width in col_widths)
    rows.insert(1, ['─' * width for width in col_widths])
    for row in rows:
        # Uncomment this version to see code points printed out (for debugging).
        # print(list(map(hex, map(ord, list(fmt % tuple(row))))))
        print(fmt % tuple(row))

def _start_end(arrow):
    start = arrow['from']
    end = arrow['to']
    return start, end, min(start, end), max(start, end)

def generate_table(conllu_sentence: str):
    """Generate table with arrows for deps."""
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
        start, end, min_id, max_id = _start_end(arrow)
        for j, other in enumerate(arrows):
            if arrow is other:
                continue
            o_start = other['from']
            o_end = other['to']
            if ((start == o_start and min_id <= o_end <= max_id) or
                (start != o_start and min_id <= o_start <= max_id)):
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
        src, dst, min_id, max_id = _start_end(arrow)
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
        for i in range(min_id + 1, max_id):
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

    could_not_print = num_arrows_left >0 and arrows_with_deps[0] == set()

    arr_chars = {'ew'  : '─',
                 'ns'  : '│',
                 'en'  : '└',
                 'es'  : '┌',
                 'enw' : '┴',
                 'ensw': '┼', 'ens':'┤',
                 'esw' : '┬'}
    # Convert the character lists into strings.
    max_len = max(len(line) for line in lines)
    for i, line in enumerate(lines):
        lines[i] = [arr_chars[''.join(sorted(ch))] if type(ch) is set else ch
                    for ch in line]
        lines[i] = ''.join(reversed(lines[i]))
        lines[i] = ' ' * (max_len - len(lines[i])) + lines[i]

    # Compile full table to print out.
    rows = [['', '', 'deprel', 'form', 'lemma', 'upos', 'xpos', 'feats', 'head']]
    for i, token in enumerate(sentence):
        conllu_token = conllu_sentence[i]
        rows.append([str(i + 1), lines[i], conllu_token.deprel, conllu_token.form,
                     conllu_token.lemma, conllu_token.upos, conllu_token.xpos,
                     "|".join(f"{f}={','.join(conllu_token.feats[f])}" for f in conllu_token.feats),
                     conllu_token.head])
    return (rows, could_not_print)

corpus = pyconll.load_from_file(sys.argv[1])
if len(sys.argv) == 2:
    for tree in corpus:
        printed_tree, non_projective = generate_table(tree)
        if non_projective:
            print(f"{tree.id} is non-projective")
        else:
            print(f"{tree.id}")
        print_table(printed_tree)
else:
    for tree in corpus:
        if re.match(sys.argv[2], tree.id):
            if len(sys.argv) == 4:
                tree_slice = [s for s in tree if "-" not in s.id][0:int(sys.argv[3])]
            else:
                tree_slice = tree
            printed_tree, non_projective = generate_table(tree_slice)
            if non_projective:
                print(f"{tree.id} is non-projective")
            else:
                print(f"{tree.id}")
            print_table(printed_tree)
