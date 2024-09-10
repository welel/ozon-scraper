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

- [x] refactor dto, repos on the top for bot
- [x] take out manage
- [x] update category loading
- parsers
    - [ ] products from cat page
    - [ ] reviews media from data-state
    - [ ] rest review from sliders


## Review Media Labling

### Label Studio

Label exported review media using [label-studio](https://labelstud.io/). Supports only images.

1. Export media files.

    ```bash
    cd src/
    python manage.py export_media --out-path <path> --media-type image --comment-count-ge 2 --skip-labeled
    ```
2. Install and start Label Studio.

    ```bash
    pip install label-studio
    label-studio start
    ```
3. Open [http://localhost:8080](http://localhost:8080), create a project with image classification label form. Use integer labels. Import data, label and export as JSON-MINI.

4. Load exported JSON-MINI labels.

    ```bash
    python manage.py import_label_studio_labels --file-path --path <path_to_json>
    ```
