import os
import re
from django.conf import settings
from django.core.management.base import BaseCommand
from article.models import Article

class Command(BaseCommand):
    help = "刪除未被引用的 article_image 圖片"

    def handle(self, *args, **kwargs):
        image_dir = os.path.join(settings.MEDIA_ROOT, "article_image")

        if not os.path.exists(image_dir):
            self.stdout.write("找不到 article_image 資料夾")
            return

        #收集所有被引用的圖片檔名
        used_images = set()
        pattern = re.compile(r'src=["\']/media/article_image/([^"\']+)["\']')

        for article in Article.objects.all():
            content = article.content or ""
            matches = pattern.findall(content)
            used_images.update(matches)

        self.stdout.write(f"引用中的圖片數量: {len(used_images)}")

        #找出所有實際存在的圖片檔案
        all_images = set(os.listdir(image_dir))
        unused_images = all_images - used_images

        self.stdout.write(f"未被引用的圖片數量: {len(unused_images)}")

        #刪除未使用的圖片
        for img_name in unused_images:
            file_path = os.path.join(image_dir, img_name)
            try:
                os.remove(file_path)
                self.stdout.write(f"已刪除: {img_name}")
            except Exception as e:
                self.stdout.write(f"刪除失敗 {img_name}: {e}")
