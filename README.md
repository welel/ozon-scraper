# Ozon Scraper

## Scraping Steps

1. Load categories

To start scrapping ...

```
python -m scrap.manage load_ozon_categories_from_api_results --path ../.vscode/categories_data
```

2. Set categories config or choose cats using cli args

## TODO

- [x] Interface via generic
- [x] create_or_update returns bool is_created
- [x] Bulk insert
- [ ] Add migration service
- [ ] Change logging prefix in yml
- [ ] Remove relative imports
- [ ] Add naming convention
- [ ] Add README.md
