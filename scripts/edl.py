"""Edit decision list.

Every piece plays the speaker's audio from `clip` over the source `ranges` (seconds).
Pauses inside a range are tightened automatically by build.py.

caption : corrected on-screen text (aligned to Whisper word timings by build.py).
broll   : list of (source_time_in_audio_clip, video_clip_or_None, video_in_seconds).
          From that moment the picture switches to the b-roll clip (None = back to the
          speaker in sync). Anchored to the audio clock so they survive pause trimming.
gfx     : list of (source_time, graphic_type, props) – motion graphics.
sfx     : list of (source_time, sound_name, volume).
zoom    : list of (source_time, scale) – punch-ins on the speaker (hides jump cuts).
"""

PIECES = [
    # ---------------------------------------------------------------- HOOK
    dict(
        id="hook", clip="0545", ranges=[(272.42, 279.56)], tighten=0.10,
        caption="Kalau mereka nak beli sayur-sayuran, buah-buahan, harga diskaun lagi 30%, boleh guna SARA.",
        gfx=[
            (272.42, "headline", dict(kicker="MULAI 1 JANUARI 2027", text="SARA BOLEH GUNA DI JUALAN AGRO MADANI", dur=5.6)),
            (277.90, "bigstat", dict(top="DISKAUN", value="30%", bottom="SEHINGGA", dur=2.2)),
        ],
        sfx=[(272.42, "impact_whoosh", 0.55), (272.6, "riser", 0.25), (277.90, "impact_logo", 0.5), (278.0, "coin_win", 0.35)],
        zoom=[(272.42, 1.12), (275.4, 1.0), (277.9, 1.22)],
    ),
    # ---------------------------------------------------------------- INTRO
    dict(
        id="intro", clip="0545", ranges=[(5.38, 22.72)], tighten=0.14,
        caption="Hari ini saya bersama dengan Pengarah FAMA Negeri Perlis, Encik Anzara Azizan, dan juga pasukan FAMA Negeri Perlis untuk meninjau aktiviti dan perjalanan di Pasar Tani Kekal Simpang 4, di Perlis ini.",
        broll=[(9.74, "0527", 1.2), (14.08, "0523", 49.5), (18.6, "0523", 157.5)],
        gfx=[(18.92, "location", dict(title="Pasar Tani Kekal Simpang 4", sub="Perlis", dur=4.2))],
        sfx=[(5.38, "whoosh_cine", 0.45), (9.74, "whoosh_fast", 0.3), (14.08, "whoosh_fast", 0.3), (18.92, "pop_long", 0.45)],
        zoom=[(5.38, 1.0), (8.4, 1.1)],
    ),
    # ---------------------------------------------------------------- WALKABOUT: TALKING TO VENDORS
    dict(
        id="v_kacau", clip="0523", ranges=[(23.75, 27.75)], tighten=None,
        caption="Niaga okey, sini? Okey. FAMA ada kacau tak? Tak.",
        gfx=[
            (23.75, "tag", dict(text="JALAN-JALAN PASAR TANI", dur=2.4)),
            (26.94, "sticker", dict(emoji="😄", dur=1.0)),
        ],
        sfx=[(23.75, "whoosh_cine", 0.35), (26.94, "pop_bubble", 0.6)],
        zoom=[(23.75, 1.0), (25.64, 1.14)],
    ),
    dict(
        id="v_daging", clip="0523", ranges=[(195.50, 198.62)], tighten=None, voice_gain=1.15,
        caption="RM28, kita jual RM26 sekilo. Oh, murah. Paling murah.",
        gfx=[(195.50, "price", dict(old="RM28", new="RM26", oldLabel="HARGA LUAR", newLabel="SEKILO DI SINI", strikeAt=1.1, dur=3.1))],
        sfx=[(195.45, "whoosh_fast", 0.3), (196.62, "coins", 0.5)],
        zoom=[(195.45, 1.06)],
    ),
    dict(
        id="v_habis", clip="0523", ranges=[(175.42, 179.08), (182.32, 184.78)], tighten=None,
        caption="Lama dah meniaga sini, okey? Boleh? Ini petang hari habis ya? Biasanya habis? Habis lah.",
        gfx=[(184.00, "stamp", dict(text="LAKU HABIS!", dur=1.3))],
        sfx=[(175.42, "whoosh_fast", 0.3), (184.00, "pop_hard", 0.45)],
        zoom=[(175.42, 1.0), (182.32, 1.1)],
    ),
    dict(
        id="v_kakjah", clip="0527", ranges=[(10.36, 11.22), (13.28, 14.60), (15.08, 16.45), (17.24, 19.28)], tighten=None,
        caption="Meniaga okey, kak? Antara orang yang lama. Haa, meniaga dekat sini. Dia punya killer produk ni.",
        broll=[(14.60, "0527", 19.0)],
        gfx=[
            (10.36, "tag", dict(text="GERAI KAK JAH", dur=2.4)),
            (18.10, "sticker", dict(emoji="🔥", dur=1.3)),
        ],
        sfx=[(10.36, "whoosh_air", 0.3), (14.60, "whoosh_fast", 0.25), (18.10, "pop_long", 0.45)],
        zoom=[(10.36, 1.0), (13.28, 1.1)],
    ),
    dict(
        id="v_original", clip="0527", ranges=[(31.48, 33.72), (35.40, 37.40)], tighten=None,
        caption="Tak buat yang color-color tu? Tak buat. Orang tak minat, orang nak yang original.",
        gfx=[(36.80, "stamp", dict(text="ORIGINAL!", dur=1.2))],
        sfx=[(36.80, "pop_hard", 0.4)],
        zoom=[(31.48, 1.06), (35.40, 1.16)],
    ),
    dict(
        id="v_bangun", clip="0528", ranges=[(5.48, 11.86), (13.26, 15.75)], tighten=None, voice_gain=1.2,
        caption="Pukul berapa bangun pagi-pagi ni? Kau ambil orang punya? Tak. Buat sendiri? Dia buat sendiri. Subhanallah. Empat pagi bangun lah. Tahajud dulu lah.",
        gfx=[(13.28, "bigstat", dict(bottom="PENIAGA KUIH TRADISIONAL", value="4 PAGI", top="DAH BANGUN!", dur=2.4))],
        sfx=[(5.48, "whoosh_fast", 0.3), (13.28, "impact_whoosh", 0.35)],
        zoom=[(5.48, 1.0), (9.66, 1.1), (13.26, 1.22)],
    ),
    # ---------------------------------------------------------------- COMBO MADANI
    dict(
        id="combo", clip="0545", ranges=[(148.82, 162.20)], tighten=0.12,
        caption="Sebentar tadi, seperti yang saya maklumkan, kita dah buat Combo Madani dengan jualan penjimatan 50% daripada harga pasaran luar. Yang asalnya RM24, tadi kita jual pada RM12.",
        drop_words=["bahagia"],
        broll=[(151.40, "0522", 79.0), (155.7, "0522", 87.0), (158.0, None, 0)],
        gfx=[
            (151.47, "combo", dict(title="SET COMBO MADANI", items=["Minyak masak", "Telur 1 papan", "Bawang"], dur=4.0)),
            (154.30, "stamp", dict(text="JIMAT 50%", dur=1.9)),
            (158.80, "price", dict(old="RM24", new="RM12", strikeAt=2.6, dur=4.3)),
        ],
        sfx=[(148.82, "whoosh_air", 0.22), (151.47, "pop_whoosh", 0.5), (154.30, "pop_hard", 0.5),
             (158.80, "swoosh_accent", 0.35), (161.45, "coins", 0.55)],
        zoom=[(158.0, 1.08), (161.5, 1.2)],
    ),
    # ---------------------------------------------------------------- LAUNCH (happy hour)
    dict(
        id="launch", clip="0522", ranges=[(52.55, 62.30)], tighten=0.12,
        caption="Maka saya umumkan, harga Happy Hour Set Combo Madani bernilai RM12, bermula sekarang!",
        gfx=[
            (52.55, "tag", dict(text="DETIK PELANCARAN", dur=3.0)),
            (61.10, "stamp", dict(text="HAPPY HOUR • RM12", dur=2.3, confetti=True)),
        ],
        sfx=[(52.55, "whoosh_cine", 0.4), (61.10, "impact_big", 0.4), (61.25, "applause_cheer", 0.45), (61.25, "achievement", 0.3)],
        zoom=[(52.55, 1.0), (55.0, 1.1), (61.1, 1.22)],
    ),
    dict(  # reaction: people collecting their yellow bags (no speech)
        id="react", clip="0522", ranges=[(64.6, 67.2)], tighten=None, voice_gain=0.35,
        caption="",
        broll=[(64.6, "0522", 81.5)],
        sfx=[],
    ),
    # ---------------------------------------------------------------- SARA
    dict(
        id="sara", clip="0545", ranges=[(237.33, 242.86), (248.86, 264.12)], tighten=0.12,
        caption="Bermula 1 Januari, sebagaimana diumumkan oleh YAB Perdana Menteri dalam bajet baru ini, SARA itu sendiri boleh digunakan untuk pembelian di Jualan Agro Madani. Dia bukan sahaja memberi keuntungan kepada pengguna, tapi juga kepada pengeluar dan usahawan. Harga yang kita tawarkan sehingga 30%.",
        broll=[(248.86, "0524", 0.4), (253.18, "0523", 232.0), (257.2, "0529", 1.0), (259.85, None, 0)],
        gfx=[
            (237.62, "calendar", dict(day="1", month="JANUARI", year="2027", dur=4.6)),
            (248.92, "sara", dict(title="SARA", sub="Boleh guna di Jualan Agro Madani", dur=4.2)),
            (255.60, "checklist", dict(items=[["Pengguna", 256.00], ["Pengeluar", 257.38], ["Usahawan", 258.82]], dur=4.2)),
            (261.80, "bigstat", dict(top="LEBIH MURAH", value="30%", bottom="SEHINGGA", dur=2.6)),
        ],
        sfx=[(237.33, "whoosh_air", 0.3), (237.62, "pop_long", 0.45), (248.86, "whoosh_fast", 0.3), (248.92, "correct", 0.35),
             (256.00, "click_ui", 0.6), (257.38, "click_ui", 0.6), (258.82, "click_ui", 0.6),
             (261.80, "impact_logo", 0.45)],
        zoom=[(259.85, 1.06), (262.6, 1.22)],
    ),
    # ---------------------------------------------------------------- SUPER EL NINO
    dict(
        id="elnino", clip="0545",
        ranges=[(285.10, 298.40), (306.95, 311.95), (323.55, 324.76), (332.78, 334.72), (370.70, 377.60)],
        tighten=0.12,
        caption="Baru-baru ini Jabatan Kaji Cuaca Malaysia telah mewar-warkan bahawa bermula November tahun ini, seluruh dunia akan mengalami satu fenomena yang namanya Super El Nino. Bila kepanasan yang melampau ni, banyak tanaman yang tak menjadi. Jadi apa yang FAMA dah buat? Kami telah mewujudkan satu task force. Bagi pihak FAMA, kami dah bersedia untuk penyediaan bekalan makanan sekurang-kurangnya 3 bulan.",
        broll=[(306.95, "0540", 86.0), (309.30, "0529", 24.0), (323.55, None, 0), (370.70, "0523", 88.0), (374.6, "0528", 28.0)],
        gfx=[
            (297.40, "warning", dict(text="SUPER EL NIÑO", sub="Bermula November 2026", dur=3.4)),
            (306.95, "heat", dict(dur=5.0)),
            (323.55, "question", dict(text="APA FAMA DAH BUAT?", dur=1.3)),
            (333.80, "tag", dict(text="✓ TASK FORCE DIBENTUK", dur=1.6)),
            (375.80, "bigstat", dict(top="BEKALAN MAKANAN", value="3 BULAN", bottom="SEKURANG-KURANGNYA", dur=2.6)),
        ],
        sfx=[(285.10, "whoosh_cine", 0.4), (297.40, "impact_whoosh", 0.45), (306.95, "whoosh_air", 0.3),
             (323.55, "swoosh_accent", 0.4), (333.80, "pop_hard", 0.45), (370.70, "whoosh_fast", 0.3),
             (375.80, "impact_logo", 0.4), (376.0, "positive", 0.3)],
        zoom=[(285.10, 1.0), (291.9, 1.1), (297.4, 1.2), (298.2, 1.0), (323.55, 1.18), (332.78, 1.06)],
    ),
    dict(
        id="outro", clip="0545", ranges=[(408.30, 412.40)], tighten=None,
        caption="Baik, terima kasih.",
        gfx=[(409.40, "endcard", dict(line1="Mulai 1 Januari 2027", line2="SARA boleh guna di Jualan Agro Madani", cta="Kongsi dengan keluarga & kawan!", dur=3.0))],
        sfx=[(409.40, "whoosh_cine", 0.35), (409.6, "positive", 0.3)],
        zoom=[(408.30, 1.0)],
    ),
]
