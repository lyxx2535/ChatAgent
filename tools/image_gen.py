from .base import BaseTool

class ImageGenTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="ImageGen",
            description="Generate an image based on a text description. Use this when the user asks to draw, generate, or create an image. Input: description of the image."
        )

    def run(self, query: str) -> str:
        # 模拟图像生成过程
        # 在真实场景中，这里会调用 DALL-E, Midjourney 或 Stable Diffusion API
        # 返回结果通常是图片的 URL 或本地路径
        
        # 为了演示，我们生成一个“模拟”的 Markdown 图片链接
        # 这里使用 placehold.co 服务来生成占位图，以便在 Markdown 预览中真正看到图片
        
        encoded_query = query.replace(" ", "+")
        image_url = f"https://placehold.co/600x400?text={encoded_query}"
        
        return f"![Generated Image]({image_url})"
