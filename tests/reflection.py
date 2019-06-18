
import discord.ext.commands as commands
import utils.dutils as dutils
import os
import sys
import inspect
import importlib
import importlib.util
import importlib.machinery
import pkgutil
import pathlib


importlib.machinery.SOURCE_SUFFIXES += ".pyi"


def get_doc(object):
    try:
        doc = object.__doc__
    except AttributeError:
        doc = None
    if not isinstance(doc, str):
        return None
    return doc


def is_docable(attr):
    if isinstance(attr, inspect.Attribute):
        member = attr.object
    else:
        member = attr
    if isinstance(member, commands.Command) or isinstance(member, dutils.EventLoop):
        return True
    return inspect.iscoroutinefunction(member) or inspect.isfunction(member) or inspect.ismethod(member) or \
        inspect.isasyncgenfunction(member) or inspect.isgeneratorfunction(member) or inspect.isclass(member) or \
        isinstance(member, property)


def classify_attr(cls, name, default=...):
    import types
    mro = inspect.getmro(cls)
    metamro = inspect.getmro(type(cls))  # for attributes stored in the metaclass
    metamro = tuple(cls for cls in metamro if cls not in (type, object))
    class_bases = (cls,) + mro
    all_bases = class_bases + metamro

    homecls = None
    get_obj = None
    dict_obj = None
    try:
        if name == '__dict__':
            raise Exception("__dict__ is special, don't want the proxy")
        get_obj = getattr(cls, name)
    except Exception:
        pass
    else:
        homecls = getattr(get_obj, "__objclass__", homecls)
        if homecls not in class_bases:
            # if the resulting object does not live somewhere in the
            # mro, drop it and search the mro manually
            homecls = None
            last_cls = None
            # first look in the classes
            for srch_cls in class_bases:
                srch_obj = getattr(srch_cls, name, None)
                if srch_obj is get_obj:
                    last_cls = srch_cls
            # then check the metaclasses
            for srch_cls in metamro:
                try:
                    srch_obj = srch_cls.__getattr__(cls, name)
                except AttributeError:
                    continue
                if srch_obj is get_obj:
                    last_cls = srch_cls
            if last_cls is not None:
                homecls = last_cls
    for base in all_bases:
        if name in base.__dict__:
            dict_obj = base.__dict__[name]
            if homecls not in metamro:
                homecls = base
            break
    if homecls is None:
        # unable to locate the attribute anywhere, most likely due to
        # buggy custom __dir__; discard and move on
        if default is ...:
            raise AttributeError(f"type object '{cls.__name__}' has no attribute '{name}'")
        else:
            return default
    obj = get_obj if get_obj is not None else dict_obj
    # Classify the object or its descriptor.
    if isinstance(dict_obj, (staticmethod, types.BuiltinMethodType)):
        kind = "static method"
        obj = dict_obj
    elif isinstance(dict_obj, (classmethod, types.ClassMethodDescriptorType)):
        kind = "class method"
        obj = dict_obj
    elif isinstance(dict_obj, property):
        kind = "property"
        obj = dict_obj
    elif inspect.isroutine(obj):
        kind = "method"
    else:
        kind = "data"
    return inspect.Attribute(name, kind, homecls, obj)


def get_declared(type, predicate=None):
    if not inspect.isclass(type):
        type = type.__class__
    attrs = inspect.classify_class_attrs(type)
    for item in attrs:
        if item.defining_class != type:
            continue
        elif not predicate or predicate(item):
            yield item


def _get_undoc_type(type):
    out = []

    if get_doc(type) is None:
        out.append((type.__name__, type))

    for attr in get_declared(type, is_docable):
        name = attr.name
        member = attr.object
        if inspect.isclass(member):
            out.extend(get_undoced(member))
        elif isinstance(member, commands.Command) or isinstance(member, dutils.EventLoop):
            if get_doc(member.callback) is None or member.description is "":
                out.append((name, member))
        else:
            if get_doc(member) is None:
                out.append((name, member))
    return out


def _get_undoc_pkg(pkg):
    found = False
    result = []
    for finder, pname, ispkg in pkgutil.walk_packages([f"./{pkg}"], f"{pkg}."):
        found = True
        if ispkg:
            continue
        pkg = importlib.import_module(pname)
        for name, member in inspect.getmembers(pkg, is_docable):
            if inspect.isclass(member):
                result.extend(get_undoced(member))
            elif get_doc(member) is None:
                result.append((name, member))
    if not found:
        raise FileNotFoundError("Unable to find any packages for the specified name")
    return result


def get_undoced(obj):
    if inspect.isclass(obj):
        return _get_undoc_type(obj)
    elif isinstance(obj, str):
        return _get_undoc_pkg(obj)
    else:
        raise TypeError("get_undoced invalid for non-class or package name type")


def walk_with_stubs(base_path, stub_dir="stub_files", skip_dirs=None, skip_files=None):

    base_path = pathlib.Path(base_path)
    base_stub_path = base_path / stub_dir
    if skip_dirs is None:
        skip_dirs = (stub_dir, "__pycache__")
    if skip_files is None:
        skip_files = ("__init__.py", "__main__.py")

    for path, dirs, files in os.walk(base_path):
        root_path = pathlib.Path(path)
        stub_path = base_stub_path / root_path.relative_to(base_path)

        remove = []
        for item in dirs:
            if item.startswith(".") or item in skip_dirs:
                remove.append(item)
        for item in remove:
            dirs.remove(item)

        files = list(filter(lambda x: x not in skip_files and x.endswith(".py"), files))

        for file in files:
            code_file = root_path / file
            stub_file = (stub_path / file).with_suffix(".pyi")
            yield code_file, stub_file


def _mod_from_path(path, base=None):
    temp = path.with_suffix("")
    if base is None:
        name = temp.name
    else:
        temp = temp.relative_to(base)
        name = ".".join(temp.parts)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if name not in sys.modules:
        sys.modules[name] = mod
    return mod


def walk_with_modules(base_path, stub_dir="stub_files", skip_dirs=None, skip_files=None):
    base_path = pathlib.Path(base_path)

    for code, stub in walk_with_stubs(base_path, stub_dir, skip_dirs, skip_files):
        if not code.exists() or not stub.exists():
            continue

        code_mod = _mod_from_path(code, base_path)
        stub_mod = _mod_from_path(stub, base_path)

        yield code_mod, stub_mod
