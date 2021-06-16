from stegano import tools
import io, json

def extract_stegano_info(input_image, encoding="UTF-8"):
    """Find a message in an image (with the LSB technique)."""
    img = tools.open_image(input_image)
    width, height = img.size
    buff, count = 0, 0
    bitab = []
    limit = None
    for row in range(height):
        for col in range(width):
            # pixel = [r, g, b] or [r,g,b,a]
            pixel = img.getpixel((col, row))
            if img.mode == "RGBA":
                pixel = pixel[:3]  # ignore the alpha
            for color in pixel:
                buff += (color & 1) << (tools.ENCODINGS[encoding] - 1 - count)
                count += 1
                if count == tools.ENCODINGS[encoding]:
                    bitab.append(chr(buff))
                    buff, count = 0, 0
                    if bitab[-1] == ":" and limit is None:
                        try:
                            limit = int("".join(bitab[:-1]))
                        except Exception:
                            pass

            if len(bitab) - len(str(limit)) - 1 == limit:
                img.close()
                return "".join(bitab)[len(str(limit)) + 1:]

            if row > 1 and limit is None:  # Si no se ha encontrado mensaje en la primera línea, abortar
                return ""

def get_metadata_from_steno(stream):
    data = extract_stegano_info(io.BytesIO(stream))
    if not data:
        return None
    as_dict = json.loads(data)
    if "notebook" not in as_dict:
        as_dict.update(notebook="VQGAN+CLIP")
    if "creator" in as_dict:
        del as_dict["creator"]
    return as_dict