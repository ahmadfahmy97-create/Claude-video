"""Edit decision list – Kunjungan hormat delegasi BPP Kamar Dagang Pengusaha Muda Indonesia ke FAMA
(19 Nov 2026, Dewan Bunga Raya, FAMA Point).

Same format as projects/fama-simpang4/edl.py (see scripts/build.py):
every piece plays the speaker's audio from `clip` over the source `ranges` (seconds);
broll / gfx / sfx / zoom are anchored to source-audio timestamps.
"""

RAW = "/home/user/raw2"
WORK = "/home/user/work2"

PIECES = [
    # ---------------------------------------------------------------- HOOK: 1 FAMA = 3 agensi Indonesia
    dict(
        id="hook", clip="0351", tighten=0.10,
        ranges=[(18.55, 23.66), (25.47, 26.82), (30.18, 31.42), (33.06, 34.36), (35.40, 36.12),
                (46.10, 47.82), (54.02, 55.80), (58.80, 60.98)],
        caption="FAMA ini, kalau dalam agensi di Republik Indonesia, ada tiga agensi setara dengan FAMA. "
                "Badan Pangan Nasional, BAPANAS. Badan Urusan Logistik, BULOG. Direktorat General Tanaman Pangan. "
                "Di Malaysia, kami rangkum 3 dalam 1.",
        gfx=[
            (18.55, "headline", dict(kicker="🇲🇾 MALAYSIA vs INDONESIA 🇮🇩", text="1 AGENSI = 3 AGENSI?", hi=["1", "3"], dur=4.6)),
            (33.06, "agencies", dict(items=[["BAPANAS", "Badan Pangan Nasional", 33.10],
                                            ["BULOG", "Badan Urusan Logistik", 46.12],
                                            ["DITJEN TP", "Direktorat Jenderal Tanaman Pangan", 54.05]],
                                     mergeAt=58.95, result="FAMA", resultSub="3 DALAM 1 🇲🇾", dur=9.0)),
        ],
        sfx=[(18.55, "riser", 0.22), (19.9, "impact_whoosh", 0.35), (33.10, "pop_whoosh", 0.45), (46.12, "pop_whoosh", 0.45),
             (54.05, "pop_whoosh", 0.45), (58.95, "swoosh_accent", 0.4), (60.30, "impact_big", 0.42), (60.35, "achievement", 0.25)],
        zoom=[(18.55, 1.0), (25.47, 1.12), (30.18, 1.0), (33.06, 1.08), (46.10, 1.0), (54.02, 1.1), (58.80, 1.0), (59.98, 1.25)],
    ),
    # ---------------------------------------------------------------- WELCOME
    dict(
        id="welcome", clip="0350", tighten=0.14,
        ranges=[(0.0, 7.10), (12.05, 18.70)],
        caption="Selamat datang ke kantor pusat FAMA Malaysia. Orang Malaysia kata, kecik tapak tangan, nyiru kami tadahkan kepada rombongan.",
        broll=[(0.0, "0347", 3.6), (3.4, None, 0)],
        gfx=[
            (0.25, "event", dict(kicker="SESI KUNJUNGAN HORMAT", title="Delegasi Pengusaha Muda Indonesia", sub="FAMA Point · 19 November 2026", dur=4.4)),
            (14.60, "proverb", dict(kicker="PERIBAHASA MELAYU", lines=["Kecil tapak tangan,", "nyiru kami tadahkan"],
                                     meaning="= sambutan paling ikhlas", muteCaptions=True, dur=4.4)),
        ],
        sfx=[(0.0, "whoosh_cine", 0.25), (0.35, "pop_long", 0.4), (14.60, "swoosh_accent", 0.35)],
        zoom=[(0.0, 1.0), (12.05, 1.08)],
    ),
    # ---------------------------------------------------------------- 34 BARANGAN
    dict(
        id="barangan", clip="0364", tighten=0.12,
        ranges=[(12.85, 28.30), (31.50, 37.92)],
        caption="Dari segi fokus, FAMA akan fokus kepada 34 barangan yang sepanjang masa FAMA kena pastikan wujud setiap hari di Malaysia. "
                "Wujud itu pula tidak boleh kurang, dia mesti lebih. Kalau kurang, kami bisa dipersalahkan.",
        broll=[(16.05, "0372", 9.0), (23.10, None, 0)],
        gfx=[
            (16.07, "bigstat", dict(top="BARANGAN MAKANAN", value="34", countFrom=0, bottom="FOKUS FAMA", dur=3.4)),
            (24.40, "tag", dict(text="WAJIB ADA SETIAP HARI", dur=2.6)),
            (32.38, "rule", dict(items=[["✕", "TAK BOLEH KURANG", 32.40], ["✓", "MESTI LEBIH", 33.24]], dur=2.8)),
            (36.20, "stamp", dict(text="DIPERSALAHKAN!", color="red", dur=1.6)),
        ],
        sfx=[(12.85, "whoosh_fast", 0.18), (16.07, "impact_logo", 0.35), (16.2, "typing", 0.2), (24.40, "click_ui", 0.5),
             (32.40, "pop_hard", 0.4), (33.24, "correct", 0.35), (36.20, "impact_big", 0.35)],
        zoom=[(12.85, 1.0), (24.30, 1.1), (31.50, 1.0), (33.98, 1.2)],
    ),
    dict(
        id="cili", clip="0364", tighten=0.10,
        ranges=[(42.40, 43.62), (45.90, 46.66), (52.74, 55.80)],
        caption="Contohnya cili. Cabai. Ada lebih kurang 8 ataupun 9 jenis cabai.",
        gfx=[
            (42.40, "kamus", dict(my="CILI", id="CABAI", dur=2.6)),
            (53.60, "bigstat", dict(top="JENIS CABAI 🌶️", value="8-9", bottom="CONTOH SATU BARANG", dur=2.6)),
        ],
        sfx=[(42.40, "swoosh_accent", 0.35), (45.92, "pop_bubble", 0.5), (53.68, "pop_hard", 0.4)],
        zoom=[(42.40, 1.08), (45.90, 1.18), (52.74, 1.0)],
    ),
    # ---------------------------------------------------------------- ROLE: lembaga pemasaran
    dict(
        id="peranan", clip="0366", tighten=0.12,
        ranges=[(27.20, 36.12), (67.15, 75.30)],
        caption="Selepas semua tanaman itu berhasil, baru FAMA datang. Kami beli, kami dapatkan, kami jadikan stok. "
                "Kami tidak terlibat dalam penanaman, tapi kami membantu dari segi pemasaran, sebab itu nama FAMA ni, lembaga pemasaran.",
        gfx=[
            (27.30, "flow", dict(items=[["🌱", "TANAM", 27.30], ["🌾", "TUAI", 29.25], ["🤝", "FAMA BELI", 33.51], ["📦", "STOK", 35.40]], dur=6.6)),
            (73.30, "stamp", dict(text="LEMBAGA PEMASARAN", small=True, dur=2.2)),
        ],
        sfx=[(27.20, "whoosh_fast", 0.18), (27.30, "click_select", 0.5), (29.25, "click_select", 0.5), (33.51, "click_select", 0.5),
             (35.40, "click_select", 0.5), (73.30, "pop_hard", 0.4)],
        zoom=[(27.20, 1.0), (31.05, 1.12), (67.15, 1.0), (72.58, 1.16)],
    ),
    # ---------------------------------------------------------------- KAMUS SERUMPUN (language fun)
    dict(
        id="timbalan", clip="0349", tighten=0.10,
        ranges=[(28.37, 33.55)],
        caption="Timbalan. Kalau di Indonesia dipanggil wakil kepala. Wakil kepala.",
        gfx=[
            (29.10, "kamus", dict(my="TIMBALAN", id="WAKIL KEPALA", dur=4.3)),
        ],
        sfx=[(28.37, "whoosh_cine", 0.22), (29.10, "swoosh_accent", 0.35), (31.85, "pop_bubble", 0.45)],
        zoom=[(28.37, 1.0)],
    ),
    dict(
        id="ole", clip="0351", tighten=0.10,
        ranges=[(151.54, 157.45)],
        caption="Saya percaya FAMA pun ada menyediakan buah tangan. Kami panggil buah tangan. Kalau Indonesia dia panggil oleh-oleh.",
        broll=[(151.54, "0372", 3.0)],
        gfx=[(154.30, "kamus", dict(my="BUAH TANGAN", id="OLEH-OLEH", dur=3.2))],
        sfx=[(154.30, "swoosh_accent", 0.35), (156.95, "pop_bubble", 0.5)],
    ),
    dict(
        id="geran", clip="0375", tighten=0.10,
        ranges=[(4.15, 12.25)],
        caption="Bantuan itu bukan harus dibayar balik ya? Bantuan itu tidak dibayar balik. Oh, geran lah! Kalau di Malaysia dipanggil geran.",
        gfx=[(9.46, "kamus", dict(my="GERAN", id="BANTUAN", dur=2.9))],
        sfx=[(9.46, "swoosh_accent", 0.35), (9.6, "pop_bubble", 0.45)],
        zoom=[(4.15, 1.0), (9.40, 1.12)],
    ),
    # ---------------------------------------------------------------- "walaupun nama saya abang"
    dict(
        id="abang", clip="0365", tighten=0.12,
        ranges=[(13.05, 14.90), (24.30, 25.60), (26.38, 28.86), (31.20, 32.70), (39.90, 45.00)],
        caption="Bila disebut muda ini, semuanya bawah 43 tahun, dipanggil muda. "
                "Macam saya ni sudah dikira tidak muda, walaupun nama saya abang.",
        gfx=[
            (26.42, "bigstat", dict(top="PENGUSAHA MUDA", value="< 43", bottom="UMUR", dur=2.8)),
            (44.20, "sticker", dict(emoji="😅", dur=1.4)),
        ],
        sfx=[(13.05, "whoosh_fast", 0.18), (26.42, "pop_hard", 0.4), (44.20, "pop_bubble", 0.6)],
        zoom=[(13.05, 1.0), (24.30, 1.1), (39.90, 1.0), (43.0, 1.22)],
    ),
    # ---------------------------------------------------------------- SARAWAK + 2 OUTLETS IN 2 MONTHS
    dict(
        id="sarawak", clip="0373", tighten=0.12,
        ranges=[(4.32, 9.40), (10.30, 14.75), (18.25, 28.50), (30.30, 32.42)],
        caption="Saya asalnya daripada Kepulauan Borneo, Kalimantan, Sarawak. Sepanjang saya jadi chairman, saya belum lagi menjejakkan kaki ke negeri saya. "
                "Jadi minggu depan baru saya balik, dan antara yang kita akan buka outlet yang terkini adalah di negeri kelahiran saya. "
                "Kita bukan buka satu, tapi dah buka dua. Itu baru 2 bulan jadi pengerusi.",
        broll=[(4.32, "0390", 86.4), (8.70, None, 0)],
        gfx=[
            (5.85, "location", dict(title="Sarawak", sub="Pulau Borneo", dur=3.4)),
            (21.40, "tag", dict(text="📍 OUTLET BARU DI SARAWAK", dur=3.2)),
            (26.00, "bigstat", dict(top="OUTLET DIBUKA", value="2", countFrom=1, bottom="BUKAN SATU", dur=2.4)),
            (30.80, "bigstat", dict(top="JADI PENGERUSI", value="2 BULAN", bottom="BARU", dur=2.4)),
        ],
        sfx=[(4.32, "whoosh_cine", 0.22), (5.85, "pop_long", 0.4), (21.40, "click_ui", 0.5), (26.00, "coin_win", 0.35),
             (27.72, "pop_hard", 0.4), (30.80, "impact_logo", 0.38)],
        zoom=[(10.30, 1.0), (12.26, 1.1), (18.25, 1.0), (25.46, 1.12), (30.30, 1.22)],
    ),
    # ---------------------------------------------------------------- CLOSING
    dict(
        id="harap", clip="0351", tighten=0.12,
        ranges=[(102.65, 109.50)],
        caption="Saya harap pertemuan ini akan melahirkan kerjasama yang berbentuk peluang-peluang.",
        broll=[(102.65, "0390", 30.0), (106.0, "0388", 44.0)],
        gfx=[(106.62, "tag", dict(text="🤝 KERJASAMA 🇲🇾🇮🇩", dur=2.8))],
        sfx=[(102.65, "whoosh_cine", 0.22), (106.62, "positive", 0.3)],
    ),
    dict(
        id="serumpun", clip="0388", tighten=None, voice_gain=1.25,
        ranges=[(39.70, 42.10)],
        caption="Jabat serumpun! Jabat serumpun!",
        gfx=[(40.20, "stamp", dict(text="JABAT SERUMPUN!", dur=1.9, confetti=True))],
        sfx=[(40.20, "impact_big", 0.35), (40.30, "applause_small", 0.35), (40.80, "shutter", 0.5)],
    ),
    dict(  # selfie moment, music up, end card
        id="selfie", clip="0390", tighten=None, voice_gain=0.45,
        ranges=[(72.60, 76.60)],
        caption="",
        broll=[(72.60, "0390", 77.0)],
        gfx=[(72.75, "endcard", dict(line1="Kunjungan Hormat · FAMA Point", line2="1 FAMA = 3 AGENSI", cta="Follow untuk lagi!", flags=True, dur=3.85))],
        sfx=[(73.0, "shutter", 0.45), (73.2, "positive", 0.25)],
    ),
]
