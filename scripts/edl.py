"""Edit decision list – PPDK Anak Istimewa Perlis visit (Pengerusi FAMA speech, clip 0659).

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

S = "0659"  # the speech

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
    # ---------------------------------------------------------------- BACKSTORY
    dict(
        id="kisah", clip=S, ranges=[(33.50, 49.20), (218.80, 224.45), (234.95, 242.40)], tighten=0.12,
        caption="Anak angkat yang ayah saya ambil, dia pula, dia bukan ambil yang normal. Dia ambil anak yang OKU. Dua orang, kakak saya lah. Jadi daripada tujuh jadi sembilan lah. Dua-dua dah meninggal dunia. Walaupun sebegini tuan-tuan, dua kakak itulah yang buat susu saya waktu saya kecil. Golongan OKU asnaf ni tak jauh daripada diri saya sendiri. Sebab dia akan mengingatkan daripada mana saya datang.",
        broll=[(234.95, "0649", 27.0), (240.00, None, 0)],
        gfx=[
            (33.55, "tag", dict(text="KISAH PERIBADI", dur=2.6)),
            (45.00, "bigstat", dict(top="ADIK-BERADIK", value="7 → 9", bottom="2 KAKAK ISTIMEWA", dur=2.7)),
        ],
        sfx=[(33.50, "whoosh_cine", 0.18), (45.00, "pop_long", 0.4), (47.80, "heartbeat", 0.45), (240.00, "bell_chime", 0.22)],
        zoom=[(33.50, 1.0), (38.4, 1.1), (47.80, 1.18), (218.80, 1.0), (222.3, 1.1), (240.00, 1.16)],
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
    # ---------------------------------------------------------------- RM100K – QURAN BAHASA ISYARAT
    dict(
        id="quran", clip=S, ranges=[(411.90, 415.05), (415.15, 427.45)], tighten=0.12,
        caption="Allah nak tunjuk pada saya tu. Saya balik tu, saya kata dengan tim saya, saya nak sumbangkan dana yang kita ada, 100 ribu saya bagi kepada Dr. Ahyari untuk Quran Bahasa Isyarat pertama di dunia.",
        gfx=[
            (420.62, "bigstat", dict(top="KEPADA DR. AHYARI", value="RM100K", bottom="SUMBANGAN", dur=3.3)),
            (424.30, "headline", dict(kicker="PERTAMA DI DUNIA", text="AL-QURAN BAHASA ISYARAT", dur=3.3)),
        ],
        sfx=[(411.90, "woosh_reverb", 0.16), (420.62, "trailer_impact", 0.26), (424.30, "harp_rise", 0.3)],
        zoom=[(411.90, 1.06), (415.15, 1.0), (418.3, 1.1), (420.62, 1.2), (424.30, 1.06)],
    ),
    # ---------------------------------------------------------------- THE FAMA SIGN
    dict(
        id="simbol", clip=S,
        ranges=[(437.40, 438.30), (439.10, 441.99), (446.04, 447.45), (452.30, 460.02),
                (478.15, 479.92), (494.35, 496.00), (497.40, 498.55)],
        tighten=0.10,
        caption="Bila saya dilantik jadi Pengerusi FAMA, orang yang pertama saya kontak, Doktor, saya nak minta tolong, bagi saya satu simbol untuk FAMA, yang kalau saya jumpa golongan ini, saya tunjuk, mereka faham saya daripada FAMA. Ini huruf F. Gerakkan daripada kiri ke kanan. FAMA.",
        broll=[(452.30, "0650", 38.0), (455.20, None, 0)],
        gfx=[
            (437.45, "tag", dict(text="SIMBOL FAMA", dur=2.4)),
            (478.15, "sign", dict(dur=5.6, fixY=360)),
        ],
        sfx=[(437.40, "whoosh_cine", 0.18), (478.15, "magic_sweep", 0.28), (497.40, "crystal_chime", 0.4)],
        zoom=[(437.40, 1.08), (446.04, 1.0), (455.20, 1.1), (478.15, 1.0)],
    ),
    # ---------------------------------------------------------------- 5 PASAR TANI WITH AN OKU LOT
    dict(
        id="pasartani", clip=S, ranges=[(632.15, 653.55)], tighten=0.12,
        caption="Saya punya planning, saya beritahu KP, tahun depan, saya tak nak yang 200 lebih punya pasar tani, saya nak pioneer paling kurang 5 pasar tani ada lot promosi OKU. Kita bagi peluang mereka untuk berniaga, sebab kalau FAMA tak bagi peluang, kita tak jadi contoh.",
        drop_words=["menaikah"],
        broll=[(634.26, "0665", 2.0), (637.10, "0657", 1.0), (639.24, None, 0),
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
    # ---------------------------------------------------------------- PAYOFF
    dict(
        id="lulus", clip=S, ranges=[(721.50, 726.08), (727.10, 730.02), (731.25, 736.95)], tighten=0.12,
        caption="Minta nanti puan buat satu paper, panjangkan kepada Pengerusi Yayasan Takwa. Just forward to me. I will make sure that berapa yang puan minta tu akan diluluskan, insyaAllah.",
        broll=[(721.50, "0660", 3.5), (724.85, "0687", 13.0), (731.25, None, 0)],
        gfx=[(735.93, "stamp", dict(text="AKAN DILULUSKAN ✓", dur=2.0))],
        sfx=[(721.50, "whoosh_cine", 0.18), (735.93, "impact_big", 0.3), (736.00, "achievement", 0.25)],
        zoom=[(731.25, 1.06), (733.6, 1.18)],
    ),
    dict(
        id="outro", clip=S, ranges=[(738.85, 742.60)], tighten=None,  # runs past the clip end: silent tail under the end card
        caption="Assalamualaikum warahmatullahi wabarakatuh.",
        broll=[(738.85, "0694", 1.0)],
        gfx=[(738.90, "endcard", dict(line1="PPDK Anak Istimewa Perlis", line2="Pemerkasaan Anak Istimewa, Aspirasi Bersama", cta="Kongsi kalau anda tersentuh 🤍", dur=3.6))],
        sfx=[(739.0, "bell_chime", 0.3)],
    ),
]
