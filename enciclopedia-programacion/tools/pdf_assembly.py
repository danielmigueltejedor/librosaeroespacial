"""Namespace internal PDF destinations before concatenating independent books."""
from io import BytesIO
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, IndirectObject, NameObject, TextStringObject


def namespace_destinations(reader, prefix: str):
    """Preserve each volume's TOC links when many books reuse chapter.1, etc."""
    destinations = reader.named_destinations
    renames = {name: prefix + ':' + name for name in destinations}
    seen = set()

    def visit(value):
        if isinstance(value, IndirectObject):
            identity = ('indirect', value.idnum, value.generation)
            if identity in seen:
                return
            seen.add(identity)
            value = value.get_object()
        identity = ('direct', id(value))
        if identity in seen:
            return
        seen.add(identity)
        if isinstance(value, DictionaryObject):
            for key, item in list(value.items()):
                if key == '/Dest' or key == '/D' and value.get('/S') == '/GoTo':
                    if isinstance(item, str) and str(item) in renames:
                        value[NameObject(key)] = TextStringObject(renames[str(item)])
            for item in value.values():
                visit(item)
        elif isinstance(value, (ArrayObject, list)):
            for item in value:
                visit(item)

    root = reader.trailer['/Root']
    visit(root)
    if destinations:
        entries = ArrayObject()
        for name, destination in sorted(destinations.items()):
            entries.extend([TextStringObject(renames[name]), destination.dest_array])
        names = root.get('/Names')
        if names is None:
            names = DictionaryObject()
            root[NameObject('/Names')] = names
        else:
            names = names.get_object()
        names[NameObject('/Dests')] = DictionaryObject({NameObject('/Names'): entries})

    # PdfReader caches named destinations. Re-read a serialized clone so the
    # public reader API sees the renamed tree, rather than mutating its cache.
    buffer = BytesIO()
    PdfWriter(clone_from=reader).write(buffer)
    return PdfReader(buffer)
