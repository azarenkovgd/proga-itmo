import os
import pathlib
import typing as tp


def repo_find(workdir: tp.Union[str, pathlib.Path] = ".") -> pathlib.Path:
    path = pathlib.Path(workdir)

    git_dir_name = os.getenv("GIT_DIR")
    if not git_dir_name:
        git_dir_name = ".git"

    git_dir = path / git_dir_name
    for parent in git_dir.parents:
        prefix, _ = os.path.split(parent)
        if str(parent) == prefix + f"/{git_dir_name}":
            git_dir = pathlib.Path(prefix + f"/{git_dir_name}")

    if git_dir.exists():
        return git_dir.absolute()

    raise Exception("Not a git repository")


def get_config_string(prefix, **kwargs):
    string = prefix
    buffer = '\n\t'

    for key, value in kwargs.items():
        if isinstance(value, bool):
            value = str(value).lower()
        string += buffer + f'{key} = {value}'
    string += '\n'

    return string


def repo_create(workdir: tp.Union[str, pathlib.Path]) -> pathlib.Path:
    path = pathlib.Path(workdir)

    if not path.is_dir():
        raise Exception(f"{path} is not a directory")
    git_dir_name = os.getenv("GIT_DIR")

    if not git_dir_name:
        git_dir_name = ".git"
    git_dir = path / git_dir_name

    if not git_dir.is_dir():
        os.makedirs(git_dir)
        os.makedirs(str(git_dir) + "/refs/heads")
        os.makedirs(str(git_dir) + "/refs/tags")
        os.makedirs(str(git_dir) + "/objects")

        with open(git_dir / "HEAD", "w") as head:
            head.write("ref: refs/heads/master\n")

        with open(git_dir / "config", "w") as config:
            str_for_configs = get_config_string(prefix='[core]', repositoryformatversion=0, filemode=True, bare=False,
                                                logallrefupdates=False)
            config.write(str_for_configs)

        with open(git_dir / "description", "w") as description:
            description.write("Unnamed pyvcs repository.\n")

    return git_dir
