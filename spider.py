import scrapy


class ProductsSpider(scrapy.Spider):
    name = "products"
    # allowed_domains = ["x"]
    start_urls = ["https://athena.eslite.com/api/v1/categories"]

    def parse(self, response):
        meta = response.meta
        categories = response.json()
        for cate in categories:
            meta['rootCateId'] = cate['id']
            meta['rootCateName'] = cate['description']
            if meta['rootCateName'] in ['家電']:
                url = 'https://athena.eslite.com/api/v2/search?final_price=0,&sort=manufacturer_date+desc&size=40&start=0&categories=["{}"]&exp=o'.format(
                    meta['rootCateId']
                )
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_root_category_v1,
                    meta=meta
                )

    def parse_root_category_v1(self, response):
        meta = response.meta
        resp = response.json()
        found = int(resp['hits']['found'])
        pages = found // 40
        for p in range(1, pages+1):
            url = 'https://athena.eslite.com/api/v2/search?final_price=0,&sort=manufacturer_date+desc&size=40&start={}&categories=["{}"]&exp=o'.format(
                p, meta['rootCateId']
            )
            yield scrapy.Request(
                url=url,
                callback=self.parse_root_category_v2,
                meta=meta
            )
        
        products = resp['hits']['hit']
        for prod in products:
            meta['dealId'] = prod['id']
            meta['dealName'] = prod['fields']['name']
            meta['saleUrl'] = prod['fields']['url']
            meta['mainImgUrl'] = response.urljoin(prod['fields']['product_photo_url'])
            meta['salePrice'] = prod['fields']['final_price']
            meta['marketPrice'] = prod['fields']['mprice']
            meta['barcode'] = prod['fields']['ean']
            meta['isbn'] = prod['fields']['isbn']
            meta['isbn10'] = prod['fields']['isbn10']
            meta['brandName'] = prod['fields']['brand']
            meta['stock'] = prod['fields']['stock']
            meta['categories'] = prod['fields']['categories']
            yield {
                'rootCateId': meta['rootCateId'],
                'rootCateName': meta['rootCateName'],
                'dealId': meta['dealId'],
                'dealName': meta['dealName'],
                'saleUrl': meta['saleUrl'],
                'mainImgUrl': meta['mainImgUrl'],
                'salePrice': meta['salePrice'],
                'marketPrice': meta['marketPrice'],
                'barcode': meta['barcode'],
                'isbn': meta['isbn'],
                'isbn10': meta['isbn10'],
                'brandName': meta['brandName'],
                'stock': meta['stock'],
                'categories': meta['categories']
            }

    def parse_root_category_v2(self, response):
        meta = response.meta
        resp = response.json()
        products = resp['hits']['hit']
        for prod in products:
            meta['dealId'] = prod['id']
            meta['dealName'] = prod['fields']['name']
            meta['saleUrl'] = prod['fields']['url']
            meta['mainImgUrl'] = response.urljoin(prod['fields']['product_photo_url'])
            meta['salePrice'] = prod['fields']['final_price']
            meta['marketPrice'] = prod['fields']['mprice']
            meta['barcode'] = prod['fields']['ean']
            meta['isbn'] = prod['fields']['isbn']
            meta['isbn10'] = prod['fields']['isbn10']
            meta['brandName'] = prod['fields']['brand']
            meta['stock'] = prod['fields']['stock']
            meta['categories'] = prod['fields']['categories']
            yield {
                'rootCateId': meta['rootCateId'],
                'rootCateName': meta['rootCateName'],
                'dealId': meta['dealId'],
                'dealName': meta['dealName'],
                'saleUrl': meta['saleUrl'],
                'mainImgUrl': meta['mainImgUrl'],
                'salePrice': meta['salePrice'],
                'marketPrice': meta['marketPrice'],
                'barcode': meta['barcode'],
                'isbn': meta['isbn'],
                'isbn10': meta['isbn10'],
                'brandName': meta['brandName'],
                'stock': meta['stock'],
                'categories': meta['categories']
            }
