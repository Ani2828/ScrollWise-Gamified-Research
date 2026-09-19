# ScrollWise — Dynamic Meme + Sticker Edition

This build keeps the research survey flow and sliding question windows, but makes the reaction layer dynamic.

## What's new
- A different original doodle meme variant is selected on every response.
- 108 local meme images: 3 variants for each of the 36 research questions.
- 9 local animated GIF sticker overlays (sparkle, heart, wow, sleepy, side-eye, nice, tap-tap, confetti, tiny-star).
- GIF stickers are decorative overlays; the main meme is a static image.
- Instagram-style framing is retained for selected social-media questions.
- Cute tap sound remains optional and can be switched off.
- No loud meme shout and no old double-tap / sound wording.
- Q36 text responses now unlock a meme after the first non-empty input.
- Tailwind CSS CDN is included for utility classes used in the UI, while the existing CSS remains as a fallback.

## Run
Open `frontend/index.html` with VS Code Live Server. The backend is optional unless you want to save responses into the research workbook.


## V3 Game Upgrade
- Fixed the Continue button state: it stays disabled until a valid response exists.
- Added XP, streak, and badge HUD. These are gameplay-only and do not alter research answers.
- Added a 3-tap emoji bonus round after Questions 5, 10, 15, 20, 25 and 30.
- Bonus rounds explicitly leave research data unchanged.
- XP is awarded once per question to prevent repeat navigation from inflating scores.
- Existing dynamic meme/GIF/sticker system and optional cute sound remain intact.
