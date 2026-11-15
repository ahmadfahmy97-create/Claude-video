"""Edit decision list – Libat Urus & Perjumpaan Kumpulan Sasar FAMA, Perlis (Pengerusi FAMA Malaysia).

Story: the question everyone asks ("FAMA buat apa?") -> the chairman's promise -> #FAMASantuni
-> "tonight we explain everything, ask anything" -> FAMA Perlis briefing -> questions from the floor
-> the chairman's answer -> KopieSatu in brief -> "the door of FAMA Perlis is open".

Every piece plays the speaker's audio from `clip` over the source `ranges` (seconds).
Range edges are snapped to the quietest 10 ms nearby and pauses inside a range are tightened by build.py.

caption : corrected on-screen text (aligned to Whisper word timings by build.py).
broll   : (source_time_in_audio_clip, video_clip_or_None, video_in_seconds). None = back to the speaker.
gfx     : (source_time, graphic_type, props). Props ending in `_t` are source times; build.py turns them
          into seconds relative to the graphic's start (key without `_t`). `items_t` = [[label, t], ...].
sfx     : (source_time, sound_name, volume).
zoom    : (source_time, scale) – punch-ins on the speaker.
"""

RAW_DIR = "/home/user/rawb"
S = "0561"  # the chairman's speech at the podium
SNAP = True  # snap range edges to the quietest 10 ms nearby

PIECES = [
    # ---------------------------------------------------------------- HOOK
    dict(
        id="hook", clip=S, ranges=[(104.30, 110.40)], tighten=0.10,
        caption="Soalan wajib yang orang ramai di luar sana tanya adalah... FAMA buat apa?",
        gfx=[
            (104.30, "search", dict(text="FAMA buat apa?", typeAt_t=108.15, typeDur=1.1,
                                    suggest=["mana pergi FAMA?", "FAMA tolong apa?", "FAMA bantu siapa?"], dur=6.4)),
        ],
        sfx=[(104.30, "whoosh_cine", 0.35), (108.15, "typing", 0.32), (110.05, "pop_hard", 0.4)],
        zoom=[(104.30, 1.12), (108.55, 1.32)],
    ),
    # ---------------------------------------------------------------- PROMISE
    dict(
        id="tegas", clip=S, ranges=[(461.78, 473.51)], tighten=0.12,
        caption="Apa pun terjadi, saya tidak mahu ada kedengaran lagi soalan-soalan ataupun persoalan yang timbul: FAMA tidak membantu.",
        broll=[(466.78, "0586", 0.6), (470.10, None, 0)],
        gfx=[
            (461.90, "lower", dict(name="Tuan Haji Abang Ahmad Kerdee", role="Pengerusi FAMA Malaysia", dur=4.2)),
            (471.43, "nope", dict(kicker="TAK MAHU DENGAR LAGI", text="FAMA TIDAK MEMBANTU", strike_t=472.95, dur=2.6)),
        ],
        sfx=[(461.90, "whoosh_air", 0.25), (471.43, "impact_big", 0.42), (472.95, "click_select", 0.5)],
        zoom=[(461.78, 1.0), (463.72, 1.14), (470.10, 1.0), (471.43, 1.28)],
    ),
    # ---------------------------------------------------------------- #FAMASANTUNI
    dict(
        id="santuni", clip=S, ranges=[(404.08, 408.66), (413.24, 418.95)], tighten=0.12,
        caption="Saya telah melancarkan satu tanda pagar. Apa slogan? Slogannya adalah FAMA Santuni.",
        broll=[(404.08, "0587", 0.8), (406.54, None, 0)],
        gfx=[
            (407.50, "tag", dict(text="# TANDA PAGAR", dur=2.2)),
            (416.80, "hashtag", dict(text="FAMASANTUNI", dur=3.9)),
        ],
        sfx=[(413.24, "pop_bubble", 0.45), (415.90, "riser", 0.3), (416.80, "impact_logo", 0.5), (416.85, "achievement", 0.25)],
        zoom=[(406.54, 1.08), (413.24, 1.2), (416.80, 1.34)],
    ),
    dict(
        id="lulus", clip=S, ranges=[(435.91, 439.30)], tighten=0.12,
        caption="Tapi tuan-tuan, santuni ni bukan maksudnya meluluskan.",
        gfx=[(438.30, "stamp", dict(text="SANTUNI ≠ LULUS", dur=1.9))],
        sfx=[(438.30, "pop_hard", 0.45)],
        zoom=[(435.91, 1.1), (437.70, 1.3)],
    ),
    # ---------------------------------------------------------------- "TONIGHT, ASK ANYTHING"
    dict(
        id="tanya", clip=S, ranges=[(356.60, 364.08)], tighten=0.12,
        caption="Jadi malam ni kita ceritakan habis kepada tuan-tuan dan puan-puan, apa itu FAMA. Kalau ada soalan, boleh tanya.",
        broll=[(357.74, "0585", 0.8), (359.54, "0563", 49.0), (361.88, None, 0)],
        gfx=[(361.88, "sticker", dict(emoji="🙋", dur=1.8))],
        sfx=[(356.60, "whoosh_fast", 0.3), (361.88, "pop_bubble", 0.5)],
        zoom=[(361.88, 1.16)],
    ),
    # ---------------------------------------------------------------- FAMA PERLIS BRIEFING
    dict(
        id="daftar", clip="0566", ranges=[(16.85, 21.61), (25.35, 29.49)], tighten=0.12,
        caption="Tuan-tuan boleh daftar dengan kami sebagai usahawan FAMA. Bila kita buka vendor, procurement dan sebagainya, kita akan buat jemputan kepada tuan-tuan.",
        gfx=[
            (16.85, "chapter", dict(kicker="BAHAGIAN 1", title="TAKLIMAT FAMA PERLIS", dur=2.4)),
            (25.35, "combo", dict(title="DAFTAR USAHAWAN FAMA", items=["Jemputan vendor", "Procurement"], dur=5.0)),
        ],
        sfx=[(16.85, "whoosh_cine", 0.35), (16.95, "impact_whoosh", 0.3), (25.35, "pop_long", 0.4)],
    ),
    dict(
        id="gerai", clip="0569", ranges=[(5.96, 9.26), (11.70, 14.70), (19.32, 25.16)], tighten=0.12,
        caption="So tuan-tuan yang ada peniaga buah, boleh mohon untuk naik taraf kedai tuan-tuan. Bukan kita bagi secara tunai, kita bagi secara komponen peralatan.",
        gfx=[
            (5.96, "tag", dict(text="NAIK TARAF GERAI BUAH", dur=3.0)),
            (19.54, "versus", dict(no="TUNAI", yesText="PERALATAN", yes_t=23.92, dur=5.6)),
        ],
        sfx=[(5.96, "whoosh_fast", 0.25), (19.54, "click_select", 0.45), (23.92, "correct", 0.35)],
        zoom=[(5.96, 1.0), (19.32, 1.12)],
    ),
    dict(
        id="dm", clip="0564", ranges=[(39.96, 46.36)], tighten=0.12,
        caption="Tuan-tuan DM lah. Facebook, TikTok, Instagram ni. InsyaAllah kita akan update.",
        gfx=[(40.06, "combo", dict(title="DM FAMA PERLIS", items=["Facebook", "TikTok", "Instagram"], dur=6.0))],
        sfx=[(40.06, "pop_long", 0.4), (41.44, "click_ui", 0.4), (42.18, "click_ui", 0.4), (42.60, "click_ui", 0.4)],
    ),
    # ---------------------------------------------------------------- QUESTIONS FROM THE FLOOR
    dict(
        id="q_bungkus", clip="0580", ranges=[(1.54, 9.64), (12.63, 15.09)], tighten=0.12, voice_gain=1.1,
        caption="Bimbingan untuk pembungkusan tu, adakah memang mesti produk makanan saja? Yang non-makanan boleh tak? Macam kami punya produk tu, kokopit tu lah.",
        gfx=[
            (1.54, "chapter", dict(kicker="BAHAGIAN 2", title="SESI SOAL JAWAB", dur=2.2)),
            (4.10, "qcard", dict(label="SOALAN PESERTA", text="Bantuan pembungkusan untuk produk bukan makanan?", dur=10.6)),
        ],
        sfx=[(1.54, "whoosh_cine", 0.35), (1.64, "impact_whoosh", 0.3), (4.10, "pop_bubble", 0.45)],
        zoom=[(1.54, 1.0), (7.40, 1.12)],
    ),
    dict(
        id="q_kelapa", clip="0581", ranges=[(13.14, 20.34), (30.90, 34.96)], tighten=0.12, voice_gain=1.1,
        caption="Selepas 4 tahun, kita tengok dalam konteks yang ada sekarang, kelapa sudah jatuh harga. Jadi bagaimana untuk masa hadapan kita?",
        broll=[(30.90, "0572", 1.0), (32.60, None, 0)],
        gfx=[(13.14, "qcard", dict(label="SOALAN PESERTA", text="Harga kelapa jatuh. Apa masa depan penanam?", dur=11.0))],
        sfx=[(13.14, "pop_bubble", 0.45), (18.16, "swoosh_accent", 0.3)],
        zoom=[(13.14, 1.0), (18.16, 1.12)],
    ),
    dict(
        id="jawab", clip="0584", ranges=[(1.06, 7.52), (9.22, 10.44), (10.89, 15.47)], tighten=0.12,
        caption="Bila disebut geran tadi, FAMA ataupun agensi, Jabatan Pertanian, dia tak bagi duit tau. Dia bagi barang, dia bagi benda.",
        gfx=[
            (1.06, "tag", dict(text="JAWAPAN PENGERUSI", dur=2.6)),
            (9.62, "versus", dict(no="DUIT", yesText="BARANG", yes_t=12.35, dur=5.2)),
        ],
        sfx=[(1.06, "whoosh_air", 0.25), (9.62, "click_select", 0.45), (12.35, "correct", 0.35)],
        zoom=[(1.06, 1.0), (9.22, 1.15)],
    ),
    # ---------------------------------------------------------------- KOPIESATU (short)
    dict(
        id="kopi", clip=S, ranges=[(700.68, 708.05)], tighten=0.12,
        caption="KopieSatu tuan-tuan, licensingnya RM20,000 lah. RM20,000 tu pula kita ikat selama lima tahun.",
        gfx=[
            (700.68, "tag", dict(text="☕ KOPIESATU", dur=2.0)),
            (701.98, "bigstat", dict(bottom="LESEN KOPIESATU", value="RM20K", top="IKAT 5 TAHUN", dur=5.2)),
        ],
        sfx=[(700.68, "whoosh_fast", 0.3), (701.98, "impact_whoosh", 0.42), (702.05, "coin_win", 0.3)],
        zoom=[(700.68, 1.0), (704.34, 1.14)],
    ),
    # ---------------------------------------------------------------- CLOSE
    dict(
        id="pintu", clip=S, ranges=[(386.94, 396.51)], tighten=0.12,
        caption="Saya buka pintu FAMA Negeri Perlis untuk tuan-tuan datang lagi sekali. Boleh tak boleh? Boleh jumpa dengan pengarah.",
        broll=[(393.99, "0591", 0.4), (395.07, None, 0)],
        gfx=[(389.21, "headline", dict(kicker="FAMA NEGERI PERLIS", text="PINTU SENTIASA TERBUKA", dur=4.6))],
        sfx=[(389.21, "pop_long", 0.4), (393.99, "applause_small", 0.22)],
        zoom=[(386.94, 1.0), (389.21, 1.12), (395.07, 1.22)],
    ),
    # ---------------------------------------------------------------- CLOSING STING (Pejabat Pengerusi FAMA)
    dict(
        id="closing", clip="closing", ranges=[(0.0, 5.0)], tighten=None, mute=True, plain=True,
        fit=dict(w=994, x=3),  # 16:9 logo on black, centred on the safe area (x 60-940)
        sfx=[(0.0, "whoosh_cine", 0.35), (0.40, "impact_logo", 0.45)],
    ),
]
