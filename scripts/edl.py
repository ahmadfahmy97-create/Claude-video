"""Edit decision list – Pengerusi FAMA's visit to PPDK ANIPS (Anak Istimewa Perlis).

v2 storyboard: hook -> how deaf jemaah pray -> the visit (founder, kids, kitchen,
greenhouse, therapy garden) -> why it matters to him -> FAMA's pasar tani plan.
No funding / donation segments.

Every piece plays the speaker's audio from `clip` over the source `ranges` (seconds).
Pauses inside a range are tightened automatically by build.py.

caption : corrected on-screen text (aligned to Whisper word timings by build.py).
broll   : list of (source_time_in_audio_clip, video_clip_or_None, video_in_seconds).
          From that moment the picture switches to the b-roll clip (None = back to the
          speaker in sync). Anchored to the audio clock so they survive pause trimming.
gfx     : list of (source_time, graphic_type, props) – motion graphics.
sfx     : list of (source_time, sound_name, volume).
zoom    : list of (source_time, scale) – punch-ins on the speaker (hides jump cuts).

The previous project's EDL (FAMA Pasar Tani Simpang 4) lives in git history.
"""

S = "0659"  # Pengerusi FAMA's talk at the centre

PIECES = [
    # ---------------------------------------------------------------- HOOK
    dict(
        id="hook", clip=S, ranges=[(344.40, 356.62)], tighten=0.12,
        caption="Kalau tuan-tuan solat dengan komuniti ni, saya percaya tuan-tuan akan khusyuk, tuan-tuan akan menangis, dan tuan-tuan akan rasa bertuahnya diri kita, sebab kita sempurna.",
        broll=[(349.62, "0646", 3.0), (351.40, "0647", 2.2), (353.12, None, 0)],
        gfx=[(344.45, "headline", dict(kicker="PENGERUSI FAMA", text="BILA SOLAT BERSAMA ANAK OKU", dur=3.9))],
        sfx=[(344.42, "woosh_reverb", 0.22), (349.62, "crystal_chime", 0.28), (355.56, "heartbeat", 0.7)],
        zoom=[(344.40, 1.0), (346.9, 1.1), (353.12, 1.04), (355.50, 1.22)],
    ),
    # ---------------------------------------------------------------- HOW THE DEAF PRAY IN JEMAAH
    dict(
        id="saf", clip=S,
        ranges=[(357.30, 358.80), (363.00, 368.95), (369.30, 371.45), (372.20, 374.32),
                (387.65, 391.65), (392.70, 396.85), (399.50, 400.84), (402.70, 403.95)],
        tighten=0.10,
        caption="Dia solat macam mana? Kalau kita yang sempurna ni, kita akan dengar imam, Allahu Akbar. Mereka pekak ni, dia tak dengar apa? Jadi kaedah yang mereka ajar, yang kanan sekali, waktu dia sujud, dia boleh tengok sikit yang kat depan, imam. So bila imam dah bergerak, yang kanan sekali akan tepuk yang sebelah dia. Yang sebelah akan tepuk yang sebelah, sampailah yang hujung.",
        broll=[(363.00, "0647", 9.0), (367.50, None, 0)],
        gfx=[
            (357.32, "question", dict(text="MACAM MANA MEREKA SOLAT?", dur=1.6)),
            (369.30, "sticker", dict(emoji="🧏", dur=1.6)),
            (387.65, "saf", dict(taps=[394.80, 400.12, 403.30], dur=11.0)),
        ],
        sfx=[(357.30, "whoosh_fast", 0.18), (357.32, "pop_bubble", 0.45), (369.30, "pop_long", 0.35),
             (387.65, "magic_sweep", 0.22), (394.80, "click_select", 0.55), (400.12, "click_select", 0.55),
             (403.30, "click_select", 0.55)],
        zoom=[(357.30, 1.12), (363.00, 1.0), (369.30, 1.15), (372.20, 1.0), (387.65, 1.0)],
    ),
    # ---------------------------------------------------------------- THE VISIT: ARRIVAL + FOUNDER
    dict(
        id="pengasas", clip="0651", ranges=[(3.90, 9.45), (11.95, 13.75), (18.20, 20.90)], tighten=0.12,
        caption="Sebab keperluan anak lah sebenarnya. Maksudnya tak ada tempat anak nak hantar ke mana. Kalau dulu, anak saya ni tak pernah pergi ke sekolah.",
        broll=[(3.90, "0688", 1.0), (5.60, "0642", 0.6), (8.00, "0651", 13.0), (18.20, None, 0)],
        gfx=[
            (3.95, "location", dict(title="PPDK ANIPS", sub="Pusat Pemulihan Dalam Komuniti • Perlis", dur=3.6)),
            (11.95, "tag", dict(text="PENGASAS PPDK ANIPS", dur=2.6)),
        ],
        sfx=[(3.90, "whoosh_cine", 0.2), (3.95, "pop_long", 0.4)],
        zoom=[(18.20, 1.08)],
    ),
    # ---------------------------------------------------------------- MEETING THE KIDS
    dict(
        id="salam", clip="0643", ranges=[(13.15, 17.35), (19.05, 21.30)], tighten=None, voice_gain=1.2,
        caption="Salam, Farhi. Salam. Boleh salam? Salam. Salam. Umur apa? Ini 22.",
        gfx=[(13.20, "tag", dict(text="BERTEMU ANAK-ANAK ANIPS", dur=2.8))],
        sfx=[(13.15, "whoosh_fast", 0.16), (16.64, "pop_bubble", 0.45)],
        zoom=[(13.15, 1.0), (19.05, 1.08)],
    ),
    # ---------------------------------------------------------------- WHY IT IS PERSONAL
    dict(
        id="kisah", clip=S, ranges=[(33.50, 43.60), (47.75, 49.20), (234.95, 242.40)], tighten=0.12,
        caption="Anak angkat yang ayah saya ambil, dia pula, dia bukan ambil yang normal. Dia ambil anak yang OKU. Dua orang, kakak saya lah. Dua-dua dah meninggal dunia. Golongan OKU asnaf ni tak jauh daripada diri saya sendiri. Sebab dia akan mengingatkan daripada mana saya datang.",
        broll=[(234.95, "0645", 34.0), (238.30, "0649", 27.0), (240.00, None, 0)],
        gfx=[(33.55, "tag", dict(text="KISAH PERIBADI", dur=2.6))],
        sfx=[(33.50, "whoosh_cine", 0.18), (47.75, "heartbeat", 0.45), (240.00, "bell_chime", 0.22)],
        zoom=[(33.50, 1.0), (38.4, 1.1), (47.75, 1.18), (234.95, 1.0), (240.00, 1.16)],
    ),
    # ---------------------------------------------------------------- KITCHEN: JELLY KERING
    dict(
        id="dapur1", clip="0664", ranges=[(10.40, 13.65)], tighten=None,
        caption="Alhamdulillah, sekarang ni anak-anak kita ni dah boleh buat secara berdikari.",
        broll=[(10.40, "0665", 2.0)],
        gfx=[(10.45, "tag", dict(text="DAPUR LATIHAN ANIPS", dur=2.8))],
        sfx=[(10.40, "whoosh_cine", 0.18)],
    ),
    dict(
        id="dapur2", clip="0665", ranges=[(7.62, 11.70), (16.55, 21.35)], tighten=0.12,
        caption="Jadi ni kami pilih jelly kering lah. Jelly kering ni dia mudah biasa kan. Dan kalau budak-budak ni silap ukur bahan tu tak ada masalah. Dia tak akan rosak produknya.",
        broll=[(7.62, "0666", 3.0), (9.94, "0672", 5.0), (16.55, "0665", 16.5), (19.30, "0657", 1.0)],
        gfx=[(19.30, "stamp", dict(text="PRODUK ANAK ANIPS", dur=2.0))],
        sfx=[(9.94, "pop_bubble", 0.4), (19.30, "pop_hard", 0.4)],
    ),
    # ---------------------------------------------------------------- GREENHOUSE
    dict(
        id="kebun", clip="0686", ranges=[(16.88, 23.85), (24.62, 32.52)], tighten=0.12,
        caption="So budak-budak ni sebenarnya, tanam sayur ni, dia orang sekejap je. Maksudnya settle, lepas tu dia dah lari lah. So kami kena sentiasa fikir pekerjaan-pekerjaan yang orang boleh buat untuk nak fulfill time dan energy dia tu.",
        broll=[(16.88, "0687", 11.0), (20.40, "0680", 1.0), (22.40, "0683", 2.5), (24.62, None, 0),
               (27.90, "0689", 4.0), (30.20, "0684", 30.0)],
        gfx=[(16.92, "tag", dict(text="RUMAH HIJAU & KEBUN TERAPI", dur=2.8))],
        sfx=[(16.88, "whoosh_cine", 0.18), (22.40, "pop_bubble", 0.35)],
        zoom=[(24.62, 1.06)],
    ),
    # ---------------------------------------------------------------- THERAPY GARDEN
    dict(
        id="laman", clip="0692", ranges=[(9.25, 17.02), (20.78, 22.80)], tighten=0.12,
        caption="So dekat sini, dia akan jadi ruang santai lah. So bila lepas dia orang buat aktiviti tanaman, pertanian dan apa semua ni, dia orang akan lepak kat sini lah. So ada trampolin, siapa nak lompat trampolin, lompat trampolin.",
        broll=[(9.25, "0693", 2.5), (12.20, None, 0), (20.78, "0692", 3.0)],
        gfx=[(9.30, "location", dict(title="Laman Terapi Hijau", sub="Ruang santai anak-anak ANIPS", dur=3.2))],
        sfx=[(9.25, "whoosh_cine", 0.18), (9.30, "pop_long", 0.35)],
    ),
    # ---------------------------------------------------------------- FAMA'S PLAN: 5 PASAR TANI WITH AN OKU LOT
    dict(
        id="pasartani", clip=S, ranges=[(632.15, 653.90)], tighten=0.12,
        caption="Saya punya planning, saya beritahu KP, tahun depan, saya tak nak yang 200 lebih punya pasar tani, saya nak pioneer paling kurang 5 pasar tani ada lot promosi OKU. Kita bagi peluang mereka untuk berniaga, sebab kalau FAMA tak bagi peluang, kita tak jadi contoh.",
        drop_words=["menaikah"],
        broll=[(634.26, "0662", 8.0), (637.10, "0657", 1.0), (639.24, None, 0),
               (644.96, "0672", 6.0), (648.38, "0686", 6.0), (651.10, None, 0)],
        gfx=[
            (634.26, "tag", dict(text="PERANCANGAN 2027", dur=2.8)),
            (640.42, "bigstat", dict(top="SEKURANG-KURANGNYA", value="5 PASAR TANI", bottom="ADA LOT PROMOSI OKU", dur=4.4)),
            (651.10, "stamp", dict(text="FAMA JADI CONTOH", dur=2.0)),
        ],
        sfx=[(632.15, "woosh_reverb", 0.18), (640.42, "trailer_impact", 0.26), (640.50, "positive", 0.22),
             (651.10, "pop_hard", 0.4)],
        zoom=[(632.15, 1.0), (639.24, 1.1), (642.3, 1.2), (651.10, 1.12)],
    ),
    # ---------------------------------------------------------------- CLOSING: THANK YOU + SALAM
    dict(
        id="terima", clip=S, ranges=[(689.60, 698.00)], tighten=0.12,
        caption="Jadi saya rasa saya ucapkan terima kasih kepada PPDK ANIPS ni juga, kerana menyambut kehadiran kami.",
        broll=[(689.60, "0687", 10.5), (693.10, "0693", 1.5)],
        sfx=[(689.55, "woosh_reverb", 0.14), (695.90, "harp_rise", 0.22)],
        soft=True,
    ),
    dict(
        id="outro", clip=S, ranges=[(738.85, 744.40)], tighten=None,  # runs past the clip end: silent tail under the end card
        caption="Assalamualaikum warahmatullahi wabarakatuh.",
        broll=[(738.85, "0694", 1.0)],
        gfx=[(740.35, "endcard", dict(line1="Lawatan ke PPDK ANIPS", line2="Pemerkasaan Anak Istimewa, Aspirasi Bersama", cta="Kongsi kalau anda tersentuh 🤍", dur=4.0))],
        sfx=[(740.35, "bell_chime", 0.3)],
        soft=True,
    ),
]
