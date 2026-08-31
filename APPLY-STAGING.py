#!/usr/bin/env python3
from pathlib import Path
import argparse, re, shutil, hashlib, json, datetime, sys

LEGACY = [
  'schedule-read-v60522.js','schedule-exact-canary-v6035.js','schedule-exact-canary-v6035.css',
  'schedule-card-clean-v6060.js','schedule-drag-mode-v6061.js','schedule-drag-focus-v6063.js',
  'schedule-drag-polish-v6064.js','schedule-drag-basket-v6066.js','schedule-ui-stability-v60726.js',
  'schedule-ui-stability-v60727.js','schedule-ui-stability-v60728.js','schedule-ui-stability-v60729.js',
  'schedule-ui-stability-v60730.js','schedule-ui-stability-v60731.js','schedule-ui-stability-v60732.js',
  'schedule-ui-stability-v60733.js','schedule-ui-stability-v60734.js','schedule-ui-stability-v60735.js',
  'schedule-runtime-authority-v60739.js','schedule-runtime-authority-v60740.js','schedule-runtime-authority-v60741.js',
  'release-marker-v6035.js'
]
TAG_MARKER='TUINBOOKS-STABILITY-STAGING-v60.8.3'

def sha(p):
    h=hashlib.sha256();
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(description='Apply TuinBooks v60.8.3 staging cutover to an existing current repository.')
    ap.add_argument('repo', nargs='?', default='.', help='Path containing the current app/ folder')
    args=ap.parse_args(); repo=Path(args.repo).resolve(); app=repo/'app'; index=app/'index.html'
    if not index.exists():
        print(f'ERROR: {index} not found. Run this against the current TuinBooks repository root.'); return 2
    appjs=app/'app.js'
    before_appjs=sha(appjs) if appjs.exists() else None
    stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S'); backup=repo/f'.tb-staging-backup-{stamp}'; backup.mkdir()
    shutil.copy2(index, backup/'index.html')
    if (app/'service-worker.js').exists(): shutil.copy2(app/'service-worker.js', backup/'service-worker.js')
    manifest={'created':stamp,'index_sha256':sha(index),'appjs_sha256':before_appjs,'legacy_removed':[]}
    source=Path(__file__).resolve().parent/'app'
    for rel in ['schedule-v2/schedule-v2.js','schedule-v2/schedule-v2.css','stability-staging-v6083.js','stability-staging-v6083.css','VERSION-STAGING.txt']:
        src=source/rel; dst=app/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
    text=index.read_text(encoding='utf-8',errors='replace')
    # Remove prior staging block so apply is idempotent.
    text=re.sub(r'\s*<!-- '+re.escape(TAG_MARKER)+r' START -->.*?<!-- '+re.escape(TAG_MARKER)+r' END -->\s*','\n',text,flags=re.S)
    # Remove external legacy Schedule authority tags by basename, regardless of query string/version.
    for name in LEGACY:
        pat=r'\s*<(?:script\b[^>]*\bsrc=["\'][^"\']*'+re.escape(name)+r'(?:\?[^"\']*)?["\'][^>]*>\s*</script>|link\b[^>]*\bhref=["\'][^"\']*'+re.escape(name)+r'(?:\?[^"\']*)?["\'][^>]*>)\s*'
        new,n=re.subn(pat,'\n',text,flags=re.I|re.S)
        if n: manifest['legacy_removed'].append({'file':name,'tags':n}); text=new
    head_block=f'''\n<!-- {TAG_MARKER} START -->\n<link rel="stylesheet" href="schedule-v2/schedule-v2.css?v=60.8.3-staging">\n<link rel="stylesheet" href="stability-staging-v6083.css?v=60.8.3-staging">\n<!-- {TAG_MARKER} END -->\n'''
    body_block=f'''\n<!-- {TAG_MARKER} START -->\n<script src="stability-staging-v6083.js?v=60.8.3-staging"></script>\n<script src="schedule-v2/schedule-v2.js?v=60.8.3-staging"></script>\n<!-- {TAG_MARKER} END -->\n'''
    # Separate markers around head/body would collide with idempotency regex, so use unique marker suffixes.
    head_block=head_block.replace(TAG_MARKER+' START',TAG_MARKER+' HEAD START').replace(TAG_MARKER+' END',TAG_MARKER+' HEAD END')
    body_block=body_block.replace(TAG_MARKER+' START',TAG_MARKER+' BODY START').replace(TAG_MARKER+' END',TAG_MARKER+' BODY END')
    # Remove old unique blocks too.
    text=re.sub(r'\s*<!-- '+re.escape(TAG_MARKER)+r' HEAD START -->.*?<!-- '+re.escape(TAG_MARKER)+r' HEAD END -->\s*','\n',text,flags=re.S)
    text=re.sub(r'\s*<!-- '+re.escape(TAG_MARKER)+r' BODY START -->.*?<!-- '+re.escape(TAG_MARKER)+r' BODY END -->\s*','\n',text,flags=re.S)
    if '</head>' not in text.lower() or '</body>' not in text.lower(): print('ERROR: index.html is malformed; no changes written.'); return 3
    text=re.sub(r'</head>',head_block+'</head>',text,count=1,flags=re.I)
    text=re.sub(r'</body>',body_block+'</body>',text,count=1,flags=re.I)
    index.write_text(text,encoding='utf-8',newline='\n')
    manifest['new_index_sha256']=sha(index); manifest['appjs_unchanged']=(before_appjs==sha(appjs) if appjs.exists() else True)
    (backup/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('APPLIED: TuinBooks stability staging v60.8.3')
    print('Backup:',backup)
    print('Legacy Schedule tags removed:',sum(x['tags'] for x in manifest['legacy_removed']))
    print('app/app.js unchanged:',manifest['appjs_unchanged'])
    print('Next: run VERIFY-STAGING.py against the same repo, then deploy ONLY to staging.')
    return 0
if __name__=='__main__': raise SystemExit(main())
