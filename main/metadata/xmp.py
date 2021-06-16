import xmltodict

def get_metadata_from_xmp(stream):
    xmp_start = stream.find(b'<x:xmpmeta')
    xmp_end   = stream.find(b'</x:xmpmeta')
    xmp_str   = stream[xmp_start:xmp_end+12]
    if not xmp_str:
        return None
    metadata = xmltodict.parse(xmp_str)
    meta     = metadata["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]
    notebook = meta["dc:creator"]["rdf:Seq"]["rdf:li"]
    title    = meta["dc:title"]["rdf:Seq"]["rdf:li"]
    model    = meta["dc:model"]["rdf:Seq"]["rdf:li"]
    i        = meta["dc:i"]["rdf:Seq"]["rdf:li"]
    seed     = meta["dc:seed"]["rdf:Seq"]["rdf:li"]

    return {"notebook": notebook, "title": title, "model": model, "i": i, "seed": seed }