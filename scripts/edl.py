"""Edit decision list – Lawatan Pengerusi FAMA ke Pusat Jualan & Agropelancongan Harumanis Y.A
(Kg. Baru Panggas, Chuping, Perlis – 10 November 2026).

Every piece plays the audio of `clip` over the source `ranges` (seconds).
Pauses inside a range are tightened automatically by build.py (`tighten` = gap kept, None = untouched).

caption : corrected on-screen text (aligned to Whisper word timings by build.py). "" = no captions.
ambient : natural sound only (applause, room) – not loudness-boosted like speech.
music   : music level while nothing is said in this piece ("up" = montage level).
broll   : list of (source_time_in_audio_clip, video_clip_or_None, video_in_seconds).
gfx     : list of (source_time, graphic_type, props) – motion graphics.
sfx     : list of (source_time, sound_name, volume).
zoom    : list of (source_time, scale) – punch-ins on the main face.

Story: hook (owner: "only a frame") -> RM195k payoff -> arrival -> orchard -> group photo (Pengerusi)
-> owner's thank-you speech -> grant -> "kuning ni premium" -> visitors' book -> group photo + end card.
"""

NAME = "Tuan Haji Abang Ahmad Kerdee"
ROLE = "Pengerusi FAMA"

PIECES = [
    # ---------------------------------------------------------------- HOOK: the owner's strongest line
    dict(
        id="hook", clip="0565", ranges=[(17.40, 21.58)], tighten=0.10,
        caption="Cuma ada rangka saja yang saya buat. Rangka tiang, rangka bumbung...",
        gfx=[(17.45, "tag", dict(text="PENGUSAHA HARUMANIS Y.A", dur=4.0))],
        sfx=[(17.45, "pop_whoosh", 0.35), (20.10, "riser", 0.22)],
        zoom=[(17.40, 1.10), (19.66, 1.22)],
    ),
    # ---------------------------------------------------------------- payoff: the cheque (natural applause)
    dict(
        id="cheque", clip="0566", ranges=[(10.45, 12.75)], tighten=None, ambient=True, voice_gain=0.55, music="up",
        caption="",
        gfx=[(10.50, "bigstat", dict(bottom="GERAN NAIK TARAF", value="RM195,000", top="UNTUK HARUMANIS Y.A", dur=2.3))],
        sfx=[(10.50, "impact_big", 0.42), (10.62, "coin_win", 0.22)],
        zoom=[(10.45, 1.0), (10.50, 1.08)],
    ),
    # ---------------------------------------------------------------- arrival montage (music carries it)
    dict(
        id="arrive", clip="0550", ranges=[(8.0, 15.4)], tighten=None, ambient=True, voice_gain=0.4, music="up",
        caption="",
        broll=[(10.55, "0558", 0.6), (12.75, "0554", 22.6)],
        gfx=[
            (8.05, "beforeafter", dict(before="RANGKA TIANG & BUMBUNG", after="PUSAT AGROPELANCONGAN", dur=2.5)),
            (10.70, "location", dict(title="Harumanis Y.A", sub="Kg. Baru Panggas, Chuping, Perlis", dur=4.6)),
        ],
        sfx=[(8.05, "whoosh_cine", 0.18), (8.95, "click_ui", 0.5), (9.25, "pop_hard", 0.35), (10.70, "pop_long", 0.4)],
        zoom=[(8.0, 1.0), (12.75, 1.06)],
    ),
    # ---------------------------------------------------------------- orchard
    dict(
        id="orchard", clip="0554", ranges=[(0.2, 4.6)], tighten=None, ambient=True, voice_gain=0.3, music="up",
        caption="",
        broll=[(2.4, "0554", 5.6)],
        gfx=[
            (0.30, "tag", dict(text="KEBUN MANGGA HARUMANIS", dur=4.1)),
            (1.40, "sticker", dict(emoji="🥭", dur=2.0)),
        ],
        sfx=[(1.40, "pop_bubble", 0.45)],
        zoom=[(0.2, 1.0), (2.4, 1.08)],
    ),
    # ---------------------------------------------------------------- group photo at the FAMA agrotourism sign (Pengerusi speaks)
    dict(
        id="photo", clip="0554", ranges=[(62.05, 64.02), (65.18, 66.55)], tighten=None, voice_gain=1.0,
        caption="Kita tunjuk agropelancongan kita. Satu, dua, tiga!",
        gfx=[
            (62.10, "nametag", dict(name=NAME, role=ROLE, dur=3.3)),
            (66.15, "flash", dict(dur=0.4)),
        ],
        sfx=[(66.12, "shutter", 0.65)],
        zoom=[(62.05, 1.0), (65.18, 1.06)],
    ),
    # ---------------------------------------------------------------- the owner's thank-you speech
    dict(
        id="speech", clip="0565", ranges=[(0.70, 8.40), (9.70, 17.25), (23.40, 30.0)], tighten=0.12,
        caption="Saya rakamkan jutaan terima kasih kepada Pengarah FAMA, timbalan-timbalan dan juga rakan-rakan FAMA. "
                "Tanpa usaha dan sokongan tuan-tuan dan puan-puan, mungkin tidak adalah apa yang kita ada hari ini di sini. "
                "Maka datanglah sokongan dan sumbangan ini, maka inilah yang kita ada.",
        broll=[(3.30, "0560", 1.2), (5.40, "0558", 12.0), (9.70, None, 0), (23.40, "0566", 21.0), (27.30, "0563", 14.4)],
        gfx=[
            (0.75, "tag", dict(text="UCAPAN PENGUSAHA", dur=2.5)),
            (11.10, "sticker", dict(emoji="🤝", dur=1.6)),
        ],
        sfx=[(0.75, "whoosh_air", 0.14), (11.10, "pop_bubble", 0.4)],
        zoom=[(9.70, 1.04), (12.70, 1.16), (16.40, 1.24)],
    ),
    # ---------------------------------------------------------------- the grant (applause)
    dict(
        id="grant", clip="0566", ranges=[(13.0, 16.6)], tighten=None, ambient=True, voice_gain=0.55, music="up",
        caption="",
        gfx=[(13.15, "stamp", dict(text="TAHNIAH!", dur=2.4, confetti=True))],
        sfx=[(13.15, "impact_logo", 0.32), (13.30, "achievement", 0.25)],
        zoom=[(13.0, 1.0), (13.15, 1.1)],
    ),
    # ---------------------------------------------------------------- "kuning ni premium"
    dict(
        id="premium", clip="0566", ranges=[(59.95, 62.45)], tighten=None, voice_gain=0.9,
        caption="Kalau ikut tadi, kuning ni premium.",
        gfx=[(61.85, "stamp", dict(text="GRED PREMIUM", dur=1.5))],
        sfx=[(61.85, "pop_hard", 0.4)],
        zoom=[(59.95, 1.0), (61.40, 1.12)],
    ),
    # ---------------------------------------------------------------- visitors' book
    dict(
        id="book", clip="0552", ranges=[(0.4, 5.0)], tighten=None, ambient=True, voice_gain=0.35, music="up",
        caption="",
        broll=[(2.5, "0551", 0.4)],
        gfx=[(0.45, "tag", dict(text="✍️ TANDATANGAN BUKU PELAWAT", dur=4.4))],
        sfx=[(0.45, "pop_long", 0.35)],
        zoom=[(0.4, 1.0), (2.5, 1.06)],
    ),
    # ---------------------------------------------------------------- outro: group photo at the welcome banner
    dict(
        id="outro", clip="0554", ranges=[(99.2, 104.6)], tighten=None, ambient=True, voice_gain=0.3, music="up",
        caption="",
        gfx=[
            (99.25, "flash", dict(dur=0.4)),
            (99.80, "endcard", dict(line1="Dulu cuma rangka...", line2="Kini Pusat Agropelancongan Harumanis", cta="Jom singgah musim Harumanis!", dur=4.8)),
        ],
        sfx=[(99.22, "shutter", 0.55), (99.80, "positive", 0.3)],
        zoom=[(99.2, 1.0)],
    ),
]
