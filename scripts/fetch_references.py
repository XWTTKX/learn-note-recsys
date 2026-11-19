"""Fetch pinned source for reading only. Does not run third-party code."""
import argparse,json,subprocess
from pathlib import Path
def main():
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'references.json').read_text())
    p=argparse.ArgumentParser()
    p.add_argument('--name',choices=sorted(manifest),help='Fetch only one reference')
    args=p.parse_args()
    for name,spec in manifest.items():
        if args.name and args.name!=name: continue
        dest=root/'vendor'/name
        if dest.exists():
            print(f'SKIP existing directory: {dest}; check its HEAD manually')
            continue
        dest.parent.mkdir(parents=True,exist_ok=True)
        subprocess.run(['git','clone','--filter=blob:none','--no-checkout',
            f"https://github.com/{spec['repository']}.git",str(dest)],check=True)
        subprocess.run(['git','-C',str(dest),'checkout','--detach',spec['commit']],check=True)
        actual=subprocess.check_output(['git','-C',str(dest),'rev-parse','HEAD'],text=True).strip()
        if actual!=spec['commit']: raise RuntimeError('commit mismatch')
        print(name,actual)
if __name__=='__main__': main()
