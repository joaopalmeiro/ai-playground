from torchvision.transforms.functional import to_pil_image, to_tensor
from transformers import AutoImageProcessor
from transformers.image_utils import load_image

if __name__ == "__main__":
    image = load_image("example.png")
    image_tensor = to_tensor(image).unsqueeze(0)  # (batch_size, num_channels, height, width)

    processor = AutoImageProcessor.from_pretrained(
        "LiquidAI/LFM2-VL-1.6B", revision="2d27610bdbe667a7abafdfbc741655df3e190e9f"
    )

    new_width, new_height = processor.smart_resize(
        height=image_tensor.shape[2],
        width=image_tensor.shape[3],
        downsample_factor=processor.downsample_factor,
        min_image_tokens=processor.min_image_tokens,
        max_image_tokens=processor.max_image_tokens,
        encoder_patch_size=processor.encoder_patch_size,
    )

    tiles, grid_width, grid_height = processor.crop_image_to_patches(
        image=image_tensor,
        min_tiles=processor.min_tiles,
        max_tiles=processor.max_tiles,
        tile_size=processor.tile_size,
        use_thumbnail=processor.use_thumbnail,
        thumbnail_size=(new_height, new_width),
        interpolation=processor.resample,
        antialias=True,
    )

    print(f"Grid layout: {grid_width}x{grid_height}")
    print(f"Number of tiles (including thumbnail): {len(tiles[0])}")

    for i, tile in enumerate(tiles[0], start=0):
        tile_pil = to_pil_image(tile)

        tile_pil.save(f"tile_{i:02d}.png")
        print(f"Saved tile_{i:02d}.png - shape: {tile.shape}")
