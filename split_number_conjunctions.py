import sys
from udapi.core.document import Document

document = Document(filename = sys.argv[1])
for b in document.bundles:
    root = b.get_tree()
    nodes = root.descendants
    for node in nodes:
        if node.form in ["sa", "'sa"] and node.xpos == "Cc":
            print(root.sent_id)
            mwt_form = node.form
            mwt_misc = node.misc.copy()
            node.form = "agus"
            node.lemma = "agus"
            node.misc = {}
            particle_node = node.create_child()
            particle_node.shift_after_node(node)
            particle_node.misc["SpaceAfter"] = node.misc["SpaceAfter"]
            particle_node.upos = "PART"
            particle_node.xpos = "Uo"
            particle_node.parent = node.parent
            particle_node.deprel = "mark:prt"
            particle_node.form = "a"
            particle_node.lemma = "a"
            particle_node.feats["PartType"] = "Num"
            nodes = [node, particle_node]
            node.root.create_multiword_token(nodes, mwt_form, mwt_misc)
document.store_conllu(sys.argv[2])
