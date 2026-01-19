# Notes

- https://github.com/joaopalmeiro/template-python-uv-script
- https://huggingface.co/docs/transformers/main_classes/image_processor
- LFM2-VL:
  - https://huggingface.co/LiquidAI/LFM2-VL-1.6B
  - https://huggingface.co/docs/transformers/en/model_doc/lfm2_vl
    - https://huggingface.co/docs/transformers/en/model_doc/lfm2_vl#transformers.Lfm2VlImageProcessorFast
  - https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/image_processing_base.py#L522
  - https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/image_utils.py#L453
  - https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/lfm2_vl/image_processing_lfm2_vl_fast.py
    - `Lfm2VlProcessor`: https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/lfm2_vl/processing_lfm2_vl.py#L147
    - Default params: https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/lfm2_vl/image_processing_lfm2_vl_fast.py#L196-L218
    - `crop_image_to_patches()`: https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/lfm2_vl/image_processing_lfm2_vl_fast.py#L261-L307
    - `resize_and_split()`: https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/lfm2_vl/image_processing_lfm2_vl_fast.py#L361-L415
    - `smart_resize()` (similar to Qwen-VL): https://github.com/huggingface/transformers/blob/v4.57.6/src/transformers/models/lfm2_vl/image_processing_lfm2_vl_fast.py#L309-L310
- Torch:
  - https://docs.pytorch.org/vision/main/generated/torchvision.transforms.functional.to_tensor.html
  - https://docs.pytorch.org/vision/0.22/generated/torchvision.transforms.functional.resize.html:
    - "The corresponding Pillow integer constants, e.g. `PIL.Image.BILINEAR` are accepted as well."

## Commands

```bash
deactivate && uv venv && source .venv/bin/activate && uv pip install -r requirements.txt
```

```bash
uv venv && source .venv/bin/activate && uv pip install -r requirements.txt
```

### Clean slate

```bash
rm -rf .mypy_cache/ .ruff_cache/ .venv/
```
