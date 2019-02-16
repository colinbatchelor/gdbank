from acainn import Features

f = Features()

def unify(lhs,rhs):
  lhsurf = lhs[0]
  lhpos = lhs[1]
  rhsurf = rhs[0]
  rhpos = rhs[1]
  lh_feats = f.feats(lhsurf, lhpos)
  rh_feats = f.feats(rhsurf, rhpos)
  result = {}
  obligatory = ["Gender","Number"]
  for feat in obligatory:
    if lh_feats[feat] == rh_feats[feat]: result[feat] = lh_feats[feat]
    else: return False
  optional = ["Case"]
  for feat in optional:
    if feat in lh_feats:
      if lh_feats[feat] == rh_feats[feat]: result[feat] = lh_feats[feat]
      else: return False
    elif feat in rh_feats:
      result[feat] = rh_feats[feat]
  return result

