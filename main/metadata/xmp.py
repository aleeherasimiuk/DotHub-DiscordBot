import xmltodict

def get_metadata_from_xmp(stream):
    xmp_start = stream.find(b'<x:xmpmeta')
    xmp_end   = stream.find(b'</x:xmpmeta')
    xmp_str   = stream[xmp_start:xmp_end+12]
    if not xmp_str:
        return None
    metadata = xmltodict.parse(xmp_str)
    meta     = metadata["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]
    title    = meta["dc:title"]["rdf:Seq"]["rdf:li"]
    model    = meta["dc:model"]["rdf:Seq"]["rdf:li"]
    i        = meta["dc:i"]["rdf:Seq"]["rdf:li"]
    seed     = meta["dc:seed"]["rdf:Seq"]["rdf:li"]

    size = "Desconocida"
    if "dc:size" in meta:
        size = meta["dc:size"]["rdf:Seq"]["rdf:li"]

    input_images = False
    if "dc:input_images" in meta:
        input_images = meta["dc:input_images"]["rdf:Seq"]["rdf:li"]

    return {"title": title, "model": model, "i": i, "seed": seed, "size": size, "input_images": input_images }