#!/usr/bin/env python3
"""Reject stale visual-review receipts after an asset or inline diagram changes."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1];P=R/'reports/edition-v2/figure-visual-review.json'
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
 review=json.loads(P.read_text());errors=[];cache={}
 for row in review['figures']:
  p=R/row['source']
  if row['kind']=='inline-tikz':
   if p not in cache:cache[p]={digest(re.sub(r'\s+',' ',b).encode()) for b in re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',p.read_text(),re.S)}
   okay=row['sha256'] in cache[p]
   for occurrence in row['occurrences']:
    q=R/occurrence['file']
    if q not in cache:cache[q]={digest(re.sub(r'\s+',' ',b).encode()) for b in re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',q.read_text(),re.S)}
    okay &= row['sha256'] in cache[q]
  else:okay=p.exists() and digest(p.read_bytes())==row['sha256']
  if not okay:errors.append(row['id'])
 report=dict(status='PASSED' if not errors else 'FAILED',reviewed_figures=len(review['figures']),stale_reviews=errors,scope='Source and asset identity of author visual-review receipts. Passing does not perform a new visual inspection or confer independent scientific approval.')
 (R/'reports/edition-v2/figure-review-checks.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],report['reviewed_figures'],'figure review receipts;',len(errors),'stale')
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
