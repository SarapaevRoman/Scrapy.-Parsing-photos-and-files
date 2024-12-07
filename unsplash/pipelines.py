import hashlib
import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class CustomImagesPipeline(ImagesPipeline):
    
    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib. sha1(request.url.encode()).hexdigest()
        return f"{'categories'}/{image_guid}.jpg"
    

    def item_completed(self, results, item, info):
        #Проверка успешности загрузки
        if not any(result[0] for result in results):
            raise DropItem(f"Failed to download image for {item}")
        #Сохраняем локальные пути к изображениям
        item['images'] = [x['path'] for ok, x in results if ok]
        return item