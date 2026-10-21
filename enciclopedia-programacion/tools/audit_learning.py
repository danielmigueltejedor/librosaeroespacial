#!/usr/bin/env python3
"""Whole-corpus pedagogical inventory with explicit remaining coverage gaps."""
import hashlib
import json
from pathlib import Path
from studium.storage.records import fold_by_id
ROOT=Path(__file__).resolve().parents[1]


def main():
    units=json.loads((ROOT/'learning/units.json').read_text())
    verification=json.loads((ROOT/'reports/learning-verification.json').read_text())
    for relative,digest in verification['files'].items():
        assert hashlib.sha256((ROOT/'learning'/relative).read_bytes()).hexdigest()==digest, 'Stale learning report: '+relative
    assert all(u['status']=='CASES_PASSED' for u in verification['units'])
    by_chapter={(u['slug'],u['chapter']):u for u in units}
    chapters=[]
    for v in sorted((ROOT/'volumes').glob('vol*')):
        sections=fold_by_id(v/'blueprint/outline.jsonl')[0]['sections']
        paragraphs=fold_by_id(v/'draft/paragraphs.jsonl')
        problems=fold_by_id(v/'problems/problems.jsonl')
        for section in sections:
            unit=by_chapter.get((v.name,section['id']))
            row={'volume':v.name,'chapter':section['id'],'title':section['title'],
                 'active_paragraphs':len([p for p in paragraphs if p['section']==section['id']]),
                 'active_exercises':len([p for p in problems if p['section']==section['id'] and p.get('role')=='practice']),
                 'independent_technical_and_pedagogical_review':'PENDING',
                 'beginner_entry_route':'ADDED_AND_EXECUTED' if unit else 'NOT_ESTABLISHED_BY_THIS_AUDIT'}
            if unit:
                lesson=next(p for p in paragraphs if p['id']==unit['paragraph_id'])
                actual=[p for p in problems if p.get('learning_unit')==unit['key']]
                assert {p['id'] for p in actual}==set(unit['exercise_ids'])
                assert len(actual)==3 and all(p.get('solution',{}).get('text') for p in actual)
                row.update({'language':unit['title'],'lesson_record':lesson['id'],'exercises':unit['exercise_ids'],
                            'scope':'Introductory path only. Existing advanced material is not certified by these tests.',
                            'features':['prerequisites','complete introductory example','explained trace','input contract','edge cases','guided practice','transfer task','debugging task','separate reference solutions','runtime-specific execution evidence']})
            chapters.append(row)
    report={'reviewer':'same model, new pass plus executable evidence; not independent academic approval',
            'chapters_inventoried':len(chapters),'beginner_routes_added':len(units),'programming_exercises_added':sum(len(u['exercise_ids']) for u in units),
            'remaining_chapters_without_an_established_beginner_route':sum(c['beginner_entry_route']!='ADDED_AND_EXECUTED' for c in chapters),
            'chapters':chapters,'resolved_findings':['Advanced internals preceded first runnable programs: add eleven beginner paths and navigation in guide.',
              'Numeric exercise contracts did not show programming answers: render explicit reference solutions with honest review status.',
              'Listing boxes could trap long practice banks: allow programming banks to flow over pages.',
              'Unknown code glyphs were silently replaced by U+ labels: reject unsupported literal glyphs and preserve Python value with an explicit Unicode escape.',
              'PDF extraction decomposed a not-equal symbol: encode exact Unicode ActualText in literal regions.',
              'Printed C/C++ newline escapes differed from runnable reference files: compile and execute the exact printed introductions as well.',
              'Distinguish Unicode scalar values from code points by excluding UTF-16 surrogate values (RFC 3629 section 3).',
              'Remove irrelevant SQL/TypeScript boilerplate from other beginner routes.'],
            'remaining_work':['Independent semantic review of all chapters and original source excerpts.','Expand entry routes for other languages and advanced project progression.','Pending or illustrative legacy snippets are not converted into verified programs.']}
    assert len(chapters)==75
    (ROOT/'reports/pedagogical-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print({k:report[k] for k in ['chapters_inventoried','beginner_routes_added','programming_exercises_added','remaining_chapters_without_an_established_beginner_route']})


if __name__=='__main__':main()
