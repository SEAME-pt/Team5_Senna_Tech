# Efficient Transfer and Synchronization Guide (`rsync` vs `scp`)

This document explains how to update files between machines efficiently, saving time and network bandwidth.

## 1. Why NOT use `scp` for updates?

The `scp` (Secure Copy) command is excellent for simple copies of a single file. However, for project folders:
- **It always overwrites everything:** It does not check whether the file already exists or changed; it just sends everything again.
- **It is slow on large folders:** If you change only one line in a 100 MB file, `scp` will send the full 100 MB again.
- **It does not remove deleted files:** If you remove a file at the source, it will still exist at the destination.

## 2. The Better Option: `rsync`

`rsync` (Remote Sync) is the standard tool for synchronization. It uses a delta-transfer algorithm, sending only the modified parts of files.

### Master synchronization command

```bash
rsync -avzP --delete /path/to/source/ user@host:/path/to/destination/
```

### What each flag does
- `-a` (**Archive**): preserves permissions, timestamps, symlinks, and subdirectories. This is the most important flag.
- `-v` (**Verbose**): shows the names of the files currently being transferred.
- `-z` (**Compress**): compresses data during transfer, which is usually faster over network connections.
- `-P` (**Progress/Partial**): shows a progress bar per file and allows interrupted transfers to be resumed.
- `--delete`: optionally removes files at the destination that no longer exist at the source, keeping both folders identical.

## 3. The trailing slash (`/`) matters

In `rsync`, a trailing slash on the source path changes the behavior:

1. **With slash (`folder/`)**: copies the **contents** of the folder.
   Result: the files from `folder/` appear directly in the destination.
2. **Without slash (`folder`)**: copies the **whole folder**.
   Result: a folder named `folder` is created inside the destination.

Recommendation: use the trailing slash when synchronizing projects:

```bash
rsync -avz /path/to/project/ user@host:/path/to/project/
```

## 4. Practical examples

### Update from your PC to the server (push)

```bash
rsync -avzP ~/project/ user@host:~/project/
```

### Update from your PC to the server excluding `hailo-env` and `shared_with_docker`

```bash
rsync -avz --progress --exclude 'hailo-env' --exclude 'shared_with_docker' /path/to/project/ user@host:~/project/
```

### Download updates from the server to your PC (pull)

```bash
rsync -avzP user@host:~/project/ ~/project/
```

### Dry run before transferring anything

Add `--dry-run` to preview what would be transferred without moving any data:

```bash
rsync -avzP --dry-run ~/project/ user@host:~/project/
```

## 5. Quick command summary

| Goal | Recommended command |
| :--- | :--- |
| Send one file quickly | `scp file.hef user@ip:/destination/` |
| Synchronize a full folder | `rsync -avzP --delete source/ user@ip:destination/` |
| Resume an interrupted transfer | `rsync -avzP source/ user@ip:destination/` |
| Preview changes without copying | `rsync -avzP --dry-run source/ user@ip:destination/` |

Generated for the Hailo/LKA project - 2026
