# CABBAGE This is the only migration step that is allowed to edit NML templates.
"""Install all seven NML templates as a single complete payload.
No later migration step is allowed to modify src/templates.
Files matching the pristine source hashes, or the installed payload, are accepted.
Any other local edits fail rather than being overwritten.
"""
from _common import ROOT, PAYLOAD
import hashlib

# CABBAGE Prior payload hashes allow correction of the previous installed templates.
# CABBAGE Other unrecognised local template edits still fail.
PREVIOUS_PAYLOAD_HASHES = {'articulated_parts': '5a80d80534f206bc00e747e922627db4c12891de35c5e0a5f0e13c40460469a4', 'capacity_switches': '12783e7aeeb0f855cfbf22c4e39a8f4db5b4ac67dad91511d37b7b1056bac3f2', 'graphics_switches': '7b0122e423d9011af20f7536d0b0f62e7e67731ff9cd7541e52932da1992a18a', 'header': 'e3c4dbff2312541a6b868b159f5609620ab6419b6d379759cb7ddcde2b116b35', 'properties': '2ecd826380cf9795115cd7e5d148f9c2576ab6aebc32acef164d9979a4bb0afc', 'spriteset_templates': 'fac5be84300e0c92e44d30eb62f158e9b497cf5563dc0465c3a3fd8b33b0ca5c', 'vehicle_default': '6f37567631c09bd5e5e25c8471eeb8be57fa2243c6e0892f4938522e98c24993'}

EXPECTED = {
    'header': '8b963b0375491a2704eaeac84b0546097c0860c2340e2c47fc8f763051f44814',
    'vehicle_default': '74795aee1d68d2f6c365480ed267bff7e7daf574008b55dfc4868d251d630399',
    'properties': 'f6258f92d3b2bac000cc30f42a7f229db4bf5aad0194556a17fd02cf4284ee42',
    'capacity_switches': '8b613f29ec085dba1a62d7da3e3f7d2d3c16c1e716a8dfa505859156fc1654cc',
    'graphics_switches': '854b53b2a0a4d53e710b63bfd1ac143b812f0ce9178bd530b44e281b8f6caaa2',
    'spriteset_templates': '48fa5e6e77850f28bfd8ec802bbc65e4d0f0a31803b872c0bc6f16f4a67c1c05',
    'articulated_parts': 'e64f608e0bb6f14eff1b20bfe92f0898d0c6f9b222a52a2eb5de730ae9adda82',
}

def main():
    updates=[]
    for stem, old_hash in EXPECTED.items():
        dest=ROOT/'src/templates'/f'{stem}.pynml'
        data=(PAYLOAD/'templates'/f'{stem}.pynml').read_bytes()
        current=dest.read_bytes()
        if current==data:
            print('UNCHANGED',dest.relative_to(ROOT)); continue
        digest=hashlib.sha256(current).hexdigest()
        if digest!=old_hash and digest!=PREVIOUS_PAYLOAD_HASHES[stem]:
            raise RuntimeError(f'Unexpected template contents: {dest} sha256={digest}')
        updates.append((dest,data))
    # Validate every input before writing a single file.
    for dest,data in updates:
        dest.write_bytes(data)
        print('UPDATED',dest.relative_to(ROOT))
    print('Ported NML templates:',len(EXPECTED))

if __name__=='__main__': main()
