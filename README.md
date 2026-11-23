# The Daily Picture — Monday, 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/AvinkLis/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/AvinkLis/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A newspaper front page that sums up 23 November 2026's world news in a
single image — drawn entirely in code with Pillow, no photographs, no
external assets. Entry for the
[make.fun news-image-20261123 competition](https://make.fun/bounty/news-image-20261123).

## The stories on the page

- **Lead — Antalya:** The UN's COP31 climate summit ends without a deal,
  closing as the longest climate conference in history after the EU and
  others reject the final draft over fossil fuels and finance.
- **Second lead — Strait of Hormuz:** At least three oil tankers are
  attacked in the strait and an Iranian strike hits an industrial site in
  Bahrain, as Tehran vows to confront the US naval blockade with all
  available tools.
- **Ukraine:** Kyiv says its naval drones sank the Russian corvette
  Mercury at Benghazi, Libya; Russian strikes kill at least 15 near Kyiv.
- **Nvidia:** Jensen Huang is reinstated as CEO weeks after his abrupt
  exit, in a reversal pressed by President Trump.
- **Spain:** The Supreme Court shelves the criminal case against Catalan
  leader Carles Puigdemont, clearing his return from nearly a decade of
  exile.
- **Bangladesh:** Dhaka vows to arrest and jail former prime minister
  Sheikh Hasina if she returns from India, and seeks her extradition.
- **Congo:** DR Congo suspends cobalt exports again from 30 November to
  tackle oversupply and weak prices.
- **Germany:** About 450 schools receive bomb threats by email on Monday
  morning, Bild reports.
- **United States:** Democrats reach at least 258 House seats — their
  largest majority since 1992 — as Trump moves to curb oversight.

## Run it

Requires Python 3 and Pillow (standard library + Pillow only):

```bash
python3 make_image.py   # draws entry.png in this directory
python3 main.py         # validates entry.png and copies it to $MAKEFUN_OUTPUT_DIR
```

`make_image.py` draws `entry.png` (1024×1024) deterministically; two
runs produce byte-identical output. At grade time `main.py` only
validates the committed `entry.png` and copies it byte-for-byte to
`$MAKEFUN_OUTPUT_DIR` (default `/output`).

## License

MIT — see [LICENSE](LICENSE).
