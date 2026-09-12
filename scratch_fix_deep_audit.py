import json
import os
import re

APP_DIR = "/Users/veneno/Projects/Apps/ppplayer/app"
WEB_DIR = "/Users/veneno/Projects/Apps/ppplayer/website"

langs = ['en', 'es', 'fr', 'de', 'pt', 'it', 'ja', 'ko', 'zh', 'hi', 'ru', 'ar']

app_translations = {
    'en': {
        "continueListening": "Continue Listening",
        "popularArtists": "Popular Artists",
        "suggestedStations": "Suggested Stations",
        "popularAlbums": "Popular Albums",
        "popularGenres": "Popular Genres",
        "newReleases": "New Releases",
        "featuredPlaylists": "Featured Playlists",
        "popularTracks": "Popular Tracks",
        "popularSongs": "Popular Songs",
        "featuringArtist": "FEATURING {artistName}",
        "@featuringArtist": {"placeholders": {"artistName": {"type": "String"}}},
        "currentCountry": "Current: {country}",
        "@currentCountry": {"placeholders": {"country": {"type": "String"}}},
        "errorLoadingMarkets": "Error loading markets: {error}",
        "@errorLoadingMarkets": {"placeholders": {"error": {"type": "String"}}},
        "queueTooltip": "Queue",
        "searchHint": "Search music, artists, albums..."
    },
    'es': {
        "continueListening": "Continuar escuchando",
        "popularArtists": "Artistas populares",
        "suggestedStations": "Estaciones sugeridas",
        "popularAlbums": "Álbumes populares",
        "popularGenres": "Géneros populares",
        "newReleases": "Nuevos lanzamientos",
        "featuredPlaylists": "Listas de reproducción destacadas",
        "popularTracks": "Pistas populares",
        "popularSongs": "Canciones populares",
        "featuringArtist": "CON {artistName}",
        "currentCountry": "Actual: {country}",
        "errorLoadingMarkets": "Error al cargar los mercados: {error}",
        "queueTooltip": "Cola",
        "searchHint": "Buscar música, artistas, álbumes..."
    },
    'fr': {
        "continueListening": "Reprendre la lecture",
        "popularArtists": "Artistes populaires",
        "suggestedStations": "Stations suggérées",
        "popularAlbums": "Albums populaires",
        "popularGenres": "Genres populaires",
        "newReleases": "Nouvelles sorties",
        "featuredPlaylists": "Playlists en vedette",
        "popularTracks": "Titres populaires",
        "popularSongs": "Chansons populaires",
        "featuringArtist": "AVEC {artistName}",
        "currentCountry": "Actuel: {country}",
        "errorLoadingMarkets": "Erreur lors du chargement des marchés: {error}",
        "queueTooltip": "File d'attente",
        "searchHint": "Rechercher de la musique, des artistes, des albums..."
    },
    'de': {
        "continueListening": "Weiterhören",
        "popularArtists": "Beliebte Künstler",
        "suggestedStations": "Vorgeschlagene Sender",
        "popularAlbums": "Beliebte Alben",
        "popularGenres": "Beliebte Genres",
        "newReleases": "Neuerscheinungen",
        "featuredPlaylists": "Empfohlene Playlists",
        "popularTracks": "Beliebte Titel",
        "popularSongs": "Beliebte Songs",
        "featuringArtist": "MIT {artistName}",
        "currentCountry": "Aktuell: {country}",
        "errorLoadingMarkets": "Fehler beim Laden der Märkte: {error}",
        "queueTooltip": "Warteschlange",
        "searchHint": "Musik, Künstler, Alben suchen..."
    },
    'pt': {
        "continueListening": "Continuar ouvindo",
        "popularArtists": "Artistas populares",
        "suggestedStations": "Estações sugeridas",
        "popularAlbums": "Álbuns populares",
        "popularGenres": "Gêneros populares",
        "newReleases": "Novos lançamentos",
        "featuredPlaylists": "Playlists em destaque",
        "popularTracks": "Faixas populares",
        "popularSongs": "Músicas populares",
        "featuringArtist": "COM {artistName}",
        "currentCountry": "Atual: {country}",
        "errorLoadingMarkets": "Erro ao carregar mercados: {error}",
        "queueTooltip": "Fila",
        "searchHint": "Buscar música, artistas, álbuns..."
    },
    'it': {
        "continueListening": "Continua ad ascoltare",
        "popularArtists": "Artisti popolari",
        "suggestedStations": "Stazioni suggerite",
        "popularAlbums": "Album popolari",
        "popularGenres": "Generi popolari",
        "newReleases": "Nuove uscite",
        "featuredPlaylists": "Playlist in primo piano",
        "popularTracks": "Brani popolari",
        "popularSongs": "Canzoni popolari",
        "featuringArtist": "CON {artistName}",
        "currentCountry": "Attuale: {country}",
        "errorLoadingMarkets": "Errore nel caricamento dei mercati: {error}",
        "queueTooltip": "Coda",
        "searchHint": "Cerca musica, artisti, album..."
    },
    'ja': {
        "continueListening": "続きを聴く",
        "popularArtists": "人気のアーティスト",
        "suggestedStations": "おすすめのステーション",
        "popularAlbums": "人気のアルバム",
        "popularGenres": "人気のジャンル",
        "newReleases": "ニューリリース",
        "featuredPlaylists": "注目のプレイリスト",
        "popularTracks": "人気のトラック",
        "popularSongs": "人気の曲",
        "featuringArtist": "{artistName} をフィーチャー",
        "currentCountry": "現在: {country}",
        "errorLoadingMarkets": "マーケットの読み込みエラー: {error}",
        "queueTooltip": "キュー",
        "searchHint": "音楽、アーティスト、アルバムを検索..."
    },
    'ko': {
        "continueListening": "계속 듣기",
        "popularArtists": "인기 아티스트",
        "suggestedStations": "추천 스테이션",
        "popularAlbums": "인기 앨범",
        "popularGenres": "인기 장르",
        "newReleases": "최신 릴리스",
        "featuredPlaylists": "추천 플레이리스트",
        "popularTracks": "인기 트랙",
        "popularSongs": "인기 곡",
        "featuringArtist": "피처링: {artistName}",
        "currentCountry": "현재: {country}",
        "errorLoadingMarkets": "시장 로딩 오류: {error}",
        "queueTooltip": "대기열",
        "searchHint": "음악, 아티스트, 앨범 검색..."
    },
    'zh': {
        "continueListening": "继续收听",
        "popularArtists": "热门歌手",
        "suggestedStations": "推荐电台",
        "popularAlbums": "热门专辑",
        "popularGenres": "热门曲风",
        "newReleases": "最新发行",
        "featuredPlaylists": "精选歌单",
        "popularTracks": "热门单曲",
        "popularSongs": "热门歌曲",
        "featuringArtist": "合作艺人: {artistName}",
        "currentCountry": "当前: {country}",
        "errorLoadingMarkets": "加载市场错误: {error}",
        "queueTooltip": "播放队列",
        "searchHint": "搜索音乐、歌手、专辑..."
    },
    'hi': {
        "continueListening": "सुनना जारी रखें",
        "popularArtists": "लोकप्रिय कलाकार",
        "suggestedStations": "सुझाए गए स्टेशन",
        "popularAlbums": "लोकप्रिय एल्बम",
        "popularGenres": "लोकप्रिय शैलियां",
        "newReleases": "नई रिलीज़",
        "featuredPlaylists": "विशेष प्लेलिस्ट",
        "popularTracks": "लोकप्रिय ट्रैक",
        "popularSongs": "लोकप्रिय गीत",
        "featuringArtist": "{artistName} की विशेषता",
        "currentCountry": "वर्तमान: {country}",
        "errorLoadingMarkets": "बाज़ार लोड करने में त्रुटि: {error}",
        "queueTooltip": "कतार",
        "searchHint": "संगीत, कलाकार, एल्बम खोजें..."
    },
    'ru': {
        "continueListening": "Продолжить",
        "popularArtists": "Популярные артисты",
        "suggestedStations": "Рекомендуемые станции",
        "popularAlbums": "Популярные альбомы",
        "popularGenres": "Популярные жанры",
        "newReleases": "Новинки",
        "featuredPlaylists": "Рекомендуемые плейлисты",
        "popularTracks": "Популярные треки",
        "popularSongs": "Популярные песни",
        "featuringArtist": "ПРИ УЧАСТИИ {artistName}",
        "currentCountry": "Текущий: {country}",
        "errorLoadingMarkets": "Ошибка загрузки рынков: {error}",
        "queueTooltip": "Очередь",
        "searchHint": "Поиск музыки, артистов, альбомов..."
    },
    'ar': {
        "continueListening": "مواصلة الاستماع",
        "popularArtists": "فنانون مشهورون",
        "suggestedStations": "محطات مقترحة",
        "popularAlbums": "ألبومات شهيرة",
        "popularGenres": "أنواع شائعة",
        "newReleases": "إصدارات جديدة",
        "featuredPlaylists": "قوائم تشغيل مميزة",
        "popularTracks": "مقاطع شائعة",
        "popularSongs": "أغاني شائعة",
        "featuringArtist": "بمشاركة {artistName}",
        "currentCountry": "الحالي: {country}",
        "errorLoadingMarkets": "خطأ في تحميل الأسواق: {error}",
        "queueTooltip": "قائمة الانتظار",
        "searchHint": "البحث عن الموسيقى والفنانين والألبومات..."
    }
}

web_translations = {
    'en': {"changelog": "Changelog", "linux": "Linux"},
    'es': {"changelog": "Registro de cambios", "linux": "Linux"},
    'fr': {"changelog": "Journal des modifications", "linux": "Linux"},
    'de': {"changelog": "Änderungsprotokoll", "linux": "Linux"},
    'pt': {"changelog": "Registro de alterações", "linux": "Linux"},
    'it': {"changelog": "Registro delle modifiche", "linux": "Linux"},
    'ja': {"changelog": "変更履歴", "linux": "Linux"},
    'ko': {"changelog": "변경 로그", "linux": "Linux"},
    'zh': {"changelog": "更新日志", "linux": "Linux"},
    'hi': {"changelog": "परिवर्तन लॉग", "linux": "Linux"},
    'ru': {"changelog": "Список изменений", "linux": "Linux"},
    'ar': {"changelog": "سجل التغييرات", "linux": "Linux"}
}

# 1. Update app .arb files
for lang in langs:
    arb_path = os.path.join(APP_DIR, f"lib/l10n/app_{lang}.arb")
    if os.path.exists(arb_path):
        with open(arb_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for k, v in app_translations[lang].items():
            if k not in data:
                data[k] = v
        with open(arb_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update web .json files
for lang in langs:
    json_path = os.path.join(WEB_DIR, f"messages/{lang}.json")
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'Footer' not in data:
            data['Footer'] = {}
        for k, v in web_translations[lang].items():
            data['Footer'][k] = v
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# 3. Replace in App Dart Files
def apply_replacements(filepath, replacements):
    full_path = os.path.join(APP_DIR, filepath)
    if not os.path.exists(full_path):
        return
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    for old, new in replacements:
        content = re.sub(old, new, content)
    if content != orig:
        if 'package:ppplayer/l10n/app_localizations.dart' not in content:
            import_match = re.search(r"import '.*?;", content)
            if import_match:
                content = content[:import_match.start()] + "import 'package:ppplayer/l10n/app_localizations.dart';\n" + content[import_match.start():]
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

app_replacements = {
    "lib/features/home/home_screen.dart": [
        (r"title:\s*'Continue Listening'", r"title: AppLocalizations.of(context)!.continueListening"),
        (r"title:\s*'Popular Artists'", r"title: AppLocalizations.of(context)!.popularArtists"),
        (r"title:\s*'Made For You'", r"title: AppLocalizations.of(context)!.madeForYou"),
        (r"title:\s*'Suggested Stations'", r"title: AppLocalizations.of(context)!.suggestedStations"),
        (r"title:\s*'Popular Albums'", r"title: AppLocalizations.of(context)!.popularAlbums"),
        (r"title:\s*'Popular Genres'", r"title: AppLocalizations.of(context)!.popularGenres"),
        (r"title:\s*'New Releases'", r"title: AppLocalizations.of(context)!.newReleases"),
        (r"title:\s*'Featured Playlists'", r"title: AppLocalizations.of(context)!.featuredPlaylists"),
        (r"title:\s*'Popular Tracks'", r"title: AppLocalizations.of(context)!.popularTracks"),
    ],
    "lib/features/home/genre_details_screen.dart": [
        (r"title:\s*'Featured Playlists'", r"title: AppLocalizations.of(context)!.featuredPlaylists"),
        (r"title:\s*'Popular Songs'", r"title: AppLocalizations.of(context)!.popularSongs"),
    ],
    "lib/features/artist/artist_screen.dart": [
        (r"title:\s*'FEATURING \$\{artistName\.toUpperCase\(\)\}'", r"title: AppLocalizations.of(context)!.featuringArtist(artistName.toUpperCase())"),
    ],
    "lib/features/settings/settings_screen.dart": [
        (r"subtitle:\s*'Current: \$\{settings\.selectedCountry\}'", r"subtitle: AppLocalizations.of(context)!.currentCountry(settings.selectedCountry)"),
        (r"Text\('Error loading markets: \$err'\)", r"Text(AppLocalizations.of(context)!.errorLoadingMarkets(err.toString()))"),
    ],
    "lib/shared/widgets/scaffold_with_nav.dart": [
        (r"tooltip:\s*'Queue'", r"tooltip: AppLocalizations.of(context)!.queueTooltip"),
        (r"hintText:\s*'Search music, artists, albums...'", r"hintText: AppLocalizations.of(context)!.searchHint"),
    ]
}

for fp, reps in app_replacements.items():
    apply_replacements(fp, reps)

# 4. Replace in Web TSX
def apply_web_replacements(filepath, replacements):
    full_path = os.path.join(WEB_DIR, filepath)
    if not os.path.exists(full_path):
        return
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    for old, new in replacements:
        content = re.sub(old, new, content)
    if content != orig:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated Web: {filepath}")

web_replacements = {
    "components/Footer.tsx": [
        (r">Changelog<", r">{t('changelog')}<"),
        (r">Linux<", r">{t('linux')}<"),
    ]
}

for fp, reps in web_replacements.items():
    apply_web_replacements(fp, reps)
