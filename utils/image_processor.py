
from io import BytesIO
from PIL import Image, ImageOps, UnidentifiedImageError

class ImageProcessor:
    MAX_SIZE = (1200, 1200)
    QUALITY = 78
    MAX_FILE_SIZE = 20 * 1024 * 1024

    @staticmethod
    def compress(image_path):
        try:
            with open(image_path, "rb") as file:
                file.seek(0, 2)
                if file.tell() > ImageProcessor.MAX_FILE_SIZE:
                    raise ValueError(
                        "Image must be smaller than 20 MB."
                    )

            with Image.open(image_path) as image:
                # Respect camera rotation metadata.
                image = ImageOps.exif_transpose(image)

                # Limit dimensions while preserving aspect ratio.
                image.thumbnail(
                    ImageProcessor.MAX_SIZE,
                    Image.Resampling.LANCZOS
                )

                # Convert transparency to a white background.
                if image.mode in ("RGBA", "LA") or (
                    image.mode == "P"
                    and "transparency" in image.info
                ):
                    image = image.convert("RGBA")
                    background = Image.new(
                        "RGB", image.size, "white"
                    )
                    background.paste(
                        image, mask=image.getchannel("A")
                    )
                    image = background
                else:
                    image = image.convert("RGB")

                buffer = BytesIO()
                image.save(
                    buffer,
                    format="JPEG",
                    quality=ImageProcessor.QUALITY,
                    optimize=True
                )

                return buffer.getvalue()

        except (UnidentifiedImageError, OSError) as error:
            raise ValueError(
                "The selected file is not a valid image."
            ) from error
