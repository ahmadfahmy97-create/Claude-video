"""Edit decision list – Lawatan Pengerusi FAMA ke Pusat Jualan & Agropelancongan Harumanis Y.A
(Kg. Baru Panggas, Chuping, Perlis – 10 November 2026).

v2: the story is the Pengerusi FAMA engaging with the pengusaha ("Cikgu") – asking, listening,
laughing, shaking hands, receiving his Harumanis.

Every piece plays the audio of `clip` over the source `ranges` (seconds).
Pauses inside a range are tightened automatically by build.py (`tighten` = gap kept, None = untouched).

caption : corrected on-screen text (aligned to Whisper word timings by build.py). "" = no captions.
ambient : natural sound only (applause, laughter, room) – not loudness-boosted like speech.
music   : music level while nothing is said in this piece ("up" = montage level).
cut     : "hard" = plain cut into this piece (no flash / push), for montage runs.
broll   : list of (source_time_in_audio_clip, video_clip_or_None, video_in_seconds).
gfx     : list of (source_time, graphic_type, props) – motion graphics.
sfx     : list of (source_time, sound_name, volume).
zoom    : list of (source_time, scale) – punch-ins on the main face.
"""

NAME = "Tuan Haji Abang Ahmad Kerdee"
ROLE = "Pengerusi FAMA"

PIECES = [
    # ---------------------------------------------------------------- HOOK: Pengerusi quizzes Cikgu about NUS
    dict(
        id="hook", clip="0556", ranges=[(6.02, 8.95), (13.30, 16.40), (17.86, 19.36)], tighten=0.10, voice_gain=1.1,
        caption="Cikgu, universiti apa yang... NUS? Singapura. Itu the best. Top 5. Sampai mereka pun mai buat kajian.",
        broll=[(6.02, "0556", 5.45), (6.75, None, 0)],  # someone walks in front of the lens at 6.2-6.7
        gfx=[
            (6.05, "nametag", dict(name=NAME, role=ROLE, dur=2.8)),
            (7.55, "sticker", dict(emoji="🎓", dur=1.5)),
            (15.40, "stamp", dict(text="TOP 5!", dur=1.0)),
        ],
        sfx=[(7.55, "pop_bubble", 0.45), (15.40, "pop_hard", 0.4), (18.30, "riser", 0.2)],
        zoom=[(6.02, 1.08), (13.30, 1.16), (17.86, 1.26)],
    ),
    # ---------------------------------------------------------------- turun padang: orchard with the pengusaha
    dict(
        id="kebun", clip="0554", ranges=[(0.0, 2.7)], tighten=None, ambient=True, voice_gain=0.35, music="up",
        caption="",
        gfx=[(0.05, "headline", dict(kicker="CHUPING, PERLIS", text="TURUN PADANG KE KEBUN HARUMANIS", dur=4.9))],
        sfx=[(0.05, "whoosh_cine", 0.16)],
        zoom=[(0.0, 1.0), (0.05, 1.06)],
    ),
    dict(
        id="kebun2", clip="0554", ranges=[(8.0, 10.25)], tighten=None, ambient=True, voice_gain=0.35, music="up", cut="hard",
        caption="",
        gfx=[(8.40, "sticker", dict(emoji="🥭", dur=1.6))],
        sfx=[(8.40, "pop_long", 0.4)],
        zoom=[(8.0, 1.04)],
    ),
    # ---------------------------------------------------------------- listening to the pengusaha's briefing
    dict(
        id="taklimat", clip="0550", ranges=[(75.6, 78.4)], tighten=None, ambient=True, voice_gain=0.45, music="up", cut="hard",
        caption="",
        gfx=[(75.65, "tag", dict(text="DENGAR SENDIRI DARI PENGUSAHA", dur=5.3))],
        sfx=[(75.65, "click_select", 0.4)],
        zoom=[(75.6, 1.0), (76.4, 1.1)],
    ),
    dict(
        id="taklimat2", clip="0550", ranges=[(100.0, 102.6)], tighten=None, ambient=True, voice_gain=0.45, music="up", cut="hard",
        caption="",
        zoom=[(100.0, 1.08)],
    ),
    # ---------------------------------------------------------------- the pengusaha's thanks, Pengerusi listening
    dict(
        id="ucapan", clip="0565", ranges=[(9.70, 17.25), (17.40, 21.58), (23.40, 27.35)], tighten=0.12,
        caption="Tanpa usaha dan sokongan tuan-tuan dan puan-puan, mungkin tidak adalah apa yang kita ada hari ini di sini. "
                "Cuma ada rangka saja yang saya buat. Rangka tiang, rangka bumbung... "
                "Maka datanglah sokongan dan sumbangan ini.",
        broll=[(13.36, "0558", 12.2), (15.95, None, 0)],
        gfx=[
            (9.75, "tag", dict(text="PENGUSAHA HARUMANIS Y.A", dur=3.4)),
            (17.90, "beforeafter", dict(before="RANGKA TIANG & BUMBUNG", after="PUSAT AGROPELANCONGAN", dur=3.6)),
        ],
        sfx=[(9.75, "whoosh_air", 0.14), (18.80, "click_ui", 0.45), (19.10, "pop_hard", 0.3)],
        zoom=[(9.70, 1.04), (16.0, 1.14), (19.66, 1.22), (23.40, 1.06)],
    ),
    # ---------------------------------------------------------------- handshake over the cheque (applause)
    dict(
        id="cek", clip="0566", ranges=[(14.6, 17.8)], tighten=None, ambient=True, voice_gain=0.55, music="up",
        caption="",
        gfx=[(14.70, "bigstat", dict(bottom="GERAN NAIK TARAF", value="RM195,000", top="UNTUK HARUMANIS Y.A", dur=3.0, confetti=True))],
        sfx=[(14.70, "impact_big", 0.4), (14.85, "coin_win", 0.22)],
        zoom=[(14.6, 1.0), (14.70, 1.08)],
    ),
    # ---------------------------------------------------------------- the gift: "kuning ni premium"
    dict(
        id="premium", clip="0566", ranges=[(58.2, 62.45)], tighten=None, voice_gain=0.9,
        caption="Kalau ikut tadi, kuning ni premium.",
        gfx=[
            (58.40, "sticker", dict(emoji="🥭", dur=1.5)),
            (61.85, "stamp", dict(text="GRED PREMIUM", dur=1.4)),
        ],
        sfx=[(58.40, "pop_bubble", 0.4), (61.85, "pop_hard", 0.4)],
        zoom=[(58.2, 1.0), (60.0, 1.1)],
    ),
    # ---------------------------------------------------------------- laughing together over the visitors' book
    dict(
        id="ketawa", clip="0552", ranges=[(21.2, 27.6)], tighten=None, ambient=True, voice_gain=0.75, music="up",
        caption="",
        gfx=[
            (21.25, "tag", dict(text="✍️ BUKU PELAWAT", dur=3.0)),
            (23.10, "sticker", dict(emoji="😄", dur=1.6)),
        ],
        sfx=[(23.10, "pop_long", 0.35)],
        zoom=[(21.2, 1.0), (24.6, 1.1)],
    ),
    # ---------------------------------------------------------------- group photo, Pengerusi counts it in
    dict(
        id="foto", clip="0554", ranges=[(62.05, 64.02), (65.18, 66.55)], tighten=None, voice_gain=1.0,
        caption="Kita tunjuk agropelancongan kita. Satu, dua, tiga!",
        gfx=[(66.15, "flash", dict(dur=0.4))],
        sfx=[(66.12, "shutter", 0.65)],
        zoom=[(62.05, 1.0), (65.18, 1.06)],
    ),
    dict(
        id="outro", clip="0554", ranges=[(99.2, 104.6)], tighten=None, ambient=True, voice_gain=0.3, music="up", cut="hard",
        caption="",
        gfx=[
            (99.25, "flash", dict(dur=0.4)),
            (99.70, "endcard", dict(line1="Pengerusi FAMA turun padang", line2="Bersama Pengusaha Harumanis Y.A",
                                    cta="Sokong usahawan tani kita!", dur=4.9)),
        ],
        sfx=[(99.22, "shutter", 0.5), (99.70, "positive", 0.3)],
        zoom=[(99.2, 1.0)],
    ),
]
