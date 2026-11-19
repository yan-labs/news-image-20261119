# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/yan-labs/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/yan-labs/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up Thursday 19 November 2026's world news as a newspaper front page: the first-ever Trump–Xi–Putin trilateral summit in Shenzhen, GTA VI's worldwide launch, Anthropic's record $107.3bn IPO, Hegseth's surprise Venezuela defence pact, a record $190.4m Van Gogh sale, and Ethiopia–Eritrea clashes risking full-scale war. `tools/render.py` draws `entry.png` from the researched stories in `tools/stories.json` (AP, AFP, Reuters, The Japan Times, The Hindu, NDTV, Manila Times, SBS); `main.ts` validates the image against the competition gate (PNG/JPEG, ≤1 MiB, ≤1024×1024) and copies it to `/output/entry.png`.

## Run it

```sh
python3 tools/render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=2ybarezg&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
