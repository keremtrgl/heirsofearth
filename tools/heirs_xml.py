"""Heirs of Earth: tiny def model and XML writer.

A def is Def(cls, name, **fields). Field values may be str/int/float/bool, list (written as <li>),
dict (nested elements; key "@Class" becomes the Class attribute), T(en, tr) for translated text,
or Raw(xml) for hand-written XML. Every T is written in English into the def and collected for
the Turkish DefInjected file under its path (defName.field.sub, list items by index).
"""
from xml.sax.saxutils import escape


class T:
    def __init__(self, en, tr):
        self.en, self.tr = en, tr

    def __repr__(self):
        return f"T({self.en!r})"


class Raw:
    def __init__(self, xml):
        self.xml = xml


class Def:
    def __init__(self, cls, name=None, abstract_name=None, parent=None, abstract=False, inject_paths=None, **fields):
        self.cls, self.name, self.fields = cls, name, fields
        self.abstract_name, self.parent, self.abstract = abstract_name, parent, abstract
        # Optional overrides: {"comps.0.useLabel": "comps.CompUsable.useLabel"}
        self.inject_paths = inject_paths or {}


def fmt(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        s = f"{v:.4f}".rstrip("0").rstrip(".")
        return s if s not in ("", "-0") else "0"
    return str(v)


def _write(key, value, ind, out, path, tr):
    pad = "  " * ind
    if value is None:
        return
    if isinstance(value, Raw):
        out.append(f"{pad}<{key}>{value.xml}</{key}>")
        return
    if isinstance(value, T):
        out.append(f"{pad}<{key}>{escape(value.en)}</{key}>")
        tr.append((path, value))
        return
    if isinstance(value, dict):
        attrs = "".join(f' {k[1:]}="{v}"' for k, v in value.items() if k.startswith("@"))
        inner = {k: v for k, v in value.items() if not k.startswith("@")}
        if "#text" in inner:
            out.append(f"{pad}<{key}{attrs}>{escape(fmt(inner['#text']))}</{key}>")
            return
        if "#items" in inner:
            out.append(f"{pad}<{key}{attrs}>")
            for i, item in enumerate(inner["#items"]):
                _write("li", item, ind + 1, out, f"{path}.{i}", tr)
            out.append(f"{pad}</{key}>")
            return
        if not inner:
            out.append(f"{pad}<{key}{attrs} />")
            return
        out.append(f"{pad}<{key}{attrs}>")
        for k, v in inner.items():
            _write(k, v, ind + 1, out, f"{path}.{k}", tr)
        out.append(f"{pad}</{key}>")
        return
    if isinstance(value, (list, tuple)):
        if not value:
            out.append(f"{pad}<{key} />")
            return
        out.append(f"{pad}<{key}>")
        for i, item in enumerate(value):
            _write("li", item, ind + 1, out, f"{path}.{i}", tr)
        out.append(f"{pad}</{key}>")
        return
    out.append(f"{pad}<{key}>{escape(fmt(value))}</{key}>")


def render(defs):
    """Returns (xml_text, [(DefType, injectionPath, turkish)])."""
    out = ['<?xml version="1.0" encoding="utf-8"?>', "<Defs>"]
    tr_all = []
    for d in defs:
        attrs = ""
        if d.abstract_name:
            attrs += f' Name="{d.abstract_name}"'
        if d.parent:
            attrs += f' ParentName="{d.parent}"'
        if d.abstract:
            attrs += ' Abstract="True"'
        out.append(f"  <{d.cls}{attrs}>")
        local = []
        if d.name:
            out.append(f"    <defName>{d.name}</defName>")
        for k, v in d.fields.items():
            _write(k, v, 2, out, f"{d.name}.{k}", local)
        out.append(f"  </{d.cls}>")
        if d.name and not d.abstract:
            for p, text in local:
                tail = p[len(d.name) + 1:]
                p = f"{d.name}.{d.inject_paths.get(tail, tail)}"
                tr_all.append((d.cls, p, text))
    out.append("</Defs>")
    return "\n".join(out) + "\n", tr_all


def injection_xml(entries):
    out = ['<?xml version="1.0" encoding="utf-8"?>', "<LanguageData>"]
    for path, text in entries:
        out.append(f"  <{path}>{escape(text)}</{path}>")
    out.append("</LanguageData>")
    return "\n".join(out) + "\n"


def keyed_xml(pairs):
    out = ['<?xml version="1.0" encoding="utf-8"?>', "<LanguageData>"]
    for k, v in pairs:
        out.append(f"  <{k}>{escape(v)}</{k}>")
    out.append("</LanguageData>")
    return "\n".join(out) + "\n"
