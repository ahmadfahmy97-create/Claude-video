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
soft    : True = montage cut (no white flash / push).
freeze  : source_time from which the picture freezes into a "photo" until the piece ends.
"""

PIECES = [
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
    # ---------------------------------------------------------------- INTERLUDE 1: alumni in the meeting (music only, no text)
    dict(id="m_a0", clip="0442", ranges=[(3.0, 5.60)], tighten=None, voice_gain=0.0, caption="", soft=False,
         sfx=[(3.0, "whoosh_cine", 0.22)], zoom=[(3.0, 1.0)]),
    dict(id="m_a1", clip="0447", ranges=[(2.0, 4.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(2.0, 1.08)]),
    dict(id="m_a2", clip="0449", ranges=[(2.0, 4.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(2.0, 1.0)]),
    dict(id="m_a3", clip="0451", ranges=[(10.0, 12.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(10.0, 1.08)]),
    dict(id="m_a4", clip="0453", ranges=[(5.0, 7.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(5.0, 1.0)]),
    dict(id="m_a5", clip="0454", ranges=[(2.0, 4.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(2.0, 1.08)]),
    dict(id="m_a6", clip="0456", ranges=[(5.0, 7.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(5.0, 1.0)]),
    dict(id="m_a7", clip="0447", ranges=[(40.0, 42.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(40.0, 1.08)]),
    dict(id="m_a8", clip="0449", ranges=[(41.0, 43.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(41.0, 1.0)]),
    dict(id="m_a9", clip="0451", ranges=[(56.0, 58.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(56.0, 1.08)]),
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
    # ---------------------------------------------------------------- INTERLUDE 2: souvenirs & handshakes (music only, no text)
    dict(id="m_b0", clip="0459", ranges=[(27.0, 29.60)], tighten=None, voice_gain=0.0, caption="", soft=False,
         sfx=[(27.0, "whoosh_cine", 0.22)], zoom=[(27.0, 1.0)]),
    dict(id="m_b1", clip="0460", ranges=[(13.0, 15.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(13.0, 1.08)]),
    dict(id="m_b2", clip="0463", ranges=[(24.0, 26.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(24.0, 1.0)]),
    dict(id="m_b3", clip="0463", ranges=[(44.0, 46.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(44.0, 1.08)]),
    dict(id="m_b4", clip="0464", ranges=[(7.0, 9.60)], tighten=None, voice_gain=0.0, caption="", soft=True,
 zoom=[(7.0, 1.0)]),
    dict(
        id="finale", clip="0461", ranges=[(20.95, 25.75)], tighten=None, voice_gain=1.1,
        caption="Ready? Satu, dua, tiga!",
        freeze=23.35,
        gfx=[(23.45, "endcard", dict(line1="Kunjungan Muhibah", line2="Persatuan Alumni FAMA", cta="Kongsi dengan warga FAMA!", dur=2.0, fixedY=1330))],
        sfx=[(23.35, "shutter", 0.7), (23.40, "impact_logo", 0.30), (23.50, "applause_small", 0.35)],
        zoom=[(20.95, 1.0)],
    ),
]
