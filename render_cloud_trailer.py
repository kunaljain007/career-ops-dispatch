import os
import subprocess
import shutil
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "cloud_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)
FRAMES_DIR = os.path.join(OUTPUT_DIR, "scenes")
os.makedirs(FRAMES_DIR, exist_ok=True)
CLIPS_DIR = os.path.join(OUTPUT_DIR, "clips")
os.makedirs(CLIPS_DIR, exist_ok=True)

WIDTH, HEIGHT = 1920, 1080
FFMPEG = shutil.which("ffmpeg") or "ffmpeg"

print("--- PHASE 1: GENERATING SYNTHESIZED NARRATION AUDIO ---")
HINDI_SCRIPT = """
ॐ क्रीं कालिकायै नमः।
जब ब्रह्मांड में न समय था, न प्रकाश, न सृष्टि... तब केवल एक ही शक्ति विद्यमान थी — महाकाली। अंधकार का वह अनंत सागर, जिससे समस्त ब्रह्मांड का जन्म हुआ।
सतयुग की उस भयंकर घड़ी को स्मरण करो, जब रक्तबीज नामक असुर को यह वरदान मिला कि उसके रक्त की प्रत्येक बूंद जब भूमि को स्पर्श करेगी, तो सहस्रों नए रक्तबीज उत्पन्न होंगे। देवताओं के अस्त्र निष्फल हो गए, स्वर्ग का सिंहासन डोल उठा।
तब महाशक्ति के भीतर से प्रगट हुईं — माँ काली! विकराल रूप, दिगम्बरा, गले में मुंडमाला, हाथ में खड़ग, और नयनों में प्रलयंकर ज्वाला। रक्तबीज का एक भी रक्त बिंदु भूमि पर नहीं गिरा। माँ ने अपनी जिह्वा फैलाकर समस्त रक्त का पान कर लिया और उस असुर का समूल नाश कर दिया।
परंतु माँ का यह रौद्र रूप शांत न हुआ। उनका तांडव तीनों लोकों को भस्म करने लगा। जब कोई उपाय न बचा, तब स्वयं देवाधिदेव महादेव शिव उनके चरणों के नीचे लेट गए। जैसे ही माँ का चरण शिव के वक्षस्थल पर पड़ा, उन्होंने लज्जा से अपनी जिह्वा बाहर निकाल ली — और वह रौद्र संहार, परम वात्सल्य और शांति में परिवर्तित हो गया।
दक्षिणेश्वर के पावन तट से लेकर, कामाख्या के शक्तिपीठ और कालीघाट की पावन गलियों तक — माँ काली केवल संहारक नहीं, अपितु अपने भक्तों के लिए 'भवतारिणी' हैं, जो अज्ञान और भय के बंधनों को काटकर मुक्ति प्रदान करती हैं।
यह समय है उस आदि अनंत शक्ति को अपने भीतर जागृत करने का। निर्भय बनो, अपने भीतर के अंधकार को भस्म करो।
जय माँ काली!
"""

tts_hi = gTTS(text=HINDI_SCRIPT, lang="hi", slow=False)
audio_file = os.path.join(OUTPUT_DIR, "voiceover_hindi.mp3")
tts_hi.save(audio_file)
print(f"Audio Generated: {audio_file} ({os.path.getsize(audio_file):,} bytes)")

print("--- PHASE 2: GENERATING 1080P SACRED SCENE ARTWORKS ---")
scenes_meta = [
    {
        "id": "scene_01",
        "title": "THE PRIMORDIAL VOID",
        "sanskrit": "ॐ क्रीं कालिकायै नमः",
        "sub": "Before Time, Space, and Form: The Infinite Darkness of Consciousness",
        "bg_color": (8, 6, 18),
        "accent": (245, 190, 60),
        "duration": 17,
        "vf": "zoompan=z='min(zoom+0.0012,1.35)':d=425:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25"
    },
    {
        "id": "scene_02",
        "title": "AWAKENING OF ADISHAKTI",
        "sanskrit": "सर्वमंगल मांगल्ये शिवे सर्वार्थ साधिके",
        "sub": "When Darkness Threatens Creation, The Supreme Mother Rises",
        "bg_color": (32, 10, 15),
        "accent": (255, 120, 40),
        "duration": 17,
        "vf": "zoompan=z='1.2':d=425:x='iw/2-(iw/zoom/2)':y='(ih-(ih/zoom))*(1-on/425)':s=1920x1080:fps=25"
    },
    {
        "id": "scene_03",
        "title": "THE BATTLE OF RAKTABEEJ",
        "sanskrit": "रक्तबीज वधाय च चण्डमुण्ड विनाशिनी",
        "sub": "Eradicating Every Drop of Darkness Before It Touches The Earth",
        "bg_color": (40, 8, 8),
        "accent": (255, 60, 60),
        "duration": 17,
        "vf": "zoompan=z='min(zoom+0.0022,1.55)':d=425:x='iw/2-(iw/zoom/2)+sin(on/2)*3':y='ih/2-(ih/zoom/2)+cos(on/2)*3':s=1920x1080:fps=25"
    },
    {
        "id": "scene_04",
        "title": "THE SUPREME FORM: MAA KAALI",
        "sanskrit": "करालवदनां घोरां मुक्तकेशीं चतुर्भुजाम्",
        "sub": "Wielding The Sword of Ultimate Truth — Severing All Ego and Illusion",
        "bg_color": (12, 12, 28),
        "accent": (220, 200, 255),
        "duration": 17,
        "vf": "zoompan=z='max(1.35-0.0012*on,1.0)':d=425:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25"
    },
    {
        "id": "scene_05",
        "title": "SHIVA & SHAKTI: ETERNAL UNION",
        "sanskrit": "शिवः शक्त्या युक्तो यदि भवति शक्तः प्रभवितुम्",
        "sub": "Pure Consciousness Meets Dynamic Energy — Cosmic Harmony Restored",
        "bg_color": (15, 20, 35),
        "accent": (100, 210, 255),
        "duration": 18,
        "vf": "zoompan=z='1.15':d=450:x='(iw-(iw/zoom))*(on/450)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25"
    },
    {
        "id": "scene_06",
        "title": "SACRED PILGRIMAGES",
        "sanskrit": "दक्षिणेश्वर • कामाख्या • कालीघाट",
        "sub": "Centuries of Devotion Along The Holy Ganges and Shakti Peethas",
        "bg_color": (25, 18, 10),
        "accent": (255, 215, 0),
        "duration": 17,
        "vf": "zoompan=z='1.18':d=425:x='iw/2-(iw/zoom/2)':y='(ih-(ih/zoom))*(on/425)':s=1920x1080:fps=25"
    },
    {
        "id": "scene_07",
        "title": "BHAVATARINI: THE LIBERATOR",
        "sanskrit": "जय माँ काली • अभयं कुरु",
        "sub": "Eradicate All Fear — Awaken The Invincible Light Within",
        "bg_color": (18, 12, 30),
        "accent": (255, 180, 50),
        "duration": 17,
        "vf": "zoompan=z='min(zoom+0.0015,1.4)':d=425:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=25"
    }
]

clip_paths = []
for idx, sc in enumerate(scenes_meta):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=sc["bg_color"])
    draw = ImageDraw.Draw(img)

    cx, cy = WIDTH // 2, HEIGHT // 2
    accent = sc["accent"]

    for r in range(500, 0, -25):
        alpha_factor = (500 - r) / 500.0
        c = (
            int(sc["bg_color"][0] * (1 - alpha_factor * 0.4) + accent[0] * alpha_factor * 0.4),
            int(sc["bg_color"][1] * (1 - alpha_factor * 0.4) + accent[1] * alpha_factor * 0.4),
            int(sc["bg_color"][2] * (1 - alpha_factor * 0.4) + accent[2] * alpha_factor * 0.4)
        )
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    bar_h = 100
    draw.rectangle([0, 0, WIDTH, bar_h], fill=(0, 0, 0))
    draw.rectangle([0, HEIGHT - bar_h, WIDTH, HEIGHT], fill=(0, 0, 0))
    draw.line([120, bar_h + 30, WIDTH - 120, bar_h + 30], fill=accent, width=2)
    draw.line([120, HEIGHT - bar_h - 30, WIDTH - 120, HEIGHT - bar_h - 30], fill=accent, width=2)

    # Central Yantra geometry
    draw.polygon([(cx, cy - 220), (cx + 180, cy), (cx, cy + 220), (cx - 180, cy)], outline=accent, width=2)
    draw.polygon([(cx, cy - 140), (cx + 110, cy), (cx, cy + 140), (cx - 110, cy)], outline=accent, width=1)

    try:
        font_sanskrit = ImageFont.truetype("DejaVuSans.ttf", 46)
        font_title = ImageFont.truetype("DejaVuSans.ttf", 34)
        font_sub = ImageFont.truetype("DejaVuSans.ttf", 22)
    except:
        font_sanskrit = font_title = font_sub = ImageFont.load_default()

    draw.text((cx - 250, cy - 35), sc["sanskrit"], fill=accent, font=font_sanskrit)
    draw.text((cx - 280, cy + 250), sc["title"], fill=(255, 255, 255), font=font_title)
    draw.text((cx - 400, cy + 305), sc["sub"], fill=(200, 200, 210), font=font_sub)

    scene_img_path = os.path.join(FRAMES_DIR, f"{sc['id']}.png")
    img.save(scene_img_path)

    # Render motion video clip
    clip_path = os.path.join(CLIPS_DIR, f"{sc['id']}.mp4")
    print(f"Rendering Dynamic Motion Clip {idx+1}/{len(scenes_meta)}...")
    cmd_clip = [
        FFMPEG, "-y",
        "-loop", "1",
        "-i", scene_img_path,
        "-vf", sc["vf"],
        "-t", str(sc["duration"]),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "faster",
        clip_path
    ]
    subprocess.run(cmd_clip, check=True)
    clip_paths.append(clip_path)

print("--- PHASE 3: CONCATENATING AND MASTERING FINAL CINEMATIC VIDEO ---")
concat_txt = os.path.join(OUTPUT_DIR, "clips.txt")
with open(concat_txt, "w", encoding="utf-8") as f:
    for cp in clip_paths:
        f.write(f"file '{os.path.abspath(cp)}'\n")

final_output = os.path.join(OUTPUT_DIR, "Maa_Kaali_Epic_Cinematic_Movie_Trailer.mp4")
cmd_final = [
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0", "-i", concat_txt,
    "-i", audio_file,
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    final_output
]
subprocess.run(cmd_final, check=True)
print(f"ALL DONE! Final Cloud Master Video: {final_output} ({os.path.getsize(final_output):,} bytes)")
