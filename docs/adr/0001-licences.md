# Content licensing strategy for mixed-ownership assets (code, scraped text, images)

## 1. Status: Accepted

## 2. Context

The project integrates three types of content with different rights origins: proprietary code, wiki-derived text under CC BY-SA, and third-party copyrighted images. It's necessary to have a per-item licensing strategy, not a single license for the entire repository.

## 3. Decision

Root LICENSE is MIT (code); wiki-derived content (data/episodes.json, future chunks) inherits CC BY-SA with per-fragment attribution (source_url, source_title); franchise images lack a specific license and rely on fair use (low resolution, attribution, non-commercial/transformative purpose, hotlinking instead of self-hosting).

Excluding fan art as an image source: this entails an additional layer of rights (held by the fan artist regarding their derivative work) alongside the original copyright, making it difficult to argue fair use against two separate rights holders.

## 4. Alternatives considered

(1) CC BY-NC-SA for all content — ruled out as incompatible with the ShareAlike clause of the CC BY-SA source (an NC restriction cannot be added to a BY-SA derivative);

(2) a single license for the entire repo — ruled out because it would not reflect the actual rights regarding each individual item.

## 5. Consequences

Mandatory attribution compliance for each scraped chunk; the fair use argument for images weakens if the project monetizes in the future; the "non-profit" statement of intent appears in the product disclaimer, not in a license file.

## 6. Date

August 21st, 2026.

## 7. Author

Iván Palacios Martínez
