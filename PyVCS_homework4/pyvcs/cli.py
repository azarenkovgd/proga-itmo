import argparse

from pyvcs.index import ls_files, read_index, update_index
from pyvcs.objects import cat_file, hash_object
from pyvcs.porcelain import checkout, commit
from pyvcs.refs import ref_resolve, symbolic_ref, update_ref
from pyvcs.repo import repo_create, repo_find
from pyvcs.tree import commit_tree, write_tree


def cmd_init(args: argparse.Namespace) -> None:
    # TODO: Reinitialized existing pyvcs repository
    git_dir = repo_create(args.path)
    print(f"Initialized empty pyvcs repository in {git_dir.absolute()}")


def cmd_hash_object(args: argparse.Namespace) -> None:
    with args.path.open(mode="rb") as f:
        data = f.read()

    sha = hash_object(data, args.type, args.write)
    print(sha)


def cmd_cat_file(args: argparse.Namespace) -> None:
    cat_file(args.object, args.pretty)


def cmd_ls_files(args: argparse.Namespace) -> None:
    git_dir = repo_find()
    ls_files(git_dir, details=args.stage)


def cmd_update_index(args: argparse.Namespace) -> None:
    git_dir = repo_find()
    update_index(git_dir, args.paths, write=args.add)


def cmd_write_tree(args: argparse.Namespace) -> None:
    git_dir = repo_find()
    entries = read_index(git_dir)
    sha = write_tree(git_dir, entries)
    print(sha)


def cmd_commit_tree(args: argparse.Namespace) -> None:
    git_dir = repo_find()
    sha = commit_tree(git_dir, args.tree, args.message, args.parent)
    print(sha)


def cmd_update_ref(args: argparse.Namespace) -> None:
    git_dir = repo_find()
    update_ref(git_dir, args.ref, args.newvalue)


def cmd_rev_parse(args: argparse.Namespace) -> None:
    git_dir = repo_find()
    sha = ref_resolve(git_dir, args.rev)
    print(sha)


def cmd_symbolic_ref(args: argparse.Namespace) -> None:
    git_dir = repo_find()
    symbolic_ref(git_dir, args.name, args.ref)


def cmd_commit(args: argparse.Namespace) -> None:
    git_dir = repo_find()
    sha = commit(git_dir, args.message, args.author)
    print(sha)


def cmd_checkout(args: argparse.Namespace) -> None:
    git_dir = repo_find()
    checkout(git_dir, args.obj_name)
