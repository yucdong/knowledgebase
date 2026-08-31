# two ways

file attachment

blob attachment: provide base64 directly

The runtime automatically processes images to fit within the model's constraints. No manual resizing is required.

Images that exceed the model's dimension or size limits are automatically resized (preserving aspect ratio) or quality-reduced.
If an image cannot be brought within limits after processing, it is skipped and not sent to the LLM.
The model's capabilities.limits.vision.max_prompt_image_size field indicates the maximum image size in bytes.

Not all models support vision. Check the model's capabilities before sending images.

```ts
interface VisionCapabilities {
    vision?: {
        supported_media_types: string[];
        max_prompt_images: number;
        max_prompt_image_size: number; // bytes
    };
}
```

tips:

use png or jpeg directly
keep images reasonably sized
use absolute path for file attachments
use blob attachments for in-memory data
check vision support first
multiple images are supported
svg is not supported