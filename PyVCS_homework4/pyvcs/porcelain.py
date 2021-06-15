import os
import pathlib
import shutil
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(git_dir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(git_dir, paths, write=True)


def commit(git_dir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(git_dir, read_index(git_dir))
    return commit_tree(git_dir, tree, message, parent=None, author=author)


def checkout(git_dir: pathlib.Path, obj_name: str) -> None:
    update_ref(git_dir, "HEAD", obj_name)
    index_names = [entry.name for entry in read_index(git_dir)]
    _, commit_data = read_object(obj_name, git_dir)
    tree_hash = commit_parse(commit_data)
    files = find_tree_files(tree_hash, git_dir)
    to_update = [pathlib.Path(i[1]) for i in files]
    update_index(git_dir, to_update, write=True)

    for name in index_names:
        nodes = name.split(os.sep)
        if pathlib.Path(nodes[0]).is_dir():
            shutil.rmtree(nodes[0])
        else:
            if pathlib.Path(nodes[0]).exists():
                os.remove(nodes[0])

    for sha, name in files:
        if name.find(os.sep) != -1:
            prefix, _ = os.path.split(name)
            if not pathlib.Path(prefix).exists():
                os.makedirs(prefix)
        _, content = read_object(sha, git_dir)
        with open(name, "wb") as file_obj:
            file_obj.write(content)
