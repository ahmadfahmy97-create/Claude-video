"""Edit decision list – Libat Urus & Perjumpaan Kumpulan Sasar FAMA, Perlis (Pengerusi FAMA Malaysia).

Story: the question everyone asks ("FAMA buat apa?") -> the chairman's promise -> #FAMASantuni
-> the concrete answer: KopieSatu (cheap licence, 18-month payback) -> call to action.

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
        sfx=[(104.30, "whoosh_cine", 0.35), (108.60, "typing", 0.32), (110.05, "pop_hard", 0.4)],
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
    # ---------------------------------------------------------------- CONTEXT
    dict(
        id="perlis", clip=S, ranges=[(23.25, 27.75)], tighten=0.10,
        caption="Perlis merupakan negeri yang ke-9 yang saya dah turun.",
        broll=[(23.25, "0555", 0.3)],
        gfx=[(25.40, "bigstat", dict(bottom="PERLIS", value="KE-9", top="NEGERI DILAWATI", dur=2.6))],
        sfx=[(23.25, "whoosh_fast", 0.3), (25.40, "impact_whoosh", 0.4)],
    ),
    # ---------------------------------------------------------------- #FAMASANTUNI
    dict(
        id="santuni", clip=S, ranges=[(399.75, 408.66), (413.24, 418.95)], tighten=0.12,
        caption="Di hari pertama saya menjadi Pengerusi FAMA Malaysia, saya telah melancarkan satu tanda pagar. Apa slogan? Slogannya adalah FAMA Santuni.",
        broll=[(399.75, "0587", 0.8), (401.96, None, 0)],
        gfx=[
            (407.50, "tag", dict(text="# TANDA PAGAR", dur=2.2)),
            (416.80, "hashtag", dict(text="FAMASANTUNI", dur=3.9)),
        ],
        sfx=[(413.24, "pop_bubble", 0.45), (415.90, "riser", 0.3), (416.80, "impact_logo", 0.5), (416.85, "achievement", 0.25)],
        zoom=[(401.96, 1.0), (404.08, 1.12), (413.24, 1.2), (416.80, 1.34)],
    ),
    dict(
        id="santuni2", clip=S, ranges=[(419.94, 426.80), (435.91, 439.30)], tighten=0.12,
        caption="InsyaAllah selagi saya jadi pengerusi kat sini, semua warga kerja FAMA akan menyantuni semua orang. Tapi tuan-tuan, santuni ni bukan maksudnya meluluskan.",
        broll=[(424.70, "0591", 0.4), (435.91, None, 0)],
        gfx=[(438.30, "stamp", dict(text="SANTUNI ≠ LULUS", dur=1.9))],
        sfx=[(438.30, "pop_hard", 0.45)],
        zoom=[(419.94, 1.06), (435.91, 1.1), (437.70, 1.3)],
    ),
    # ---------------------------------------------------------------- KOPIESATU
    dict(
        id="kpi", clip=S, ranges=[(653.88, 656.30), (659.84, 665.05), (666.75, 671.95), (673.41, 680.50)], tighten=0.12,
        caption="Kenapa saya tekankan KopieSatu? KPI saya adalah sehingga tahun 2027, semua negeri di Malaysia ada outlet ataupun premis KopieSatu. Ada tinggal dua ataupun tiga negeri saja yang belum ada KopieSatu.",
        gfx=[
            (653.88, "question", dict(text="KENAPA KOPIESATU?", dur=2.3)),
            (661.80, "goal", dict(kicker="KPI 2027", title="SEMUA NEGERI ADA KOPIESATU", total=13,
                                  done=10, pending_t=675.83, dur=18.7)),
        ],
        sfx=[(653.88, "whoosh_cine", 0.35), (661.80, "pop_long", 0.4), (675.83, "click_ui", 0.5)],
        zoom=[(653.88, 1.15), (659.84, 1.0), (666.75, 1.1), (673.41, 1.0), (675.83, 1.18)],
    ),
    dict(
        id="harga", clip=S, ranges=[(693.70, 699.50), (699.98, 708.05)], tighten=0.12,
        caption="Orang lain RM200,000, orang lain sampai RM400,000, RM600,000. Tapi KopieSatu tuan-tuan, licensingnya RM20,000 lah. RM20,000 tu pula kita ikat selama lima tahun.",
        gfx=[
            (693.70, "ladder", dict(label="FRANCAIS LAIN", items_t=[["RM200K", 694.74], ["RM400K", 697.10], ["RM600K", 698.60]],
                                    strike_t=700.10, heroText="RM20K", heroLabel="LESEN KOPIESATU", hero_t=701.98,
                                    chipText="IKAT 5 TAHUN", chip_t=706.54, dur=14.3)),
        ],
        sfx=[(694.74, "pop_bubble", 0.4), (697.10, "pop_bubble", 0.4), (698.60, "pop_bubble", 0.45),
             (700.10, "swoosh_accent", 0.35), (701.98, "impact_whoosh", 0.45), (702.05, "coin_win", 0.32),
             (706.54, "click_select", 0.45)],
        zoom=[(693.70, 1.0), (699.98, 1.14), (704.34, 1.0), (706.30, 1.16)],
    ),
    dict(
        id="desaru", clip=S, ranges=[(820.43, 829.62), (838.25, 844.15)], tighten=0.12,
        caption="Di Desaru, Johor, ada seorang usahawan yang buka KopieSatu. Dia kata modal dia semua sekali RM120,000. Tuan-tuan nak tahu, 18 bulan sahaja, dia dah dapat balik modal.",
        broll=[(824.20, "0585", 3.2), (827.10, None, 0)],
        gfx=[
            (820.50, "location", dict(title="Desaru, Johor", sub="Usahawan KopieSatu", dur=3.6)),
            (828.40, "bigstat", dict(bottom="MODAL", value="RM120K", top="SEMUA SEKALI", dur=2.3)),
            (839.10, "roi", dict(value=18, unit="BULAN", stampText="BALIK MODAL", stamp_t=843.00, dur=5.2)),
        ],
        sfx=[(820.50, "pop_long", 0.4), (828.40, "coins", 0.45), (838.30, "riser_stutter", 0.28),
             (839.75, "impact_big", 0.45), (843.00, "coin_win", 0.4), (843.05, "correct", 0.25)],
        zoom=[(820.43, 1.0), (827.10, 1.1), (838.25, 1.18), (843.00, 1.3)],
    ),
    # ---------------------------------------------------------------- CALL TO ACTION
    dict(
        id="cta", clip=S, ranges=[(864.90, 877.58)], tighten=0.12,
        caption="Kalau ada yang pencen-pencen, yang duit gratuiti tak bergerak lagi tu, bolehlah fikir-fikirkan untuk buat perniagaan KopieSatu yang ketiga di Negeri Perlis.",
        broll=[(866.10, "0586", 6.2), (869.96, "0579", 38.2), (871.60, None, 0)],
        gfx=[
            (867.70, "sticker", dict(emoji="💰", dur=1.6)),
            (874.40, "bigstat", dict(bottom="KOPIESATU", value="KE-3", top="DI PERLIS?", dur=3.2)),
        ],
        sfx=[(867.70, "pop_bubble", 0.5), (874.40, "impact_whoosh", 0.4)],
        zoom=[(864.90, 1.0), (871.60, 1.12), (874.34, 1.25)],
    ),
    # ---------------------------------------------------------------- OUTRO (picture only, music up)
    dict(
        id="outro", clip="0583", ranges=[(1.0, 4.4)], tighten=None, mute=True,
        gfx=[(1.05, "endcard", dict(line1="#FAMASANTUNI", line2="BERMINAT BUKA KOPIESATU?",
                                    cta="HUBUNGI FAMA NEGERI", dur=3.35))],
        sfx=[(1.05, "whoosh_cine", 0.3)],
    ),
]
