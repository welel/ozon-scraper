# Ozon Reviews

## Plan

- [x] Get category catalog links
    - [x] Gather by hand 10 categories
- [x] Parse category page for product IDs
    - [x] Parse 10 categories by 100 pages with #product
- [ ] Parse product reviews content
    - Order and prioritize parsing order
    - Parse reviews with #review
    - Parse reviews media with #review_media

## TODO

- refactor dto, repos on the top for bot
- take out manage
- update category loading
- parsers
    - products from cat page
    - reviews media from data-state
    - rest review from sliders

## Details

- https://www.ozon.ru/product/479739633
- https://www.ozon.ru/product/479739633/videos
- https://www.ozon.ru/product/479739633/reviews

```
#product
id: int - PK - autoincrement
sku_id: 1589976777
name: Джинсы GATIN Бананы
price: 1883
original_price: 7000
stock: 32
rating: 4.9
review_count: 151
url:
image_url:

#review
id
parsed_by_product_id
sku_id
review_uuid
review_puuid
rating: 5
user_name: Светлана Т.
user_image_url:
comment_count:
url:
like_count:
dislike_count:
text:
advantages_text:
disadvantages_text:

pros/cons: https://www.ozon.ru/product/1415400098?reviewUuid=018e6618-0f91-95a4-9d14-9337b00e169b&reviewPuuid=018e6618-0fa5-2bc2-1545-5e945ed1d2c5

#review_media
id:
review_id:
type: video/image
url:
template_url:
extension:

#timestamps-mixin
created_at: timestamp
updated_at: timestamp

#product
id: int - PK - autoincrement
sku_id: bigint
name: string(1024)
price: int
original_price: int
stock: int
rating: float
review_count: int
url: string(2048)
image_url: string(2048)
+timestamps-mixin

#review
id: int - PK - autoincrement
parsed_by_product_id: int - FK - on #product.id 
sku_id: bigint
review_uuid: uuid
review_puuid: uuid
rating: int
user_name: string(64)
user_image_url: string(2048)
comment_count: int
url: string(2048)
like_count: int
dislike_count: int
text: text
advantages_text: text
disadvantages_text: text
+timestamps-mixin

pros/cons: https://www.ozon.ru/product/1415400098?reviewUuid=018e6618-0f91-95a4-9d14-9337b00e169b&reviewPuuid=018e6618-0fa5-2bc2-1545-5e945ed1d2c5

#review_media
id: int - PK - autoincrement
review_id: int - FK - on #review.id 
type: enum(video | image)
url: string(2048)
template_url: string(2048)
extension: string(16)
+timestamps-mixin
```