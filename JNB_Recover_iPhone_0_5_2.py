#!/usr/bin/env python3
"""
JNB Recover iPhone MVP 0.5

Single-file Pyto workflow for local, read-only SigmaPlot JNB recovery.

Scientific boundary:
    The embedded recovery engine is the frozen MVP 0.3.0 engine.
    Its embedded source is verified at runtime with SHA-256 before use.
    This wrapper does not modify parser logic or scientific semantics.
"""

from pathlib import Path
import hashlib
import json


WORKFLOW_VERSION = "0.5.2"
REQUIRED_ENGINE_VERSION = "0.3.0"
FROZEN_ENGINE_SHA256 = "7ae046dc62b5ace46061bc9b7b6c33d4179036a48ac8adfecf4cea7547d45c40"

# Exact UTF-8 text of the frozen MVP 0.3.0 recovery engine.
# It is executed under a non-main module name, so its CLI entry point does not run.
FROZEN_ENGINE_SOURCE = '#!/usr/bin/env python3\n"""JNB Recover MVP 0.3 — clean-room SigmaPlot scientific-data recovery.\n\nPure Python standard library. Read-only. No SigmaPlot, Origin, network, or paid API.\nValidated record families:\n  * SigmaPlot 11 public Dryad fixtures: 0x2002 and 0x2012 column records\n  * SigmaPlot 12 public fixture: same base record grammar, numeric/text cells\n\nCommands:\n  python jnb_recover.py inspect sample.JNB\n  python jnb_recover.py recover sample.JNB -o recovered\n  python jnb_recover.py validate sample.JNB ground_truth.csv\n  python jnb_recover.py batch-recover input_dir -o recovered_batch\n  python jnb_recover.py batch-validate input_dir\n"""\nfrom __future__ import annotations\nimport argparse, csv, json, math, struct, sys\nfrom dataclasses import asdict, dataclass\nfrom decimal import Decimal, InvalidOperation\nfrom pathlib import Path\nfrom typing import Sequence\n\n# CFB/OLE constants\nFREE=0xFFFFFFFF; ENDOFCHAIN=0xFFFFFFFE\nCFB_MAGIC=bytes.fromhex(\'d0cf11e0a1b11ae1\')\n\n# SigmaPlot worksheet constants observed in public fixtures\nCOLUMN_RECORD_MAGIC=b"\\x01\\x20\\x05\\x00"\nMARKER_1=b"\\x02\\x70\\x00\\x05"\nMARKER_1_SP14=b"\\x02\\x70\\x00\\x06"\nMARKER_2=b"\\x80\\x20\\x05\\x0c"\nMARKER_3=b"\\x87\\x20\\x13\\x00"\nSUBTYPE_REGULAR=0x2002\nSUBTYPE_EXTENDED=0x2012\nSUBTYPE_SP14_NUMERIC=0x2000\nSUBTYPE_SP14_TEXT=0x2008\nCELL_SIZE=16\nNUMERIC_TAG=0x16\nMISSING_TAG=0x12\nVERSION=\'0.3.0\'\n\nclass JNBError(RuntimeError): pass\n\n@dataclass\nclass Cell:\n    kind:str\n    value:object|None\n    raw_hex:str\n    tag:int\n\n@dataclass\nclass Column:\n    index:int\n    subtype:int\n    max_row_index:int\n    name:str|None\n    cells:list[Cell]\n    offset:int\n    record_size:int\n    warnings:list[str]\n\n@dataclass\nclass Worksheet:\n    stream_path:str\n    stream_size:int\n    declared_max_column_index:int|None\n    declared_max_row_index:int|None\n    columns:list[Column]\n\nclass CFBReader:\n    """Minimal read-only Compound File Binary reader sufficient for JNB streams."""\n    def __init__(self,path:Path):\n        self.path=path; self.data=path.read_bytes()\n        if len(self.data)<512 or self.data[:8]!=CFB_MAGIC:\n            raise JNBError(f"{path} is not an OLE Compound Document")\n        h=self.data[:512]\n        if struct.unpack_from(\'<H\',h,28)[0] != 0xFFFE:\n            raise JNBError(\'unsupported CFB byte order\')\n        self.sector_size=1<<struct.unpack_from(\'<H\',h,30)[0]\n        self.mini_sector_size=1<<struct.unpack_from(\'<H\',h,32)[0]\n        self.num_fat=struct.unpack_from(\'<I\',h,44)[0]\n        self.first_dir=struct.unpack_from(\'<I\',h,48)[0]\n        self.cutoff=struct.unpack_from(\'<I\',h,56)[0]\n        self.first_mini_fat=struct.unpack_from(\'<I\',h,60)[0]\n        self.num_mini_fat=struct.unpack_from(\'<I\',h,64)[0]\n        first_difat=struct.unpack_from(\'<I\',h,68)[0]\n        num_difat=struct.unpack_from(\'<I\',h,72)[0]\n        difat=[x for x in struct.unpack_from(\'<109I\',h,76) if x!=FREE]\n        sid=first_difat\n        for _ in range(num_difat):\n            if sid in (FREE,ENDOFCHAIN): break\n            sec=self._sector(sid); n=self.sector_size//4-1\n            difat += [x for x in struct.unpack_from(f\'<{n}I\',sec,0) if x!=FREE]\n            sid=struct.unpack_from(\'<I\',sec,n*4)[0]\n        self.fat=[]\n        for fsid in difat[:self.num_fat]:\n            self.fat.extend(struct.unpack(f\'<{self.sector_size//4}I\',self._sector(fsid)))\n        dbytes=b\'\'.join(self._sector(s) for s in self._chain(self.first_dir))\n        self.entries=[]\n        for off in range(0,len(dbytes),128):\n            e=dbytes[off:off+128]\n            if len(e)<128: break\n            nlen=struct.unpack_from(\'<H\',e,64)[0]\n            name=e[:max(0,nlen-2)].decode(\'utf-16le\',\'replace\') if nlen>=2 else \'\'\n            typ=e[66]\n            left,right,child=struct.unpack_from(\'<III\',e,68)\n            start=struct.unpack_from(\'<I\',e,116)[0]\n            size=struct.unpack_from(\'<Q\',e,120)[0]\n            self.entries.append({\'id\':off//128,\'name\':name,\'type\':typ,\'left\':left,\'right\':right,\'child\':child,\'start\':start,\'size\':size})\n        if not self.entries: raise JNBError(\'CFB directory is empty\')\n        root=self.entries[0]\n        self.root_mini=self._read_normal(root[\'start\'],root[\'size\']) if root[\'size\'] else b\'\'\n        self.minifat=[]\n        if self.num_mini_fat and self.first_mini_fat not in (FREE,ENDOFCHAIN):\n            mb=b\'\'.join(self._sector(s) for s in self._chain(self.first_mini_fat))\n            self.minifat=list(struct.unpack(f\'<{len(mb)//4}I\',mb[:len(mb)//4*4]))\n    def _sector(self,sid:int)->bytes:\n        off=512+sid*self.sector_size\n        if off<512 or off+self.sector_size>len(self.data): raise JNBError(f\'CFB sector out of range: {sid}\')\n        return self.data[off:off+self.sector_size]\n    def _chain(self,start:int,fat=None):\n        fat=self.fat if fat is None else fat; out=[]; seen=set(); sid=start\n        while sid not in (FREE,ENDOFCHAIN) and sid<0xFFFFFFF0:\n            if sid in seen: raise JNBError(\'CFB chain cycle\')\n            if sid>=len(fat): raise JNBError(f\'CFB chain sector out of range: {sid}\')\n            seen.add(sid); out.append(sid); sid=fat[sid]\n            if len(out)>1000000: raise JNBError(\'CFB chain too long\')\n        return out\n    def _read_normal(self,start:int,size:int)->bytes:\n        return b\'\'.join(self._sector(s) for s in self._chain(start))[:size] if size else b\'\'\n    def _tree_ids(self,idx:int):\n        if idx in (FREE,ENDOFCHAIN) or idx>=len(self.entries): return []\n        e=self.entries[idx]\n        return self._tree_ids(e[\'left\'])+[idx]+self._tree_ids(e[\'right\'])\n    def _walk(self,storage_id=0,prefix=\'\'):\n        st=self.entries[storage_id]\n        for idx in self._tree_ids(st[\'child\']):\n            e=self.entries[idx]; path=prefix+e[\'name\']\n            yield path,e\n            if e[\'type\']==1: yield from self._walk(idx,path+\'/\')\n    def read_entry(self,e)->bytes:\n        if e[\'type\']==5: return self._read_normal(e[\'start\'],e[\'size\'])\n        if not e[\'size\']: return b\'\'\n        if e[\'size\']<self.cutoff:\n            chunks=[]\n            for msid in self._chain(e[\'start\'],self.minifat):\n                o=msid*self.mini_sector_size; chunks.append(self.root_mini[o:o+self.mini_sector_size])\n            return b\'\'.join(chunks)[:e[\'size\']]\n        return self._read_normal(e[\'start\'],e[\'size\'])\n    def streams(self):\n        for path,e in self._walk():\n            if e[\'type\']==2: yield path,e,self.read_entry(e)\n\ndef _u32(b:bytes,o:int)->int: return struct.unpack_from(\'<I\',b,o)[0]\n\ndef _try_text_cell(block:bytes)->str|None:\n    if len(block)!=16:return None\n    n=block[-1]\n    if n==0 or n>15:return None\n    payload=block[:n]\n    if b\'\\x00\' in payload:return None\n    for enc in (\'utf-8\',\'cp1252\'):\n        try:s=payload.decode(enc)\n        except UnicodeDecodeError:continue\n        if s and all(ch.isprintable() for ch in s):return s\n    return None\n\ndef decode_cell(block:bytes)->Cell:\n    if len(block)!=16:return Cell(\'unsupported\',None,block.hex(),-1)\n    tag=block[-1]\n    if tag==NUMERIC_TAG:\n        v=struct.unpack_from(\'<d\',block,0)[0]\n        if math.isnan(v):return Cell(\'numeric_nan\',None,block.hex(),tag)\n        return Cell(\'numeric\',v,block.hex(),tag)\n    txt=_try_text_cell(block)\n    if txt is not None:return Cell(\'text\',txt,block.hex(),tag)\n    # SigmaPlot documentation distinguishes occupied missing-value cells (shown as --)\n    # from empty cells/text. In legacy public Samples.jnb we observe two distinct 0x12\n    # payload families. NaN-like payloads are therefore tracked separately as a\n    # high-confidence *candidate* for the occupied missing-value representation; the\n    # all-zero 0x12 form remains an empty/placeholder candidate until independent\n    # cell-level ground truth is available. Neither is silently converted to CSV data.\n    if tag==MISSING_TAG:\n        try:\n            probe=struct.unpack_from(\'<d\',block,0)[0]\n        except struct.error:\n            probe=None\n        if probe is not None and math.isnan(probe):\n            return Cell(\'missing_nan_candidate\',None,block.hex(),tag)\n        if block[:15]==b\'\\x00\'*15:\n            return Cell(\'empty_or_placeholder_candidate\',None,block.hex(),tag)\n    if block==b\'\\x00\'*16:return Cell(\'empty_candidate\',None,block.hex(),tag)\n    return Cell(\'unsupported\',None,block.hex(),tag)\n\ndef _valid_record(stream:bytes,off:int)->bool:\n    if off+0x38>len(stream):return False\n    if stream[off:off+4]!=COLUMN_RECORD_MAGIC:return False\n    if stream[off+8:off+12] not in (MARKER_1,MARKER_1_SP14):return False\n    if stream[off+0x10:off+0x14]!=MARKER_2:return False\n    if stream[off+0x18:off+0x1c]!=MARKER_3:return False\n    return _u32(stream,off+0x24) in (SUBTYPE_REGULAR,SUBTYPE_EXTENDED,SUBTYPE_SP14_NUMERIC,SUBTYPE_SP14_TEXT)\n\ndef parse_column_record(stream:bytes,off:int)->Column:\n    if not _valid_record(stream,off):raise JNBError(f\'invalid column record at 0x{off:x}\')\n    record_size=_u32(stream,off+4)+8\n    if off+record_size>len(stream):raise JNBError(f\'truncated column record at 0x{off:x}\')\n    idx=_u32(stream,off+0x14); sub=_u32(stream,off+0x24)\n    rep_a=_u32(stream,off+0x28); rep_b=_u32(stream,off+0x30)\n    max_row=_u32(stream,off+0x34); n=max_row+1\n    warnings=[]\n    if rep_a!=idx or rep_b!=idx:warnings.append(f\'column index repetitions differ: {idx}, {rep_a}, {rep_b}\')\n    rec=stream[off:off+record_size]\n    if sub==SUBTYPE_REGULAR:\n        name=_try_text_cell(rec[0x40:0x50]); data_off=0x50; cell_size=16\n        cells=[decode_cell(rec[data_off+r*cell_size:data_off+(r+1)*cell_size]) for r in range(n)]\n    elif sub==SUBTYPE_EXTENDED:\n        # SP11/SP12: n 16-byte first-plane cells, then name, then n data cells.\n        name_off=0x40+n*16; name=_try_text_cell(rec[name_off:name_off+16]); data_off=name_off+16; cell_size=16\n        cells=[decode_cell(rec[data_off+r*cell_size:data_off+(r+1)*cell_size]) for r in range(n)]\n    elif sub==SUBTYPE_SP14_NUMERIC:\n        # SP14 observed numeric record: 64-byte header + n 31-byte cells.\n        # Each cell stores the IEEE-754 double at bytes 0..7 and tag 0x16 at byte 30.\n        name=None; data_off=0x40; cell_size=31; cells=[]\n        for r in range(n):\n            b=rec[data_off+r*cell_size:data_off+(r+1)*cell_size]\n            if len(b)<cell_size: break\n            if b[-1]==NUMERIC_TAG:\n                v=struct.unpack_from(\'<d\',b,0)[0]\n                cells.append(Cell(\'numeric_nan\' if math.isnan(v) else \'numeric\',None if math.isnan(v) else v,b.hex(),b[-1]))\n            else: cells.append(Cell(\'unsupported\',None,b.hex(),b[-1]))\n    else:\n        # SP14 observed text/group record: 64-byte header + n 37-byte cells.\n        # Public fixtures place a short UTF-16LE label at byte 33 onward.\n        name=None; data_off=0x40; cell_size=37; cells=[]\n        for r in range(n):\n            b=rec[data_off+r*cell_size:data_off+(r+1)*cell_size]\n            if len(b)<cell_size: break\n            tail=b[33:]\n            try: txt=tail.decode(\'utf-16le\',\'ignore\').rstrip(\'\\x00\')\n            except Exception: txt=\'\'\n            cells.append(Cell(\'text\' if txt else \'unsupported\',txt or None,b.hex(),b[-1]))\n    needed=data_off+n*cell_size\n    if len(rec)<needed:\n        warnings.append(f\'record too short for {n} cells: {len(rec)} < {needed}\')\n    return Column(idx,sub,max_row,name,cells,off,record_size,warnings)\n\ndef find_column_records(stream:bytes)->list[Column]:\n    cols=[]; start=0\n    while True:\n        off=stream.find(COLUMN_RECORD_MAGIC,start)\n        if off<0:break\n        start=off+1\n        if not _valid_record(stream,off):continue\n        try:c=parse_column_record(stream,off)\n        except JNBError:continue\n        cols.append(c); start=max(start,off+c.record_size)\n    return cols\n\ndef list_ole_entries(path:Path):\n    c=CFBReader(path)\n    return [{\'path\':p,\'size\':e[\'size\']} for p,e,_ in c.streams()]\n\ndef _safe_declared_dims(data:bytes, cols:list[Column])->tuple[int|None,int|None]:\n    # Across observed SigmaPlot generations, the worksheet-level max column/row\n    # pair sits immediately before the first column record. Older notebooks use\n    # a shorter worksheet header, so fixed absolute offsets are unsafe.\n    if not cols:return None,None\n    first=min(c.offset for c in cols)\n    obs_c=max(c.index for c in cols); obs_r=max(c.max_row_index for c in cols)\n    if first>=8:\n        dc=_u32(data,first-8); dr=_u32(data,first-4)\n        # Accept only values consistent with the records we actually parsed.\n        # This prevents corrupt/legacy header interpretation from allocating a\n        # gigantic matrix (the bug exposed by SigmaPlot 7 Samples.jnb).\n        if dc>=obs_c and dr>=obs_r and dc<=1_000_000 and dr<=10_000_000:\n            return dc,dr\n    return obs_c,obs_r\n\ndef recover_worksheets(path:Path)->list[Worksheet]:\n    c=CFBReader(path); out=[]\n    for p,e,data in c.streams():\n        if not p.lower().endswith(\'/jnbcontents\'):continue\n        if b\'JSDataWorksheet\' not in data and \'JSDataWorksheet\'.encode(\'utf-16le\') not in data:continue\n        cols=find_column_records(data)\n        if not cols:continue\n        dmc,dmr=_safe_declared_dims(data,cols)\n        out.append(Worksheet(p,len(data),dmc,dmr,cols))\n    return out\n\ndef worksheet_shape(ws:Worksheet):\n    if not ws.columns:return 0,0\n    by={c.index:c for c in ws.columns}\n    max_col=ws.declared_max_column_index if ws.declared_max_column_index is not None else max(by)\n    max_row=ws.declared_max_row_index if ws.declared_max_row_index is not None else max(c.max_row_index for c in ws.columns)\n    return max_row+1,max_col+1\n\ndef worksheet_headers(ws:Worksheet):\n    _,ncols=worksheet_shape(ws); by={c.index:c for c in ws.columns}\n    return [(by.get(ci).name if by.get(ci) and by.get(ci).name else f\'C{ci+1}\') for ci in range(ncols)]\n\ndef worksheet_cell(ws:Worksheet,row:int,col:int):\n    by={c.index:c for c in ws.columns}\n    c=by.get(col)\n    if c is None or row>=len(c.cells):\n        return None, \'structural_missing\'\n    cell=c.cells[row]\n    return (cell.value if cell.kind in (\'numeric\',\'text\') else None), cell.kind\n\ndef iter_worksheet_rows(ws:Worksheet):\n    nrows,ncols=worksheet_shape(ws)\n    by={c.index:c for c in ws.columns}\n    for ri in range(nrows):\n        row=[]\n        for ci in range(ncols):\n            c=by.get(ci)\n            if c is None or ri>=len(c.cells):\n                row.append(None); continue\n            cell=c.cells[ri]\n            row.append(cell.value if cell.kind in (\'numeric\',\'text\') else None)\n        yield row\n\ndef worksheet_matrix(ws:Worksheet):\n    # Compatibility helper for validation/small fixtures. Production CSV export\n    # uses iter_worksheet_rows() so it does not materialize the whole matrix.\n    return worksheet_headers(ws), list(iter_worksheet_rows(ws))\n\ndef _cell_kind_counts(ws:Worksheet):\n    counts={}\n    for c in ws.columns:\n        for cell in c.cells:counts[cell.kind]=counts.get(cell.kind,0)+1\n    return counts\n\ndef _ambiguous_cells(ws:Worksheet, worksheet_index:int):\n    out=[]\n    for c in ws.columns:\n        for ri,cell in enumerate(c.cells):\n            if cell.kind in (\'numeric\',\'text\'):continue\n            if cell.kind==\'structural_missing\':continue\n            out.append({\n                \'worksheet\':worksheet_index,\'stream_path\':ws.stream_path,\n                \'row\':ri,\'column\':c.index,\'kind\':cell.kind,\'tag\':cell.tag,\n                \'raw_hex\':cell.raw_hex\n            })\n    return out\n\ndef export_recovery(path:Path,outdir:Path, strict:bool=False):\n    outdir.mkdir(parents=True,exist_ok=True)\n    wslist=recover_worksheets(path)\n    if not wslist:raise JNBError(\'no supported worksheet data found\')\n    written=[]; summaries=[]; ambiguous=[]\n    for i,w in enumerate(wslist):\n        rows,cols=worksheet_shape(w); kinds=_cell_kind_counts(w)\n        amb=_ambiguous_cells(w,i); ambiguous.extend(amb)\n        summaries.append({\n            \'index\':i,\'stream_path\':w.stream_path,\'stream_size\':w.stream_size,\n            \'shape\':[rows,cols],\'headers\':worksheet_headers(w),\n            \'column_count\':len(w.columns),\'cell_kind_counts\':kinds,\n            \'warnings\':[x for c in w.columns for x in c.warnings],\n            \'ambiguous_count\':len(amb)\n        })\n    if strict and ambiguous:\n        raise JNBError(f\'strict mode refused export: {len(ambiguous)} ambiguous cells\')\n    for i,w in enumerate(wslist):\n        cp=outdir/f\'worksheet_{i}.csv\'\n        with cp.open(\'w\',newline=\'\',encoding=\'utf-8\') as f:\n            wr=csv.writer(f); wr.writerow(worksheet_headers(w))\n            for r in iter_worksheet_rows(w):\n                wr.writerow([\'\' if v is None else v for v in r])\n        written.append(cp)\n    manifest_data={\n        \'schema\':\'jnb-recover-manifest-1\',\'tool_version\':VERSION,\n        \'source\':{\'path\':str(path),\'size_bytes\':path.stat().st_size},\n        \'policy\':{\n            \'read_only\':True,\n            \'csv_blank_for\':[\'structural_missing\',\'missing_nan_candidate\',\'empty_or_placeholder_candidate\',\'empty_candidate\',\'unsupported\',\'numeric_nan\'],\n            \'missing_nan_candidate_status\':\'high_confidence_candidate_not_cell_level_ground_truth\',\n            \'unknown_cells_are_never_coerced_to_numeric_or_text\':True\n        },\n        \'worksheets\':summaries,\n        \'ambiguous_cells\':ambiguous\n    }\n    manifest=outdir/\'recovery_manifest.json\'\n    manifest.write_text(json.dumps(manifest_data,indent=2,ensure_ascii=False),encoding=\'utf-8\')\n    written.append(manifest)\n    return written\n\ndef _half_quantum(s:str)->float:\n    try:d=Decimal(s)\n    except InvalidOperation:return 0.0\n    q=Decimal(1).scaleb(d.as_tuple().exponent)\n    return float(abs(q)/2)\n\ndef validate_jnb_csv(jnb:Path,expected:Path):\n    wslist=recover_worksheets(jnb)\n    if len(wslist)!=1:raise JNBError(f\'expected one worksheet, found {len(wslist)}\')\n    ws=wslist[0]\n    headers,rows=worksheet_matrix(ws)\n    with expected.open(newline=\'\',encoding=\'utf-8-sig\') as f:raw=list(csv.reader(f))\n    if not raw:raise JNBError(\'ground-truth CSV is empty\')\n    eh,erows=raw[0],raw[1:]\n    mism=[]; numeric=0; text=0; missing=0; unresolved=0\n    if len(erows)!=len(rows):mism.append({\'kind\':\'row_count\',\'jnb\':len(rows),\'csv\':len(erows)})\n    if len(eh)>len(headers):mism.append({\'kind\':\'csv_has_more_columns\',\'jnb\':len(headers),\'csv\':len(eh)})\n    for r in range(min(len(rows),len(erows))):\n        for c in range(min(len(headers),len(eh))):\n            av,ak=worksheet_cell(ws,r,c); ev=erows[r][c]\n            if ak not in (\'numeric\',\'text\',\'structural_missing\'):\n                unresolved+=1\n                mism.append({\'kind\':\'unresolved_cell_semantics\',\'row\':r,\'column\':c,\'cell_kind\':ak,\'jnb\':av,\'csv\':ev})\n                continue\n            if ev==\'\':\n                missing+=1\n                if ak!=\'structural_missing\':mism.append({\'kind\':\'missing\',\'row\':r,\'column\':c,\'jnb\':av,\'cell_kind\':ak,\'csv\':\'\'})\n                continue\n            try:ef=float(ev)\n            except ValueError:ef=None\n            if ak==\'numeric\' and ef is not None:\n                numeric+=1; tol=_half_quantum(ev)+1e-12*max(1,abs(ef))\n                if abs(float(av)-ef)>tol:mism.append({\'kind\':\'numeric\',\'row\':r,\'column\':c,\'jnb\':av,\'csv\':ev,\'tolerance\':tol})\n            elif ak==\'text\' and ef is None:\n                text+=1\n                if av!=ev:mism.append({\'kind\':\'text\',\'row\':r,\'column\':c,\'jnb\':av,\'csv\':ev})\n            else:mism.append({\'kind\':\'type_or_value\',\'row\':r,\'column\':c,\'jnb\':av,\'cell_kind\':ak,\'csv\':ev})\n    return {\n      \'jnb\':str(jnb),\'csv\':str(expected),\'match\':not mism,\n      \'jnb_shape\':[len(rows),len(headers)],\'csv_shape\':[len(erows),len(eh)],\n      \'coverage\':\'full\' if len(headers)==len(eh) else (\'csv_subset_of_jnb\' if len(eh)<len(headers) else \'csv_wider_than_jnb\'),\n      \'numeric_cells_compared\':numeric,\'text_cells_compared\':text,\'structural_missing_cells_compared\':missing,\n      \'unresolved_cells_in_csv_coverage\':unresolved,\n      \'header_pairs\':list(zip(headers[:len(eh)],eh)),\n      \'mismatch_count\':len(mism),\'mismatches\':mism[:100]\n    }\n\ndef batch_validate(directory:Path):\n    pairs=[]\n    for jnb in sorted(directory.glob(\'*.JNB\'))+sorted(directory.glob(\'*.jnb\')):\n        csvp=jnb.with_suffix(\'.csv\')\n        if csvp.exists():pairs.append((jnb,csvp))\n    if not pairs:raise JNBError(f\'no same-name JNB/CSV pairs found in {directory}\')\n    results=[]\n    totals={\'pairs\':0,\'passed\':0,\'numeric_cells_compared\':0,\'text_cells_compared\':0,\'structural_missing_cells_compared\':0,\'unresolved_cells_in_csv_coverage\':0,\'mismatch_count\':0}\n    for jnb,csvp in pairs:\n        r=validate_jnb_csv(jnb,csvp);results.append(r)\n        totals[\'pairs\']+=1;totals[\'passed\']+=int(r[\'match\'])\n        for k in (\'numeric_cells_compared\',\'text_cells_compared\',\'structural_missing_cells_compared\',\'unresolved_cells_in_csv_coverage\',\'mismatch_count\'):\n            totals[k]+=r[k]\n    return {\'version\':VERSION,\'directory\':str(directory),\'totals\':totals,\'results\':results,\'match\':totals[\'passed\']==totals[\'pairs\']}\n\ndef batch_recover(directory:Path,outdir:Path):\n    jnbs=sorted(set(directory.glob(\'*.JNB\'))|set(directory.glob(\'*.jnb\')))\n    if not jnbs:raise JNBError(f\'no JNB files found in {directory}\')\n    results=[]\n    for jnb in jnbs:\n        target=outdir/jnb.stem\n        written=export_recovery(jnb,target)\n        results.append({\'jnb\':str(jnb),\'output\':str(target),\'files\':[str(x) for x in written]})\n    return results\n\ndef scan_jnb(path:Path):\n    wslist=recover_worksheets(path)\n    results=[]; total_cols=0; total_cells=0; interior=[]\n    for wi,w in enumerate(wslist):\n        total_cols+=len(w.columns); total_cells+=sum(len(c.cells) for c in w.columns)\n        for c in w.columns:\n            valid=[i for i,x in enumerate(c.cells) if x.kind in (\'numeric\',\'text\')]\n            if not valid:continue\n            lo,hi=min(valid),max(valid)\n            for ri in range(lo,hi+1):\n                x=c.cells[ri]\n                if x.kind in (\'numeric\',\'text\'):continue\n                # 0x12 is deliberately reported as ambiguous, not \'missing\'.\n                # SigmaPlot 7 fixtures demonstrate that tag 0x12 can also carry\n                # valid numeric payloads, so missing semantics cannot be inferred\n                # from the tag alone.\n                interior.append({\'worksheet\':wi,\'stream_path\':w.stream_path,\'column\':c.index,\'row\':ri,\'kind\':x.kind,\'tag\':x.tag})\n    return {\'version\':VERSION,\'jnb\':str(path),\'worksheets\':len(wslist),\'columns\':total_cols,\'cells\':total_cells,\'interior_ambiguous_count\':len(interior),\'interior_ambiguous\':interior[:1000]}\n\ndef cmd_scan(a): print(json.dumps(scan_jnb(Path(a.jnb)),indent=2,ensure_ascii=False));return 0\ndef cmd_inspect(a): print(json.dumps(list_ole_entries(Path(a.jnb)),indent=2,ensure_ascii=False));return 0\ndef cmd_recover(a):\n    for p in export_recovery(Path(a.jnb),Path(a.output),strict=a.strict):print(p)\n    return 0\ndef cmd_validate(a):\n    r=validate_jnb_csv(Path(a.jnb),Path(a.csv));print(json.dumps(r,indent=2,ensure_ascii=False));return 0 if r[\'match\'] else 2\ndef cmd_batch_validate(a):\n    r=batch_validate(Path(a.directory))\n    text=json.dumps(r,indent=2,ensure_ascii=False)\n    print(text)\n    if a.report:Path(a.report).write_text(text,encoding=\'utf-8\')\n    return 0 if r[\'match\'] else 2\ndef cmd_batch_recover(a):\n    r=batch_recover(Path(a.directory),Path(a.output));print(json.dumps(r,indent=2,ensure_ascii=False));return 0\ndef cmd_version(a):print(VERSION);return 0\n\ndef build_parser():\n    p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest=\'command\',required=True)\n    x=s.add_parser(\'inspect\');x.add_argument(\'jnb\');x.set_defaults(func=cmd_inspect)\n    x=s.add_parser(\'scan\');x.add_argument(\'jnb\');x.set_defaults(func=cmd_scan)\n    x=s.add_parser(\'recover\');x.add_argument(\'jnb\');x.add_argument(\'-o\',\'--output\',default=\'recovered\');x.add_argument(\'--strict\',action=\'store_true\',help=\'refuse CSV export if any cell has ambiguous semantics\');x.set_defaults(func=cmd_recover)\n    x=s.add_parser(\'validate\');x.add_argument(\'jnb\');x.add_argument(\'csv\');x.set_defaults(func=cmd_validate)\n    x=s.add_parser(\'batch-recover\');x.add_argument(\'directory\');x.add_argument(\'-o\',\'--output\',default=\'recovered_batch\');x.set_defaults(func=cmd_batch_recover)\n    x=s.add_parser(\'batch-validate\');x.add_argument(\'directory\');x.add_argument(\'--report\');x.set_defaults(func=cmd_batch_validate)\n    x=s.add_parser(\'version\');x.set_defaults(func=cmd_version)\n    return p\n\ndef main(argv:Sequence[str]|None=None):\n    a=build_parser().parse_args(argv)\n    try:return int(a.func(a))\n    except (JNBError,OSError) as e:print(f\'error: {e}\',file=sys.stderr);return 1\nif __name__==\'__main__\':raise SystemExit(main())\n'


def load_frozen_engine():
    """Verify and load the embedded MVP 0.3.0 recovery engine."""
    raw = FROZEN_ENGINE_SOURCE.encode("utf-8")
    actual_hash = hashlib.sha256(raw).hexdigest()

    if actual_hash != FROZEN_ENGINE_SHA256:
        raise RuntimeError(
            "Embedded recovery engine integrity check failed. "
            "The scientific parser source does not match the frozen build."
        )

    # dataclasses and some other stdlib features expect the executing
    # module to exist in sys.modules. Register a real in-memory module
    # before executing the frozen engine source.
    import sys
    import types

    module_name = "jnb_recover_frozen"
    module = types.ModuleType(module_name)
    module.__file__ = "<embedded:jnb_recover.py>"
    sys.modules[module_name] = module

    try:
        code = compile(
            FROZEN_ENGINE_SOURCE,
            module.__file__,
            "exec",
        )
        exec(code, module.__dict__)
    except Exception:
        # Do not leave a half-initialized module behind after a failed load.
        sys.modules.pop(module_name, None)
        raise

    actual_version = getattr(module, "VERSION", None)
    if actual_version != REQUIRED_ENGINE_VERSION:
        sys.modules.pop(module_name, None)
        raise RuntimeError(
            f"Wrong embedded recovery engine version: {actual_version!r}. "
            f"Required: {REQUIRED_ENGINE_VERSION}."
        )

    export_recovery = getattr(module, "export_recovery", None)
    if export_recovery is None:
        sys.modules.pop(module_name, None)
        raise RuntimeError(
            "Embedded recovery engine does not expose export_recovery()."
        )

    return module


def choose_jnb():
    """Open the native iOS Files picker and return the selected JNB path."""
    try:
        import file_system as fs
    except ImportError as exc:
        raise RuntimeError(
            "Pyto file_system module is unavailable. Run this script inside Pyto."
        ) from exc

    cancellation_type = getattr(fs, "FilePickerCancellation", None)

    try:
        # Explicitly declare the proprietary JNB extension.
        # Pyto converts this with UTType(filenameExtension:) before
        # presenting UIDocumentPickerViewController.
        selected = fs.import_file(file_extension="jnb")
    except Exception as exc:
        if cancellation_type is not None and isinstance(exc, cancellation_type):
            print("\nRESULT: CANCELLED")
            return None
        raise

    if not selected:
        print("\nRESULT: CANCELLED")
        return None

    source = Path(selected)

    if source.suffix.lower() != ".jnb":
        raise ValueError(
            f"Selected file is not a .JNB file: {source.name}"
        )

    if not source.exists():
        raise FileNotFoundError(
            f"Selected file is unavailable: {source}"
        )

    # Confirm that the picker result is actually readable before recovery.
    with source.open("rb") as handle:
        handle.read(8)

    return source


def make_output_dir(source):
    """
    Create a non-overwriting recovery directory under Pyto Documents.
    """
    documents = Path("~/Documents").expanduser()
    documents.mkdir(parents=True, exist_ok=True)

    base = documents / f"{source.stem}_recovered"
    if not base.exists():
        return base

    index = 2
    while True:
        candidate = documents / f"{source.stem}_recovered_{index}"
        if not candidate.exists():
            return candidate
        index += 1


def load_manifest(path):
    return json.loads(path.read_text(encoding="utf-8"))


def count_ambiguous(manifest):
    """
    Count ambiguous cells without altering engine semantics.
    """
    top = manifest.get("ambiguous_cells")
    if isinstance(top, list):
        return len(top)

    total = 0
    for worksheet in manifest.get("worksheets", []):
        cells = worksheet.get("ambiguous_cells")
        if isinstance(cells, list):
            total += len(cells)

    return total


def main():
    engine = load_frozen_engine()

    print(f"JNB Recover iPhone {WORKFLOW_VERSION}")
    print("Recovery engine:", engine.VERSION)
    print("Engine integrity: VERIFIED")
    print("Choose a SigmaPlot .JNB file in Files...")

    source = choose_jnb()
    if source is None:
        return None

    output = make_output_dir(source)

    # All JNB parsing remains inside the frozen engine.
    written = engine.export_recovery(source, output)

    manifest_path = output / "recovery_manifest.json"
    if not manifest_path.exists():
        raise RuntimeError(
            "Recovery engine did not create recovery_manifest.json"
        )

    manifest = load_manifest(manifest_path)
    ambiguous = count_ambiguous(manifest)
    worksheets = len(manifest.get("worksheets", []))

    print(f"\nJNB Recover iPhone {WORKFLOW_VERSION}")
    print("Recovery engine:", engine.VERSION)
    print("Engine integrity: VERIFIED")
    print("Source:", source.name)
    print("Worksheets:", worksheets)
    print("Output:", output)
    print("Files written:", len(written))

    if ambiguous:
        print("RESULT: RECOVERED WITH SCIENTIFIC WARNING")
        print("Ambiguous cells:", ambiguous)
        print("See recovery_manifest.json before scientific reuse.")
    else:
        print("RESULT: RECOVERED")
        print(
            "No ambiguous cells were reported by the supported parser."
        )

    return output


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nRESULT: FAILED")
        print(type(exc).__name__ + ":", exc)
        print("The source JNB was not modified.")
