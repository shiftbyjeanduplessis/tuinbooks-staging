#!/usr/bin/env python3
from pathlib import Path
import argparse,re,subprocess,shutil,sys
LEGACY=['schedule-read-v60522.js','schedule-exact-canary-v6035.js','schedule-card-clean-v6060.js','schedule-drag-mode-v6061.js','schedule-drag-focus-v6063.js','schedule-drag-polish-v6064.js','schedule-drag-basket-v6066.js','schedule-ui-stability-v60735.js','schedule-runtime-authority-v60739.js','schedule-runtime-authority-v60740.js','schedule-runtime-authority-v60741.js','release-marker-v6035.js']
REQUIRED=['schedule-v2/schedule-v2.js','schedule-v2/schedule-v2.css','stability-staging-v6083.js','stability-staging-v6083.css','VERSION-STAGING.txt']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('repo',nargs='?',default='.');a=ap.parse_args();root=Path(a.repo).resolve();app=root/'app';idx=app/'index.html';fails=[]
 if not idx.exists(): print('FAIL: app/index.html missing');return 2
 text=idx.read_text(encoding='utf-8',errors='replace')
 for x in REQUIRED:
  if not (app/x).exists():fails.append(f'missing app/{x}')
 if 'schedule-v2/schedule-v2.js?v=60.8.3-staging' not in text:fails.append('new Schedule V2 JS not referenced by index')
 if 'schedule-v2/schedule-v2.css?v=60.8.3-staging' not in text:fails.append('new Schedule V2 CSS not referenced by index')
 for x in LEGACY:
  if re.search(r'(?:src|href)=["\'][^"\']*'+re.escape(x),text,re.I):fails.append(f'legacy Schedule authority still loaded: {x}')
 ids=re.findall(r'\bid=["\']([^"\']+)',text,re.I);dups=sorted({x for x in ids if ids.count(x)>1})
 if dups:fails.append('duplicate HTML IDs in index: '+', '.join(dups[:20]))
 node=shutil.which('node')
 if node:
  for rel in ['schedule-v2/schedule-v2.js','stability-staging-v6083.js']:
   p=app/rel;r=subprocess.run([node,'--check',str(p)],capture_output=True,text=True)
   if r.returncode:fails.append(f'node --check failed for app/{rel}: {r.stderr.strip()}')
 else: print('WARN: node not installed; JavaScript syntax check skipped')
 if fails:
  print('STAGING VERIFY: FAIL');[print(' -',x) for x in fails];return 1
 print('STAGING VERIFY: PASS')
 print(' - isolated Schedule V2 files present')
 print(' - known legacy Schedule authority tags absent')
 print(' - no duplicate IDs detected in app/index.html')
 if node:print(' - new JavaScript syntax checks passed')
 print('Proceed to staging agent QA. Do NOT promote to production yet.')
 return 0
if __name__=='__main__':raise SystemExit(main())
