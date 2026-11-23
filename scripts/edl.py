"""Edit decision list – Kunjungan Muhibah Persatuan Alumni FAMA (Pengerusi FAMA).

Every piece plays the speaker's audio from `clip` over the source `ranges` (seconds).
Pauses inside a range are tightened automatically by build.py.

caption : corrected on-screen text (aligned to Whisper word timings by build.py).
broll   : list of (source_time_in_audio_clip, video_clip_or_None, video_in_seconds).
          From that moment the picture switches to the b-roll clip (None = back to the
          speaker in sync). Anchored to the audio clock so they survive pause trimming.
gfx     : list of (source_time, graphic_type, props) – motion graphics.
sfx     : list of (source_time, sound_name, volume).
zoom    : list of (source_time, scale) – punch-ins on the speaker (hides jump cuts).
freeze  : source_time from which the picture freezes into a "photo" until the piece ends.
"""

PIECES = [
    # ---------------------------------------------------------------- HOOK
    dict(
        id="hook", clip="0444", ranges=[(8.86, 13.10)], tighten=0.10,
        caption="Jadi kalau kita jumpa orang bisu, kita boleh kata saya dari FAMA.",
        # picture: the whole group doing the FAMA hand sign, then back to him on "FAMA"
        broll=[(8.86, "0460", 2.7), (12.02, None, 0)],
        gfx=[
            (8.86, "headline", dict(kicker="ISYARAT TANGAN RASMI", text="🤟 'SAYA DARI FAMA'", dur=3.1)),
            (12.07, "sticker", dict(emoji="🤟", dur=1.2)),
        ],
        sfx=[(8.86, "pop_long", 0.40), (12.07, "pop_bubble", 0.55)],
        zoom=[(8.86, 1.0), (12.02, 1.16)],
    ),
    # ---------------------------------------------------------------- INTRO
    dict(
        id="intro", clip="0439", ranges=[(33.03, 39.80)], tighten=0.12,
        caption="Rombongan daripada Persatuan Alumni FAMA, ramai ini, semua bekas-bekas orang-orang hebat.",
        broll=[(35.95, "0442", 2.2), (38.09, "0447", 4.6)],
        gfx=[
            (33.03, "headline", dict(kicker="KUNJUNGAN MUHIBAH", text="PERSATUAN ALUMNI FAMA", dur=3.4)),
            (38.40, "sticker", dict(emoji="👏", dur=1.3)),
        ],
        sfx=[(33.03, "whoosh_cine", 0.22), (33.10, "pop_long", 0.40), (38.40, "pop_bubble", 0.5)],
        zoom=[(33.03, 1.0)],
    ),
    # ---------------------------------------------------------------- LAWYER: OPPONENT vs GUEST OF HONOUR
    dict(
        id="lawyer", clip="0439", ranges=[(47.35, 48.75), (50.80, 58.16)], tighten=0.10,
        caption="Of course lah, background lawyer kan. Kalau mahkamah itu, we need to know who is our opponent. Tapi dalam ini bukan opponent, it's our guest of honour.",
        gfx=[
            (47.40, "tag", dict(text="⚖️  LATAR BELAKANG: PEGUAM", dur=3.0)),
            (53.42, "sticker", dict(emoji="⚔️", dur=1.2)),
            (56.20, "stamp", dict(text="GUEST OF HONOUR", dur=2.2)),
        ],
        sfx=[(47.35, "whoosh_fast", 0.16), (47.40, "click_select", 0.45), (53.42, "pop_hard", 0.35),
             (56.20, "impact_logo", 0.40)],
        zoom=[(47.35, 1.0), (50.80, 1.12), (53.78, 1.0), (56.20, 1.2)],
    ),
    # ---------------------------------------------------------------- MEMORY
    dict(
        id="memory", clip="0440", ranges=[(2.42, 6.90)], tighten=0.10,
        caption="Sebab satu kelebihan jadi lawyer ni, memori apa nama tu, tu dah melekat lah.",
        gfx=[(4.50, "sticker", dict(emoji="🧠", dur=1.4))],
        sfx=[(4.50, "pop_bubble", 0.5)],
        zoom=[(2.42, 1.0), (4.50, 1.14)],
    ),
    dict(  # rattles off the alumni's names from memory – shown as a counter, not as (risky) spelled names
        id="names", clip="0440", ranges=[(14.66, 19.32)], tighten=None,
        caption="",
        gfx=[(14.66, "namecount", dict(label="NAMA DISEBUT TANPA TEKS", ticks=[14.66, 15.66, 16.34, 17.16, 18.76], dur=4.66))],
        sfx=[(14.66, "click_ui", 0.55), (15.66, "click_ui", 0.55), (16.34, "click_ui", 0.55),
             (17.16, "click_ui", 0.55), (18.76, "click_ui", 0.55), (18.90, "correct", 0.3)],
        zoom=[(14.66, 1.06), (16.34, 1.14), (18.76, 1.22)],
    ),
    # ---------------------------------------------------------------- LEGACY (shot is on the alumni)
    dict(
        id="legacy", clip="0439", ranges=[(94.74, 102.30)], tighten=0.10,
        caption="Masing-masing sudah melepasi zaman kegemilangan masing-masing, dan meninggalkan legasi yang cukup hebat pada saya.",
        broll=[(99.16, "0454", 2.5)],
        gfx=[(99.96, "stamp", dict(text="LEGASI HEBAT", dur=2.3))],
        sfx=[(94.74, "whoosh_cine", 0.2), (99.96, "impact_logo", 0.35), (100.05, "positive", 0.25)],
    ),
    # ---------------------------------------------------------------- HUMBLE: 4 TIMES POSTPONED
    dict(
        id="humble", clip="0445", ranges=[(0.0, 11.04)], tighten=0.12,
        caption="Sebenarnya nak minta maaf. Ini pertemuan kita berjaya dibuat hari ini selepas empat kali tunda. Empat kali tunda itu mungkin sebab kelemahan saya sendiri.",
        gfx=[
            (5.30, "bigstat", dict(bottom="PERTEMUAN INI", value="4 KALI", top="DITUNDA", dur=2.8)),
            (10.06, "sticker", dict(emoji="🙏", dur=1.3)),
        ],
        sfx=[(0.0, "whoosh_fast", 0.16), (5.30, "impact_big", 0.30), (10.06, "pop_bubble", 0.5)],
        zoom=[(0.0, 1.0), (1.94, 1.12), (5.30, 1.22), (8.18, 1.06)],
    ),
    # ---------------------------------------------------------------- ALUMNI'S VOICE
    dict(
        id="alumni1", clip="0448", ranges=[(14.01, 19.70)], tighten=0.12,
        caption="Jadi, kita buat kesatuan ini, kita boleh membantu. Sebenarnya, kita nak membantu rakan-rakan kita.",
        gfx=[(14.01, "tag", dict(text="🎙️  SUARA ALUMNI FAMA", dur=3.0)),
             (17.79, "sticker", dict(emoji="🤝", dur=1.4))],
        sfx=[(14.01, "whoosh_cine", 0.2), (14.05, "click_select", 0.45), (17.79, "pop_bubble", 0.5)],
        zoom=[(14.01, 1.0), (16.91, 1.12)],
    ),
    dict(
        id="alumni2", clip="0452", ranges=[(18.11, 26.70)], tighten=0.12,
        caption="Kita dihormati oleh pengeksport, transporter, forwarder, agen-agen pemasaran di dalam dan di luar negara.",
        gfx=[(18.43, "checklist", dict(title="FAMA DIHORMATI OLEH", items=[["Pengeksport", 19.91], ["Transporter", 21.17], ["Forwarder", 22.77], ["Agen pemasaran", 23.99]], dur=6.0)),
             (25.47, "sticker", dict(emoji="🌏", dur=1.3))],
        sfx=[(19.91, "click_ui", 0.55), (21.17, "click_ui", 0.55), (22.77, "click_ui", 0.55),
             (23.99, "click_ui", 0.55), (25.47, "pop_long", 0.35)],
        zoom=[(18.11, 1.0), (22.0, 1.1)],
    ),
    # ---------------------------------------------------------------- LIGHT MOMENT: BOWLING
    dict(
        id="bowling", clip="0457", ranges=[(61.49, 68.66), (71.99, 78.20)], tighten=0.10,
        caption="Ucap terima kasih juga lah alumni-alumni yang turun ke program-program, support kami punya ni. Kita dapat nombor 3. Tapi naik pentas, naik pentas, nombor 2. Turun pentas, silap kira!",
        gfx=[
            (61.49, "tag", dict(text="🎳  TERIMA KASIH ALUMNI", dur=2.8)),
            (68.17, "sticker", dict(emoji="🥉", dur=1.3)),
            (72.55, "price", dict(old="NO. 3", new="NO. 2", oldLabel="KIRAAN AWAL", newLabel="ATAS PENTAS", strikeAt=2.25, dur=3.6)),
            (77.27, "sticker", dict(emoji="😂", dur=1.2)),
        ],
        sfx=[(61.49, "whoosh_fast", 0.16), (61.55, "click_select", 0.45), (68.17, "pop_bubble", 0.5),
             (74.80, "pop_hard", 0.45), (77.27, "pop_bubble", 0.55)],
        zoom=[(61.49, 1.0), (66.21, 1.1), (71.99, 1.0), (74.95, 1.18), (77.27, 1.26)],
    ),
    # ---------------------------------------------------------------- PAYOFF: THE FAMA HAND SIGN
    dict(
        id="logo1", clip="0443", ranges=[(21.70, 25.14)], tighten=0.10,
        caption="Saya kata, oleh kerana dia lihat logo FAMA, kebetulan ada tiga garis.",
        broll=[(21.70, "0458", 0.4)],
        gfx=[(22.40, "fsign", dict(dur=3.4))],
        sfx=[(21.70, "riser", 0.22), (23.18, "swoosh_accent", 0.35), (24.44, "pop_hard", 0.35)],
    ),
    dict(
        id="logo2", clip="0444", ranges=[(1.34, 4.86)], tighten=0.10,
        caption="Daripada huruf F, dilencongkan tangan jadi sebegini.",
        gfx=[(3.04, "stamp", dict(text="🤟 ISYARAT FAMA", dur=2.0))],
        sfx=[(3.04, "impact_logo", 0.4), (3.10, "achievement", 0.25)],
        zoom=[(1.34, 1.08), (3.04, 1.2)],
    ),
    dict(
        id="maha", clip="0461", ranges=[(27.53, 31.75), (31.89, 34.96), (39.60, 44.20)], tighten=0.10,
        caption="Waktu MAHA itu, mana Jabatan Perikanan punya? Dia kata, cuma dia buat macam goyang. Saya kata, MAHA lagi dua tahun, semua agensi ada simbol.",
        gfx=[(27.53, "tag", dict(text="🎪  CERITA DI MAHA", dur=2.6)),
             (34.40, "sticker", dict(emoji="🐟", dur=1.3)),
             (42.56, "stamp", dict(text="SEMUA AGENSI ADA SIMBOL", dur=2.0))],
        sfx=[(27.53, "whoosh_fast", 0.16), (27.58, "click_select", 0.45), (34.40, "pop_bubble", 0.55),
             (42.56, "pop_hard", 0.4)],
        zoom=[(27.53, 1.0), (29.55, 1.1), (39.60, 1.0), (42.56, 1.14)],
    ),
    # ---------------------------------------------------------------- FINALE: GROUP PHOTO
    dict(
        id="finale", clip="0461", ranges=[(20.95, 25.75)], tighten=None, voice_gain=1.1,
        caption="Ready? Satu, dua, tiga!",
        freeze=23.35,
        gfx=[(23.45, "endcard", dict(line1="Kunjungan Muhibah", line2="Persatuan Alumni FAMA", cta="Kongsi dengan warga FAMA!", dur=2.0, fixedY=1330))],
        sfx=[(23.35, "shutter", 0.7), (23.40, "impact_logo", 0.30), (23.50, "applause_small", 0.35)],
        zoom=[(20.95, 1.0)],
    ),
]
