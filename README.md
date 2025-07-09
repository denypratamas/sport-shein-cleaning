## 🧼 Data Cleaning Pipeline - Shein Sports & Outdoor Dataset

This notebook/project cleans and preprocesses messy product data scraped from Shein (specifically the Sports & Outdoor category) as part of the Dirty E-Commerce dataset on Kaggle.

## 📂 Source:
- [Dirty E-Commerce Data [80,000+ Products]](https://www.kaggle.com/datasets/oleksiimartusiuk/e-commerce-data-shein)

### 🔧 What’s Cleaned:
| Step | Description |
|------|-------------|
| 1. | Dropped noisy columns (like banners, unused images, and empty metadata) |
| 2. | Merged two broken product title columns into one (`goods-title-link--jump` + `goods-title-link`) |
| 3. | Cleaned `price` to float (removed `$`, fixed commas) |
| 4. | Transformed `discount` from string like `"25%"` to float (e.g., `25.0`) |
| 5. | Parsed `selling_proposition` like `"1.2k sold recently"` into integer values |
| 6. | Split `rank-title` (e.g., `#3 Best Sellers`) into two separate columns:
   - `rank_number`: integer (e.g., 3)
   - `rank_type`: string (e.g., "Best Sellers") |
| 7. | Cleaned `rank-sub` column into `rank_category` (e.g., "Dice games") |
| 8. | Added `is_ranked` flag (1 if product is ranked, 0 otherwise) |

### 💡 Notes:
- Kept `NaN` values where ranking or sales data was missing — we don’t fake it.
- All transformation logic is modular and lives in `utils.py`, so it’s reusable.
- Just call `clean_dataset(df)` and you're good.

> Built this to practice real-world data wrangling with semi-structured e-commerce data. Focused more on practical cleaning than overengineering.
> Feel free to contribute or suggest improvements!