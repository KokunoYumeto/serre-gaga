# Checkpoint and final-package creation

`package_deliverable.py` creates a complete snapshot of the current deliverables.
It never schedules itself, waits for an hour, uploads a file, or declares a
checkpoint persistently saved. Invoke it only when the actual hourly checkpoint
is due, or once the final deliverable is ready.

## First checkpoint

Run from the deliverable root:

```sh
python scripts/package_deliverable.py --root . --output-dir .. --kind checkpoint --number 1 --preflight
python scripts/package_deliverable.py --root . --output-dir .. --kind checkpoint --number 1
```

The first line of `progress.log` supplies the work-start timestamp. The script
refuses to create checkpoint 1 until at least one actual hour has elapsed. An
explicit `--work-start-utc` may supply that same timestamp if needed. Preflight
creates no archive and returns exit status 3 when the hour has not elapsed.

## Later checkpoints

Increment the checkpoint number by one, preserving all previous ZIPs. Supply
the actual UTC time at which the previous checkpoint was successfully saved
persistently, replacing the timestamp placeholder below:

```sh
python scripts/package_deliverable.py --root . --output-dir .. --kind checkpoint --number 2 --previous-save-utc "YYYY-MM-DDTHH:MM:SSZ" --preflight
python scripts/package_deliverable.py --root . --output-dir .. --kind checkpoint --number 2 --previous-save-utc "YYYY-MM-DDTHH:MM:SSZ"
```

The minimum interval is one hour. Page, section and layer boundaries do not
affect eligibility. A local archive creation time is not a successful-save time.
After successful upload, retain the returned save evidence and use its actual
time for the next checkpoint. The caller controls the sequential counter and
must account for checkpoints that remain only in persistent storage after an
environment restoration.

## Final ZIP

```sh
python scripts/package_deliverable.py --root . --output-dir .. --kind final --preflight
python scripts/package_deliverable.py --root . --output-dir .. --kind final
```

The final filename is `GAGA_CHECK.zip`; checkpoint filenames use
`GAGA_CHECK_checkpoint_NN.zip`. The script refuses any existing destination.
It first writes and verifies a temporary file, then publishes the ZIP through
an atomic operation that cannot replace a previous file. The output directory
must be outside the deliverable root.

## Inventory, exclusions and privacy

Every included file is hashed and rechecked while it is written. If a file
changes during packaging, the script stops and publishes no ZIP. Pause writes
to the deliverable tree while packaging. The archive adds:

- `PACKAGE_FILES.tsv`: byte sizes and SHA-256 hashes for every other member;
  its own hash is omitted to avoid a circular checksum.
- `PACKAGE_EXCLUSIONS.tsv`: the relative names and reasons for excluded files.
- `PACKAGE_INFO.md`: snapshot scope, timestamp and interpretation of the lists.

No owned deliverable is omitted merely because it is unchanged. The snapshot
is complete; therefore there are no unchanged omissions to assign to earlier
checkpoints. Current sources, records, scripts, sanitized build logs, final
PDFs and images already in `evidence/` are retained. Raw inputs, dependency
caches, rendered work images outside `evidence/`, generated source-directory
PDFs and logs, TeX/Python intermediate files, temporary files and earlier
archives are excluded. Use `--list-files` with preflight to inspect the exact
selection. The script does not follow symlinked directories and rejects a
symlink that would otherwise be an included file.

Returned UTF-8 text files are scanned for email addresses and recognizable
machine-local paths. Findings report the relative file, line and kind without
echoing the private string. Any finding stops packaging. The script does not
rewrite source text, credits or rights notices. Binary PDF/image content is
not inspected by this text privacy scan; the reader remains responsible for
the content and metadata of the final PDFs and evidence images.

The complete compressed ZIP is checked against a strict limit of 500,000,000
bytes and undergoes CRC and member-list verification. A package at or above
the limit is not published. Automatic splitting is not implemented; if this
limit is reached, the caller must create separate independent ZIP parts under
the requested naming convention and place their combined file list in part 1.

## Infrastructure validation

The script was exercised only on a separate synthetic fixture. Its complete
inventory hashes and exclusions were verified; a second write to the same
filename was rejected; an early-hour checkpoint preflight returned ineligible
without creating a checkpoint; a synthetic email finding blocked publication
without exposing the address; and a deliberately tiny size limit blocked the
test ZIP. No actual GAGA checkpoint was created by this infrastructure test.
