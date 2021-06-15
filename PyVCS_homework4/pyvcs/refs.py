import pathlib
import typing as tp


def update_ref(git_dir: pathlib.Path, ref: tp.Union[str, pathlib.Path], new_value: str) -> None:
    with open(pathlib.Path(git_dir / ref), "w") as ref_file:
        ref_file.write(new_value)


def symbolic_ref(git_dir: pathlib.Path, name: str, ref: str) -> None:
    with open(git_dir / name, "w") as ref_file:
        ref_file.write(ref)


def ref_resolve(git_dir: pathlib.Path, ref_name: str) -> str:
    if ref_name == "HEAD":
        ref_name = get_ref(git_dir)

    if is_detached(git_dir):
        return ref_name

    with open(git_dir / pathlib.Path(ref_name), "r") as ref:
        data = ref.read()

    return data


def resolve_head(git_dir: pathlib.Path) -> tp.Optional[str]:
    refname = get_ref(git_dir)
    if not (git_dir / pathlib.Path(refname)).exists():
        return None
    with open(git_dir / pathlib.Path(refname), "r") as ref:
        data = ref.read()
    return data


def is_detached(git_dir: pathlib.Path) -> bool:
    with open(git_dir / "HEAD", "r") as head:
        data = head.read()
    if data[:3] == "ref":
        return False

    return True


def get_ref(git_dir: pathlib.Path) -> str:
    with open(git_dir / "HEAD", "r") as head:
        if not is_detached(git_dir):
            ref_name = head.read()[5:-1]
        else:
            ref_name = head.read()
    return ref_name
