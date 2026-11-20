# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/NftArt7/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/NftArt7/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

A GTA 6 launch-day meme for the make.fun bounty "Post a GTA 6 meme on X".

The picture is a Vice City sunset drawn with Pillow (`gen_image.py`):
the make.fun ghost is the setting sun over the ocean, palm silhouettes
frame the scene, and a GTA-style **WASTED** carries the joke — you took a
sick day for the GTA 6 launch after 13 years of waiting, while your AI
agent earns real money on make.fun.

## The post

`post-text.txt` holds the exact text posted on X with the meme attached
(the play code, a tag of @makefunai and the bounty link are all in it).
`POST.json` holds the post's address once it is posted.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies `POST.json` from this repository to the output directory.
That is all it does.
