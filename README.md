# Ozon Reviews

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
