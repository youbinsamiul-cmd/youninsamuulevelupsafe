# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════════════
#  🇧🇩  YOUBIN SAMIUL v5.1 — SQUAD + GUILD PREMIUM BOT  🇧🇩
#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#     👑 Owner      : YOUBIN SAMIUL
#     🌏 Country    : Bangladesh 🇧🇩
#     🎮 Mode       : Manual Squad Creation + Guild
#     ⚡ Version    : GLORY EDITION v5.1 (syntax fixed)
#     📅 Build      : 2026
#     🔐 Admin Pass : frexy1only
#  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import sys, asyncio, httpx, random, json, socket, struct, time, os, uuid
import itertools, secrets, traceback, base64, ssl, threading, re
import urllib.parse, urllib.request, urllib.error
import hashlib, hmac
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

try:
    from google_play_scraper import app as play_scraper
except Exception:
    play_scraper = None

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

try:
    from protobuf_decoder.protobuf_decoder import Parser
except Exception:
    Parser = None

try:
    from message_ids import MESSAGE_ID_TO_NAME
except Exception:
    MESSAGE_ID_TO_NAME = {}

try:
    import thunderFF_pb2
except Exception:
    thunderFF_pb2 = None

try:
    import CguFF_pb2
    _HAS_CGU = True
except Exception:
    _HAS_CGU = False

try:
    import requests as _requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception:
    _requests = None

# ═══════════════════════════ CONFIG ═══════════════════════════
WEB_HOST = "0.0.0.0"
WEB_PORT = 20333
ADMIN_PASSWORD = "samuu"
BRAND_WEB_NAME = "YOUBIN SAMIUL"

ACCOUNTS_FILE = "accounts.json"
TOKEN_CACHE_FILE = "token_cache.json"
DEVICES_FILE = "devices.json"
TOKEN_CACHE_TTL = 4500

NEW_MATCH_DELAY         = 6.0
MAX_MATCH_DURATION      = 3000
MATCH_IDLE_TIMEOUT      = 90.0
EXP_REFRESH_INTERVAL    = 30.0
EXP_REFRESH_AFTER_MATCH_DELAY = 9.0
NON_MATCH_RECONNECT_DELAY      = 1.0

BR_MODE_ID             = 1
BR_MAP_ID              = 1

ANTI_AFK_MIN_INTERVAL  = 1.8
ANTI_AFK_MAX_INTERVAL  = 3.5

MATCH_SEARCH_TIMEOUT   = 90.0
MATCH_WATCHDOG_CHECK   = 30.0

REGION_ROTATION_LIST   = ["BD", "BD", "SG", "TH", "MY", "IN"]
REGION_ROTATE_EVERY_N  = 2
MAX_SEARCH_ATTEMPTS    = 25
DEFAULT_REGION         = "BD"
DEFAULT_SERVER_CODE    = "BDC3"

SAFE_PLAY_MODE        = True
BYPASS_TIMING_JITTER  = True
BYPASS_PACKET_JITTER  = True
BYPASS_HELLO_DELAY    = True
BYPASS_KA_JITTER      = True

ENABLE_SPEED_MOVEMENT       = True
MOVEMENT_SPEED_MIN          = 1.0
MOVEMENT_SPEED_MAX          = 1.4
MOVEMENT_PATTERN            = "circle"
MOVEMENT_TICK_MS            = 240
MOVEMENT_RADIUS             = 180
MOVEMENT_UPDATE_SPEED_EVERY = 4.0
MOVEMENT_STATE_IDLE_CHANCE   = 0.10
MOVEMENT_STATE_WALK_CHANCE   = 0.28
MOVEMENT_STATE_RUN_CHANCE    = 0.32
MOVEMENT_STATE_SPRINT_CHANCE = 0.10
MOVEMENT_STATE_JUMP_CHANCE   = 0.08
MOVEMENT_STATE_CROUCH_CHANCE = 0.06
MOVEMENT_STATE_PRONE_CHANCE  = 0.06

ENABLE_HTTP_PING = True
PING_INTERVAL    = 20.0
PING_TIMEOUT     = 8.0
PING_URL         = "https://loginbp.ppmainecoonghj.com/Ping"
PING_REAL_IP     = "103.109.214.211"

FALLBACK_UID = ""
FALLBACK_PASSWORD = ""

# ═══════════════════════════ SQUAD CONFIG ═══════════════════════════
TEAM_MODE               = True
TEAM_SIZE               = 4
TEAM_PEER_WAIT_TIMEOUT  = 25.0
TEAM_CREATE_WAIT        = 2.0
TEAM_INVITE_CYCLE_WAIT  = 2.0
TEAM_INVITE_MAX_TIME    = 60.0
TEAM_HEARTBEAT_INTERVAL = 2.5
TEAM_IDLE_ITERS_TEAM    = 1800
TEAM_MEMBER_START_DELAY = 12.0
TEAM_FINAL_WAIT         = 4.0
TEAM_READY_DELAY        = 3.0
_accept_friend_request  = True
DEBUG_TEAM_PACKETS      = False

# ═══════════════════════════ GUILD CONFIG ═══════════════════════════
GUILD_BASE = "https://danger-guild-management-web.vercel.app"
GUILD_JOIN_API = os.environ.get("GUILD_JOIN_API", "https://raiful.gamer.free/api.php")
GUILD_LEAVE_API = os.environ.get("GUILD_LEAVE_API", GUILD_JOIN_API)
GUILD_JOIN_ENDPOINTS  = [f"{GUILD_BASE}/join"]
GUILD_LEAVE_ENDPOINTS = [
    f"{GUILD_BASE}/leave", f"{GUILD_BASE}/guild/leave",
    f"{GUILD_BASE}/quit", f"{GUILD_BASE}/guild/quit", f"{GUILD_BASE}/exit",
]
GUILD_UA = "Mozilla/5.0 (Linux; Android 10) GREAT_JOHIR/4.4"
GUILD_TAG = "GREAT JOHIR"

JWT_API_ENDPOINTS = [
    ("AGS COMMUNITY JWT API", "https://ags-community-jwt-api.vercel.app/token"),
]
BD_FRIEND_URLS = [
    "https://clientbp.ggblueshark.com/RequestAddingFriend",
    "https://client.bd.freefiremobile.com/RequestAddingFriend",
    "https://client.ind.freefiremobile.com/RequestAddingFriend",
]
FRIEND_AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
FRIEND_AES_IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
FRIEND_HEADERS = {
    "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB54",
    "Content-Type": "application/octet-stream",
    "X-Unity-Version": "2022.3.47f1",
    "Connection": "Keep-Alive"
}

# ═══════════════════════════ BRAND ═══════════════════════════
BRAND_NAME       = "YOUBIN SAMIUL"
BRAND_COUNTRY    = "Bangladesh 🇧🇩"
BRAND_VERSION    = "GLORY v5.1"
BRAND_YEAR       = "2026"
BRAND_TAGLINE    = "🔥 Bangladesh's #1 Squad Bot 🔥"

# ═══════════════════════════ ANTI-BAN ═══════════════════════════
def bypass_jitter(base, spread=0.35):
    if not (SAFE_PLAY_MODE and BYPASS_TIMING_JITTER): return base
    return max(0.05, base + random.uniform(-spread, spread))

def bypass_packet_jitter(base, spread_ratio=0.35):
    if not (SAFE_PLAY_MODE and BYPASS_PACKET_JITTER): return base
    return max(0.1, base + random.uniform(-base * spread_ratio, base * spread_ratio))

def bypass_hello_delay():
    if not (SAFE_PLAY_MODE and BYPASS_HELLO_DELAY): return 0.0
    return random.uniform(0.05, 0.45)

def bypass_ka_jitter(base=5.0):
    if not (SAFE_PLAY_MODE and BYPASS_KA_JITTER): return base
    return max(3.0, base + random.uniform(-0.8, 1.2))

def bypass_human_reconnect_delay(attempt):
    if not (SAFE_PLAY_MODE and BYPASS_TIMING_JITTER): return min(attempt * 0.5, 2.0)
    return max(0.05, min(attempt * 0.5, 2.0) + random.uniform(-0.4, 0.7))

# ═══════════════════════════ DEVICE ═══════════════════════════
def get_device_for_account(account_identifier):
    devices = {}
    if os.path.exists(DEVICES_FILE):
        try:
            with open(DEVICES_FILE, "r", encoding="utf-8") as f:
                devices = json.load(f)
        except Exception: pass
    key = str(account_identifier)
    if key in devices: return devices[key]
    dev_list = [
        ("Samsung", "SM-G998B", "Adreno (TM) 660", "Android OS 12 / API-31"),
        ("Xiaomi", "2201122G", "Adreno (TM) 730", "Android OS 13 / API-33"),
        ("Realme", "RMX3700", "Mali-G710", "Android OS 14 / API-34"),
        ("OnePlus", "CPH2451", "Adreno (TM) 740", "Android OS 13 / API-33"),
        ("OPPO", "CPH2611", "Adreno (TM) 720", "Android OS 14 / API-34"),
    ]
    brand, model, gpu, os_ver = random.choice(dev_list)
    dev = {
        "unique_device_id": f"Google|{uuid.uuid4()}",
        "brand": brand, "model": model, "gpu_renderer": gpu, "system_software": os_ver,
        "screen_width": random.choice([1080, 1440, 720]),
        "screen_height": random.choice([2400, 3200, 1600]),
        "screen_dpi": str(random.randint(300, 420)),
        "memory": random.randint(2800, 6500),
        "processor_details": f"ARM64 FP ASIMD AES | {random.randint(2200, 3200)} | {random.randint(6, 12)}",
        "client_ip": f"{random.randint(103, 223)}.{random.randint(10, 250)}.{random.randint(10, 250)}.{random.randint(10, 250)}",
    }
    devices[key] = dev
    try:
        with open(DEVICES_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2)
    except Exception: pass
    return dev

# ═══════════════════════════ DNS ═══════════════════════════
_DNS_CACHE: Dict[str, Tuple[str, float]] = {}
_DNS_CACHE_TTL = 300.0

async def resolve_host_cloudflare(hostname):
    if not hostname: return hostname
    parts = hostname.split('.')
    if len(parts) == 4 and all(p.isdigit() for p in parts): return hostname
    now = time.time()
    if hostname in _DNS_CACHE:
        ip, exp = _DNS_CACHE[hostname]
        if now < exp: return ip
    try:
        loop = asyncio.get_running_loop()
        info = await loop.getaddrinfo(hostname, None, family=socket.AF_INET)
        if info:
            ip = info[0][4][0]
            _DNS_CACHE[hostname] = (ip, now + _DNS_CACHE_TTL)
            return ip
    except Exception: pass
    return hostname

def optimize_tcp_socket(sock):
    try:
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
    except Exception: pass

def optimize_udp_socket(sock):
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 131072)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 131072)
    except Exception: pass

# ═══════════════════════════ HTTP CLIENT ═══════════════════════════
client = httpx.AsyncClient(verify=False, timeout=10.0,
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=50))
headers = {
    'User-Agent': 'UnityPlayer/2018.4.12f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)',
    'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Unity-Version': '2018.4.12f1', 'X-GA-SV': '1789535859',
    'X-GA': 'v1 1', 'ReleaseVersion': 'OB55'
}

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV  = b'6oyZDr22E3ychjM%'

CRC7_TABLE = bytes([
    0,9,18,27,36,45,54,63,72,65,90,83,108,101,126,119,25,16,11,2,61,52,47,38,
    81,88,67,74,117,124,103,110,50,59,32,41,22,31,4,13,122,115,104,97,94,87,76,69,
    43,34,57,48,15,6,29,20,99,106,113,120,71,78,85,92,100,109,118,127,64,73,82,91,
    44,37,62,55,8,1,26,19,125,116,111,102,89,80,75,66,53,60,39,46,17,24,3,10,
    86,95,68,77,114,123,96,105,30,23,12,5,58,51,40,33,79,70,93,84,107,98,121,112,
    7,14,21,28,35,42,49,56,65,72,83,90,101,108,119,126,9,0,27,18,45,36,63,54,
    88,81,74,67,124,117,110,103,16,25,2,11,52,61,38,47,115,122,97,104,87,94,69,76,
    59,50,41,32,31,22,13,4,106,99,120,113,78,71,92,85,34,43,48,57,6,15,20,29,
    37,44,55,62,1,8,19,26,109,100,127,118,73,64,91,82,60,53,46,39,24,17,10,3,
    116,125,102,111,80,89,66,75,23,30,5,12,51,58,33,40,95,86,77,68,123,114,105,96,
    14,7,28,21,42,35,56,49,70,79,84,93,98,107,112,121,
])
_DELTA = 0x9E3779B9
_ROUNDS = 16
_FIELD_SIZES = {0:1, 1:2, 2:2, 3:1, 4:2}
_FIELD_NAMES = {0:"sendOption", 1:"cmd", 2:"orderId", 3:"flags", 4:"length"}

# ═══════════════════════════ BOT STATE ═══════════════════════════
class BotState:
    def __init__(self):
        self.accounts: Dict[str, dict] = {}
        self.account_workers: Dict[str, asyncio.Task] = {}
        self.account_credentials: Dict[str, dict] = {}
        self.logs: Dict[str, List[dict]] = {}
        self.squad_logs: Dict[int, List[dict]] = {}
        self._log_lock = asyncio.Lock()
        self.paused: set = set()
        self.refresh_callbacks: dict = {}
        self.guild_jobs: Dict[int, dict] = {}
        self._guild_job_lock = asyncio.Lock()
        self._guild_job_counter = 0
        self._guild_nums: Dict[str, int] = {}

    def _fmt_time(self):
        return datetime.now().strftime("%H:%M:%S")

    async def log(self, uid: str, msg: str, level: str = "info"):
        uid = str(uid)
        entry = {"t": self._fmt_time(), "m": msg, "lvl": level}
        async with self._log_lock:
            if uid not in self.logs: self.logs[uid] = []
            self.logs[uid].append(entry)
            if len(self.logs[uid]) > 200:
                self.logs[uid] = self.logs[uid][-200:]

    def log_sync(self, uid: str, msg: str, level: str = "info"):
        uid = str(uid)
        entry = {"t": self._fmt_time(), "m": msg, "lvl": level}
        if uid not in self.logs: self.logs[uid] = []
        self.logs[uid].append(entry)
        if len(self.logs[uid]) > 200:
            self.logs[uid] = self.logs[uid][-200:]

    def squad_log(self, squad_id: int, msg: str, level: str = "info"):
        try:
            sid = int(squad_id)
        except Exception:
            return
        # users only ever see their own squad numbers, never the global internal id
        try:
            _num = squad_mgr.squads.get(sid, {}).get("num")
            if _num and _num != sid:
                msg = str(msg).replace(f"Squad {sid}", f"Squad {_num}")
        except Exception:
            pass
        entry = {"t": self._fmt_time(), "m": msg, "lvl": level}
        if sid not in self.squad_logs: self.squad_logs[sid] = []
        self.squad_logs[sid].append(entry)
        if len(self.squad_logs[sid]) > 300:
            self.squad_logs[sid] = self.squad_logs[sid][-300:]

    def register_account(self, uid, nickname, region, level, exp, likes, password="", slot=0):
        uid = str(uid)
        cur = self.accounts.get(uid, {})
        self.accounts[uid] = {
            **cur,
            "uid": uid, "nickname": nickname, "region": region,
            "level": level, "exp": exp, "likes": likes,
            "password": password, "slot": slot,
            "status": cur.get("status", "ONLINE"),
            "matches": cur.get("matches", 0),
            "added_at": cur.get("added_at", time.time()),
            "guild_status": cur.get("guild_status", "—"),
            "guild_detail": cur.get("guild_detail", ""),
            "squad_id": cur.get("squad_id", 0),
        }

    def update_status(self, uid, status, matches=None):
        uid = str(uid)
        if uid in self.accounts:
            self.accounts[uid]["status"] = status
            if matches is not None:
                self.accounts[uid]["matches"] = matches

    def update_exp(self, uid, exp, level):
        uid = str(uid)
        if uid in self.accounts:
            self.accounts[uid]["exp"] = exp
            self.accounts[uid]["level"] = level

    def update_guild(self, uid, status, detail=""):
        uid = str(uid)
        if uid in self.accounts:
            self.accounts[uid]["guild_status"] = status
            self.accounts[uid]["guild_detail"] = detail

    def increment_match(self, uid):
        uid = str(uid)
        if uid in self.accounts:
            self.accounts[uid]["matches"] = self.accounts[uid].get("matches", 0) + 1

    def is_paused(self, uid):
        return str(uid) in self.paused

    async def new_guild_job(self, guild_id, action, uids, owner=None):
        async with self._guild_job_lock:
            self._guild_job_counter += 1
            jid = self._guild_job_counter
            num = self._guild_nums.get(owner, 0) + 1
            self._guild_nums[owner] = num
            self.guild_jobs[jid] = {
                "id": jid, "num": num, "owner": owner,
                "guild_id": str(guild_id), "action": action,
                "uids": list(uids), "results": {}, "started": time.time(),
                "done": False, "owner_uid": None,
            }
            mine = [k for k, j in self.guild_jobs.items() if j.get("owner") == owner]
            for k in mine[:-20]:
                self.guild_jobs.pop(k, None)
            return jid

    def purge_owner(self, owner):
        for k in [k for k, j in self.guild_jobs.items() if j.get("owner") == owner]:
            self.guild_jobs.pop(k, None)
        self._guild_nums.pop(owner, None)

    def add_guild_result(self, jid, uid, ok, msg, detail=""):
        if jid in self.guild_jobs:
            self.guild_jobs[jid]["results"][str(uid)] = {
                "ok": bool(ok), "msg": str(msg)[:200], "detail": str(detail)[:200],
                "at": time.time(),
            }

    def finish_guild_job(self, jid):
        if jid in self.guild_jobs:
            self.guild_jobs[jid]["done"] = True

bot_state = BotState()

# ═══════════════════════════ CONSOLE COLORS ═══════════════════════════
class Colors:
    GREEN='\033[92m'; FAIL='\033[91m'; WARNING='\033[93m'
    CYAN='\033[96m'; MAGENTA='\033[95m'; WHITE='\033[97m'; ENDC='\033[0m'
    BRAND   = '\033[38;5;208m'
    BDRED   = '\033[38;5;196m'
    BDGREEN = '\033[38;5;46m'
    GOLD    = '\033[38;5;220m'
    PURPLE  = '\033[38;5;93m'
    PINK    = '\033[38;5;213m'
    SKY     = '\033[38;5;51m'
    DIM     = '\033[2m'
    BOLD    = '\033[1m'

def print_colored(t, c=Colors.WHITE):
    try: print(f"{c}{t}{Colors.ENDC}")
    except Exception: pass

def print_banner():
    banner = f"""
{Colors.BDRED}╔══════════════════════════════════════════════════════════════════╗
{Colors.BDRED}║{Colors.BDGREEN}                                                                  {Colors.BDRED}║
{Colors.BDRED}║{Colors.BDGREEN}              Y  O  U  B  I  N     S  A  M  I  U  L               {Colors.BDRED}║
{Colors.BDRED}║{Colors.GOLD}          ━━━━━━  P R E M I U M   E D I T I O N  ━━━━━━           {Colors.BDRED}║
{Colors.BDRED}║{Colors.BDGREEN}                                                                  {Colors.BDRED}║
{Colors.BDRED}╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
{Colors.GOLD}     ⚡  {Colors.BOLD}YOUBIN SAMIUL — SQUAD + GUILD PREMIUM BOT{Colors.ENDC} {Colors.GOLD}⚡{Colors.ENDC}
{Colors.BDGREEN}     🇧🇩  Made in {BRAND_COUNTRY}  |  © {BRAND_YEAR} {BRAND_NAME}  🇧🇩{Colors.ENDC}
{Colors.PINK}              {BRAND_TAGLINE}{Colors.ENDC}
{Colors.DIM}      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.ENDC}
"""
    try: print(banner)
    except Exception: pass

def print_success(t, uid=""):
    print_colored(f"  {Colors.BDGREEN}✔{Colors.ENDC} {t}", Colors.WHITE)
    if uid: bot_state.log_sync(uid, t, "success")

def print_error(t, uid=""):
    print_colored(f"  {Colors.BDRED}✘{Colors.ENDC} {t}", Colors.WHITE)
    if uid: bot_state.log_sync(uid, t, "error")

def print_warning(t, uid=""):
    print_colored(f"  {Colors.GOLD}⚠{Colors.ENDC} {t}", Colors.WHITE)
    if uid: bot_state.log_sync(uid, t, "warning")

def print_info(t, uid=""):
    print_colored(f"  {Colors.SKY}ℹ{Colors.ENDC} {t}", Colors.WHITE)
    if uid: bot_state.log_sync(uid, t, "info")

def print_section(title, color=None):
    color = color or Colors.PURPLE
    bar = "━" * 62
    print_colored(f"\n{color}┏{bar}┓{Colors.ENDC}", color)
    print_colored(f"{color}┃{Colors.ENDC}  {Colors.BOLD}{Colors.GOLD}{title.center(58)}{Colors.ENDC}  {color}┃{Colors.ENDC}", color)
    print_colored(f"{color}┗{bar}┛{Colors.ENDC}\n", color)

def get_proto_field(d, key, default=None):
    if not d or not isinstance(d, dict): return default
    if key in d:
        v = d[key].get('data'); return v if v is not None else default
    if str(key) in d:
        v = d[str(key)].get('data'); return v if v is not None else default
    return default

# ═══════════════════════════ MATCH COUNTER ═══════════════════════════
_match_counters: Dict[str, int] = {}
_match_counter_lock = asyncio.Lock()

async def _inc_match(uid):
    async with _match_counter_lock:
        _match_counters[uid] = _match_counters.get(uid, 0) + 1
        return _match_counters[uid]

async def _dec_match(uid):
    async with _match_counter_lock:
        if uid in _match_counters and _match_counters[uid] > 0:
            _match_counters[uid] -= 1
        return _match_counters.get(uid, 0)

async def _get_match_count(uid):
    async with _match_counter_lock:
        return _match_counters.get(uid, 0)

# ═══════════════════════════ SQUAD RUNTIME ═══════════════════════════
class SquadRuntime:
    def __init__(self, squad_id):
        self.squad_id = squad_id
        self.members_uids: List[str] = []
        self.peers: Dict[str, dict] = {}
        self.leader_uid: Optional[str] = None
        self.team_code: Optional[str] = None
        self.pk_code: Optional[str] = None
        self.members_joined: set = set()
        self.lock = asyncio.Lock()
        self.members_lock = asyncio.Lock()
        self.is_running = False
        self.team_active = True
        self.match_count = 0

    async def member_join(self, uid):
        uid = str(uid)
        async with self.members_lock:
            before = len(self.members_joined)
            self.members_joined.add(uid)
            after = len(self.members_joined)
        if after != before:
            print_success(f"👥 [SQUAD-{self.squad_id}] Member Joined ({after}/{TEAM_SIZE}) → {uid}", uid)
            bot_state.squad_log(self.squad_id, f"Member joined ({after}/{TEAM_SIZE}): {uid}", "success")
        return after

    async def member_leave(self, uid):
        async with self.members_lock:
            self.members_joined.discard(str(uid))

    async def member_count(self):
        async with self.members_lock:
            return len(self.members_joined)

    async def reset_members(self, keep_leader=True):
        async with self.members_lock:
            self.members_joined.clear()
            if keep_leader and self.leader_uid:
                self.members_joined.add(self.leader_uid)

# ═══════════════════════════ TOKEN CACHE ═══════════════════════════
_token_cache_memo = {}
_token_cache_memo_time = 0.0
_TOKEN_CACHE_MEMO_TTL = 5.0

def _json_serializer(obj):
    if isinstance(obj, (bytes, bytearray)): return {"__bytes_hex__": bytes(obj).hex()}
    raise TypeError(f"not serializable: {type(obj)}")

def _json_deserializer(obj):
    if isinstance(obj, dict):
        if "__bytes_hex__" in obj and len(obj) == 1:
            try: return bytes.fromhex(obj["__bytes_hex__"])
            except Exception: return b""
        return {k: _json_deserializer(v) for k, v in obj.items()}
    if isinstance(obj, list): return [_json_deserializer(x) for x in obj]
    return obj

def _load_token_cache():
    global _token_cache_memo, _token_cache_memo_time
    now = time.time()
    if _token_cache_memo and (now - _token_cache_memo_time) < _TOKEN_CACHE_MEMO_TTL:
        return _token_cache_memo
    if not os.path.exists(TOKEN_CACHE_FILE): return {}
    try:
        with open(TOKEN_CACHE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content: return {}
        data = json.loads(content)
        if not isinstance(data, dict): raise ValueError("root must be dict")
        parsed = _json_deserializer(data)
        _token_cache_memo = parsed; _token_cache_memo_time = now
        return parsed
    except Exception as e:
        print_error(f"Token cache corrupt → delete: {e}")
        try: os.remove(TOKEN_CACHE_FILE)
        except Exception: pass
        return {}

def _save_token_cache(cache):
    global _token_cache_memo, _token_cache_memo_time
    try:
        tmp = TOKEN_CACHE_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, default=_json_serializer)
        os.replace(tmp, TOKEN_CACHE_FILE)
        _token_cache_memo = cache; _token_cache_memo_time = time.time()
    except Exception as e: print_error(f"Cache save: {e}")

def cache_get(uid):
    cache = _load_token_cache()
    e = cache.get(str(uid))
    if not e: return None
    if time.time() - e.get("cached_at", 0) > TOKEN_CACHE_TTL:
        cache_invalidate(uid); return None
    if str(e.get("account_id", "")).isdigit(): e["account_id"] = int(e["account_id"])
    if not isinstance(e.get("login_payload_data"), (bytes, bytearray)):
        cache_invalidate(uid); return None
    return e

def cache_set(uid, data):
    cache = _load_token_cache()
    e = dict(data); e["cached_at"] = time.time()
    cache[str(uid)] = e; _save_token_cache(cache)
    print_success(f"💾 [CACHE] Saved UID {uid}")

def cache_invalidate(uid):
    cache = _load_token_cache()
    if str(uid) in cache:
        del cache[str(uid)]; _save_token_cache(cache)

def _update_cache_profile(data, level, exp):
    try:
        keys = []
        if data.get('auth_uid'): keys.append(str(data['auth_uid']))
        if data.get('auth_token'): keys.append(f"tok_{data['auth_token'][:20]}")
        if not keys: return
        cache = _load_token_cache(); ch = False
        for k in keys:
            if k in cache and isinstance(cache[k], dict):
                cache[k]['level'] = level; cache[k]['exp'] = exp; ch = True
        if ch: _save_token_cache(cache)
    except Exception: pass

# ═══════════════════════════ ENCRYPTION ═══════════════════════════
async def aes_encrypt(payload, key, iv):
    return AES.new(key, AES.MODE_CBC, iv).encrypt(pad(payload, AES.block_size))

async def get_playstore_version():
    if play_scraper is None: return "1.132.9"
    loop = asyncio.get_event_loop()
    try:
        res = await loop.run_in_executor(None, lambda: play_scraper('com.dts.freefireth', lang='hi', country='bd'))
        return res.get("version") or "1.132.9"
    except Exception:
        return "1.132.9"

async def version_config():
    app_version = await get_playstore_version()
    url = ("https://version.ggwhitehawk.com/live/ver.php"
           f"?version={app_version}&lang=hi&device=android&channel=android"
           "&appstore=googleplay&region=BD&whitelist_version=1.3.0&whitelist_sp_version=1.0.0")
    try:
        r = await client.get(url); r.raise_for_status()
        d = r.json()
        su = d.get("server_url"); rv = d.get("remote_version"); lr = d.get("latest_release_version")
        if not su or not rv or not lr: return None
        return lr, rv, su
    except Exception: return None

async def get_access_token(uid, password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    hdrs = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; SM-G998B)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br", "Connection": "close"
    }
    data = {
        "uid": uid, "password": password, "response_type": "token", "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    for attempt in range(5):
        try:
            r = await client.post(url, headers=hdrs, data=data)
            if r.status_code == 200:
                d = r.json()
                oid = d.get("open_id"); at = d.get("access_token"); pf = d.get("platform", 4)
                if oid and at: return oid, at, pf
            if r.status_code == 429: await asyncio.sleep(1); continue
        except Exception: pass
        await asyncio.sleep(0.5)
    return None

async def parse_results(parsed):
    out = {}
    for r in parsed:
        fd = {"wire_type": r.wire_type}
        if r.wire_type in ("varint", "string", "bytes"): fd["data"] = r.data
        elif r.wire_type == "length_delimited":
            fd["data"] = await parse_results(r.data.results)
        out[r.field] = fd
    return out

async def decode_protobuf(data):
    if Parser is None: return "{}"
    parsed = Parser().parse(data)
    return json.dumps(await parse_results(parsed))

def decode_protobuf_dict_safe(data):
    if Parser is None: return {}
    try:
        parsed = Parser().parse(data)
        return _recursive_dict(parsed)
    except Exception: return {}

def _recursive_dict(results):
    out = {}
    for r in results:
        fd = {"wire_type": r.wire_type}
        if r.wire_type in ("varint", "string", "bytes"): fd["data"] = r.data
        elif r.wire_type == "length_delimited":
            if hasattr(r.data, "results"): fd["data"] = _recursive_dict(r.data.results)
            elif isinstance(r.data, list): fd["data"] = _recursive_dict(r.data)
            else: fd["data"] = str(r.data)
        out[str(r.field)] = fd
    return out

def _decode_proto_manual(data):
    result = {}; offset = 0; data_len = len(data)
    while offset < data_len:
        header = 0; shift = 0
        while offset < data_len:
            b = data[offset]; offset += 1
            header |= (b & 0x7F) << shift
            if not (b & 0x80): break
            shift += 7
            if shift > 28: break
        if header == 0: break
        fn = header >> 3; wt = header & 0x7
        if fn == 0: break
        if wt == 0:
            v = 0; shift = 0
            while offset < data_len:
                b = data[offset]; offset += 1
                v |= (b & 0x7F) << shift
                if not (b & 0x80): break
                shift += 7
                if shift > 63: break
            result[fn] = v
        elif wt == 2:
            length = 0; shift = 0
            while offset < data_len:
                b = data[offset]; offset += 1
                length |= (b & 0x7F) << shift
                if not (b & 0x80): break
                shift += 7
                if shift > 28: break
            if length > data_len - offset: break
            value = data[offset:offset+length]; offset += length
            try:
                s = value.decode('utf-8')
                if s and all(31 < ord(c) < 127 or ord(c) in (9,10,13) for c in s):
                    result[fn] = s
                else:
                    nested = _decode_proto_manual(value)
                    result[fn] = nested if nested else value.hex()
            except UnicodeDecodeError:
                nested = _decode_proto_manual(value)
                result[fn] = nested if nested else value.hex()
        elif wt == 5: offset += 4
        elif wt == 1: offset += 8
        else: break
    return result

# ═══════════════════════════ PROTOBUF ENCODE ═══════════════════════════
def encode_varint(n):
    if n < 0: return b''
    out = bytearray()
    while True:
        b = n & 0x7F; n >>= 7
        if n: b |= 0x80
        out.append(b)
        if not n: break
    return bytes(out)

def build_proto(fields):
    parts = []
    for k, v in fields.items():
        if isinstance(v, dict):
            nested = build_proto(v)
            parts.append(encode_varint((k << 3) | 2) + encode_varint(len(nested)) + nested)
        elif isinstance(v, int):
            parts.append(encode_varint((k << 3) | 0) + encode_varint(v))
        elif isinstance(v, (str, bytes)):
            ev = v.encode() if isinstance(v, str) else v
            parts.append(encode_varint((k << 3) | 2) + encode_varint(len(ev)) + ev)
    return b''.join(parts)

def encrypt_api(plain_hex):
    return AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(
        pad(bytes.fromhex(plain_hex), AES.block_size)).hex()

def encrypt_api_bytes(plain_bytes):
    return AES.new(AES_KEY, AES.MODE_CBC, AES_IV).encrypt(pad(plain_bytes, AES.block_size))

# ═══════════════════════════ SQUAD BUILDERS ═══════════════════════════
def _pb_varint(fn, val): return encode_varint((fn << 3) | 0) + encode_varint(val)
def _pb_length(fn, val):
    enc = val.encode('utf-8') if isinstance(val, str) else val
    return encode_varint((fn << 3) | 2) + encode_varint(len(enc)) + enc

def create_proto(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(field, str): field = int(field)
        if isinstance(value, dict):
            packet.extend(_pb_length(field, bytes(create_proto(value))))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    packet.extend(_pb_length(field, bytes(create_proto(item))))
                elif isinstance(item, str): packet.extend(_pb_length(field, item))
                elif isinstance(item, (bytes, bytearray)): packet.extend(_pb_length(field, bytes(item)))
                elif isinstance(item, bool): packet.extend(_pb_varint(field, 1 if item else 0))
                elif isinstance(item, int): packet.extend(_pb_varint(field, item))
        elif isinstance(value, bool): packet.extend(_pb_varint(field, 1 if value else 0))
        elif isinstance(value, int): packet.extend(_pb_varint(field, value))
        elif isinstance(value, str): packet.extend(_pb_length(field, value))
        elif isinstance(value, (bytes, bytearray)): packet.extend(_pb_length(field, bytes(value)))
    return bytes(packet)

def create_packet(Pk, N, K, V):
    if isinstance(K, str): K = bytes.fromhex(K) if len(K) == 32 else K.encode()
    if isinstance(V, str): V = bytes.fromhex(V) if len(V) == 32 else V.encode()
    PkEnc = AES.new(K, AES.MODE_CBC, V).encrypt(pad(bytes.fromhex(Pk), 16)).hex()
    L = len(PkEnc) // 2
    hexlen = hex(L)[2:]
    if len(hexlen) % 2 != 0: hexlen = '0' + hexlen
    pad_len = 12 - len(N) - len(hexlen)
    if pad_len < 0: pad_len = 0
    return bytes.fromhex(N + ('0' * pad_len) + hexlen + PkEnc)

def create_team(key, iv, game_version="1.132.9"):
    fields = {
        1: 1, 2: {2: bytes.fromhex("01"), 3: 1, 4: 3, 5: "en",
            8: {1: "BDC3", 2: 123, 3: "BD"}, 9: 1,
            10: bytes.fromhex("01090a0b1219202729"), 11: 2, 13: 1,
            14: {1: "08FBA33B4BABE2790205390333330000009700050092005F72697EB2134DCBB2467625142201040e38e848dc0e748c3f6aa04d81000000ff1113090dcacfa16d",
                 2: 478, 3: "7e585d55", 4: "y[Z]", 6: 12, 7: "15686677735a7506101c",
                 8: str(game_version), 9: 3, 10: 1, 11: "03626253513637754174"},
            19: 329, 21: bytes.fromhex("374f521955"), 24: {1: 21},
            27: "a_6534489873065906362"}}
    return create_packet(create_proto(fields).hex(), "0515", key, iv)

def team_fresh(account_id, key, iv):
    return create_packet(create_proto({1: 72, 2: {1: int(account_id)}}).hex(), "0515", key, iv)

def invite_player_in_team(target_uid, key, iv, region="BD"):
    return create_packet(create_proto({1: 2, 2: {1: int(target_uid), 2: region, 4: 1}}).hex(),
                         "0515", key, iv)

def accept_team_invite(target_uid, group_id, key, iv):
    fields = {1: 4, 2: {1: int(target_uid), 3: int(target_uid),
        4: bytes.fromhex("0107090a0b120f19202729"), 8: 1,
        9: {1: "08FBA33B0522052002041B0222220007000C00010004000547E265AE1080779546762514110104076fa2e8770e748c3f6a68ed75000000ff08080500cacfa16d",
            2: 235, 3: {14: 80, 11: 86}, 4: "{Y\\R", 6: 13, 7: {2: 4},
            8: "1.132.9", 9: 2, 10: 1, 11: "0362625351"},
        10: str(group_id),
        11: {"1": "BDC3", "2": 107, "3": "BD"}, 13: "en", 16: "374f5219",
        20: {1: 21}, 23: "a_6534489873065906362",
        24: "https://dl-sg-production.freefiremobile.com/",
        27: {1: 2, 2: 4}}}
    return create_packet(create_proto(fields).hex(), "0515", key, iv)

def start_match_team(account_id, key, iv, region="BD"):
    fields = {1: 9, 2: {1: int(account_id), 7: {1: "BDC3", 2: 410, 3: region}}}
    return create_packet(create_proto(fields).hex(), "0515", key, iv)

def ready_for_game(uid, key, iv):
    return create_packet(create_proto({1: 15, 2: {1: uid, 2: 1}}).hex(), "0519", key, iv)

# ═══════════════════════════ MAJORLOGIN ═══════════════════════════
async def build_majorlogin_payload(open_id, access_token, platform, client_version, dev):
    try:
        p = {
            3: str(datetime.now())[:-7], 4: "free fire", 5: "1",
            7: str(client_version) if client_version else "1.132.8",
            8: str(dev.get("system_software", "Android OS 14 / API-34")),
            9: "Handheld", 10: "Grameenphone", 11: "CarrierDataNetwork",
            12: str(dev.get("screen_width", 1639)),
            13: str(dev.get("screen_height", 720)),
            14: str(dev.get("screen_dpi", 320)),
            15: str(dev.get("processor_details", "ARM64 FP ASIMD AES | 2000 | 8")),
            16: str(dev.get("memory", 5653)),
            17: str(dev.get("gpu_renderer", "Mali-G52 MC2")),
            18: "OpenGL ES 3.2 v1.r49p1-03bet0",
            19: str(dev.get("unique_device_id", f"Google|{uuid.uuid4()}")),
            20: str(dev.get("client_ip", "182.5.135.225")),
            21: "en", 22: str(open_id), 23: str(platform), 24: "Handheld",
            25: str(dev.get("model", "Xiaomi")), 26: "BD",
            29: str(access_token), 30: "1", 41: "Grameenphone", 42: "4G",
            57: "7428b253defc164018c604a1ebbfebdf", 60: "109278", 61: "55402",
            62: "868", 64: "55927", 65: "109278", 66: "55927", 67: "109278",
            73: 2,
            74: "/data/app/~~6Cw028g_ld-8Z0z2qhrOLA==/com.dts.freefireth-i3wiaEmpx8CbiRVhUMx_ag==/lib/arm64",
            76: 1,
            77: "b8e0cd5e295eee42f5860d3c86e483dd|/data/app/~~6Cw028g_ld-8Z0z2qhrOLA==/com.dts.freefireth-i3wiaEmpx8CbiRVhUMx_ag==/base.apk",
            78: 6, 79: 1, 81: "32", 83: "2019121229", 85: 3,
            86: "OpenGLES2", 87: 3071, 88: 4, 89: 14466, 93: "3rd_party",
            94: "KqsHTyb7yHjsAiyNWUUZa0DSOD6U0AhDQ76smAo1WeHHHpSmJ8KMRyRrxb2ttgJqO9YOqO/K6AORAvDMAX/qBS8+JahIkrM7kHfzlfULbgRAoZ9r",
            95: "111207", 96: "{\"cur_rate\":[60,90,120],\"support_etc2\":true}", 97: "1",
            98: "1", 99: str(platform), 100: str(platform),
            103: "1", 104: "52837", 105: "1",
            106: "https://dl.gmc.freefiremobile.com/live/ABHotUpdates/|211c933168f55902c7dfbfd8c4e2957d",
            107: "1.3fb8adbf45f44ce9",
        }
        return encrypt_api_bytes(build_proto(p))
    except Exception as e:
        print_error(f"build_majorlogin_payload: {e}"); return None

async def send_majorlogin(data, release_version, server_url):
    if thunderFF_pb2 is None: return None
    try:
        url = f"{server_url}MajorLogin" if server_url.endswith('/') else f"{server_url}/MajorLogin"
        hdrs = headers.copy(); hdrs["ReleaseVersion"] = str(release_version)
        r = await client.post(url, headers=hdrs, data=data)
        if r.status_code != 200:
            print_error(f"[MAJORLOGIN] HTTP {r.status_code}"); return None
        c = r.content
        if len(c) < 40: return None
        for off in [0, 64] + list(range(128)):
            try:
                m = thunderFF_pb2.MajorLoginRes(); m.ParseFromString(c[off:])
                if m.region and m.token: return m
            except Exception: continue
        return None
    except Exception as e:
        print_error(f"[MAJORLOGIN] {e}"); return None

async def send_getlogin(data, base_url, token, release_version):
    if thunderFF_pb2 is None: return None
    try:
        url = f"{base_url.rstrip('/')}/GetLoginData"
        hdrs = headers.copy()
        hdrs["ReleaseVersion"] = release_version
        hdrs['Authorization'] = f"Bearer {token}"
        hdrs['Host'] = "clientbp.ppmainecoonghj.com"
        r = await client.post(url, headers=hdrs, data=data)
        if r.status_code != 200: return None
        c = r.content
        rp = thunderFF_pb2.GetLoginDataRes()
        ok = False
        try:
            rp.ParseFromString(c)
            if rp.functional_addrs or rp.informational_addrs: ok = True
        except Exception: pass
        if not ok:
            for off in range(min(128, len(c))):
                try:
                    cand = thunderFF_pb2.GetLoginDataRes(); cand.ParseFromString(c[off:])
                    if cand.functional_addrs or cand.informational_addrs:
                        rp = cand; break
                except Exception: continue
        dd = {}
        try:
            if Parser is not None:
                parsed = Parser().parse(c.hex())
                dd = await parse_results(parsed)
        except Exception: pass
        return rp, dd
    except Exception: return None

# ═══════════════════════════ HTTP PING ═══════════════════════════
async def send_ping(account_id, token, release_version):
    try:
        try: acc = int(account_id)
        except Exception: acc = 0
        now_ms = int(time.time() * 1000)
        payload = struct.pack("<Q", acc & 0xFFFFFFFFFFFFFFFF) + struct.pack("<Q", now_ms & 0xFFFFFFFFFFFFFFFF)
        req_id = secrets.token_urlsafe(18)[:22]
        hdrs = {
            'accept': '*/*', 'accept-encoding': 'deflate, gzip',
            'authorization': f'Bearer {token}',
            'content-type': 'application/x-www-form-urlencoded',
            'releaseversion': release_version,
            'user-agent': 'UnityPlayer/2018.4.12f1',
            'x-ga': 'v1 1', 'x-ga-sv': str(int(time.time())),
            'x-railway-edge': 'sin1', 'x-railway-request-id': req_id,
            'x-real-ip': PING_REAL_IP, 'x-request-start': str(now_ms),
            'x-unity-version': '2018.4.12f1',
        }
        r = await client.post(PING_URL, headers=hdrs, content=payload, timeout=PING_TIMEOUT)
        return r.status_code == 200
    except Exception: return False

async def ping_worker(account_id, token, release_version, region="BD"):
    if not ENABLE_HTTP_PING: return
    uid_str = str(account_id); ok_count = 0; fails = 0
    try:
        await asyncio.sleep(5.0 + random.uniform(0, 2.0))
        while True:
            ok = await send_ping(uid_str, token, release_version)
            if ok: ok_count += 1; fails = 0
            else: fails += 1
            await asyncio.sleep(max(5.0, PING_INTERVAL + random.uniform(-3.0, 3.0)))
    except asyncio.CancelledError: pass

# ═══════════════════════════ TCP STARTUP ═══════════════════════════
async def build_tcp_startup_packet(account_id, token, server_time, key, iv, region="BD", typ='OnLine'):
    uid_hex = f"{int(account_id):016x}"
    ts_hex = f"{int(server_time):08x}"
    enc = (await aes_encrypt(token.encode(), key, iv)).hex()
    enc_len = f"{len(enc)//2:08x}"
    reg = str(region).upper() if region else "BD"
    if typ == 'OnLine':
        if reg == 'BD':     pfx = '7119'
        elif reg == 'IND':  pfx = '7114'
        else:               pfx = '7115'
        return f"{pfx}{uid_hex}{ts_hex}00000000{enc_len}{enc}"
    if reg == 'BD':     pfx = '9219'
    elif reg == 'IND':  pfx = '9214'
    else:               pfx = '9215'
    return f"{pfx}{uid_hex}{ts_hex}{enc_len}{enc}"

async def send_keep_alive(region="BD"):
    try:
        reg = str(region).upper() if region else "BD"
        if reg == "BD":  return bytes.fromhex("0219")
        if reg == "IND": return bytes.fromhex("0214")
        return bytes.fromhex("0215")
    except Exception:
        return bytes.fromhex("0219")

# ═══════════════════════════ BR SEARCH ═══════════════════════════
BR_HEX = (
    "080112800a0a010110013a110a044944433110aa011a064555524f50453a100a044944433210311a064555524f5045"
    "40014a0801090a0b1219202758016291090a80013038384638324246303241393637363730323031303130303030"
    "30303030303030303030303030303031363030303130303135303030323232463937454545304630303030303034363736323531"
    "34303030303030303030303030303030303030303030303030303030303030303030303030306666303030303030"
    "3030636163666131366410241afb02735d5e571400024a775d45414d1a041b1c001f11010449715f4243481a001e"
    "1d071c1703004b1a4066785c524570735c51486775421b5c5a4c07504042685a63610816054e19025e7519600147"
    "7c015165406370195f5547404e4550640103020f1304064863754268676c755f65576e40467e5f0a417a4701026d"
    "675d6e73670b1108495a4c6a0b78470b740065645e525a057258425f584a447d4e6759440c11044e7c596d7f4b62"
    "5f7d04055a47505c4e1d6b5b4107447d7201057d7f0f14084e430457674f7e517d72015172415d027473577c4d61"
    "5f79535256780911030f4d5e027a797f614165067806505d53777750475e75064257076500460817014e741e7e50"
    "78487e7a7c465e7669767153497064605a7376677773550d160148037e18675966787f4c42607a645f577e7b44"
    "1b460776026b18685d0b110205490060020f70676175654674706671797f41067346677c4e06585e780f15074c57"
    "047b40517075415f6364027259674b5b0166407f7340600407770a22047a5d5c52300b3a0a167305067162727516"
    "134208312e3133302e3232480350015ae90403626253513635686e556f4e36416456324b796f566c636f47777648"
    "4f624e56526c4d727073504b4f43654177616848494176795556497273743752737149734a7a786b324752526837"
    "7a2f637664626d504f6a73552f79626d38547a4c69586d2f474351696d494b53486833447955726f39515152756c"
    "34545350626d6d624b7949565937545671577059455372323646572f59624578507338514f706d317372785455736c"
    "30796a434144444d4f34616a654b615753366361496c554b4963797a494e396d52516f715277687939797257476d"
    "337a644345337a6a61436f492f5a585233656f65365a42647a64677654636b6b665733356e4d4c6a6a56507256"
    "4b6433523172756174394e50514150724a5546627859696c4c5a3859707336654d5447666b6649793574666a526c"
    "314d4648706b51774c6373374439656378566c41636f374e664f6d2b30654756466c443474447870677138553359"
    "5973587645384842502f70666c767a737138316a32524f4d7857437556445442492f684735625462773166456e42"
    "49725162762b636144775147696f74554e316d4c4b77734379456f4766706746614251457645672b736a764c4c78"
    "704743334c304a5344532f74526169504354553344374e6249306547516651622f5a466f4c36455630775a324d6f"
    "583932414c572f5049752f56634663584e70596b356f7966326151416a536971486a2f363276354843644f525551"
    "303578754e6171795251625653704654303137655237675255636b4966366c6f447476342b514e4a4670766d7475"
    "7077707774396a5a5974437a4b56743657726d6e36785837706658456251555434684f3758a201050803108703a2"
    "01050804108103a20105080510c001a20105081d10cc01a2010408161078a20105080e10af01a201020815"
)

async def start_game_battle_royale(region, client_version, writer, key, iv):
    packet = bytes.fromhex(BR_HEX)
    try:
        if _HAS_CGU:
            proto = CguFF_pb2.StartMatch(); proto.ParseFromString(packet)
            if hasattr(proto.main, 'region_list') and len(proto.main.region_list) > 0:
                proto.main.region_list[0].region = region
                if len(proto.main.region_list) > 1: proto.main.region_list[1].region = region
            if hasattr(proto.main, 'client_version'):
                proto.main.client_version.remote_version = client_version
            packet = proto.SerializeToString()
    except Exception: pass
    enc = (await aes_encrypt(packet, key, iv)).hex()
    plen = len(enc) // 2
    hl = hex(plen)[2:]
    hl = hl if len(hl) > 1 else "0" + hl
    reg = str(region).upper() if region else "BD"
    if reg == "BD":    pfx = "031900"
    elif reg == "IND": pfx = "031400"
    else:              pfx = "031500"
    final = pfx + "0" * (6 - len(hl)) + hl + enc
    writer.write(bytes.fromhex(final)); await writer.drain()
    print_success(f"🇧🇩 [BR] Search Sent → {plen}B | Region={reg}")

# ═══════════════════════════ UDP HELPERS ═══════════════════════════
async def has_ssan_zig(n):
    z = (n << 1) & 0xFFFFFFFFFFFFFFFF
    out = bytearray()
    while z >= 0x80: out.append((z & 0x7F) | 0x80); z >>= 7
    out.append(z); return bytes(out)

async def uleb_encode(n):
    out = bytearray()
    while True:
        b = n & 0x7F; n >>= 7
        if n: b |= 0x80
        out.append(b)
        if not n: break
    return bytes(out)

async def zigzag_encode_signed(n):
    try: n = int(n)
    except Exception: n = 0
    zz = (n << 1) ^ (n >> 63)
    if zz < 0: zz = -zz
    out = bytearray()
    while True:
        b = zz & 0x7F; zz >>= 7
        if zz: b |= 0x80
        out.append(b)
        if not zz: break
    return bytes(out)

async def tea_enc(v0, v1, k0, k1, k2, k3):
    s = 0
    for _ in range(_ROUNDS):
        s = (s + _DELTA) & 0xFFFFFFFF
        v0 = (v0 + (((((v1<<4)&0xFFFFFFFF)+k0)&0xFFFFFFFF ^ ((v1+s)&0xFFFFFFFF) ^ (((v1>>5)+k1)&0xFFFFFFFF)))) & 0xFFFFFFFF
        v1 = (v1 + (((((v0<<4)&0xFFFFFFFF)+k2)&0xFFFFFFFF ^ ((v0+s)&0xFFFFFFFF) ^ (((v0>>5)+k3)&0xFFFFFFFF)))) & 0xFFFFFFFF
    return v0, v1

async def tea_dec(v0, v1, k0, k1, k2, k3):
    s = (_DELTA * _ROUNDS) & 0xFFFFFFFF
    for _ in range(_ROUNDS):
        v1 = (v1 - (((((v0<<4)&0xFFFFFFFF)+k2)&0xFFFFFFFF ^ ((v0+s)&0xFFFFFFFF) ^ (((v0>>5)+k3)&0xFFFFFFFF)))) & 0xFFFFFFFF
        v0 = (v0 - (((((v1<<4)&0xFFFFFFFF)+k0)&0xFFFFFFFF ^ ((v1+s)&0xFFFFFFFF) ^ (((v1>>5)+k1)&0xFFFFFFFF)))) & 0xFFFFFFFF
        s = (s - _DELTA) & 0xFFFFFFFF
    return v0, v1

async def tea_cbc_encrypt(padded, key_bytes):
    k0,k1,k2,k3 = (struct.unpack_from("<I", key_bytes, o)[0] for o in (0,4,8,12))
    out = bytearray(len(padded)); pc = bytearray(8); pi = bytearray(8)
    for i in range(0, len(padded), 8):
        x = bytearray(8)
        for j in range(8): x[j] = padded[i+j] ^ pc[j]
        e0,e1 = await tea_enc(struct.unpack_from("<I", x, 0)[0],
                              struct.unpack_from("<I", x, 4)[0], k0,k1,k2,k3)
        enc = bytearray(8)
        struct.pack_into("<I", enc, 0, e0); struct.pack_into("<I", enc, 4, e1)
        for j in range(8): out[i+j] = enc[j] ^ pi[j]
        pc[:] = out[i:i+8]; pi[:] = x
    return bytes(out)

async def tea_cbc_decrypt(body, key_bytes):
    k0,k1,k2,k3 = (struct.unpack_from("<I", key_bytes, o)[0] for o in (0,4,8,12))
    out = bytearray(len(body)); pi = bytearray(8); pc = bytearray(8)
    x = bytearray(8); dec = bytearray(8)
    for i in range(0, len(body), 8):
        for j in range(8): x[j] = body[i+j] ^ pi[j]
        d0,d1 = await tea_dec(struct.unpack_from("<I", x, 0)[0],
                              struct.unpack_from("<I", x, 4)[0], k0,k1,k2,k3)
        struct.pack_into("<I", dec, 0, d0); struct.pack_into("<I", dec, 4, d1)
        for j in range(8): out[i+j] = dec[j] ^ pc[j]
        pc[:] = body[i:i+8]; pi[:] = dec
    return bytes(out)

async def build_padded(content):
    pad_len = (8 - (len(content) + 10) % 8) % 8
    return bytes([pad_len, 0, 0]) + b"\x00" * pad_len + content + b"\x00" * 7

async def encode_header(layout, so, cmd, oid, flags, length, k, v80):
    out = bytearray()
    for code in layout:
        val = {0:so, 1:cmd, 2:oid, 3:flags, 4:length}[code]
        if _FIELD_SIZES[code] == 1: out.append((val & 0xFF) ^ k)
        else:
            v = ((val & 0xFFFF) ^ v80) & 0xFFFF
            out.append(v & 0xFF); out.append((v >> 8) & 0xFF)
    return bytes(out)

async def crc7_buff(crc, buf):
    c = crc & 0x7F
    for b in buf: c = CRC7_TABLE[((2*(c & 0xFF)) ^ (b & 0xFF)) & 0xFF] & 0x7F
    return c & 0x7F

async def sv_frame(msg_key, layout, so, cmd, oid, flags, content, key, encrypted=True):
    k = key[0]; v80 = ((k << 8) | k) & 0xFFFF
    body = await tea_cbc_encrypt(await build_padded(content), key) if encrypted else content
    hdr = bytearray([msg_key, 0]) + await encode_header(layout, so, cmd, oid, flags, len(body), k, v80)
    pkt = bytearray(hdr + body)
    pkt[1] = await crc7_buff(0, bytes(pkt[2:])) & 0x7F
    return bytes(pkt)

async def build_packet(msg_key, layout, so, cmd, oid, flags, content, key, encrypted=True):
    k = key[0]; v80 = ((k << 8) | k) & 0xFFFF
    body = await tea_cbc_encrypt(await build_padded(content), key) if encrypted else content
    hdr = bytearray([msg_key, 0])
    for code in layout:
        val = {0:so, 1:cmd, 2:oid, 3:flags, 4:len(body)}[code]
        if _FIELD_SIZES[code] == 1: hdr.append((val & 0xFF) ^ k)
        else:
            v = ((val & 0xFFFF) ^ v80) & 0xFFFF
            hdr.append(v & 0xFF); hdr.append((v >> 8) & 0xFF)
    pkt = bytearray(hdr + body)
    pkt[1] = await crc7_buff(0, bytes(pkt[2:])) & 0x7F
    return bytes(pkt)

async def layouts_from_mask(mask):
    ru = [int(c) for c in str(mask).strip()]
    nr = [c for c in ru if c != 2]
    return ru, nr

async def build_hello_packet(text, key, layout):
    data = text.encode("utf-8")
    if len(data) > 25: raise ValueError("too long")
    content = b"\x10\x00\x00\x00" + data + b"\x00" * (29 - 4 - len(data))
    k = key[0] if key else 10
    v80 = ((k << 8) | k) & 0xFFFF
    layout = [int(c) for c in str(layout).strip()] if isinstance(layout, str) else list(layout)
    padded = await build_padded(content)
    enc_body = await tea_cbc_encrypt(padded, key)
    hdr = await encode_header(layout, 1, 1, 0, 1, len(enc_body), k, v80)
    pkt = bytearray([0x63, 0x00]) + hdr + enc_body
    pkt[1] = await crc7_buff(0, pkt[2:]) & 0x7F
    return bytes(pkt).hex()

async def classify(frame):
    cmd = frame["cmd"]
    name = MESSAGE_ID_TO_NAME.get(cmd, f"UNKNOWN_{cmd}")
    if name == "UDP_HELLO": return "HELLO"
    if name == "UDP_ACK": return "ACK"
    if name == "UDP_PING": return "PING"
    if name == "RUDP_JOIN_MATCH": return "JOIN_MATCH"
    if name.startswith("RUDP_"): return name
    if name.startswith("UDP_"): return name
    return "DATA"

async def reply_for(frame, key, mask, ack_key=0x68, ping_key=0x6D, hello_key=0x5B, ack_style="short"):
    _, nr = await layouts_from_mask(mask)
    typ = await classify(frame)
    if typ == "HELLO":
        if ack_style == "echo":
            content = frame["content"] if frame["content"] else b"\x10\x00\x00\x00"
            return typ, await build_packet(hello_key, nr, 1, 1, None, 1, content, key)
        return typ, await build_packet(ack_key, nr, 0, 2, None, 1, b"\x01\x00", key)
    if typ == "ACK":
        content = frame["content"] if frame["content"] else b"\x01\x00"
        return typ, await build_packet(ack_key, nr, 0, 2, None, 1, content, key)
    if typ == "PING":
        c = frame["content"]
        counter = c[:4] if len(c) >= 4 else c
        return typ, await build_packet(ping_key, nr, 0, 3, None, 0, counter + b"\x00\x00\x00", key, encrypted=False)
    if typ == "JOIN_MATCH":
        return typ, await build_packet(ack_key, nr, 0, 2, None, 1, b"\x02\x00", key)
    return typ, None

async def keepalive_ping(sock, ip, port, key_bytes, mask, stop_event):
    nr = (await layouts_from_mask(mask))[1]
    ping_keys = [0x66, 0x6D, 0x69, 0x6C, 0x6B, 0x6E, 0x6F, 0x70]
    loop = asyncio.get_event_loop(); i = 0
    while not stop_event.is_set():
        pk = ping_keys[i % len(ping_keys)]
        counter = int(time.time() * 1000) & 0xFFFFFFFF
        pkt = await build_packet(pk, nr, 0, 3, None, 0, struct.pack("<I", counter) + b"\x00\x00\x00",
                                 key_bytes, encrypted=False)
        try: await loop.sock_sendto(sock, pkt, (ip, port))
        except Exception: pass
        i += 1
        try: await asyncio.wait_for(stop_event.wait(), timeout=bypass_packet_jitter(3.0, 0.4))
        except asyncio.TimeoutError: pass

async def try_header(buf, layout, k, v80):
    off = 2; out = {}
    for code in layout:
        size = _FIELD_SIZES[code]
        if off + size > len(buf): return None
        out[_FIELD_NAMES[code]] = ((buf[off] ^ k) if size == 1
                                    else ((buf[off] | (buf[off+1] << 8)) ^ v80) & 0xFFFF)
        off += size
    out["headerLen"] = off
    return out

async def oicq_unpad(padded):
    if not padded or len(padded) < 8: return None
    if not all(padded[-1-i] == 0 for i in range(7)): return None
    pad_len = padded[0] & 0x07
    s = 3 + pad_len; e = len(padded) - 7
    return padded[s:e] if s < e else b""

async def decode_packet(packet, key, mask=None):
    data = bytes(packet) if isinstance(packet, bytes) else bytes.fromhex(packet)
    if len(data) < 8: return None
    k = key[0]; v80 = ((k << 8) | k) & 0xFFFF
    crc_ok = (data[1] & 0x7F) == await crc7_buff(0, data[2:])
    candidates = []
    if mask:
        ru, nr = await layouts_from_mask(mask)
        layouts = [("RUDP", ru), ("nonRUDP", nr)]
    else:
        layouts = [("RUDP", list(p)) for p in itertools.permutations([0,1,2,3,4])]
        layouts += [("nonRUDP", list(p)) for p in itertools.permutations([0,1,3,4])]
    for kind, layout in layouts:
        f = await try_header(data, layout, k, v80)
        if not f: continue
        if f["flags"] > 7 or f["sendOption"] > 7: continue
        if f["length"] != len(data) - f["headerLen"]: continue
        body = data[f["headerLen"]:f["headerLen"]+f["length"]]
        content = None
        if f["flags"] & 1:
            if len(body) < 8 or len(body) % 8 != 0: continue
            padded = await tea_cbc_decrypt(body, key)
            content = await oicq_unpad(padded)
            if content is None: continue
        else: content = body
        score = (1 if crc_ok else 0) + (1 if content is not None else 0)
        candidates.append({"kind":kind, "layout":layout, "headerLen":f["headerLen"],
            "msgKey":data[0], "cmd":f["cmd"], "flags":f["flags"],
            "sendOption":f["sendOption"], "orderId":f.get("orderId"),
            "length":f["length"], "content":content, "crcOk":crc_ok,
            "score":score, "total":len(data)})
    if not candidates: return None
    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates[0]

async def build_match_startup_packets(token, udp_key, match_code, account_id, block_val,
                                      server_ip="", region="BD", client_version="1.132.6",
                                      client_version_code="2019121229", access_token="",
                                      mode_id=BR_MODE_ID, map_id=BR_MAP_ID):
    token = token.strip()
    udp_key = bytes.fromhex(udp_key)
    match_code = [int(ch) for ch in str(match_code).strip()]
    thunder_jwt = token[:660] if len(token) > 660 else token
    sharma_jwt = token[660:] if len(token) > 660 else ""
    eth = thunder_jwt.encode() if isinstance(thunder_jwt, str) else thunder_jwt
    esh = sharma_jwt.encode() if isinstance(sharma_jwt, str) else sharma_jwt
    garena420 = await has_ssan_zig(len(eth)) + eth
    reg = str(region).upper() if region else "BD"
    csoversea_block = bytes.fromhex(
        "ca0163736f7665727365612e7374726f6e67686f6c642e66726565666972656d6f62696c652e636f6d"
        "3b302e302e302e303b33342e3132362e37362e34353b33342e38372e3137372e31343b33342e38372e"
        "3137302e3233303b33352e3138352e3138332e35370000000000000100000000000000000000000001"
        "00000800000100000000000100a8a2d7bebd8d8bdf110200")
    mid = bytes.fromhex('0000000001000102030101') + await has_ssan_zig(len(reg)) + reg.encode()
    mid += bytes.fromhex('0001030003000004')
    mid += await has_ssan_zig(len(client_version)) + client_version.encode()
    mid += await has_ssan_zig(len(client_version_code)) + client_version_code.encode()
    mid += csoversea_block
    clean_ip = server_ip.split(':')[0] if server_ip else "0.0.0.0"
    mid += await has_ssan_zig(len(clean_ip)) + clean_ip.encode()
    if access_token:
        clean_acc = access_token.strip()
        mid += await has_ssan_zig(len(clean_acc)) + clean_acc.encode()
    mid += await has_ssan_zig(len(esh)) + esh
    tg = (await uleb_encode(int(account_id)) + await uleb_encode(int(block_val)) +
          await uleb_encode(1) + await uleb_encode(int(mode_id)) +
          await uleb_encode(int(block_val)) + await uleb_encode(int(map_id)) + mid)
    process = await sv_frame(0x5E, match_code, 2, 447, 0, 1, garena420, udp_key)
    loading = await sv_frame(0x5A, match_code, 2, 448, 1, 1, tg, udp_key)
    return process.hex(), loading.hex()

# ═══════════════════════════ MOVEMENT 2001 ═══════════════════════════
async def build_movement_packet_2001(key_bytes, msg_key, player_state, x, y, z,
                                     tick, counter, move_state, account_uid,
                                     room_code, phase="arena"):
    if phase == "game":
        TAIL = (b"\x00"*7 + b"\x93\xca\xd5\xf9\x0b" + b"\x8e\xfe\xfc\xf7\x0b"
                + b"\xf4\xe0\xfe\xf7\x03" + b"\x00\x00")
    else:
        TAIL = (b"\x00"*7 + b"\xbd\xb6\xe1\xf3\x03" + b"\x00"
                + b"\xc4\xb6\xe1\xfb\x0b" + b"\x00\x00")
    body = bytearray()
    body += await uleb_encode(int(account_uid))
    body += await uleb_encode(int(player_state))
    body += await zigzag_encode_signed(int(x))
    body += await zigzag_encode_signed(int(y))
    body += await zigzag_encode_signed(int(z))
    body += b"\x00"
    body += await uleb_encode(int(move_state))
    body += TAIL
    body += await uleb_encode(int(tick))
    body += b"\x00\x00\x00"
    body += await uleb_encode(int(counter))
    body = bytes(body)
    k = key_bytes[0]; v80 = ((k << 8) | k) & 0xFFFF
    h = bytearray()
    h.append(msg_key & 0xFF); h.append(0x00); h.append(0x00 ^ k)
    h += ((2001 ^ v80) & 0xFFFF).to_bytes(2, "little")
    h += ((len(body) ^ v80) & 0xFFFF).to_bytes(2, "little")
    h.append(0x00 ^ k)
    h[1] = (await crc7_buff(0, bytes(h[2:]) + body)) & 0x7F
    return bytes(h) + body

class MovementTracker:
    PLAYER_STATE = {"idle":0, "walk":1, "run":2, "sprint":3, "jump":4, "crouch":5, "prone":6}
    def __init__(self, pattern="circle", radius=180):
        self.pattern = pattern; self.radius = int(radius)
        self.tick = 0; self.counter = 0
        self.angle = random.uniform(0, 6.2832)
        self.speed_multiplier = 1.0; self.dir_flip = 1
        self._next_speed_roll = time.time()
        self.state = "walk"; self.state_start = time.time()
        self.state_duration = random.uniform(2.0, 4.0)
        self._roll_new_speed()
    def _roll_new_speed(self):
        try:
            lo, hi = float(MOVEMENT_SPEED_MIN), float(MOVEMENT_SPEED_MAX)
            if hi < lo: lo, hi = hi, lo
            self.speed_multiplier = round(random.uniform(lo, hi), 2)
        except Exception: self.speed_multiplier = 1.0
        self._next_speed_roll = time.time() + MOVEMENT_UPDATE_SPEED_EVERY
    def _pick_next_state(self):
        r = random.random()
        ci = MOVEMENT_STATE_IDLE_CHANCE
        cw = ci + MOVEMENT_STATE_WALK_CHANCE
        cr = cw + MOVEMENT_STATE_RUN_CHANCE
        cs = cr + MOVEMENT_STATE_SPRINT_CHANCE
        cj = cs + MOVEMENT_STATE_JUMP_CHANCE
        cc = cj + MOVEMENT_STATE_CROUCH_CHANCE
        if r < ci: return "idle", random.uniform(0.6, 1.6)
        elif r < cw: return "walk", random.uniform(1.6, 3.0)
        elif r < cr: return "run", random.uniform(2.0, 4.0)
        elif r < cs: return "sprint", random.uniform(1.2, 2.5)
        elif r < cj: return "jump", random.uniform(0.35, 0.65)
        elif r < cc: return "crouch", random.uniform(1.2, 2.5)
        else: return "prone", random.uniform(1.5, 3.5)
    def _generate_movement(self):
        p = (self.pattern or "circle").lower()
        x = y = z = 0; ms = 0
        if p == "circle":
            self.angle += 0.35 * self.dir_flip
            if self.angle > 6.2832: self.angle -= 6.2832
            elif self.angle < 0: self.angle += 6.2832
            x = int(self.radius * random.uniform(0.9, 1.1) * (1.0 if self.angle % 3.14 < 1.57 else -1.0))
            y = int(self.radius * random.uniform(0.4, 0.6))
            z = int(self.radius * random.uniform(0.9, 1.1) * (1.0 if self.angle % 6.28 < 3.14 else -1.0))
            ms = 0x0F
        else:
            x = random.randint(-self.radius, self.radius)
            y = random.randint(-40, 40)
            z = random.randint(-self.radius, self.radius)
            ms = random.choice([0x01, 0x02, 0x04, 0x08, 0x0F])
        return x, y, z, ms
    def next(self):
        now = time.time()
        if now >= self._next_speed_roll: self._roll_new_speed()
        if now - self.state_start > self.state_duration:
            self.state, self.state_duration = self._pick_next_state()
            self.state_start = now
        self.tick = (self.tick + 1) & 0xFFFFFFFF
        self.counter = (self.counter + 1) & 0xFFFFFFFF
        ps = self.PLAYER_STATE.get(self.state, 1)
        if self.state in ("idle", "crouch", "prone"): x = y = z = 0; move_state = 0
        else: x, y, z, move_state = self._generate_movement()
        return ps, x, y, z, move_state, self.tick, self.counter, self.speed_multiplier, self.state

async def movement_worker(sock, ip, port, udp_key_bytes, match_code, account_id, stop_event, match_index):
    loop = asyncio.get_event_loop(); addr = (ip, port)
    tracker = MovementTracker(pattern=MOVEMENT_PATTERN, radius=MOVEMENT_RADIUS)
    sent = 0
    try:
        await asyncio.sleep(bypass_jitter(3.0, 0.5))
        while not stop_event.is_set():
            try:
                ps, x, y, z, ms, tick, cnt, sm, st = tracker.next()
                pkt = await build_movement_packet_2001(udp_key_bytes, 0x6B, ps, x, y, z, tick, cnt, ms,
                                                       account_id, match_code, phase="arena")
                await loop.sock_sendto(sock, pkt, addr); sent += 1
                base = MOVEMENT_TICK_MS / 1000.0
                try: smx = max(0.7, min(float(sm), 1.6))
                except Exception: smx = 1.0
                wait = max(0.10, min(base / smx, 0.40))
                wait = bypass_packet_jitter(wait, 0.20)
                try: await asyncio.wait_for(stop_event.wait(), timeout=wait); break
                except asyncio.TimeoutError: pass
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.5)
    except asyncio.CancelledError: pass

async def send_anti_afk_fire(sock, addr, udp_key_bytes, match_code, account_id):
    try:
        _, nr = await layouts_from_mask(match_code)
        try: pid = int(account_id)
        except Exception: pid = 0
        ts = int(time.time() * 1000) & 0xFFFFFFFF
        wid = random.choice([101, 102, 103, 201, 202])
        fire = struct.pack("<IIHB", pid & 0xFFFFFFFF, ts, wid, 1)
        fp = await build_packet(0x68, nr, 0, 104, None, 0, fire, udp_key_bytes, encrypted=False)
        loop = asyncio.get_event_loop()
        await loop.sock_sendto(sock, fp, addr)
        await asyncio.sleep(bypass_jitter(random.uniform(0.15, 0.30), 0.05))
        stop = struct.pack("<IIHB", pid & 0xFFFFFFFF, ts + 200, wid, 0)
        sp = await build_packet(0x68, nr, 0, 105, None, 0, stop, udp_key_bytes, encrypted=False)
        await loop.sock_sendto(sock, sp, addr)
        return True
    except Exception: return False

async def anti_afk_worker(sock, ip, port, udp_key_bytes, match_code, account_id, stop_event, match_index):
    addr = (ip, port); fires = 0
    try:
        await asyncio.sleep(bypass_jitter(2.5, 0.5))
        while not stop_event.is_set():
            try:
                if await send_anti_afk_fire(sock, addr, udp_key_bytes, match_code, account_id): fires += 1
                w = random.uniform(ANTI_AFK_MIN_INTERVAL, ANTI_AFK_MAX_INTERVAL)
                w = bypass_packet_jitter(w, 0.25)
                try: await asyncio.wait_for(stop_event.wait(), timeout=w); break
                except asyncio.TimeoutError: pass
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(1.0)
    except asyncio.CancelledError: pass

# ═══════════════════════════ PLAY GAME ═══════════════════════════
async def play_game(server_ip_port, thunder, sharma, udp_key, match_code,
                    account_id, player_region, client_version, key, iv,
                    match_index, on_match_complete=None):
    t0 = time.time()
    ping_task = anti_task = move_task = None
    sock = None
    ping_stop = asyncio.Event(); anti_stop = asyncio.Event(); move_stop = asyncio.Event()
    uid_str = str(account_id); completed = False
    try:
        ip, port = server_ip_port.split(":"); port = int(port)
        rip = await resolve_host_cloudflare(ip)
        loop = asyncio.get_event_loop()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try: sock.bind(('0.0.0.0', 0))
        except Exception: pass
        optimize_udp_socket(sock); sock.setblocking(False)
        udp_key_bytes = bytes.fromhex(udp_key)
        await asyncio.sleep(bypass_hello_delay())
        hello = await build_hello_packet(f"{account_id}_2585", udp_key_bytes, match_code)
        await loop.sock_sendto(sock, bytes.fromhex(hello), (rip, port))
        ack_state = "waiting_for_hello_reply"
        thunder_sent = False; join_match_rcv = False; local_closed = False
        send_lock = asyncio.Lock(); anti_started = False
        ping_task = asyncio.create_task(keepalive_ping(sock, rip, port, udp_key_bytes, match_code, ping_stop))
        last_activity = time.time()
        socket_error_streak = 0
        packet_error_streak = 0

        async def start_workers():
            nonlocal anti_task, move_task, anti_started
            if anti_started: return
            anti_started = True
            anti_task = asyncio.create_task(anti_afk_worker(sock, rip, port, udp_key_bytes, match_code,
                                                            account_id, anti_stop, match_index))
            if ENABLE_SPEED_MOVEMENT:
                move_task = asyncio.create_task(movement_worker(sock, rip, port, udp_key_bytes, match_code,
                                                                account_id, move_stop, match_index))

        async def send_startup():
            nonlocal ack_state, thunder_sent
            if thunder_sent: return
            async with send_lock:
                if thunder_sent: return
                try:
                    await loop.sock_sendto(sock, bytes.fromhex(thunder), (rip, port))
                    thunder_sent = True
                    await asyncio.sleep(bypass_jitter(0.1, 0.05))
                    _, nr = await layouts_from_mask(match_code)
                    ack = await build_packet(0x68, nr, 0, 2, None, 1, b"\x01\x00", udp_key_bytes)
                    await loop.sock_sendto(sock, ack, (rip, port))
                    await asyncio.sleep(bypass_jitter(0.2, 0.05))
                    await loop.sock_sendto(sock, bytes.fromhex(sharma), (rip, port))
                    ack_state = "thunder_sharma_sent"
                    await start_workers()
                except Exception as e: print_error(f"[MATCH #{match_index}] startup: {e}", uid_str)

        while not local_closed:
            if time.time() - t0 > MAX_MATCH_DURATION: break
            try:
                resp, saddr = await asyncio.wait_for(loop.sock_recvfrom(sock, 65535), timeout=1.5)
                if resp:
                    frame = await decode_packet(resp, udp_key_bytes, match_code)
                    if frame:
                        socket_error_streak = 0
                        packet_error_streak = 0
                        last_activity = time.time()
                        pt = await classify(frame)
                        if frame['cmd'] in [103, 107]:
                            completed = True; local_closed = True; continue
                        if frame['cmd'] == 101:
                            try:
                                _, nr = await layouts_from_mask(match_code)
                                a = await build_packet(0x68, nr, 0, 2, None, 1, b"\x01\x00", udp_key_bytes)
                                await loop.sock_sendto(sock, a, saddr)
                            except Exception: pass
                            continue
                        if pt in ["ACK", "PING", "HELLO", "JOIN_MATCH"]:
                            if pt == "HELLO" and ack_state == "waiting_for_hello_reply":
                                _, r = await reply_for(frame, udp_key_bytes, match_code, ack_style="short")
                                if r: await loop.sock_sendto(sock, r, saddr)
                                ack_state = "ack_sent_waiting"
                            elif pt == "ACK":
                                if ack_state == "waiting_for_hello_reply":
                                    _, r = await reply_for(frame, udp_key_bytes, match_code)
                                    if r: await loop.sock_sendto(sock, r, saddr)
                                    ack_state = "ready_to_send_thunder"
                                elif ack_state == "ack_sent_waiting":
                                    ack_state = "ready_to_send_thunder"
                                else:
                                    _, r = await reply_for(frame, udp_key_bytes, match_code)
                                    if r: await loop.sock_sendto(sock, r, saddr)
                            elif pt == "PING":
                                _, r = await reply_for(frame, udp_key_bytes, match_code)
                                if r: await loop.sock_sendto(sock, r, saddr)
                            elif pt == "JOIN_MATCH" and not join_match_rcv:
                                _, r = await reply_for(frame, udp_key_bytes, match_code)
                                if r: await loop.sock_sendto(sock, r, saddr); join_match_rcv = True
            except asyncio.TimeoutError:
                if ack_state == "ready_to_send_thunder" and not thunder_sent:
                    await send_startup()
                elif ack_state == "waiting_for_hello_reply":
                    if (time.time() - last_activity) > 7.0:
                        try:
                            hp = await build_hello_packet(f"{account_id}_2585", udp_key_bytes, match_code)
                            await loop.sock_sendto(sock, bytes.fromhex(hp), (rip, port))
                        except Exception: pass
                        last_activity = time.time()
                    if (time.time() - t0) > 25.0:
                        break
                elif ack_state == "thunder_sharma_sent":
                    if (time.time() - last_activity) > MATCH_IDLE_TIMEOUT:
                        completed = True; break
                continue
            except BlockingIOError:
                await asyncio.sleep(0.05)
            except OSError as e:
                socket_error_streak += 1
                if socket_error_streak >= 8:
                    print_error(f"[MATCH #{match_index}] UDP socket repeatedly failed; reconnecting", uid_str)
                    break
                await asyncio.sleep(0.5)
                continue
            except Exception as e:
                packet_error_streak += 1
                if packet_error_streak >= 20:
                    print_error(f"[MATCH #{match_index}] repeated packet errors; reconnecting", uid_str)
                    break
                await asyncio.sleep(0.5)
                continue
            if ack_state == "ready_to_send_thunder" and not thunder_sent:
                try: await send_startup()
                except Exception: pass
        return f"match #{match_index} finished"
    except Exception as e:
        print_error(f"[MATCH #{match_index}] {e}", uid_str); return f"match #{match_index} error"
    finally:
        if completed:
            try: bot_state.increment_match(uid_str)
            except Exception: pass
            if on_match_complete:
                try: asyncio.create_task(on_match_complete())
                except Exception: pass
        anti_stop.set()
        move_stop.set()
        for t in (anti_task, move_task):
            if t:
                try:
                    await asyncio.wait_for(t, timeout=2.0)
                except Exception:
                    t.cancel()
                    try:
                        await t
                    except Exception:
                        pass
        ping_stop.set()
        if ping_task:
            ping_task.cancel()
            try:
                await ping_task
            except asyncio.CancelledError:
                pass
        if sock:
            try: sock.close()
            except Exception: pass
        rem = await _dec_match(uid_str)
        try: bot_state.update_status(uid_str, "IN_MATCH" if rem > 0 else "ONLINE", rem)
        except Exception: pass

# ═══════════════════════════ FRIEND / TEAM HANDLERS ═══════════════════════════
async def _process_social_packet(raw_bytes, account_data, tag="MAIN"):
    try:
        hex_data = raw_bytes.hex()
        candidates = []
        if len(raw_bytes) >= 6:
            plen = raw_bytes[4]
            if 0 < plen <= (len(raw_bytes) - 5):
                try:
                    inner = bytes(raw_bytes[5:5 + plen])
                    d0 = decode_protobuf_dict_safe(inner) or _wrap_manual(inner)
                    if d0: candidates.append((5, d0))
                except Exception: pass
        for off in [5, 6, 10, 8, 12, 4, 0]:
            if off >= len(hex_data): continue
            try: inner = bytes.fromhex(hex_data[off:])
            except Exception: continue
            decoded = decode_protobuf_dict_safe(inner) or _wrap_manual(inner)
            if decoded: candidates.append((off, decoded))
        if not candidates: return
        candidates.sort(key=lambda x: len(x[1]) if isinstance(x[1], dict) else 0, reverse=True)
        _, decoded = candidates[0]
        def _v(c, k):
            if not isinstance(c, dict): return None
            v = c.get(k) if k in c else c.get(str(k))
            if isinstance(v, dict) and "data" in v: return v["data"]
            return v
        f5w = decoded.get("5") or decoded.get(5) if isinstance(decoded, dict) else None
        f5 = f5w["data"] if isinstance(f5w, dict) and "data" in f5w else f5w
        target = None
        if isinstance(f5, dict):
            for fk in [1, 2, 3, 4, 6]:
                c = _v(f5, fk)
                if c and str(c).isdigit() and 6 <= len(str(c)) <= 15:
                    target = str(c); break
        if not target: return
        own = str(account_data.get('account_id', '')) if account_data else ''
        if own and target == own: return
        if not _accept_friend_request or not account_data: return
        jwt = account_data.get('token'); srv = account_data.get('server_url')
        rel = account_data.get('release_version'); own_id = account_data.get('account_id')
        if not (jwt and srv and rel and own_id): return
        url = f"{srv.rstrip('/')}/ConfirmFriendRequest"
        fields = {"1": int(target), "2": int(own_id)}
        try:
            payload = bytes.fromhex(encrypt_api(create_proto(fields).hex()))
            hdrs = {
                "authorization": f"Bearer {jwt}",
                "host": srv.replace("https://", "").replace("http://", "").split("/")[0],
                "x-ga": "v1 1", "content-type": "application/x-www-form-urlencoded",
                "accept-encoding": "deflate, gzip", "releaseversion": f"{rel}",
                "user-agent": "UnityPlayer/2022.3.47f1", "accept": "*/*",
                "x-unity-version": "2022.3.47f1",
            }
            async with httpx.AsyncClient(verify=False, timeout=8.0) as s:
                r = await s.post(url, headers=hdrs, content=payload)
                if r.status_code == 200 and len(r.content) > 0:
                    print_success(f"👥 [FRIEND-{tag}] ✅ {target}", str(own_id))
        except Exception: pass
    except Exception: pass

def _wrap_manual(inner):
    try:
        alt = _decode_proto_manual(inner)
        if alt and len(alt) > 0:
            return {str(k): {"data": v} for k, v in alt.items()}
    except Exception: pass
    return None

async def _handle_team_invite(hex_data, pl, uid_str, current_account_data,
                              current_key, current_iv, writer, runtime=None):
    try:
        candidates = []
        for off in [10, 8, 6, 12, 14, 4, 16, 0, 20, 2]:
            if off >= len(hex_data) or len(hex_data) - off < 4: continue
            try: inner = bytes.fromhex(hex_data[off:])
            except Exception: continue
            dec = decode_protobuf_dict_safe(inner)
            if dec and isinstance(dec, dict) and len(dec) > 0:
                candidates.append((off, "parser", dec)); continue
            alt = _decode_proto_manual(inner)
            if alt and len(alt) > 0:
                candidates.append((off, "manual", {str(k): {"data": v} for k, v in alt.items()}))
        if not candidates: return False
        candidates.sort(key=lambda x: len(x[2]) if isinstance(x[2], dict) else 0, reverse=True)
        _, _, dec = candidates[0]

        def _unwrap(d, keys):
            if not isinstance(d, dict): return None
            for k in keys:
                v = d.get(k) if k in d else d.get(str(k))
                if isinstance(v, dict) and "data" in v: return v["data"]
                if isinstance(v, dict): return v
            return None

        target_dict = None
        for kp in [["5"], ["4"], ["6"], ["2"], ["1"]]:
            u = _unwrap(dec, kp)
            if isinstance(u, dict) and len(u) >= 3:
                target_dict = u; break
        if target_dict is None: target_dict = dec

        def _g(d, k):
            if not isinstance(d, dict): return None
            v = d.get(k) if k in d else d.get(str(k))
            if isinstance(v, dict) and "data" in v: return v["data"]
            if isinstance(v, dict):
                for kk in ["1","2","3","4","5","6","7","8"]:
                    vv = v.get(kk) if kk in v else v.get(int(kk))
                    if isinstance(vv, dict) and "data" in vv: return vv["data"]
            return v

        group_id = None
        for k in list(target_dict.keys()):
            c = _g(target_dict, k)
            if isinstance(c, str) and 20 <= len(c) <= 40:
                group_id = c; break
        if not group_id:
            for k in list(dec.keys()):
                c = _g(dec, k)
                if isinstance(c, str) and 20 <= len(c) <= 40:
                    group_id = c; break

        own_acc = str(current_account_data.get('account_id')) if current_account_data else None
        inviter = None
        all_f = list(target_dict.keys()) + list(dec.keys())
        for k in all_f:
            c = _g(target_dict, k) or _g(dec, k)
            if c and str(c).isdigit() and 6 <= len(str(c)) <= 15:
                if str(c) != uid_str and str(c) != own_acc:
                    inviter = str(c); break

        if inviter and group_id and runtime:
            is_member = (runtime.leader_uid != uid_str)
            if is_member:
                async with runtime.members_lock:
                    already = uid_str in runtime.members_joined
                if already: return True
                accepted = False
                for attempt in range(3):
                    try:
                        acc = accept_team_invite(int(inviter), group_id, current_key, current_iv)
                        if writer and not writer.is_closing():
                            writer.write(acc); await writer.drain()
                            accepted = True; break
                    except Exception: pass
                    await asyncio.sleep(0.8)
                if accepted:
                    await runtime.member_join(uid_str)
                return True
        return False
    except Exception:
        return False

# ═══════════════════════════ FUNCTIONAL (per-squad main loop) ═══════════════════════════
async def functional_battle_royale(runtime: SquadRuntime, addrs, starter_packet, account_region,
                                    client_version, key, iv, account_id="", account_data=None,
                                    account_level=2, max_reconnects=10):
    sid = runtime.squad_id
    reconnects = 0
    ip, port = addrs.split(":")
    play_matches: List[asyncio.Task] = []
    no_response_count = 0
    search_attempts = 0
    uid_str = str(account_id)
    current_level = int(account_level or 2)
    current_token = starter_packet
    current_key = key; current_iv = iv
    current_account_data = account_data
    reconnect_count_total = 0
    region_index = 0
    current_search_region = REGION_ROTATION_LIST[0]
    _writer_ref = {"w": None}
    _team_active = {"flag": True}

    async def trigger_post_match_refresh():
        await asyncio.sleep(EXP_REFRESH_AFTER_MATCH_DELAY)
        try:
            f = bot_state.account_credentials.get(uid_str)
            if f: await refresh_account_profile(f)
        except Exception: pass

    async def _team_coordinator():
        try:
            deadline = time.time() + TEAM_PEER_WAIT_TIMEOUT
            while time.time() < deadline:
                async with runtime.lock:
                    n = len(runtime.peers)
                if n >= TEAM_SIZE: break
                if not runtime.is_running: return
                await asyncio.sleep(0.5)

            async with runtime.lock:
                n = len(runtime.peers)
                is_leader = (runtime.leader_uid == uid_str)
                peers_snapshot = dict(runtime.peers)

            if not is_leader: return
            if n < TEAM_SIZE:
                bot_state.squad_log(sid, f"Only {n}/{TEAM_SIZE} peers — waiting", "warning")

            await asyncio.sleep(TEAM_READY_DELAY)
            async with runtime.lock:
                runtime.team_code = None
                runtime.pk_code = None

            own_id_num = None
            if current_account_data: own_id_num = current_account_data.get('account_id')
            if not own_id_num:
                try: own_id_num = int(uid_str)
                except Exception: own_id_num = 0

            try:
                pkt = create_team(current_key, current_iv, client_version)
                if _writer_ref["w"] and not _writer_ref["w"].is_closing():
                    _writer_ref["w"].write(pkt); await _writer_ref["w"].drain()
                    await runtime.reset_members(keep_leader=False)
                    await runtime.member_join(uid_str)
            except Exception: pass

            await asyncio.sleep(TEAM_CREATE_WAIT)

            peer_uids = []
            for peer_uid, info in peers_snapshot.items():
                if peer_uid == uid_str: continue
                pa = None
                try: pa = info["data"].get("account_id")
                except Exception: pass
                if not pa: pa = peer_uid
                peer_uids.append(int(pa))

            heartbeat_stop = asyncio.Event()
            async def heartbeat_loop():
                while not heartbeat_stop.is_set():
                    try:
                        if _writer_ref["w"] and not _writer_ref["w"].is_closing():
                            pkt = team_fresh(int(own_id_num), current_key, current_iv)
                            _writer_ref["w"].write(pkt); await _writer_ref["w"].drain()
                    except Exception: pass
                    try: await asyncio.wait_for(heartbeat_stop.wait(), timeout=TEAM_HEARTBEAT_INTERVAL)
                    except asyncio.TimeoutError: pass
            hb_task = asyncio.create_task(heartbeat_loop())

            invite_start = time.time(); cycle = 0
            while time.time() - invite_start < TEAM_INVITE_MAX_TIME:
                if not _team_active["flag"]: break
                if not runtime.is_running: break
                cnt = await runtime.member_count()
                if cnt >= TEAM_SIZE: break
                cycle += 1
                for tuid in peer_uids:
                    async with runtime.members_lock:
                        joined = str(tuid) in runtime.members_joined
                    if joined: continue
                    try:
                        inv = invite_player_in_team(tuid, current_key, current_iv, region=account_region)
                        if _writer_ref["w"] and not _writer_ref["w"].is_closing():
                            _writer_ref["w"].write(inv); await _writer_ref["w"].drain()
                    except Exception: pass
                    await asyncio.sleep(0.4)
                try: await asyncio.wait_for(heartbeat_stop.wait(), timeout=TEAM_INVITE_CYCLE_WAIT)
                except asyncio.TimeoutError: pass

            final_cnt = await runtime.member_count()
            if final_cnt < TEAM_SIZE:
                bot_state.squad_log(sid, f"Team only {final_cnt}/{TEAM_SIZE} — retry", "warning")
                heartbeat_stop.set()
                try: hb_task.cancel(); await hb_task
                except Exception: pass
                return

            bot_state.squad_log(sid, f"✅ Team full {final_cnt}/{TEAM_SIZE} — starting match loop", "success")
            await asyncio.sleep(TEAM_FINAL_WAIT)
            heartbeat_stop.set()
            try: hb_task.cancel(); await hb_task
            except Exception: pass

            while _team_active["flag"] and runtime.is_running:
                try:
                    async with runtime.lock:
                        if runtime.leader_uid != uid_str: break
                    oid = current_account_data.get('account_id', own_id_num) if current_account_data else own_id_num
                    try:
                        rdy = ready_for_game(int(oid), current_key, current_iv)
                        if _writer_ref["w"] and not _writer_ref["w"].is_closing():
                            _writer_ref["w"].write(rdy); await _writer_ref["w"].drain()
                    except Exception: pass
                    await asyncio.sleep(1.0)
                    sm = start_match_team(int(oid), current_key, current_iv, region=account_region)
                    if _writer_ref["w"] and not _writer_ref["w"].is_closing():
                        _writer_ref["w"].write(sm); await _writer_ref["w"].drain()
                except Exception: pass
                try: await asyncio.wait_for(asyncio.sleep(5.0), timeout=5.5)
                except asyncio.TimeoutError: pass
        except asyncio.CancelledError: raise
        except Exception as e:
            bot_state.squad_log(sid, f"Coordinator error: {e}", "error")

    async def _member_match_trigger():
        try:
            await asyncio.sleep(TEAM_READY_DELAY + TEAM_MEMBER_START_DELAY)
            async with runtime.lock:
                if runtime.leader_uid == uid_str: return
            my_id = current_account_data.get('account_id', uid_str) if current_account_data else uid_str
            while _team_active["flag"] and runtime.is_running:
                try:
                    if _writer_ref["w"] and not _writer_ref["w"].is_closing():
                        try:
                            rdy = ready_for_game(int(my_id), current_key, current_iv)
                            _writer_ref["w"].write(rdy); await _writer_ref["w"].drain()
                        except Exception: pass
                        await asyncio.sleep(1.0)
                        sm = start_match_team(int(my_id), current_key, current_iv, region=account_region)
                        _writer_ref["w"].write(sm); await _writer_ref["w"].drain()
                except Exception: pass
                try: await asyncio.wait_for(asyncio.sleep(5.0), timeout=5.5)
                except asyncio.TimeoutError: pass
        except asyncio.CancelledError: raise
        except Exception: pass

    try:
        while runtime.is_running:
            writer = None; gateway_ping_task = None
            team_coord_task = None; member_trigger_task = None
            try:
                if current_account_data:
                    fresh = None
                    if current_account_data.get('auth_type') == 'guest' and current_account_data.get('auth_uid'):
                        fresh = cache_get(str(current_account_data['auth_uid']))
                    elif current_account_data.get('auth_type') == 'token' and current_account_data.get('auth_token'):
                        fresh = cache_get(f"tok_{current_account_data['auth_token'][:20]}")
                    if fresh:
                        current_account_data = fresh
                        current_key = fresh['aes_ak']; current_iv = fresh['iv_i']
                        current_token = await build_tcp_startup_packet(
                            fresh['account_id'], fresh['token'], fresh['server_time'],
                            current_key, current_iv,
                            region=fresh.get('region', account_region), typ='OnLine')
                        try:
                            lv = int(fresh.get('level', current_level) or current_level)
                            if lv != current_level: current_level = lv
                        except Exception: pass
                    else:
                        try:
                            if current_account_data.get('auth_uid'):
                                cache_invalidate(str(current_account_data['auth_uid']))
                            if current_account_data.get('auth_token'):
                                cache_invalidate(f"tok_{current_account_data['auth_token'][:20]}")
                            new_cred = await relogin_account(uid_str, current_account_data)
                            if new_cred:
                                current_account_data = new_cred
                                current_key = new_cred['aes_ak']; current_iv = new_cred['iv_i']
                                current_token = await build_tcp_startup_packet(
                                    new_cred['account_id'], new_cred['token'], new_cred['server_time'],
                                    current_key, current_iv,
                                    region=new_cred.get('region', account_region), typ='OnLine')
                            else:
                                raise ConnectionError("Re-login returned empty credentials")
                        except Exception:
                            await asyncio.sleep(5)
                            raise ConnectionError("Cache expired")

                try:
                    if uid_str in bot_state.accounts:
                        ll = int(bot_state.accounts[uid_str].get('level', current_level) or current_level)
                        if ll != current_level: current_level = ll
                except Exception: pass

                rip = await resolve_host_cloudflare(ip)
                reader, writer = await asyncio.open_connection(rip, int(port))
                _writer_ref["w"] = writer
                raw_sock = writer.get_extra_info('socket')
                if raw_sock: optimize_tcp_socket(raw_sock)
                await asyncio.sleep(bypass_hello_delay())
                writer.write(bytes.fromhex(current_token)); await writer.drain()
                try:
                    ka = await send_keep_alive(account_region)
                    if ka and not writer.is_closing():
                        writer.write(ka); await asyncio.wait_for(writer.drain(), timeout=3)
                except Exception: pass

                async def func_gateway_keepalive():
                    ka_bytes = await send_keep_alive(account_region)
                    while True:
                        await asyncio.sleep(bypass_ka_jitter(5.0))
                        try:
                            if writer and not writer.is_closing():
                                writer.write(ka_bytes); await writer.drain()
                        except Exception: break
                gateway_ping_task = asyncio.create_task(func_gateway_keepalive())

                connection_start_time = asyncio.get_running_loop().time()
                last_watchdog_check = connection_start_time
                search_attempts = 0
                if reconnect_count_total > 0 and (reconnect_count_total % REGION_ROTATE_EVERY_N == 0):
                    region_index = (region_index + 1) % len(REGION_ROTATION_LIST)
                    current_search_region = REGION_ROTATION_LIST[region_index]
                else:
                    current_search_region = REGION_ROTATION_LIST[region_index]

                bot_state.squad_log(sid, f"🔗 TCP connected {uid_str} Lvl{current_level} R:{current_search_region}", "info")
                reconnects = 0; no_response_count = 0

                async with runtime.lock:
                    runtime.peers[uid_str] = {
                        "writer": writer, "data": current_account_data,
                        "key": current_key, "iv": current_iv}
                    if runtime.leader_uid is None:
                        runtime.leader_uid = uid_str
                        bot_state.squad_log(sid, f"👑 Leader: {uid_str}", "success")

                if TEAM_MODE:
                    team_coord_task = asyncio.create_task(_team_coordinator())
                    member_trigger_task = asyncio.create_task(_member_match_trigger())
                else:
                    await start_game_battle_royale(current_search_region, client_version, writer, current_key, current_iv)

                while runtime.is_running:
                    play_matches[:] = [m for m in play_matches if not m.done()]
                    active = await _get_match_count(uid_str)
                    try: bot_state.update_status(uid_str, "ONLINE" if active == 0 else "IN_MATCH", active)
                    except Exception: pass

                    now = asyncio.get_running_loop().time()
                    if now - last_watchdog_check >= MATCH_WATCHDOG_CHECK:
                        last_watchdog_check = now
                        sd = now - connection_start_time
                        if sd > MATCH_SEARCH_TIMEOUT:
                            raise ConnectionError("Search watchdog")
                    if search_attempts >= MAX_SEARCH_ATTEMPTS:
                        raise ConnectionError("Max attempts")

                    try:
                        data = await asyncio.wait_for(reader.read(8192), timeout=0.5)
                    except asyncio.TimeoutError:
                        no_response_count += 1
                        if TEAM_MODE:
                            if no_response_count > TEAM_IDLE_ITERS_TEAM:
                                raise ConnectionError("Team idle timeout")
                        else:
                            if no_response_count > 80: raise ConnectionError("idle")
                        continue

                    if not data: raise ConnectionError("closed")
                    hex_data = data.hex()
                    pl = len(data)
                    no_response_count = 0

                    if hex_data.startswith("0600") and pl > 20:
                        await _process_social_packet(data, current_account_data, tag="MAIN")
                        continue

                    if hex_data.startswith("05") and pl > 10:
                        await _handle_team_invite(hex_data, pl, uid_str, current_account_data,
                                                  current_key, current_iv, writer, runtime)
                        continue

                    if hex_data.startswith("0300") and 10 < pl < 30:
                        continue

                    if hex_data.startswith("0300") and pl >= 300:
                        for tk in (team_coord_task, member_trigger_task):
                            if tk and not tk.done():
                                tk.cancel()
                                try: await tk
                                except asyncio.CancelledError: pass
                        team_coord_task = None; member_trigger_task = None
                        _team_active["flag"] = False

                        try:
                            res = json.loads(await decode_protobuf(hex_data[10:]))
                            token = udp_key = match_code = server_ip_port = None
                            match_account_id = block_val = None
                            if '42' in res and 'data' in res['42']:
                                match_code = res['42']['data']
                            if '5' in res and 'data' in res['5']:
                                r5 = res['5']['data']
                                server_ip_port = r5.get('2', {}).get('data')
                                udp_key = r5.get('3', {}).get('data')
                                token = r5.get('4', {}).get('data')
                                if '42' in r5: match_code = r5['42']['data']
                            if '1' in res and 'data' in res['1']:
                                match_account_id = res['1']['data']
                            if '5' in res and 'data' in res['5']:
                                block_val = res['5']['data'].get('1', {}).get('data')

                            effective = match_account_id or account_id or "BD_BOT"
                            if token and udp_key and match_code and server_ip_port:
                                try:
                                    async with runtime.lock:
                                        runtime.pk_code = str(match_code)
                                        runtime.team_code = str(match_code)
                                except Exception: pass
                                bot_state.squad_log(sid, f"🎯 Match found | Room: {match_code} | Server: {server_ip_port}", "success")

                                acc_tok = current_account_data.get('access_token', '') if current_account_data else ""
                                thunder, sharma = await build_match_startup_packets(
                                    token, udp_key, match_code, effective, block_val or 0,
                                    server_ip=server_ip_port, region=account_region,
                                    client_version=client_version, access_token=acc_tok,
                                    mode_id=BR_MODE_ID, map_id=BR_MAP_ID)
                                match_index = await _inc_match(uid_str)
                                runtime.match_count += 1
                                bot_state.squad_log(sid, f"🎮 Match #{match_index} starting UDP...", "info")

                                new_match = asyncio.create_task(play_game(
                                    server_ip_port, thunder, sharma, udp_key, match_code,
                                    effective, current_search_region, client_version,
                                    current_key, current_iv,
                                    match_index=match_index, on_match_complete=trigger_post_match_refresh))
                                play_matches.append(new_match)

                                async def drain_gw():
                                    while not new_match.done():
                                        try:
                                            dg = await asyncio.wait_for(reader.read(4096), timeout=1.0)
                                            if not dg: break
                                            gh = dg.hex()
                                            if gh.startswith("0600") and len(dg) > 20:
                                                await _process_social_packet(dg, current_account_data, tag="DRAIN")
                                        except asyncio.TimeoutError: continue
                                        except Exception: break
                                drain_task = asyncio.create_task(drain_gw())
                                try: await new_match
                                except Exception as e: bot_state.squad_log(sid, f"Match error: {e}", "error")
                                finally:
                                    drain_task.cancel()
                                    try: await drain_task
                                    except asyncio.CancelledError: pass
                                play_matches[:] = [m for m in play_matches if not m.done()]

                                async with runtime.lock:
                                    runtime.peers.pop(uid_str, None)
                                    if runtime.leader_uid == uid_str:
                                        runtime.leader_uid = None
                                    runtime.pk_code = None
                                await runtime.member_leave(uid_str)
                                _team_active["flag"] = True
                                try: writer.close(); await asyncio.wait_for(writer.wait_closed(), 2.0)
                                except Exception: pass
                                bot_state.squad_log(sid, f"🔁 {uid_str} restarting for new match...", "info")
                                await asyncio.sleep(NEW_MATCH_DELAY)
                                reconnect_count_total += 1
                                # Exit this TCP session cleanly; the outer loop opens a fresh
                                # session and sends the matchmaking request again.
                                break
                            else:
                                try: writer.close(); await asyncio.wait_for(writer.wait_closed(), 2.0)
                                except Exception: pass
                                await asyncio.sleep(NON_MATCH_RECONNECT_DELAY)
                                break
                        except Exception as e:
                            bot_state.squad_log(sid, f"Parse error: {e}", "error")
                            try: writer.close(); await asyncio.wait_for(writer.wait_closed(), 2.0)
                            except Exception: pass
                            await asyncio.sleep(NON_MATCH_RECONNECT_DELAY)
                            break

                    if 30 <= pl <= 40: continue

            except asyncio.CancelledError:
                for m in play_matches:
                    if not m.done(): m.cancel()
                if play_matches:
                    await asyncio.gather(*play_matches, return_exceptions=True)
                play_matches.clear()
                if gateway_ping_task: gateway_ping_task.cancel()
                async with runtime.lock:
                    runtime.peers.pop(uid_str, None)
                    if runtime.leader_uid == uid_str:
                        runtime.leader_uid = None
                await runtime.member_leave(uid_str)
                raise
            except Exception as e:
                if gateway_ping_task: gateway_ping_task.cancel()
                play_matches[:] = [m for m in play_matches if not m.done()]
                if writer:
                    try: writer.close(); await asyncio.wait_for(writer.wait_closed(), 2.0)
                    except Exception: pass
                if "Cache expired" in str(e):
                    break
                reconnect_count_total += 1
                reconnects += 1
                if reconnects > max_reconnects:
                    reconnects = 0
                    await asyncio.sleep(3)
                    continue
                await asyncio.sleep(bypass_human_reconnect_delay(reconnects))
            finally:
                _team_active["flag"] = False
                for tk in (team_coord_task, member_trigger_task):
                    if tk and not tk.done():
                        tk.cancel()
                        try: await tk
                        except (asyncio.CancelledError, Exception): pass
                if gateway_ping_task: gateway_ping_task.cancel()
                if writer:
                    try: writer.close(); await asyncio.wait_for(writer.wait_closed(), 2.0)
                    except Exception: pass
                async with runtime.lock:
                    runtime.peers.pop(uid_str, None)
                    if runtime.leader_uid == uid_str:
                        runtime.leader_uid = None
                await runtime.member_leave(uid_str)
                _team_active["flag"] = True
    except asyncio.CancelledError:
        for m in play_matches:
            if not m.done(): m.cancel()
        if play_matches: await asyncio.gather(*play_matches, return_exceptions=True)
        play_matches.clear()
        raise

# ═══════════════════════════ INFORMATIONAL ═══════════════════════════
async def informational(addrs, starter_packet, key, iv, region="BD", max_reconnects=3):
    reconnects = 0
    ip, port = addrs.split(":")
    while True:
        writer = None; ping_task = None
        try:
            rip = await resolve_host_cloudflare(ip)
            reader, writer = await asyncio.open_connection(rip, int(port))
            rs = writer.get_extra_info('socket')
            if rs: optimize_tcp_socket(rs)
            writer.write(bytes.fromhex(starter_packet)); await writer.drain()
            reconnects = 0
            try:
                ka = await send_keep_alive(region)
                if ka and not writer.is_closing():
                    writer.write(ka); await asyncio.wait_for(writer.drain(), timeout=3)
            except Exception: pass
            async def info_ka():
                ka = await send_keep_alive(region)
                while True:
                    await asyncio.sleep(bypass_ka_jitter(5.0))
                    try:
                        if writer and not writer.is_closing():
                            writer.write(ka); await writer.drain()
                    except Exception: break
            ping_task = asyncio.create_task(info_ka())
            while True:
                data = await reader.read(8192)
                if not data: raise ConnectionError("closed")
        except asyncio.CancelledError:
            if ping_task: ping_task.cancel()
            if writer:
                try: writer.close(); await asyncio.wait_for(writer.wait_closed(), 2.0)
                except Exception: pass
            raise
        except Exception:
            if ping_task: ping_task.cancel()
            if writer:
                try: writer.close(); await asyncio.wait_for(writer.wait_closed(), 2.0)
                except Exception: pass
            reconnects += 1
            if reconnects > max_reconnects:
                await asyncio.sleep(3); reconnects = 0
            else: await asyncio.sleep(1)

# ═══════════════════════════ GUILD ENGINE ═══════════════════════════
_guild_ssl = ssl.create_default_context()
_guild_ssl.check_hostname = False
_guild_ssl.verify_mode    = ssl.CERT_NONE

def _guild_get(url, timeout=20):
    req = urllib.request.Request(url, method="GET", headers={
        "User-Agent": GUILD_UA,
        "Accept": "application/json, text/plain, */*",
        "Connection": "close",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_guild_ssl) as r:
            return True, r.status, r.read().decode("utf-8", "replace"), url, None
    except urllib.error.HTTPError as e:
        try:  body = e.read().decode("utf-8", "replace")
        except: body = ""
        return False, e.code, body, url, None
    except Exception as e:
        return False, 0, "", url, str(e)

def _guild_call(endpoints, guild_id, uid, pwd):
    last = (False, 0, "", endpoints[0])
    for ep in endpoints:
        q = urllib.parse.urlencode({"guild_id": guild_id, "uid": uid, "password": pwd})
        ok, code, body, used, err = _guild_get(f"{ep}?{q}")
        if ok: return True, code, body, used
        last = (False, code, body, used)
    return last

def _guild_body_failed(body):
    try:
        data = json.loads(body) if body else {}
        if isinstance(data, dict) and (
            data.get("success") is False or data.get("ok") is False or
            str(data.get("status", "")).lower() in ("error", "failed", "fail")
        ):
            return True
    except Exception:
        pass
    return False

def guild_result_msg(ok, code, body):
    """Short human readable reason for the UI (API message, or a clear network error)."""
    msg = ""
    try:
        data = json.loads(body) if body else {}
        if isinstance(data, dict):
            msg = str(data.get("message") or data.get("msg") or data.get("error") or data.get("status") or "")
        else:
            msg = str(body or "")
    except Exception:
        msg = str(body or "")
    msg = re.sub(r"\s+", " ", msg).strip()[:160]
    if not ok:
        low = msg.lower()
        if code == 0:
            if any(k in low for k in ("name or service not known", "name resolution", "getaddrinfo", "errno -2", "errno -3", "errno 11001", "failed to resolve")):
                msg = "API host not found (DNS). Check GUILD_JOIN_API in the code."
            elif "timed out" in low:
                msg = "API timed out. Try again."
            elif not msg:
                msg = "Cannot reach the guild API."
        elif not msg:
            msg = {401: "Rejected by API (401)", 403: "Blocked by API (403)", 404: "API endpoint not found (404)",
                   429: "Rate limited, try later"}.get(code, f"API returned HTTP {code}")
    return msg

def _guild_api_call(api_url, action, g, u, p, region):
    q = urllib.parse.urlencode({
        "action": action, "uid": str(u), "pass": str(p),
        "clan_id": str(g), "region": str(region or "BD")
    })
    ok, code, body, used, err = _guild_get(f"{api_url}?{q}")
    if err:
        return False, code, body or err, used
    if ok and _guild_body_failed(body):
        ok = False
    return ok, code, body, used

def guild_do_join(g, u, p, region="BD"):
    return _guild_api_call(GUILD_JOIN_API, "join_clan", g, u, p, region)

def guild_do_leave(g, u, p, region="BD"):
    # same API + same fields as join (action=leave_clan); old endpoints stay as a fallback
    res = _guild_api_call(GUILD_LEAVE_API, "leave_clan", g, u, p, region)
    if res[0]:
        return res
    legacy = _guild_call(GUILD_LEAVE_ENDPOINTS, g, u, p)
    return legacy if legacy[0] else res

def guild_call_with_retry(fn, gid, uid, pwd, max_retries=3):
    backoff = 0.6
    last = (False, 0, "", "")
    for attempt in range(max_retries + 1):
        try:
            ok, code, body, ep = fn(gid, uid, pwd)
            last = (ok, code, body, ep)
            if ok: return ok, code, body, ep, attempt
            if code == 429 or (500 <= code < 600):
                time.sleep(backoff + random.uniform(0, 0.3))
                backoff *= 2
                continue
            return ok, code, body, ep, attempt
        except Exception as e:
            last = (False, 0, str(e), "")
            time.sleep(backoff)
            backoff *= 2
    return (*last, max_retries)

def get_guild_owner_uid(guild_id):
    endpoints = [
        f"{GUILD_BASE}/guild/info?guild_id={guild_id}",
        f"{GUILD_BASE}/info?guild_id={guild_id}",
        f"{GUILD_BASE}/guild/details?guild_id={guild_id}",
    ]
    for ep in endpoints:
        ok, code, body, _, _ = _guild_get(ep, timeout=12)
        if ok and body:
            try:
                data = json.loads(body)
                owner = (
                    data.get("owner_id") or data.get("leader_id") or
                    data.get("owner_uid") or data.get("leader_uid") or
                    data.get("data", {}).get("owner_id") or
                    data.get("guild_info", {}).get("owner_id")
                )
                if owner and str(owner).isdigit(): return int(owner)
            except Exception: continue
    return None

def guild_encrypt_data(data: bytes) -> bytes:
    cipher = AES.new(FRIEND_AES_KEY, AES.MODE_CBC, FRIEND_AES_IV)
    return cipher.encrypt(pad(data, AES.block_size))

def guild_encode_varint(n: int) -> bytes:
    result = []
    while True:
        byte = n & 0x7F; n >>= 7
        if n: byte |= 0x80
        result.append(byte)
        if not n: break
    return bytes(result)

def guild_build_friend_request_payload(target_uid: int) -> bytes:
    body  = guild_encode_varint(8) + guild_encode_varint(target_uid)
    body += guild_encode_varint(16) + guild_encode_varint(target_uid)
    body += guild_encode_varint(24) + guild_encode_varint(26)
    return body

def guild_jwt_from_external_api(api_url: str, uid: str, password: str, retries: int = 1):
    if _requests is None: return None, "requests unavailable"
    err_msg = ""
    for attempt in range(retries + 1):
        try:
            url = f"{api_url}?uid={uid}&password={password}"
            resp = _requests.get(url, timeout=12, verify=False)
            if resp.status_code == 200:
                data = resp.json()
                token = (
                    data.get("token") or data.get("jwt") or data.get("access_token") or
                    data.get("data", {}).get("token") or data.get("data", {}).get("jwt")
                )
                if token and len(token) > 50: return token, None
                err_msg = "API json missing Token"
            else:
                err_msg = f"API HTTP {resp.status_code}"
        except Exception as e:
            err_msg = str(e)[:30]
        if attempt < retries: time.sleep(0.3)
    return None, err_msg

def guild_get_jwt(uid: str, password: str, retries: int = 1):
    for mname, url in JWT_API_ENDPOINTS:
        jwt, err = guild_jwt_from_external_api(url, uid, password, retries)
        if jwt: return jwt, mname, None
    return None, None, "JWT failed"

def guild_send_friend_request(jwt: str, target_uid: int, retries: int = 1):
    if _requests is None: return False, 0, "requests unavailable"
    plain = guild_build_friend_request_payload(target_uid)
    encrypted = guild_encrypt_data(plain)
    headers = FRIEND_HEADERS.copy()
    headers["Authorization"] = f"Bearer {jwt}"
    last_err = "Max retries"; last_code = 0
    for target_url in BD_FRIEND_URLS:
        for attempt in range(retries + 1):
            try:
                resp = _requests.post(target_url, headers=headers, data=encrypted, timeout=10, verify=False)
                if resp.status_code == 200: return True, resp.status_code, None
                last_code = resp.status_code
                last_err = f"HTTP_{resp.status_code}"
            except Exception as e:
                last_err = str(e)[:25]
            if attempt < retries: time.sleep(0.2)
        if last_code == 200: break
    return False, last_code, last_err

def guild_record_failed(uid, pwd):
    log_dir = "AGS_JOHIR"
    try:
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, "failed_accounts.txt"), "a", encoding="utf-8") as f:
            f.write(f"{uid}:{pwd}\n")
    except Exception: pass

# ═══════════════════════════ GUILD RUNNERS ═══════════════════════════
async def guild_run_join_or_leave(jid, guild_id, action, accounts, delay, workers):
    fn = guild_do_join if action == "JOIN" else guild_do_leave
    sem = asyncio.Semaphore(max(1, workers))

    async def one(uid, pwd):
        async with sem:
            try:
                ok, code, body, ep, retries = await asyncio.to_thread(
                    guild_call_with_retry, fn, guild_id, uid, pwd, 3)
                msg = ""
                try:
                    if body:
                        j = json.loads(body)
                        msg = str(j.get("message") or j.get("msg") or j.get("error") or "")[:120]
                except Exception:
                    msg = (body or "")[:120].replace("\n", " ")
                detail = f"HTTP {code} | ep={ep.split('/')[-1]}"
                if not ok:
                    guild_record_failed(uid, pwd)
                bot_state.add_guild_result(jid, uid, ok, msg, detail)
                bot_state.update_guild(str(uid), "SUCCESS" if ok else "FAILED", detail)
                if ok:
                    print_success(f"🏰 [GUILD-{action}] {uid} OK | {msg}", str(uid))
                else:
                    print_error(f"🏰 [GUILD-{action}] {uid} FAIL | {msg}", str(uid))
            except Exception as e:
                bot_state.add_guild_result(jid, uid, False, str(e), "exception")
            await asyncio.sleep(delay)

    tasks = [asyncio.create_task(one(u, p)) for u, p in accounts]
    if tasks: await asyncio.gather(*tasks, return_exceptions=True)
    bot_state.finish_guild_job(jid)

async def guild_run_owner_spam(jid, guild_id, owner_uid, accounts, delay, workers):
    sem = asyncio.Semaphore(max(1, workers))

    async def one(uid, pwd):
        async with sem:
            try:
                g_ok, g_code, g_body, ep, retries = await asyncio.to_thread(
                    guild_call_with_retry, guild_do_join, guild_id, uid, pwd, 2)
                f_status = "Skipped"; fail_reason = ""
                jwt, method, jwt_err = await asyncio.to_thread(guild_get_jwt, uid, pwd, 1)
                if jwt:
                    ok_f, scode, f_err = await asyncio.to_thread(guild_send_friend_request, jwt, owner_uid, 1)
                    if ok_f: f_status = f"Sent ({scode})"
                    else: f_status = f"Fail ({scode})"; fail_reason = f"Request: {f_err}"
                else:
                    f_status = "JWT Failed"; fail_reason = f"JWT: {jwt_err}"
                extra = f"Guild:{'OK' if g_ok else 'FAIL'} | FR:{f_status}"
                msg = ""
                try:
                    if g_body:
                        j = json.loads(g_body)
                        msg = str(j.get("message") or j.get("msg") or j.get("error") or "")[:120]
                except Exception:
                    msg = (g_body or "")[:120]
                if not g_ok:
                    guild_record_failed(uid, pwd)
                bot_state.add_guild_result(jid, uid, g_ok, msg, extra + (f" | {fail_reason}" if fail_reason else ""))
                bot_state.update_guild(str(uid), "SUCCESS" if g_ok else "FAILED", extra)
                if g_ok:
                    print_success(f"👑 [OWNER-SPAM] {uid} | {extra}", str(uid))
                else:
                    print_error(f"👑 [OWNER-SPAM] {uid} | {extra}", str(uid))
            except Exception as e:
                bot_state.add_guild_result(jid, uid, False, str(e), "exception")
            await asyncio.sleep(delay)

    tasks = [asyncio.create_task(one(u, p)) for u, p in accounts]
    if tasks: await asyncio.gather(*tasks, return_exceptions=True)
    bot_state.finish_guild_job(jid)

# ═══════════════════════════ ACCOUNT HELPERS ═══════════════════════════
def _register_credentials(ad):
    try:
        acc_id = str(ad['account_id'])
        bot_state.account_credentials[acc_id] = ad
        if ad.get('auth_uid'): bot_state.account_credentials[str(ad['auth_uid'])] = ad
        if ad.get('auth_token'): bot_state.account_credentials[f"tok_{ad['auth_token'][:20]}"] = ad
    except Exception: pass

async def relogin_account(uid_str, old_account_data):
    if not old_account_data: return None
    if old_account_data.get('auth_type') == 'guest':
        u = old_account_data.get('auth_uid'); p = old_account_data.get('auth_password')
        if u and p: return await process_account_uid_pass(str(u), str(p), _skip_cache=True)
    elif old_account_data.get('auth_type') == 'token':
        t = old_account_data.get('auth_token')
        if t: return await process_account_token(str(t), _skip_cache=True)
    return None

async def refresh_account_profile(ad_or_uid):
    try:
        if isinstance(ad_or_uid, str):
            uid = str(ad_or_uid); ad = bot_state.account_credentials.get(uid)
        else:
            ad = ad_or_uid; uid = str(ad.get('account_id')) if ad else "?"
        if not ad: return
        url = ad.get('server_url'); token = ad.get('token')
        rel = ad.get('release_version'); payload = ad.get('login_payload_data')
        if not (url and token and rel and payload): return
        res = await send_getlogin(payload, url, token, rel)
        if not res: return
        rp, dd = res
        def _si(v, d):
            try:
                if v is None or v == "": return d
                return int(v)
            except Exception: return d
        level = _si(get_proto_field(dd, 6, None), None)
        exp = _si(get_proto_field(dd, 7, None), None)
        likes = _si(get_proto_field(dd, 8, None), None)
        try: nick = rp.nickname or get_proto_field(dd, 4, "") or ""
        except Exception: nick = ""
        if level is None and exp is None: return
        level = level if level is not None else 1
        exp = exp if exp is not None else 0
        likes = likes if likes is not None else 0
        acc_id = str(ad['account_id'])
        try: bot_state.update_exp(acc_id, exp, level)
        except Exception: pass
        if likes > 0 and acc_id in bot_state.accounts:
            bot_state.accounts[acc_id]["likes"] = likes
        if nick and acc_id in bot_state.accounts:
            bot_state.accounts[acc_id]["nickname"] = nick
        _update_cache_profile(ad, level, exp)
        ad['level'] = level; ad['exp'] = exp
        if likes > 0: ad['likes'] = likes
        if nick: ad['nickname'] = nick
    except Exception: pass

async def process_account_uid_pass(uid, password, _skip_cache=False):
    if not _skip_cache:
        cached = cache_get(uid)
        if cached:
            acc_id = str(cached['account_id'])
            bot_state.register_account(uid=acc_id,
                nickname=cached.get('nickname', f"Player_{acc_id}"),
                region=cached.get('region', 'BD'),
                level=cached.get('level', 1), exp=cached.get('exp', 0),
                likes=cached.get('likes', 0), password=password)
            _register_credentials(cached); return cached
    try:
        vc = await version_config()
        if not vc: return None
        rel, cv, su = vc
        tg = await get_access_token(uid, password)
        if not tg: return None
        oid, at, pf = tg
        dev = get_device_for_account(uid)
        lpd = await build_majorlogin_payload(oid, at, pf, cv, dev)
        if not lpd: return None
        mresp = await send_majorlogin(lpd, rel, su)
        if mresp is None: return None
        gl = await send_getlogin(lpd, mresp.url, mresp.token, rel)
        if gl is None: return None
        rp, dd = gl
        acc_id = str(mresp.account_id)
        level = int(get_proto_field(dd, 6, 1) or 1)
        exp = int(get_proto_field(dd, 7, 0) or 0)
        likes = int(get_proto_field(dd, 8, 0) or 0)
        nick = rp.nickname or get_proto_field(dd, 4, f"Player_{acc_id}")
        region = mresp.region or get_proto_field(dd, 3, "BD")
        bot_state.register_account(uid=acc_id, nickname=nick, region=region,
                                    level=level, exp=exp, likes=likes, password=password)
        ad = {
            'account_id': mresp.account_id, 'nickname': nick, 'region': region,
            'level': level, 'exp': exp, 'likes': likes,
            'open_id': oid, 'access_token': at, 'platform': str(pf),
            'token': mresp.token, 'server_time': mresp.server_time,
            'aes_ak': mresp.aes_ak, 'iv_i': mresp.iv_i,
            'functional_addrs': rp.functional_addrs or get_proto_field(dd, 14),
            'informational_addrs': rp.informational_addrs or get_proto_field(dd, 32),
            'release_version': rel, 'client_version': cv, 'server_url': mresp.url,
            'login_payload_data': lpd,
            'auth_type': 'guest', 'auth_uid': uid, 'auth_password': password,
        }
        _register_credentials(ad); cache_set(uid, ad); return ad
    except Exception as e:
        print_error(f"process_account_uid_pass: {e}"); return None

async def process_account_token(access_token, _skip_cache=False):
    cache_key = f"tok_{access_token[:20]}"
    if not _skip_cache:
        cached = cache_get(cache_key)
        if cached:
            acc_id = str(cached['account_id'])
            bot_state.register_account(uid=acc_id,
                nickname=cached.get('nickname', f"Player_{acc_id}"),
                region=cached.get('region', 'BD'),
                level=cached.get('level', 1), exp=cached.get('exp', 0),
                likes=cached.get('likes', 0))
            _register_credentials(cached); return cached
    try:
        vc = await version_config()
        if not vc: return None
        rel, cv, su = vc
        if _requests is None: return None
        url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
        hdrs = {"User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)"}
        resp = await asyncio.to_thread(_requests.get, url, headers=hdrs, timeout=10)
        d = resp.json()
        if 'error' in d: return None
        oid = d.get('open_id'); pf = d.get('platform', 4)
        if not oid: return None
        dev = get_device_for_account(oid)
        lpd = await build_majorlogin_payload(oid, access_token, str(pf), cv, dev)
        if not lpd: return None
        mresp = await send_majorlogin(lpd, rel, su)
        if mresp is None: return None
        gl = await send_getlogin(lpd, mresp.url, mresp.token, rel)
        if gl is None: return None
        rp, dd = gl
        acc_id = str(mresp.account_id)
        level = int(get_proto_field(dd, 6, 1) or 1)
        exp = int(get_proto_field(dd, 7, 0) or 0)
        likes = int(get_proto_field(dd, 8, 0) or 0)
        nick = rp.nickname or get_proto_field(dd, 4, f"Player_{acc_id}")
        region = mresp.region or get_proto_field(dd, 3, "BD")
        bot_state.register_account(uid=acc_id, nickname=nick, region=region,
                                    level=level, exp=exp, likes=likes)
        ad = {
            'account_id': mresp.account_id, 'nickname': nick, 'region': region,
            'level': level, 'exp': exp, 'likes': likes,
            'open_id': oid, 'access_token': access_token, 'platform': str(pf),
            'token': mresp.token, 'server_time': mresp.server_time,
            'aes_ak': mresp.aes_ak, 'iv_i': mresp.iv_i,
            'functional_addrs': rp.functional_addrs or get_proto_field(dd, 14),
            'informational_addrs': rp.informational_addrs or get_proto_field(dd, 32),
            'release_version': rel, 'client_version': cv, 'server_url': mresp.url,
            'login_payload_data': lpd,
            'auth_type': 'token', 'auth_token': access_token,
        }
        _register_credentials(ad); cache_set(cache_key, ad); return ad
    except Exception as e:
        print_error(f"process_account_token: {e}"); return None

async def run_account_worker(runtime: SquadRuntime, ad, label):
    acc_id = str(ad['account_id'])
    info_task = None; exp_task = None; ping_task = None
    try:
        reg = ad.get('region', 'BD')
        tcp_online = await build_tcp_startup_packet(
            ad['account_id'], ad['token'], ad['server_time'],
            ad['aes_ak'], ad['iv_i'], region=reg, typ='OnLine')
        tcp_chat = await build_tcp_startup_packet(
            ad['account_id'], ad['token'], ad['server_time'],
            ad['aes_ak'], ad['iv_i'], region=reg, typ='ChaT')
        info_task = asyncio.create_task(informational(ad['informational_addrs'], tcp_chat,
                                                      ad['aes_ak'], ad['iv_i'], region=reg))
        if ENABLE_HTTP_PING:
            ping_task = asyncio.create_task(ping_worker(acc_id, ad['token'], ad['release_version'], region=reg))

        async def exp_refresher():
            try:
                f = bot_state.account_credentials.get(acc_id)
                if f: await refresh_account_profile(f)
            except Exception: pass
            while True:
                await asyncio.sleep(EXP_REFRESH_INTERVAL + random.uniform(-3.0, 3.0))
                try:
                    f = bot_state.account_credentials.get(acc_id)
                    if f: await refresh_account_profile(f)
                except Exception: pass
        exp_task = asyncio.create_task(exp_refresher())
        await functional_battle_royale(runtime, ad['functional_addrs'], tcp_online, ad['region'], ad['client_version'],
            ad['aes_ak'], ad['iv_i'], account_id=acc_id, account_data=ad,
            account_level=int(ad.get('level', 2) or 2))
    except asyncio.CancelledError: raise
    except Exception as e:
        bot_state.squad_log(runtime.squad_id, f"Account worker error {label}: {e}", "error")
    finally:
        for t in (info_task, exp_task, ping_task):
            if t and not t.done(): t.cancel()
        for t in (info_task, exp_task, ping_task):
            if t:
                try: await t
                except Exception: pass

async def account_loop_guest(runtime: SquadRuntime, uid, password):
    while runtime.is_running:
        try:
            bot_state.update_status(str(uid), "CONNECTING")
            bot_state.squad_log(runtime.squad_id, f"🔐 Logging in {uid}...", "info")
            ad = await process_account_uid_pass(uid, password)
            if not ad:
                bot_state.update_status(str(uid), "ERROR")
                bot_state.squad_log(runtime.squad_id, f"❌ Login failed {uid}", "error")
                await asyncio.sleep(10); continue
            bot_state.squad_log(runtime.squad_id, f"✅ Logged in {uid} ({ad.get('nickname','?')})", "success")
            await run_account_worker(runtime, ad, uid)
            await asyncio.sleep(2)
        except asyncio.CancelledError:
            bot_state.update_status(str(uid), "OFFLINE")
            break
        except Exception as e:
            bot_state.update_status(str(uid), "ERROR")
            bot_state.squad_log(runtime.squad_id, f"Worker error {uid}: {e}", "error")
            await asyncio.sleep(8)

# ═══════════════════════════ SQUAD MANAGER ═══════════════════════════
SQUADS_FILE       = "squads.json"
STOP_WAIT_TIMEOUT = 8.0     # max seconds to wait for workers to die on stop/restart

class SquadManager:
    """Start / Stop / Restart are idempotent, bounded in time and never leave a
    half-changed state behind (no CancelledError leaks, no lock held forever)."""

    def __init__(self):
        self.squads: Dict[int, dict] = {}
        self._lock = asyncio.Lock()              # create / id allocation only
        self._slocks: Dict[int, asyncio.Lock] = {}   # one lock per squad
        self._counter = 0

    def _allocate_squad_id(self):
        self._counter += 1
        return self._counter

    def _slock(self, sid: int) -> asyncio.Lock:
        lk = self._slocks.get(sid)
        if lk is None:
            lk = self._slocks[sid] = asyncio.Lock()
        return lk

    @staticmethod
    def _is_alive(squad: dict) -> bool:
        t = squad.get("task")
        return bool(t is not None and not t.done())

    # ── ownership: every squad belongs to exactly one user ──
    def _owned(self, sid, owner):
        sq = self.squads.get(sid)
        if sq is None or (owner is not None and sq.get("owner") != owner):
            return None
        return sq

    def sid_for(self, owner, num):
        for sid, sq in self.squads.items():
            if sq.get("owner") == owner and sq.get("num") == num:
                return sid
        return None

    def count_for(self, owner):
        return sum(1 for sq in self.squads.values() if sq.get("owner") == owner)

    def sids_of(self, owner):
        return [sid for sid, sq in self.squads.items() if sq.get("owner") == owner]

    # ── persistence: squads survive a panel/host restart (they come back STOPPED) ──
    def _save(self):
        try:
            data = {"counter": self._counter, "squads": {
                str(sid): {"members": [[u, s["credentials"].get(u, "")] for u in s["uids"]],
                           "owner": s.get("owner"), "num": s.get("num")}
                for sid, s in self.squads.items()}}
            tmp = SQUADS_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            try: os.chmod(tmp, 0o600)
            except Exception: pass
            os.replace(tmp, SQUADS_FILE)
        except Exception as e:
            print_error(f"squads save failed: {e}")

    def load(self):
        try:
            if not os.path.exists(SQUADS_FILE): return
            with open(SQUADS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._counter = int(data.get("counter", 0) or 0)
            # A game UID identifies one account globally, not one squad slot.
            # Older squads.json files may contain duplicate UIDs across squads;
            # loading them would overwrite account_workers[uid] and cross-wire workers.
            globally_seen_uids = set()
            for sid_s, sq in sorted((data.get("squads") or {}).items(),
                                    key=lambda item: int(item[0])):
                sid = int(sid_s)
                owner = str(sq.get("owner") or user_store.admin_id() or "")
                if owner not in user_store.users:
                    continue
                num = int(sq.get("num") or 0) or user_store.next_squad_num(owner)
                user_store.bump_seq(owner, num)
                uids, creds = [], {}
                for uid, pw in sq.get("members", []):
                    uid, pw = str(uid).strip(), str(pw).strip()
                    if not uid or not pw or uid in creds:
                        continue
                    if uid in globally_seen_uids:
                        bot_state.squad_log(
                            sid,
                            f"Skipped duplicate UID {uid}; it is already assigned to another squad",
                            "warning",
                        )
                        continue
                    globally_seen_uids.add(uid)
                    uids.append(uid)
                    creds[uid] = pw
                    bot_state.register_account(uid=uid, nickname=f"Player_{uid}",
                        region="BD", level=1, exp=0, likes=0, password=pw)
                    bot_state.accounts[uid]["squad_id"] = sid
                    bot_state.accounts[uid]["owner"] = owner
                    bot_state.accounts[uid]["slot"] = len(uids)
                    bot_state.accounts[uid]["status"] = "STOPPED"
                if not uids:
                    continue
                self.squads[sid] = {
                    "id": sid, "runtime": SquadRuntime(sid), "uids": uids,
                    "task": None, "is_started": False, "credentials": creds,
                    "owner": owner, "num": num,
                }
                self._counter = max(self._counter, sid)
                bot_state.squad_log(
                    sid,
                    f"♻️ Squad {sid} restored ({len(uids)} accounts) — press Start",
                    "info",
                )
            # Rewrite the cleaned state so invalid duplicate assignments don't return
            # on every restart. Squad IDs remain stable; new squads get a fresh ID.
            self._save()
            print_success(f"♻️ Restored {len(self.squads)} squad(s) from {SQUADS_FILE}")
        except Exception as e:
            print_error(f"squads load failed: {e}")

    # ── create ──
    async def create_squad(self, members: List[Tuple[str, str]], owner: str = "") -> Tuple[bool, str, int]:
        async with self._lock:
            clean, seen = [], set()
            for uid, pw in members:
                uid = str(uid).strip()
                pw = str(pw).strip()
                if not uid or not pw:
                    continue
                if uid in seen:
                    return False, f"UID {uid} appears more than once in this squad", 0
                # Different passwords do not make a duplicate UID a separate account.
                # A UID must belong to exactly one squad to avoid worker/runtime collisions.
                for other_sid, other in self.squads.items():
                    if uid in other["uids"]:
                        if other.get("owner") == owner:
                            return False, f"UID {uid} is already in Squad {other.get('num')}.", 0
                        return False, f"UID {uid} is already in use on this panel.", 0
                seen.add(uid)
                clean.append((uid, pw))
            if not clean:
                return False, "No valid accounts", 0
            sid = self._allocate_squad_id()
            num = user_store.next_squad_num(owner)
            for slot, (uid, pw) in enumerate(clean, 1):
                bot_state.register_account(uid=uid, nickname=f"Player_{uid}",
                    region="BD", level=1, exp=0, likes=0, password=pw)
                bot_state.accounts[uid]["squad_id"] = sid
                bot_state.accounts[uid]["owner"] = owner
                bot_state.accounts[uid]["slot"] = slot
                bot_state.accounts[uid]["status"] = "STOPPED"
            self.squads[sid] = {
                "id": sid, "runtime": SquadRuntime(sid),
                "uids": [u for u, _ in clean], "task": None,
                "is_started": False, "credentials": dict(clean),
                "owner": owner, "num": num,
            }
            self._save()
            bot_state.squad_log(sid, f"🛡️ Squad {sid} created with {len(clean)} accounts", "success")
            return True, f"Squad {num} created", num

    # ── internals ──
    async def _kill(self, squad: dict):
        """Cancel every worker of this squad and wait a bounded time. Never raises, never hangs."""
        sid = squad["id"]
        squad["runtime"].is_running = False
        squad["runtime"].team_active = False
        tasks = []
        for uid in list(squad["uids"]):
            t = bot_state.account_workers.pop(uid, None)
            if t is not None and not t.done():
                t.cancel(); tasks.append(t)
        main_t = squad.get("task")
        if main_t is not None and not main_t.done():
            main_t.cancel(); tasks.append(main_t)
        squad["task"] = None
        if tasks:
            # asyncio.wait() does NOT re-raise the workers' CancelledError (await t does!)
            _, pending = await asyncio.wait(tasks, timeout=STOP_WAIT_TIMEOUT)
            for t in pending:
                t.cancel()
            if pending:
                bot_state.squad_log(sid, f"⚠️ {len(pending)} stuck worker(s) force-stopped", "warning")
            for t in tasks:
                if t.done() and not t.cancelled():
                    t.exception()          # mark retrieved, avoids 'never retrieved' warnings
        for uid in squad["uids"]:
            bot_state.update_status(uid, "STOPPED")

    def _spawn(self, squad: dict) -> bool:
        """Start fresh workers on a FRESH runtime (a stuck old worker keeps the old, dead runtime)."""
        sid = squad["id"]
        runtime = SquadRuntime(sid)
        runtime.is_running = True
        runtime.team_active = True
        squad["runtime"] = runtime
        tasks = []
        for uid in squad["uids"]:
            pw = squad["credentials"].get(uid, "")
            if not pw: continue
            t = asyncio.create_task(account_loop_guest(runtime, uid, pw))
            bot_state.account_workers[uid] = t
            tasks.append(t)
        if not tasks:
            runtime.is_running = False
            return False
        async def run_all():
            await asyncio.gather(*tasks, return_exceptions=True)
        squad["task"] = asyncio.create_task(run_all())
        squad["is_started"] = True
        return True

    async def _start(self, sid: int, owner=None) -> Tuple[bool, str]:
        async with self._slock(sid):
            squad = self._owned(sid, owner)
            if not squad: return False, "Squad not found"
            if squad["is_started"] and self._is_alive(squad):
                return False, "Already running"
            if squad["is_started"] or squad.get("task") is not None:
                await self._kill(squad)          # stale flag / dead task → clean first
            if not self._spawn(squad):
                squad["is_started"] = False
                return False, "No account with password in this squad"
            bot_state.squad_log(sid, f"▶️ Squad {sid} started", "success")
            return True, f"Squad {sid} started"

    async def _restart(self, sid: int, owner=None) -> Tuple[bool, str]:
        async with self._slock(sid):
            squad = self._owned(sid, owner)
            if not squad: return False, "Squad not found"
            await self._kill(squad)
            await asyncio.sleep(1.0)
            if not self._spawn(squad):
                squad["is_started"] = False
                return False, "No account with password in this squad"
            bot_state.squad_log(sid, f"🔄 Squad {sid} restarted", "success")
            return True, f"Squad {sid} restarted"

    async def _stop(self, sid: int, owner=None) -> Tuple[bool, str]:
        async with self._slock(sid):
            squad = self._owned(sid, owner)
            if not squad: return False, "Squad not found"
            await self._kill(squad)
            squad["is_started"] = False
            bot_state.squad_log(sid, f"⏹ Squad {sid} stopped", "warning")
            return True, f"Squad {sid} stopped"

    async def _delete(self, sid: int, owner=None) -> Tuple[bool, str]:
        async with self._slock(sid):
            squad = self._owned(sid, owner)
            if not squad: return False, "Not found"
            await self._kill(squad)
            for uid in squad["uids"]:
                bot_state.accounts.pop(uid, None)
                bot_state.account_credentials.pop(uid, None)
            self.squads.pop(sid, None)
            bot_state.squad_logs.pop(sid, None)
            self._save()
        self._slocks.pop(sid, None)
        return True, "Deleted"

    async def _remove(self, sid: int, uid: str, owner=None) -> Tuple[bool, str]:
        async with self._slock(sid):
            squad = self._owned(sid, owner)
            if not squad: return False, "Squad not found"
            if uid not in squad["uids"]: return False, "Not found"
            t = bot_state.account_workers.pop(uid, None)
            if t is not None and not t.done():
                t.cancel()
                await asyncio.wait([t], timeout=STOP_WAIT_TIMEOUT)
            squad["uids"].remove(uid)
            squad["credentials"].pop(uid, None)
            bot_state.accounts.pop(uid, None)
            bot_state.account_credentials.pop(uid, None)
            self._save()
            return True, "Removed"

    # ── public API (shielded: a dropped HTTP connection can't leave a half-done stop/restart) ──
    async def start_squad(self, sid: int, owner=None):
        if self._owned(sid, owner) is None: return False, "Squad not found"
        return await asyncio.shield(self._start(sid, owner))
    async def restart_squad(self, sid: int, owner=None):
        if self._owned(sid, owner) is None: return False, "Squad not found"
        return await asyncio.shield(self._restart(sid, owner))
    async def stop_squad(self, sid: int, owner=None):
        if self._owned(sid, owner) is None: return False, "Squad not found"
        return await asyncio.shield(self._stop(sid, owner))
    async def delete_squad(self, sid: int, owner=None):
        if self._owned(sid, owner) is None: return False, "Squad not found"
        return await asyncio.shield(self._delete(sid, owner))
    async def remove_member(self, sid: int, uid: str, owner=None):
        if self._owned(sid, owner) is None: return False, "Squad not found"
        return await asyncio.shield(self._remove(sid, uid, owner))

    def get_squads(self, owner=None):
        out = []
        if owner is None:
            return out
        for sid, s in sorted(self.squads.items(), key=lambda kv: kv[1].get("num", 0)):
            if s.get("owner") != owner:
                continue
            members = []
            for uid in s["uids"]:
                acc = bot_state.accounts.get(uid, {})
                members.append({
                    "uid": uid,
                    "nickname": acc.get("nickname", "?"),
                    "level": acc.get("level", 1),
                    "matches": acc.get("matches", 0),
                    "status": acc.get("status", "STOPPED"),
                    "guild_status": acc.get("guild_status", "—"),
                })
            out.append({
                "id": s.get("num", sid),
                "is_started": bool(s["is_started"] and self._is_alive(s)),
                "members": members,
            })
        return out

squad_mgr = SquadManager()

# ═══════════════════════════ USER SYSTEM (every user is fully isolated) ═══════════════════════════
USERS_FILE = "users.json"
SESSIONS_FILE = "sessions.json"
ADMIN_USERNAME = "admin"                       # password = ADMIN_PASSWORD above
ALLOW_REGISTRATION = os.environ.get("ALLOW_REGISTRATION", "1") != "0"
MAX_USERS = 500
MAX_SQUADS_PER_USER = 5                        # the admin account is unlimited
SESSION_TTL = 30 * 86400
PBKDF2_ITERS = 200000
MIN_PASSWORD = 8
USERNAME_RE = re.compile(r"^[A-Za-z0-9_.]{3,20}$")
RESERVED_NAMES = {"admin", "administrator", "root", "support", "owner", "system", "staff", "moderator"}

def _hash_pw(password, salt=None, iters=PBKDF2_ITERS):
    salt = salt or secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iters)
    return f"pbkdf2${iters}${salt.hex()}${dk.hex()}"

def _verify_pw(password, stored):
    try:
        _, iters, salt_hex, dk_hex = str(stored).split("$")
        dk = hashlib.pbkdf2_hmac("sha256", str(password).encode("utf-8"), bytes.fromhex(salt_hex), int(iters))
        return hmac.compare_digest(dk.hex(), dk_hex)
    except Exception:
        return False

_DUMMY_HASH = _hash_pw("timing-equalizer-password")

def _atomic_json_write(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    try: os.chmod(tmp, 0o600)
    except Exception: pass
    os.replace(tmp, path)

class UserStore:
    def __init__(self):
        self.users: Dict[str, dict] = {}
        self.sessions: Dict[str, dict] = {}
        self._counter = 0

    def load(self):
        try:
            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, "r", encoding="utf-8") as f:
                    d = json.load(f)
                self.users = {str(k): v for k, v in (d.get("users") or {}).items()}
                self._counter = int(d.get("counter", 0) or 0)
                for k in self.users:
                    self._counter = max(self._counter, int(k))
        except Exception as e:
            print_error(f"users load failed: {e}")
        try:
            if os.path.exists(SESSIONS_FILE):
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                now = time.time()
                self.sessions = {h: v for h, v in raw.items()
                                 if isinstance(v, dict) and v.get("exp", 0) > now and v.get("uid") in self.users}
        except Exception as e:
            print_error(f"sessions load failed: {e}")

    def save(self):
        try: _atomic_json_write(USERS_FILE, {"counter": self._counter, "users": self.users})
        except Exception as e: print_error(f"users save failed: {e}")

    def _save_sessions(self):
        try: _atomic_json_write(SESSIONS_FILE, self.sessions)
        except Exception as e: print_error(f"sessions save failed: {e}")

    def find(self, username):
        lc = str(username).strip().lower()
        for u in self.users.values():
            if u["username"].lower() == lc:
                return u
        return None

    def admin_id(self):
        u = self.find(ADMIN_USERNAME)
        return u["id"] if u else None

    def ensure_admin(self):
        u = self.find(ADMIN_USERNAME)
        if u is None:
            self._counter += 1
            uid = str(self._counter)
            self.users[uid] = {"id": uid, "username": ADMIN_USERNAME, "pw": _hash_pw(ADMIN_PASSWORD),
                               "role": "admin", "created": time.time(), "disabled": False, "seq": 0}
            self.save()
            return
        changed = False
        if u.get("role") != "admin" or u.get("disabled"):
            u["role"] = "admin"; u["disabled"] = False; changed = True
        if not _verify_pw(ADMIN_PASSWORD, u.get("pw", "")):     # the constant in the code is the admin password
            u["pw"] = _hash_pw(ADMIN_PASSWORD); self.drop_user_sessions(u["id"]); changed = True
        if changed: self.save()

    def create(self, username, pw_hash):
        self._counter += 1
        uid = str(self._counter)
        rec = {"id": uid, "username": username, "pw": pw_hash, "role": "user",
               "created": time.time(), "disabled": False, "seq": 0}
        self.users[uid] = rec
        self.save()
        return rec

    def next_squad_num(self, uid):
        u = self.users.get(str(uid))
        if not u: return 1
        u["seq"] = int(u.get("seq", 0)) + 1
        self.save()
        return u["seq"]

    def bump_seq(self, uid, num):
        u = self.users.get(str(uid))
        if u and int(num) > int(u.get("seq", 0)):
            u["seq"] = int(num); self.save()

    @staticmethod
    def _h(token): return hashlib.sha256(str(token).encode("utf-8")).hexdigest()

    def new_session(self, uid):
        token = secrets.token_urlsafe(32)
        self.sessions[self._h(token)] = {"uid": str(uid), "exp": time.time() + SESSION_TTL}
        self._save_sessions()
        return token

    def session_user(self, token):
        if not token: return None
        h = self._h(token)
        s_ = self.sessions.get(h)
        if not s_: return None
        if s_.get("exp", 0) < time.time():
            self.sessions.pop(h, None); return None
        u = self.users.get(s_["uid"])
        if not u or u.get("disabled"): return None
        return u

    def drop_session(self, token):
        if self.sessions.pop(self._h(token), None) is not None:
            self._save_sessions()

    def drop_user_sessions(self, uid, keep_token=None):
        keep = self._h(keep_token) if keep_token else None
        for h in [h for h, v in self.sessions.items() if v.get("uid") == str(uid) and h != keep]:
            self.sessions.pop(h, None)
        self._save_sessions()

    def delete_user(self, uid):
        self.users.pop(str(uid), None)
        self.drop_user_sessions(uid)
        self.save()

    @staticmethod
    def public(u):
        return {"username": u["username"], "role": u.get("role", "user"), "created": u.get("created", 0)}

user_store = UserStore()

_RATE: Dict[str, List[float]] = {}
def _rate_count(key, window):
    now = time.time()
    lst = [t for t in _RATE.get(key, []) if now - t < window]
    if lst: _RATE[key] = lst
    else: _RATE.pop(key, None)
    return len(lst)
def _rate_add(key):
    _RATE.setdefault(key, []).append(time.time())
    if len(_RATE) > 5000:
        for k in list(_RATE.keys())[:1000]: _RATE.pop(k, None)
def _rate_blocked(key, limit, window): return _rate_count(key, window) >= limit
def _rate_clear(key): _RATE.pop(key, None)

# ═══════════════════════════ WEB SERVER ═══════════════════════════
try:
    from aiohttp import web as aioweb
    _HAS_AIOHTTP = True
except Exception:
    _HAS_AIOHTTP = False

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YOUBIN SAMIUL · Premium Panel</title><meta name="theme-color" content="#05060f">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a1020;--panel:#111a30;--raise:#18233f;--line:#25324f;--tx:#e8edf7;--mut:#8a97b4;--gold:#f0b84a;--grn:#2fcf8e;--red:#ef5a5a;--blu:#5aa9ff;--amb:#f5a742;--r:12px}
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{background:var(--bg);color:var(--tx);font-family:'Plus Jakarta Sans','Segoe UI','Noto Sans Bengali',system-ui,sans-serif;font-size:15px;line-height:1.45;min-height:100vh;font-variant-numeric:tabular-nums;-webkit-tap-highlight-color:transparent}
button,input,select,textarea{font:inherit;color:inherit}
:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
code{background:var(--raise);padding:1px 6px;border-radius:6px;font-size:.85em}
svg.i{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.header{position:sticky;top:0;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;background:rgba(10,16,32,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.brand{display:flex;align-items:center;gap:10px}
.mark{width:34px;height:34px;flex:none}
.brand b{display:block;font-size:1.05rem;font-weight:800;letter-spacing:.02em}
.brand span{display:block;font-size:.76rem;color:var(--mut)}
.iconbtn{width:40px;height:40px;display:grid;place-items:center;border-radius:10px;background:var(--panel);border:1px solid var(--line);color:var(--mut);cursor:pointer}
.iconbtn:hover{color:var(--tx);border-color:var(--mut)}
.tabs{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;gap:4px;background:rgba(17,26,48,.97);backdrop-filter:blur(10px);border-top:1px solid var(--line);padding:6px 8px calc(6px + env(safe-area-inset-bottom,0px))}
.tab{flex:1;white-space:nowrap;display:flex;flex-direction:column;align-items:center;gap:3px;padding:6px 4px;border-radius:10px;color:var(--mut);font-size:.72rem;font-weight:600;cursor:pointer;user-select:none}
.tab.active{color:var(--gold);background:rgba(240,184,74,.1)}
.content{max-width:1100px;margin:0 auto;padding:16px 14px 100px}
.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin-bottom:14px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:12px 14px}
.stat .num{font-size:1.7rem;font-weight:800;line-height:1.1}
.stat .lbl{font-size:.8rem;color:var(--mut);margin-top:2px}
.squad-card{position:relative;overflow:hidden;background:var(--panel);border:1px solid var(--line);border-radius:var(--r);padding:14px;margin-bottom:14px}
.squad-card.run{border-color:rgba(47,207,142,.45)}
.squad-card.run::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--grn)}
.squad-card h3{font-size:1.05rem;font-weight:800;margin-bottom:12px}
.squad-card.empty{text-align:center;padding:30px 16px;color:var(--mut)}
.squad-card.empty b{display:block;color:var(--tx);font-size:1.05rem;margin-bottom:4px}
.squad-card.empty p{margin-bottom:14px}
.sq-head{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}
.sq-title{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.sq-title h3{margin:0}
.sq-meta{color:var(--mut);font-size:.85rem}
.sq-actions{display:flex;gap:8px;flex-wrap:wrap}
.pill{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;font-size:.78rem;font-weight:700;background:var(--raise);color:var(--mut)}
.pill i{width:7px;height:7px;border-radius:50%;background:currentColor}
.pill.run{background:rgba(47,207,142,.14);color:var(--grn)}
.pill.run i{animation:pulse 1.6s ease-out infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(47,207,142,.6)}100%{box-shadow:0 0 0 7px rgba(47,207,142,0)}}
@media(prefers-reduced-motion:reduce){.pill.run i{animation:none}}
.squad-slots{display:grid;grid-template-columns:minmax(0,1fr);gap:8px}
.slot{display:flex;align-items:flex-start;gap:10px;min-width:0;min-height:68px;padding:10px 12px;border-radius:10px;background:var(--bg);border:1px dashed var(--line);color:var(--mut);font-size:.88rem}
.slot:not(.filled){align-items:center;min-height:52px}
.slot.filled{border-style:solid;color:var(--tx)}
.avatar{width:36px;height:36px;margin-top:2px;flex:none;border-radius:50%;display:grid;place-items:center;font-weight:800;background:var(--raise);color:var(--mut)}
.slot.online .avatar{background:rgba(47,207,142,.16);color:var(--grn)}
.slot.inmatch .avatar{background:rgba(240,184,74,.16);color:var(--gold)}
.slot.connecting .avatar{background:rgba(245,167,66,.16);color:var(--amb)}
.slot.error .avatar{background:rgba(239,90,90,.16);color:var(--red)}
.s-main{min-width:0;flex:1}
.s-name{font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.s-sub{font-size:.76rem;color:var(--mut)}
.s-badges{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
.x{width:28px;height:28px;flex:none;margin-top:2px;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--mut);cursor:pointer}
.x:hover{color:var(--red);border-color:var(--red)}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.72rem;font-weight:700;background:var(--raise);color:var(--mut);white-space:nowrap}
.badge.online,.badge.success{background:rgba(47,207,142,.15);color:var(--grn)}
.badge.inmatch{background:rgba(240,184,74,.15);color:var(--gold)}
.badge.connecting{background:rgba(245,167,66,.15);color:var(--amb)}
.badge.error,.badge.failed{background:rgba(239,90,90,.15);color:var(--red)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:9px 16px;border-radius:10px;border:1px solid var(--line);background:var(--raise);color:var(--tx);font-weight:700;font-size:.88rem;cursor:pointer;transition:background .15s,border-color .15s}
.btn:hover{border-color:var(--mut)}
.btn:active{transform:translateY(1px)}
.btn.small{padding:7px 12px;font-size:.82rem}
.btn.green{background:var(--grn);border-color:var(--grn);color:#04251a}
.btn.gold{background:var(--gold);border-color:var(--gold);color:#2a1d00}
.btn.blue{background:var(--blu);border-color:var(--blu);color:#04152b}
.btn.red,.btn.danger{background:rgba(239,90,90,.12);border-color:rgba(239,90,90,.5);color:var(--red)}
.btn.ghost{background:transparent;color:var(--mut)}
.btn.ghost:hover,.btn.red:hover,.btn.danger:hover{border-color:var(--red);color:var(--red)}
input,textarea,select{width:100%;padding:11px 12px;background:var(--bg);border:1px solid var(--line);border-radius:10px;font-size:1rem}
input[type=checkbox],input[type=radio]{width:auto}
input:focus,textarea:focus,select:focus{border-color:var(--gold);outline:none}
.member-input textarea{min-height:140px;resize:vertical;font-family:ui-monospace,Consolas,monospace;font-size:.9rem}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}
.add-form{display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:8px;margin-bottom:16px}
.row{display:flex;gap:8px;align-items:center;margin-top:8px;flex-wrap:wrap}
.guild-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:8px;margin-top:12px}
.guild-item{background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px;font-size:.85rem}
.guild-item.ok{border-color:rgba(47,207,142,.5)}
.guild-item.fail{border-color:rgba(239,90,90,.5)}
.guild-item .u{font-weight:700}
.guild-item .m{color:var(--mut);font-size:.78rem;margin-top:3px;word-break:break-word}
.alert-red,.alert-green,.alert-info{border:1px solid;border-radius:10px;padding:12px 14px;margin-bottom:12px;font-size:.9rem}
.alert-red{background:rgba(239,90,90,.1);border-color:rgba(239,90,90,.45);color:#ff9d9d}
.alert-green{background:rgba(47,207,142,.1);border-color:rgba(47,207,142,.45);color:#7ce8bd}
.alert-info{background:rgba(90,169,255,.1);border-color:rgba(90,169,255,.4);color:#a9d0ff}
.chips{display:flex;gap:8px;overflow-x:auto;padding-bottom:4px;margin-bottom:12px;scrollbar-width:none}
.chip{flex:none;padding:8px 14px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--mut);font-weight:700;font-size:.86rem;cursor:pointer}
.chip.on{background:var(--gold);border-color:var(--gold);color:#2a1d00}
.log-panel{background:#070c19;border:1px solid var(--line);border-radius:10px;padding:12px;height:min(60vh,460px);overflow-y:auto;font-family:ui-monospace,'Cascadia Mono',Consolas,monospace;font-size:.78rem;line-height:1.6}
.log-line{padding:1px 0;word-break:break-word}
.log-line .lt{color:#5b6a8c;margin-right:8px}
.log-line.success{color:#5fe3ae}.log-line.error{color:#ff8585}.log-line.warning{color:#f5c26b}.log-line.info{color:#9cc7ff}
.login-wrap{min-height:100vh;display:grid;place-items:center;padding:20px;background:radial-gradient(900px 500px at 50% -10%,rgba(240,184,74,.10),transparent 60%)}
.login-box{width:100%;max-width:380px;padding:28px 24px;background:var(--panel);border:1px solid var(--line);border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.45)}
.login-box .mark{width:48px;height:48px;display:block;margin:0 auto 14px}
.login-box h2{text-align:center;font-size:1.3rem;font-weight:800}
.login-box .sub{text-align:center;color:var(--mut);font-size:.88rem;margin:4px 0 18px}
.login-box .btn{width:100%;margin-top:12px;padding:12px}
#toast{position:fixed;left:50%;bottom:calc(86px + env(safe-area-inset-bottom,0px));transform:translateX(-50%);max-width:90%;padding:11px 16px;border-radius:10px;background:var(--raise);border:1px solid var(--line);color:var(--tx);font-size:.92rem;z-index:9999;display:none;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,.4)}
#toast.ok{border-color:var(--grn)}
#toast.err{border-color:var(--red);color:#ffb0b0}
#modal{position:fixed;inset:0;background:rgba(4,8,18,.75);display:none;align-items:center;justify-content:center;z-index:9998}
#modal .box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:20px;max-width:320px;width:86%;text-align:center}
#modal .box p{margin-bottom:16px}
#modal .box .row{justify-content:center}
@media(min-width:700px){.stats{grid-template-columns:repeat(4,1fr)}.squad-slots{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(min-width:820px){
.tabs{position:static;width:fit-content;margin:14px max(16px,calc((100% - 1100px)/2 + 16px)) 0;padding:4px;background:var(--panel);border:1px solid var(--line);border-radius:12px;backdrop-filter:none}
.tab{flex:none;flex-direction:row;gap:8px;padding:8px 16px;font-size:.9rem}
.content{padding:18px 16px 40px}
#toast{bottom:24px}}

/* ===== YOUBIN SAMIUL PREMIUM LAYER ===== */
:root{--bg:#05060f;--panel:#0d1124;--raise:#161b38;--line:#242b4d;--tx:#eef1ff;--mut:#8c94ba;--gold:#ffc65c;--grn:#27e0a3;--red:#ff5d7a;--blu:#5b9dff;--vio:#9b6bff;--amb:#ffa94d;--r:16px;--disp:'Sora','Plus Jakarta Sans',system-ui,sans-serif}
body{background:var(--bg)}
body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;background:radial-gradient(700px 420px at 90% -5%,rgba(155,107,255,.17),transparent 60%),radial-gradient(620px 400px at -5% 8%,rgba(255,198,92,.11),transparent 60%),radial-gradient(760px 520px at 50% 115%,rgba(39,224,163,.08),transparent 60%)}
::selection{background:rgba(255,198,92,.35)}
.header{background:rgba(7,9,22,.84);border-bottom:1px solid rgba(255,255,255,.07)}
.brand b{font-family:var(--disp);font-size:1rem;letter-spacing:.1em;background:linear-gradient(100deg,#fff,#ffe08a 55%,#ff9ec0);-webkit-background-clip:text;background-clip:text;color:transparent}
.prem{font-style:normal;font-family:'Plus Jakarta Sans',sans-serif;font-size:.54rem;letter-spacing:.12em;padding:2px 6px;border-radius:6px;margin-left:8px;vertical-align:middle;background:linear-gradient(135deg,#ffe08a,#f5a524);color:#3a2300;-webkit-text-fill-color:#3a2300}
.iconbtn{border-radius:12px;background:linear-gradient(180deg,#1a2040,#121631);box-shadow:0 3px 0 rgba(0,0,0,.4);transition:transform .15s,color .2s,border-color .2s}
.iconbtn:hover{color:#ff8fa5;border-color:rgba(255,93,122,.55)}
.iconbtn:active{transform:translateY(2px);box-shadow:none}
.tabs{left:12px;right:12px;bottom:calc(10px + env(safe-area-inset-bottom,0px));padding:6px;gap:6px;border-radius:22px;background:rgba(10,13,30,.92);border:1px solid rgba(255,255,255,.09);box-shadow:0 18px 40px -10px rgba(0,0,0,.85)}
.tab{border-radius:16px;transition:background .2s,color .2s,box-shadow .2s}
.tab.active{color:#3a2300;background:linear-gradient(135deg,#ffe08a,#f5a524);box-shadow:0 8px 20px -8px rgba(245,165,36,.75)}
.stat{position:relative;overflow:hidden;border-radius:var(--r);background:linear-gradient(160deg,var(--raise),var(--panel));border-color:rgba(255,255,255,.07)}
.stat::before{content:"";position:absolute;left:0;right:0;top:0;height:2px;background:var(--acc,var(--gold))}
.stat:nth-child(1){--acc:var(--gold)}.stat:nth-child(2){--acc:var(--blu)}.stat:nth-child(3){--acc:var(--vio)}.stat:nth-child(4){--acc:var(--grn)}
.stat .num{font-family:var(--disp);background:linear-gradient(180deg,#fff,var(--acc,var(--gold)));-webkit-background-clip:text;background-clip:text;color:transparent}
.squad-card{border-radius:20px;border-color:rgba(255,255,255,.07);background:linear-gradient(165deg,rgba(22,27,56,.96),rgba(11,14,30,.96));box-shadow:0 16px 36px -20px rgba(0,0,0,.9)}
.squad-card h3{font-family:var(--disp);letter-spacing:.02em}
.squad-card.run{border-color:rgba(39,224,163,.5);box-shadow:0 0 0 1px rgba(39,224,163,.12),0 16px 44px -18px rgba(39,224,163,.4)}
.squad-card.run::before{width:4px;background:linear-gradient(180deg,#34f0b0,#0fb98a)}
.slot{border-radius:14px;background:rgba(5,6,15,.55)}
.badge,.pill{letter-spacing:.02em}
input,textarea,select{background:rgba(5,6,15,.7);border-radius:14px;transition:border-color .2s,box-shadow .2s}
input:focus,textarea:focus,select:focus{border-color:var(--gold);box-shadow:0 0 0 3px rgba(255,198,92,.16)}
.chip{background:linear-gradient(180deg,#1a2040,#121631);box-shadow:0 3px 0 rgba(0,0,0,.35);border-color:rgba(255,255,255,.07)}
.chip.on{background:linear-gradient(135deg,#ffe08a,#f5a524);color:#3a2300;box-shadow:0 3px 0 #a86a0a,0 10px 22px -8px rgba(255,198,92,.5)}
.log-panel{background:#04050c;border-radius:14px}
/* buttons */
.btn{position:relative;overflow:hidden;isolation:isolate;border-radius:14px;padding:10px 18px;font-weight:800;letter-spacing:.02em;border:1px solid rgba(255,255,255,.09);background:linear-gradient(180deg,#1b2142,#121631);color:var(--tx);box-shadow:0 1px 0 rgba(255,255,255,.08) inset,0 4px 0 rgba(0,0,0,.4),0 12px 22px -10px rgba(0,0,0,.7);transition:transform .15s,box-shadow .2s,filter .2s}
.btn::after{content:"";position:absolute;z-index:-1;top:0;bottom:0;left:-70%;width:45%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.32),transparent);transform:skewX(-20deg);transition:left .6s}
.btn:hover{filter:brightness(1.1);border-color:rgba(255,255,255,.2)}
.btn:hover::after{left:130%}
.btn:active{transform:translateY(3px);box-shadow:0 1px 0 rgba(255,255,255,.08) inset,0 1px 0 rgba(0,0,0,.4),0 4px 10px -6px rgba(0,0,0,.7)}
.btn.small{padding:8px 13px;border-radius:12px;font-size:.8rem}
.btn.green{background:linear-gradient(135deg,#34f0b0,#0fb98a);color:#022c1f;border-color:rgba(255,255,255,.28);box-shadow:0 1px 0 rgba(255,255,255,.45) inset,0 4px 0 #087a5c,0 14px 26px -10px rgba(39,224,163,.6)}
.btn.gold{background:linear-gradient(135deg,#ffe08a,#f5a524);color:#3a2300;border-color:rgba(255,255,255,.3);box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 4px 0 #a86a0a,0 14px 26px -10px rgba(255,198,92,.6)}
.btn.blue{background:linear-gradient(135deg,#6fd3ff,#4f7dff);color:#041339;border-color:rgba(255,255,255,.28);box-shadow:0 1px 0 rgba(255,255,255,.45) inset,0 4px 0 #2b4fc2,0 14px 26px -10px rgba(79,125,255,.6)}
.btn.violet{background:linear-gradient(135deg,#c4a0ff,#8a5cff);color:#1b0b3d;border-color:rgba(255,255,255,.28);box-shadow:0 1px 0 rgba(255,255,255,.45) inset,0 4px 0 #4b2bb0,0 14px 26px -10px rgba(138,92,255,.6)}
.btn.red,.btn.danger{background:linear-gradient(180deg,rgba(255,93,122,.2),rgba(255,93,122,.06));color:#ff8fa5;border-color:rgba(255,93,122,.55);box-shadow:0 4px 0 rgba(110,18,42,.75),0 12px 22px -12px rgba(255,93,122,.5)}
.btn.red:hover,.btn.danger:hover{color:#ffc0cc;border-color:rgba(255,93,122,.85)}
.btn.gray{background:linear-gradient(180deg,#1c2243,#131833);color:var(--mut)}
.btn.ghost{background:transparent;color:var(--mut);box-shadow:none;border-color:rgba(255,255,255,.12)}
.btn.ghost:hover{color:#ff8fa5;border-color:rgba(255,93,122,.6)}
#toast{background:rgba(22,27,56,.96);border-radius:14px;bottom:calc(92px + env(safe-area-inset-bottom,0px))}
#modal{backdrop-filter:blur(6px)}
#modal .box{background:linear-gradient(160deg,#171d3d,#0d1124);border-color:rgba(255,255,255,.1);border-radius:22px}
/* login */
@media(prefers-reduced-motion:reduce){.btn::after{animation:none;transition:none}}
@media(min-width:820px){.tabs{position:static;left:auto;right:auto;bottom:auto;width:fit-content;margin:14px max(16px,calc((100% - 1100px)/2 + 16px)) 0;padding:5px;border-radius:16px;background:rgba(13,17,36,.9);box-shadow:none}.tab{flex:none;flex-direction:row;gap:8px;padding:8px 16px;font-size:.9rem}#toast{bottom:24px}}

/* ===== COLOUR GRADING v2 + GUILD ===== */
:root{--a1:#ffc65c;--a2:#27e0a3}
body[data-tab=create]{--a1:#5bd0ff;--a2:#5b7dff}
body[data-tab=guild]{--a1:#b48cff;--a2:#ff6a95}
body[data-tab=consoles]{--a1:#27e0a3;--a2:#5bd0ff}
body::before{background:radial-gradient(720px 440px at 92% -6%,color-mix(in srgb,var(--a2) 22%,transparent),transparent 62%),radial-gradient(640px 420px at -6% 6%,color-mix(in srgb,var(--a1) 16%,transparent),transparent 62%),radial-gradient(800px 560px at 50% 118%,color-mix(in srgb,var(--vio) 12%,transparent),transparent 60%),linear-gradient(180deg,rgba(5,6,15,0),rgba(2,3,8,.55))}
.header::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:linear-gradient(90deg,transparent,var(--a1),var(--a2),var(--vio),transparent);opacity:.85}
.tab.active{background:linear-gradient(135deg,var(--a1),var(--a2));color:#071018;box-shadow:0 8px 22px -8px color-mix(in srgb,var(--a2) 80%,transparent)}
.squad-card::after{content:"";position:absolute;left:18px;right:18px;top:0;height:1px;background:linear-gradient(90deg,transparent,var(--a1),transparent);opacity:.7}
.chip.on{background:linear-gradient(135deg,var(--a1),var(--a2));color:#071018;box-shadow:0 3px 0 color-mix(in srgb,var(--a1) 45%,#000),0 10px 22px -8px color-mix(in srgb,var(--a2) 70%,transparent)}
.stat:nth-child(1){--acc:var(--a1)}.stat:nth-child(2){--acc:var(--blu)}.stat:nth-child(3){--acc:var(--vio)}.stat:nth-child(4){--acc:var(--a2)}
.badge.online,.badge.success{background:linear-gradient(135deg,rgba(39,224,163,.22),rgba(91,208,255,.12));color:#5ff0b8}
.badge.inmatch{background:linear-gradient(135deg,rgba(255,198,92,.24),rgba(255,106,149,.12));color:#ffd27a}
.badge.connecting{background:linear-gradient(135deg,rgba(255,169,77,.24),rgba(255,198,92,.1));color:#ffc88a}
.badge.error,.badge.failed{background:linear-gradient(135deg,rgba(255,93,122,.24),rgba(255,169,77,.1));color:#ff8fa5}
.slot.online .avatar{background:linear-gradient(135deg,rgba(39,224,163,.32),rgba(91,208,255,.15));color:#5ff0b8}
.slot.inmatch .avatar{background:linear-gradient(135deg,rgba(255,198,92,.32),rgba(255,106,149,.15));color:#ffd27a}
.slot.connecting .avatar{background:linear-gradient(135deg,rgba(255,169,77,.3),rgba(255,198,92,.12));color:#ffc88a}
.slot.error .avatar{background:linear-gradient(135deg,rgba(255,93,122,.32),rgba(255,169,77,.12));color:#ff8fa5}
.alert-red{background:linear-gradient(135deg,rgba(255,93,122,.14),rgba(255,169,77,.06))}
.alert-green{background:linear-gradient(135deg,rgba(39,224,163,.14),rgba(91,208,255,.06))}
.alert-info{background:linear-gradient(135deg,rgba(91,157,255,.14),rgba(155,107,255,.06))}
.log-line.success{color:#5ff0b8}.log-line.error{color:#ff8fa5}.log-line.warning{color:#ffd27a}.log-line.info{color:#8fd0ff}
.btn.rose{background:linear-gradient(135deg,#ff9bb0,#ff5d7a 55%,#ff8a3d);color:#3b0615;border-color:rgba(255,255,255,.28);box-shadow:0 1px 0 rgba(255,255,255,.45) inset,0 4px 0 #a3213f,0 14px 26px -10px rgba(255,93,122,.65)}
.btn.load{pointer-events:none;opacity:.8}
.btn.load::before{content:"";width:16px;height:16px;border:2.5px solid currentColor;border-right-color:transparent;border-radius:50%;animation:lgspin .7s linear infinite}
.gh{display:flex;align-items:center;gap:14px;margin-bottom:6px}
.gh .gi{width:50px;height:50px;border-radius:16px;display:grid;place-items:center;flex:none;background:linear-gradient(135deg,#b48cff,#ff6a95);color:#1b0b3d;box-shadow:0 10px 26px -10px rgba(255,106,149,.7)}
.gh .gi svg{width:26px;height:26px}
.gh h3{margin:0}
.gh p{color:var(--mut);font-size:.84rem}
.glbl{display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--mut);margin:14px 0 7px}
.gcount{padding:2px 9px;border-radius:999px;background:rgba(39,224,163,.15);color:var(--grn);letter-spacing:.02em;text-transform:none}
.gcount.warn{background:rgba(255,169,77,.15);color:var(--amb)}
.grow{display:grid;grid-template-columns:minmax(0,1fr) 110px;gap:10px;margin-top:4px}
.grow .glbl{margin-top:8px}
.gta{min-height:170px;resize:vertical;font-family:ui-monospace,Consolas,monospace;font-size:.88rem;line-height:1.6}
.gact{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px}
.gact .btn{height:54px;font-size:.98rem;letter-spacing:.04em}
.gact .btn svg.i{width:20px;height:20px}
.ghint{color:var(--mut);font-size:.78rem;margin-top:12px}
.jobhead{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-bottom:10px}
.jobhead h3{margin:0}
.act{padding:3px 10px;border-radius:999px;font-size:.68rem;font-weight:800;letter-spacing:.12em}
.act.join{background:linear-gradient(135deg,#34f0b0,#0fb98a);color:#022c1f}
.act.leave{background:linear-gradient(135deg,#ff9bb0,#ff5d7a);color:#3b0615}
.prog{height:8px;border-radius:99px;background:rgba(255,255,255,.07);overflow:hidden;margin:2px 0 14px}
.prog i{display:block;height:100%;border-radius:inherit;background:linear-gradient(90deg,#27e0a3,#5bd0ff,#9b6bff);transition:width .4s}
.prog.leave i{background:linear-gradient(90deg,#ff5d7a,#ffa94d)}
.stats.three{grid-template-columns:repeat(3,1fr)}
.guild-item{border-radius:12px;background:rgba(5,6,15,.55)}
.guild-item.ok{border-color:rgba(39,224,163,.5)}
.guild-item.fail{border-color:rgba(255,93,122,.5)}
/* ===== LOGIN v2 : aurora command center ===== */
@property --lxa{syntax:'<angle>';inherits:false;initial-value:0deg}
.lx{position:relative;min-height:100vh;min-height:100dvh;display:grid;place-items:center;padding:max(22px,env(safe-area-inset-top)) 16px max(22px,env(safe-area-inset-bottom));isolation:isolate;transition:opacity .32s ease}
.lx.out{opacity:0}
.lx-bg{position:absolute;inset:0;z-index:-1;pointer-events:none;overflow:hidden;background:radial-gradient(900px 520px at 12% -8%,rgba(155,107,255,.20),transparent 62%),radial-gradient(760px 520px at 100% 108%,rgba(255,170,60,.16),transparent 62%),radial-gradient(560px 380px at 92% 12%,rgba(255,106,149,.10),transparent 60%),#05060f}
.lx-bg::before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.032) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.032) 1px,transparent 1px);background-size:46px 46px;-webkit-mask-image:radial-gradient(ellipse at 50% 45%,#000 20%,transparent 72%);mask-image:radial-gradient(ellipse at 50% 45%,#000 20%,transparent 72%)}
.lx-bg::after{content:"";position:absolute;inset:0;background-image:radial-gradient(1.2px 1.2px at 12% 22%,rgba(255,255,255,.55),transparent),radial-gradient(1px 1px at 78% 14%,rgba(255,224,138,.6),transparent),radial-gradient(1px 1px at 34% 72%,rgba(255,255,255,.4),transparent),radial-gradient(1.4px 1.4px at 88% 64%,rgba(155,107,255,.7),transparent),radial-gradient(1px 1px at 58% 38%,rgba(39,224,163,.55),transparent),radial-gradient(1px 1px at 6% 84%,rgba(255,255,255,.4),transparent);background-size:340px 300px}
.lx-orb{position:absolute;border-radius:50%;pointer-events:none;will-change:transform;animation:lxfloat 18s ease-in-out infinite}
.lx-o1{width:460px;height:460px;top:-150px;left:-130px;background:radial-gradient(circle,rgba(124,92,255,.46),transparent 66%)}
.lx-o2{width:420px;height:420px;bottom:-150px;right:-110px;background:radial-gradient(circle,rgba(245,165,36,.38),transparent 66%);animation-delay:-6s}
.lx-o3{width:320px;height:320px;top:46%;left:60%;background:radial-gradient(circle,rgba(39,224,163,.22),transparent 66%);animation-delay:-11s}
.lx-shell{position:relative;width:100%;max-width:1080px;display:grid;grid-template-columns:minmax(0,1fr);gap:22px;justify-items:center}

/* hero + live preview (desktop only) */
.lx-hero{display:none}
.lx-pill{display:inline-flex;align-items:center;gap:8px;padding:6px 13px 6px 10px;border-radius:999px;font-size:.8rem;font-weight:700;color:#ffe08a;background:rgba(255,198,92,.08);border:1px solid rgba(255,198,92,.3);margin-bottom:20px}
.lx-pill i{width:8px;height:8px;border-radius:50%;background:var(--gold);box-shadow:0 0 12px var(--gold)}
.lx-hero h1{font-family:var(--disp);font-size:clamp(2.2rem,4vw,3rem);line-height:1.1;text-wrap:balance;font-weight:800;letter-spacing:-.02em;margin-bottom:16px;background:linear-gradient(100deg,#fff 18%,#ffe08a 58%,#ff9ec0);-webkit-background-clip:text;background-clip:text;color:transparent}
.lx-hero>p{color:var(--mut);max-width:44ch;margin-bottom:26px;font-size:1rem;line-height:1.6}
.lx-pv{position:relative;max-width:480px;padding:16px;border-radius:22px;background:linear-gradient(160deg,rgba(22,27,56,.78),rgba(8,10,24,.86));border:1px solid rgba(255,255,255,.09);box-shadow:0 30px 60px -34px rgba(0,0,0,.95),0 0 0 1px rgba(155,107,255,.06)}
.lx-pv-top{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}
.lx-pv-top b{font-family:var(--disp);font-size:1rem;letter-spacing:.01em}
.lx-st{display:inline-flex;align-items:center;gap:6px;padding:3px 10px;border-radius:999px;font-size:.74rem;font-weight:700;background:rgba(39,224,163,.14);color:var(--grn)}
.lx-st i{width:7px;height:7px;border-radius:50%;background:currentColor;animation:pulse 1.8s ease-out infinite}
.lx-slots{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.lx-slot{display:flex;align-items:center;gap:10px;min-width:0;padding:10px;border-radius:14px;background:rgba(5,6,15,.6);border:1px solid rgba(255,255,255,.06)}
.lx-slot em{width:34px;height:34px;flex:none;border-radius:50%;display:grid;place-items:center;font-style:normal;font-weight:800;font-size:.88rem;color:var(--c);background:color-mix(in srgb,var(--c) 14%,transparent);box-shadow:0 0 0 1.5px color-mix(in srgb,var(--c) 55%,transparent)}
.lx-slot div{min-width:0}
.lx-slot b{display:block;font-size:.84rem;font-weight:700;line-height:1.2}
.lx-slot small{display:block;font-size:.72rem;color:var(--mut)}
.lx-slot.on{--c:var(--grn)}.lx-slot.mt{--c:var(--gold)}.lx-slot.cn{--c:var(--amb)}
.lx-slot.em{--c:#5b6288;border-style:dashed;background:transparent}
.lx-bar{height:6px;border-radius:99px;background:rgba(255,255,255,.07);overflow:hidden;margin:12px 0}
.lx-bar i{display:block;height:100%;width:72%;border-radius:inherit;background:linear-gradient(90deg,#27e0a3,#5bd0ff,#9b6bff);transform-origin:left;animation:lxgrow 1.4s .3s cubic-bezier(.2,.8,.2,1) both}
.lx-con{padding:10px 12px;border-radius:12px;background:#04050c;border:1px solid rgba(255,255,255,.06);font-family:ui-monospace,'Cascadia Mono',Consolas,monospace;font-size:.74rem;line-height:1.75;min-height:96px}
.lx-con p{opacity:0;transform:translateY(4px);animation:lxline .45s ease forwards;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lx-con p:nth-child(1){animation-delay:.7s}.lx-con p:nth-child(2){animation-delay:1.3s}.lx-con p:nth-child(3){animation-delay:1.9s}.lx-con p:nth-child(4){animation-delay:2.5s}
.lx-con span{color:#5b6a8c;margin-right:8px}
.lx-con .g{color:#5fe3ae}.lx-con .y{color:#f5c26b}.lx-con .b{color:#9cc7ff}
.lx-con u{display:inline-block;width:7px;height:13px;margin-left:3px;vertical-align:-2px;background:var(--gold);text-decoration:none;animation:lxcaret 1s steps(1) infinite 3s}

/* sign-in card */
.lx-card{position:relative;width:100%;max-width:410px;padding:34px 28px 20px;border-radius:30px;background:linear-gradient(162deg,rgba(26,32,66,.8),rgba(7,9,22,.93));-webkit-backdrop-filter:blur(22px);backdrop-filter:blur(22px);box-shadow:0 40px 90px -30px rgba(0,0,0,.95),0 0 80px -26px rgba(155,107,255,.6),0 1px 0 rgba(255,255,255,.07) inset;animation:lxrise .7s cubic-bezier(.2,.8,.2,1) both}
.lx-card::before{content:"";position:absolute;inset:0;border-radius:inherit;padding:1.5px;pointer-events:none;background:conic-gradient(from var(--lxa),rgba(255,198,92,.95),rgba(255,106,149,.7) 17%,rgba(155,107,255,.9) 35%,rgba(91,208,255,.5) 52%,rgba(39,224,163,.85) 68%,rgba(255,198,92,.06) 84%,rgba(255,198,92,.95));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;animation:lxspin 9s linear infinite}
.lx-card.shake{animation:lxshake .45s}
.lx-emb{width:78px;height:78px;margin:0 auto 16px;display:grid;place-items:center;border-radius:26px;background:linear-gradient(145deg,rgba(255,198,92,.22),rgba(124,92,255,.22));border:1px solid rgba(255,255,255,.14);box-shadow:0 0 46px -8px rgba(255,198,92,.55),0 1px 0 rgba(255,255,255,.18) inset}
.lx-emb .mark{width:48px;height:48px}
.lx-title{text-align:center;font-family:var(--disp);font-weight:800;font-size:1.55rem;letter-spacing:.14em;background:linear-gradient(100deg,#fff 0%,#ffe08a 42%,#ff9ec0 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.lx-badge{display:flex;width:fit-content;align-items:center;gap:6px;margin:11px auto 0;padding:4px 12px 4px 9px;border-radius:999px;font-size:.72rem;font-weight:800;letter-spacing:.04em;background:linear-gradient(135deg,#ffe9a8,#f5a524);color:#3a2300}
.lx-badge svg{width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.lx-sub{text-align:center;color:var(--mut);font-size:.9rem;line-height:1.5;margin:14px 0 24px}
.lx-lbl{display:block;font-size:.8rem;font-weight:700;color:#aeb5d6;margin-bottom:8px}
.lx-field{position:relative;border-radius:17px;transition:box-shadow .2s}
.lx-field input{height:56px;padding:0 54px 0 50px;border-radius:17px;background:rgba(4,5,13,.8);border:1px solid rgba(255,255,255,.1);font-size:1rem;letter-spacing:.02em}
.lx-field input::placeholder{color:#5f6890;letter-spacing:0}
.lx-field input:focus{border-color:var(--gold);box-shadow:none}
.lx-field:focus-within{box-shadow:0 0 0 4px rgba(255,198,92,.14),0 12px 30px -14px rgba(255,198,92,.5)}
.lx-ic{position:absolute;left:16px;top:50%;margin-top:-11px;color:var(--mut);pointer-events:none;transition:color .2s}
.lx-field:focus-within .lx-ic{color:var(--gold)}
.lx-field.bad input{border-color:rgba(255,93,122,.75)}
.lx-field.bad{box-shadow:0 0 0 4px rgba(255,93,122,.12)}
.lx-field.bad .lx-ic{color:#ff8fa5}
.lx-eye{position:absolute;right:7px;top:50%;margin-top:-21px;width:42px;height:42px;display:grid;place-items:center;border-radius:12px;border:0;background:transparent;color:var(--mut);cursor:pointer;transition:background .15s,color .15s}
.lx-eye:hover{color:var(--gold);background:rgba(255,198,92,.08)}
.lx-eye .off{display:none}
.lx-eye.on .off{display:block}.lx-eye.on .see{display:none}
.lx-note{display:none;align-items:flex-start;gap:9px;margin-top:12px;padding:10px 12px;border-radius:13px;font-size:.84rem;font-weight:600;line-height:1.4}
.lx-note svg{width:18px;height:18px;flex:none;margin-top:1px}
.lx-note.show{display:flex}
.lx-note.caps{background:rgba(255,169,77,.1);border:1px solid rgba(255,169,77,.4);color:#ffc88a}
.lx-note.err{background:rgba(255,93,122,.1);border:1px solid rgba(255,93,122,.45);color:#ffa3b5}
.lx-rem{display:flex;align-items:center;gap:12px;margin-top:16px;cursor:pointer;user-select:none;font-size:.86rem;font-weight:600;color:#aeb5d6}
.lx-rem input{position:absolute;opacity:0;width:1px;height:1px;padding:0;border:0}
.lx-sw{position:relative;width:42px;height:24px;flex:none;border-radius:99px;background:#1b2142;border:1px solid rgba(255,255,255,.12);transition:background .2s,border-color .2s}
.lx-sw::after{content:"";position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:#8c94ba;transition:transform .22s cubic-bezier(.3,1.4,.5,1),background .2s}
.lx-rem input:checked+.lx-sw{background:linear-gradient(135deg,#34f0b0,#0fb98a);border-color:transparent}
.lx-rem input:checked+.lx-sw::after{transform:translateX(18px);background:#fff}
.lx-rem input:focus-visible+.lx-sw{outline:2px solid var(--gold);outline-offset:3px}
.lx-go{position:relative;overflow:hidden;isolation:isolate;display:block;width:100%;height:58px;margin-top:20px;border:1px solid rgba(255,255,255,.3);border-radius:17px;cursor:pointer;font-family:var(--disp);font-weight:800;font-size:1.02rem;letter-spacing:.05em;color:#3a2300;background:linear-gradient(135deg,#ffe9a8 0%,#ffc65c 40%,#ff9d4d 100%);box-shadow:0 1px 0 rgba(255,255,255,.55) inset,0 4px 0 #a86a0a,0 18px 34px -12px rgba(255,160,50,.7);transition:transform .15s,box-shadow .2s,filter .2s,background .3s}
.lx-go::after{content:"";position:absolute;z-index:-1;top:0;bottom:0;left:-70%;width:45%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.5),transparent);transform:skewX(-20deg);transition:left .65s}
.lx-go:hover{filter:brightness(1.06)}
.lx-go:hover::after{left:130%}
.lx-go:active{transform:translateY(3px);box-shadow:0 1px 0 rgba(255,255,255,.55) inset,0 1px 0 #a86a0a,0 8px 16px -10px rgba(255,160,50,.7)}
.lx-go-in{display:flex;align-items:center;justify-content:center;gap:10px;height:100%}
.lx-go svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2.1;stroke-linecap:round;stroke-linejoin:round}
.lx-go .i-spin,.lx-go .i-ok{display:none}
.lx-go.load{pointer-events:none;filter:saturate(.85)}
.lx-go.load .i-open,.lx-go.ok .i-open,.lx-go.cool .i-open{display:none}
.lx-go.load .i-spin{display:block;animation:lgspin .7s linear infinite}
.lx-go.ok{pointer-events:none;color:#022c1f;background:linear-gradient(135deg,#7bffd0,#27e0a3 45%,#0fb98a);box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 4px 0 #087a5c,0 18px 34px -12px rgba(39,224,163,.7)}
.lx-go.ok .i-ok{display:block}
.lx-go.cool{pointer-events:none;color:#8c94ba;background:linear-gradient(180deg,#1c2243,#131833);border-color:rgba(255,255,255,.1);box-shadow:0 4px 0 rgba(0,0,0,.4)}
.lx-foot{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:20px;padding-top:14px;border-top:1px solid rgba(255,255,255,.07)}
.lx-ping{display:inline-flex;align-items:center;gap:8px;padding:6px 11px 6px 9px;border-radius:999px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.03);font-size:.76rem;color:var(--mut);cursor:pointer;transition:border-color .2s,background .2s}
.lx-ping:hover{border-color:rgba(255,255,255,.22)}
.lx-ping i{width:8px;height:8px;border-radius:50%;background:#6b7398;transition:background .2s,box-shadow .2s}
.lx-ping b{font-weight:700;color:#c3c9e6}
.lx-ping em{font-style:normal;font-variant-numeric:tabular-nums}
.lx-ping em:empty{display:none}
.lx-ping.ok i{background:var(--grn);box-shadow:0 0 10px var(--grn)}
.lx-ping.bad{border-color:rgba(255,93,122,.5);background:rgba(255,93,122,.08)}
.lx-ping.bad i{background:var(--red);box-shadow:0 0 10px var(--red)}
.lx-ping.bad b{color:#ffa3b5}
.lx-ver{font-size:.74rem;color:#5f6890;font-variant-numeric:tabular-nums}
@keyframes lxfloat{0%,100%{transform:translate3d(0,0,0)}50%{transform:translate3d(28px,-34px,0)}}
@keyframes lxspin{to{--lxa:360deg}}
@keyframes lxrise{from{opacity:0;transform:translateY(16px) scale(.985)}to{opacity:1;transform:none}}
@keyframes lxshake{0%,100%{transform:translateX(0)}20%{transform:translateX(-9px)}40%{transform:translateX(8px)}60%{transform:translateX(-6px)}80%{transform:translateX(4px)}}
@keyframes lxline{to{opacity:1;transform:none}}
@keyframes lxgrow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes lxcaret{50%{opacity:0}}
@keyframes lgspin{to{transform:rotate(360deg)}}
@media(min-width:940px){.lx-shell{grid-template-columns:minmax(0,1fr) 410px;gap:76px;align-items:center}.lx-hero{display:block;justify-self:start}}
@media(max-width:400px){.lx-card{padding:28px 20px 16px;border-radius:26px}.lx-title{font-size:1.35rem;letter-spacing:.1em}.lx-emb{width:68px;height:68px;border-radius:22px}.lx-emb .mark{width:42px;height:42px}}
@media(max-height:640px){.lx{place-items:start center}.lx-emb{width:54px;height:54px;margin-bottom:10px;border-radius:18px}.lx-emb .mark{width:34px;height:34px}.lx-sub{margin:10px 0 16px}}
@media(prefers-reduced-motion:reduce){.lx-orb,.lx-card,.lx-card::before,.lx-card.shake,.lx-bar i,.lx-st i,.lx-con u{animation:none}.lx-con p{opacity:1;transform:none;animation:none}.lx-go::after{transition:none}}
.lx-con i{font-style:normal}
</style>
</head>
<body>
<div id="app"></div>
<div id="toast"></div>
<div id="modal"><div class="box"><p id="modalMsg"></p><div class="row"><button class="btn green" id="modalYes">Confirm</button><button class="btn" id="modalNo">Cancel</button></div></div></div>
<script>
const API = window.location.origin;
let adminToken = tokGet();
let currentTab = 'dashboard';
let pollTimer = null;
let currentConsoleSquad = null;
let lastDashHtml = '';
let busy = false;
let toastTimer = null;

function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}

function toast(msg, kind) {
  const t = document.getElementById('toast'); if (!t) return;
  t.textContent = msg; t.className = kind || ''; t.style.display = 'block';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { t.style.display = 'none'; }, kind === 'err' ? 5000 : 2500);
}
// native alert()/confirm() are silently blocked in many mobile browsers/webviews -> use our own
window.alert = function(m) { m = String(m); toast(m.replace(/\n/g, ' '), m.indexOf('✅') === 0 ? 'ok' : 'err'); };
function askConfirm(msg) {
  return new Promise(res => {
    const m = document.getElementById('modal');
    document.getElementById('modalMsg').textContent = msg;
    m.style.display = 'flex';
    const done = v => { m.style.display = 'none'; res(v); };
    document.getElementById('modalYes').onclick = () => done(true);
    document.getElementById('modalNo').onclick = () => done(false);
  });
}
function handleUnauthorized() {
  tokClear(); adminToken = '';
  if (pollTimer) clearInterval(pollTimer);
  renderLogin();
}

async function api(path, opts={}) {
  opts.headers = opts.headers || {};
  if (adminToken) opts.headers['X-Session-Token'] = adminToken;
  if (opts.body && typeof opts.body !== 'string') { opts.body = JSON.stringify(opts.body); opts.headers['Content-Type']='application/json'; }
  const ctl = new AbortController();
  const to = setTimeout(() => ctl.abort(), 30000);
  opts.signal = ctl.signal;
  try {
    const r = await fetch(API+path, opts);
    if (r.status === 401) { handleUnauthorized(); return {ok:false, error:'Unauthorized'}; }
    return await r.json();
  } catch(e) { return {ok:false, error: (e && e.name === 'AbortError') ? 'timeout' : 'network error'}; }
  finally { clearTimeout(to); }
}

const MARK = '<svg class="mark" viewBox="0 0 32 32"><defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe08a"/><stop offset=".55" stop-color="#f5a524"/><stop offset="1" stop-color="#ff6a95"/></linearGradient></defs><path d="M16 2l11 4v9c0 7-4.6 12.4-11 15C9.6 27.4 5 22 5 15V6z" fill="url(#mg)"/><path d="M10.5 10.5L16 17l5.5-6.5M16 17v6" stroke="#1a1030" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>';
const IC = {
  dash:'<svg class="i" viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>',
  add:'<svg class="i" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/></svg>',
  guild:'<svg class="i" viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 4.5-3.2 8-8 9-4.8-1-8-4.5-8-9V6z"/></svg>',
  term:'<svg class="i" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 9l3 3-3 3M13 15h4"/></svg>',
  out:'<svg class="i" viewBox="0 0 24 24"><path d="M9 4H5a2 2 0 00-2 2v12a2 2 0 002 2h4M16 8l4 4-4 4M20 12H9"/></svg>',
  join:'<svg class="i" viewBox="0 0 24 24"><path d="M15 4h4a2 2 0 012 2v12a2 2 0 01-2 2h-4M10 8l4 4-4 4M14 12H3"/></svg>'
};

/* ---- token storage: "keep me signed in" = localStorage, otherwise this tab only ---- */
function tokGet() { try { return localStorage.getItem('fglory_token') || sessionStorage.getItem('fglory_token') || ''; } catch (e) { return ''; } }
function tokSave(t, keep) { try { localStorage.removeItem('fglory_token'); sessionStorage.removeItem('fglory_token'); (keep ? localStorage : sessionStorage).setItem('fglory_token', t); } catch (e) {} }
function tokClear() { try { localStorage.removeItem('fglory_token'); sessionStorage.removeItem('fglory_token'); } catch (e) {} }

let lxBusy = false, lxCool = null;

function renderLogin() {
  document.body.removeAttribute('data-tab');
  lxBusy = false; clearInterval(lxCool);
  document.getElementById('app').innerHTML = `
    <div class="lx" id="lxRoot">
      <div class="lx-bg"><i class="lx-orb lx-o1"></i><i class="lx-orb lx-o2"></i><i class="lx-orb lx-o3"></i></div>
      <div class="lx-shell">
        <div class="lx-hero">
          <span class="lx-pill"><i></i>Premium control panel</span>
          <h1>Every squad,<br>one command center.</h1>
          <p>Start, stop and watch your squads and guild groups live, from your phone or your desktop.</p>
          <div class="lx-pv" aria-hidden="true">
            <div class="lx-pv-top"><b>Squad 1</b><span class="lx-st"><i></i>Running</span></div>
            <div class="lx-slots">
              <div class="lx-slot on"><em>1</em><div><b>Online</b><small>Ready</small></div></div>
              <div class="lx-slot mt"><em>2</em><div><b>In match</b><small>Playing now</small></div></div>
              <div class="lx-slot cn"><em>3</em><div><b>Connecting</b><small>Signing in</small></div></div>
              <div class="lx-slot em"><em>4</em><div><b>Empty slot</b><small>Add an account</small></div></div>
            </div>
            <div class="lx-bar"><i></i></div>
            <div class="lx-con">
              <p><span>09:41:02</span><i class="g">Squad 1 started</i></p>
              <p><span>09:41:04</span><i class="g">Slot 1 connected</i></p>
              <p><span>09:41:07</span><i class="y">Slot 3 reconnecting</i></p>
              <p><span>09:41:09</span><i class="b">Match found, joining<u></u></i></p>
            </div>
          </div>
        </div>
        <form class="lx-card" id="lxCard" onsubmit="return doLogin(event)" novalidate>
          <div class="lx-emb">${MARK}</div>
          <h2 class="lx-title">YOUBIN SAMIUL</h2>
          <div class="lx-badge"><svg viewBox="0 0 24 24"><path d="M6 4h12l4 6-10 11L2 10z"/><path d="M2 10h20M9 4l-2 6 5 11 5-11-2-6"/></svg>Premium access</div>
          <p class="lx-sub">Enter the panel password to manage your squads and guild groups.</p>
          <label class="lx-lbl" for="pw">Panel password</label>
          <div class="lx-field" id="lxField">
            <svg class="i lx-ic" viewBox="0 0 24 24"><rect x="4" y="10" width="16" height="10" rx="2.5"/><path d="M8 10V7a4 4 0 018 0v3"/></svg>
            <input type="password" id="pw" name="password" placeholder="Enter password" autocomplete="current-password" autocapitalize="off" autocorrect="off" spellcheck="false" enterkeyhint="go" oninput="lxTyping()" onkeydown="capsCheck(event)" onkeyup="capsCheck(event)">
            <button type="button" class="lx-eye" id="lxEye" onclick="togglePw()" aria-label="Show password" aria-pressed="false">
              <svg class="i see" viewBox="0 0 24 24"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>
              <svg class="i off" viewBox="0 0 24 24"><path d="M3 3l18 18M10.6 5.1A10 10 0 0112 5c6.4 0 10 7 10 7a17 17 0 01-3.2 4M6.5 6.6C3.7 8.3 2 12 2 12s3.6 7 10 7c1.7 0 3.2-.4 4.5-1M9.9 9.9a3 3 0 004.2 4.2"/></svg>
            </button>
          </div>
          <div class="lx-note caps" id="lxCaps"><svg class="i" viewBox="0 0 24 24"><path d="M12 3l8 9h-5v6H9v-6H4zM9 21h6"/></svg><span>Caps Lock is on. Passwords are case sensitive.</span></div>
          <div class="lx-note err" id="lxErr" role="alert" aria-live="assertive"><svg class="i" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16.5v.5"/></svg><span id="lxErrTx"></span></div>
          <label class="lx-rem"><input type="checkbox" id="lxRem" checked><span class="lx-sw"></span><span>Keep me signed in on this device</span></label>
          <button type="submit" class="lx-go" id="goBtn"><span class="lx-go-in">
            <svg class="i-open" viewBox="0 0 24 24"><rect x="4" y="10" width="16" height="10" rx="2.5"/><path d="M8 10V7a4 4 0 017.5-2"/></svg>
            <svg class="i-spin" viewBox="0 0 24 24"><path d="M12 3a9 9 0 109 9" opacity=".9"/></svg>
            <svg class="i-ok" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>
            <span class="tx">Open panel</span></span></button>
          <div class="lx-foot">
            <button type="button" class="lx-ping" id="lxPing" onclick="pingServer()" aria-live="polite"><i></i><b>Checking server</b><em></em></button>
            <span class="lx-ver">v5.1</span>
          </div>
        </form>
      </div>
    </div>`;
  if (!(window.matchMedia && matchMedia('(pointer:coarse)').matches)) {
    setTimeout(() => { const p = document.getElementById('pw'); if (p) p.focus({preventScroll:true}); }, 120);
  }
  pingServer();
}

function togglePw() {
  const p = document.getElementById('pw'), b = document.getElementById('lxEye'); if (!p) return;
  const show = p.type === 'password';
  p.type = show ? 'text' : 'password';
  if (b) { b.classList.toggle('on', show); b.setAttribute('aria-pressed', show ? 'true' : 'false'); b.setAttribute('aria-label', show ? 'Hide password' : 'Show password'); }
  p.focus({preventScroll:true});
}
function capsCheck(e) { const c = document.getElementById('lxCaps'); if (c && e && e.getModifierState) c.classList.toggle('show', e.getModifierState('CapsLock')); }
function lxClearErr() {
  const err = document.getElementById('lxErr'), f = document.getElementById('lxField'), pw = document.getElementById('pw');
  if (err) err.classList.remove('show'); if (f) f.classList.remove('bad'); if (pw) pw.removeAttribute('aria-invalid');
}
function lxTyping() { lxClearErr(); }
function lxBtn(state, text) {
  const b = document.getElementById('goBtn'); if (!b) return;
  b.className = 'lx-go' + (state ? ' ' + state : '');
  b.disabled = (state === 'load' || state === 'ok' || state === 'cool');
  const t = b.querySelector('.tx'); if (t && text) t.textContent = text;
}
function loginFail(msg) {
  const err = document.getElementById('lxErr'), tx = document.getElementById('lxErrTx'), card = document.getElementById('lxCard'),
        f = document.getElementById('lxField'), pw = document.getElementById('pw');
  if (tx) tx.textContent = msg;
  if (err) err.classList.add('show');
  if (f) f.classList.add('bad');
  if (pw) { pw.setAttribute('aria-invalid', 'true'); pw.select(); }
  if (card) { card.classList.remove('shake'); void card.offsetWidth; card.classList.add('shake'); }
}
function lxCooldown(sec) {
  clearInterval(lxCool);
  let n = sec;
  const tick = () => {
    if (!document.getElementById('goBtn')) { clearInterval(lxCool); return; }
    if (n <= 0) { clearInterval(lxCool); lxBtn('', 'Open panel'); return; }
    lxBtn('cool', 'Try again in ' + n + 's'); n--;
  };
  tick(); lxCool = setInterval(tick, 1000);
}

async function pingServer() {
  const set = (cls, txt, sub) => {
    const n = document.getElementById('lxPing'); if (!n) return;
    n.className = 'lx-ping' + (cls ? ' ' + cls : '');
    n.querySelector('b').textContent = txt; n.querySelector('em').textContent = sub || '';
  };
  if (!document.getElementById('lxPing')) return;
  set('', 'Checking server', '');
  const t0 = performance.now(), ctl = new AbortController(), to = setTimeout(() => ctl.abort(), 7000);
  try {
    const r = await fetch(API + '/api/config', {cache:'no-store', signal: ctl.signal});
    if (!r.ok) throw new Error('bad status');
    set('ok', 'Server online', Math.round(performance.now() - t0) + ' ms');
  } catch (e) {
    set('bad', 'Server unreachable', 'Tap to retry');
  } finally { clearTimeout(to); }
}

async function doLogin(e) {
  if (e && e.preventDefault) e.preventDefault();
  const pw = document.getElementById('pw');
  if (!pw || lxBusy) return false;
  lxClearErr();
  if (!pw.value) { loginFail('Enter the panel password to continue.'); pw.focus(); return false; }
  lxBusy = true; lxBtn('load', 'Checking password');
  const r = await api('/api/login', {method:'POST', body:{password: pw.value}});
  if (!document.getElementById('goBtn')) { lxBusy = false; return false; }
  if (r && r.ok && r.token) {
    adminToken = r.token;
    const rem = document.getElementById('lxRem');
    tokSave(adminToken, !rem || rem.checked);
    lxBtn('ok', 'Access granted');
    setTimeout(() => { const root = document.getElementById('lxRoot'); if (root) root.classList.add('out'); setTimeout(renderMain, 320); }, 480);
    return false;
  }
  lxBusy = false; lxBtn('', 'Open panel');
  const er = (r && r.error) || 'error';
  if (er === 'network error' || er === 'timeout') { loginFail('Cannot reach the server. Check your connection and try again.'); pingServer(); }
  else if (er === 'Wrong password' || er === 'invalid_credentials') loginFail('That password is not correct. Check it and try again.');
  else if (er === 'rate_limited') { loginFail('Too many attempts. Wait a few minutes before trying again.'); lxCooldown(20); }
  else if (er === 'disabled') loginFail('This account is disabled. Contact the panel owner.');
  else loginFail('Sign-in failed: ' + er);
  return false;
}

function renderMain() {
  document.body.setAttribute('data-tab', currentTab);
  lastDashHtml = '';
  const tabs = [['dashboard','dash','Dashboard'],['create','add','New squad'],['guild','guild','Guild'],['consoles','term','Consoles']];
  document.getElementById('app').innerHTML = `
    <div class="header">
      <div class="brand">${MARK}<div><b>YOUBIN SAMIUL<em class="prem">PREMIUM</em></b><span>Premium squad and guild control · v5.1</span></div></div>
      <button class="iconbtn" title="Sign out" onclick="logout()">${IC.out}</button>
    </div>
    <div class="tabs">${tabs.map(([k, ic, l]) => `<div class="tab ${currentTab===k?'active':''}" onclick="switchTab('${k}')">${IC[ic]}<span>${l}</span></div>`).join('')}</div>
    <div class="content" id="content"></div>`;
  if (pollTimer) clearInterval(pollTimer);
  if (currentTab==='dashboard') { renderDashboard(); pollTimer = setInterval(renderDashboard, 2000); }
  else if (currentTab==='create') { renderCreate(); }
  else if (currentTab==='guild') { renderGuild(); pollTimer = setInterval(refreshGuild, 1500); }
  else if (currentTab==='consoles') { renderConsoles(); pollTimer = setInterval(refreshConsoles, 2000); }
}

function switchTab(t){ currentTab=t; renderMain(); }

function commitDash(c, html) {
  // only touch the DOM when something really changed -> buttons are not destroyed under the finger
  if (html !== lastDashHtml || !c.firstChild) { c.innerHTML = html; lastDashHtml = html; }
}

const stLabel = s => { s = String(s || 'STOPPED'); return s.charAt(0) + s.slice(1).toLowerCase().replace('_', ' '); };

async function renderDashboard(force) {
  const d = await api('/api/status');
  if (!d.ok || currentTab !== 'dashboard') return;
  if (force !== true && busy) return;
  const c = document.getElementById('content');
  if (!c) return;
  const failed = d.failed_uids || [];
  let html = `<div class="stats">
    <div class="stat"><div class="num">${d.total_squads}</div><div class="lbl">Squads</div></div>
    <div class="stat"><div class="num">${d.total_accounts}</div><div class="lbl">Accounts</div></div>
    <div class="stat"><div class="num">${d.total_matches}</div><div class="lbl">Matches played</div></div>
    <div class="stat"><div class="num">${d.active_workers}</div><div class="lbl">Workers running</div></div></div>`;
  if (failed.length) html += `<div class="alert-red"><b>${failed.length} account(s) failed the guild request:</b> ${failed.map(esc).join(', ')}. Try again with a new ID.</div>`;
  if (!d.squads || d.squads.length === 0) {
    html += `<div class="squad-card empty"><b>No squads yet</b><p>Create as many separate squads as needed; each squad holds up to four unique UIDs.</p><button class="btn gold" onclick="switchTab('create')">Create a squad</button></div>`;
    commitDash(c, html);
    return;
  }
  for (const s of d.squads) {
    const run = s.is_started;
    const online = s.members.filter(m => ['ONLINE', 'IN_MATCH'].includes((m.status || '').toUpperCase())).length;
    let slots = '';
    for (let i = 0; i < 4; i++) {
      const m = s.members[i];
      if (!m) { slots += `<div class="slot">Open slot ${i + 1}</div>`; continue; }
      const st = (m.status || 'STOPPED').toUpperCase();
      const cls = st==='ONLINE'?'online':st==='IN_MATCH'?'inmatch':st==='ERROR'?'error':st==='CONNECTING'?'connecting':'stopped';
      const gst = (m.guild_status || '—').toUpperCase();
      const gcls = gst==='SUCCESS'?'success':gst==='FAILED'?'failed':'pending';
      slots += `<div class="slot filled ${cls}">
        <div class="avatar">${i + 1}</div>
        <div class="s-main"><div class="s-name">${esc(m.nickname || '?')}</div><div class="s-sub">UID ${esc(m.uid)}</div><div class="s-sub">Lv ${m.level || 1} · ${m.matches || 0} matches</div>
          <div class="s-badges"><span class="badge ${cls}">${esc(stLabel(st))}</span>${gst !== '—' ? `<span class="badge ${gcls}">Guild ${esc(stLabel(gst))}</span>` : ''}</div></div>
        <button class="x" title="Remove from squad" onclick="removeMember(${s.id}, '${esc(m.uid)}')">✕</button></div>`;
    }
    const actions = run
      ? `<button class="btn small violet" onclick="restartSquad(${s.id})">↻ Restart</button><button class="btn small red" onclick="stopSquad(${s.id})">■ Stop</button>`
      : `<button class="btn small green" onclick="startSquad(${s.id})">▶ Start</button>`;
    html += `<section class="squad-card ${run ? 'run' : ''}">
      <div class="sq-head">
        <div class="sq-title"><h3>Squad ${s.id}</h3><span class="pill ${run ? 'run' : ''}"><i></i>${run ? 'Running' : 'Stopped'}</span><span class="sq-meta">${online}/${s.members.length} online</span></div>
        <div class="sq-actions">${actions}<button class="btn small ghost" onclick="deleteSquad(${s.id})">Delete</button></div>
      </div>
      <div class="squad-slots">${slots}</div></section>`;
  }
  commitDash(c, html);
}

function renderCreate() {
  document.getElementById('content').innerHTML = `
    <div class="squad-card">
      <h3>New squad</h3>
      <p style="color:var(--mut);font-size:.88rem;margin-bottom:12px;">একটি squad-এর জন্য সর্বোচ্চ ৪টি unique UID/password দাও — প্রতি লাইনে একটি করে <code>UID:Password</code>। আলাদা squad তৈরি করতে আবার এই পেজ ব্যবহার করো।</p>
      <div class="member-input"><textarea id="bulkAccounts" placeholder="123456789:password1&#10;987654321:password2"></textarea></div>
      <button class="btn green" style="width:100%;padding:13px;margin-top:6px;" onclick="createSquad()">Create squad</button>
    </div>`;
}

async function createSquad() {
  const raw = document.getElementById('bulkAccounts').value.trim();
  const members = [];
  const invalid = [];
  for (const [idx, line] of raw.split(/\r?\n/).map(x => x.trim()).filter(Boolean).entries()) {
    const sep = line.indexOf(':');
    if (sep <= 0 || sep === line.length - 1) { invalid.push(idx + 1); continue; }
    const uid = line.slice(0, sep).trim();
    const pw = line.slice(sep + 1).trim();
    if (uid && pw) members.push({uid, password:pw}); else invalid.push(idx + 1);
  }
  if (members.length === 0) return alert('অন্তত ১টি UID:Password দাও');
  if (members.length > 4) return alert('একটি squad-এ সর্বোচ্চ ৪টি UID:Password দেওয়া যাবে');
  if (invalid.length) return alert('ভুল ফরম্যাটের লাইন: ' + invalid.join(', ') + '\nসঠিক ফরম্যাট: UID:Password');
  const r = await api('/api/squad/create', {method:'POST', body:{members}});
  if (!r.ok) return alert('Error: '+r.error);
  alert('✅ Squad '+r.squad_id+' তৈরি হয়েছে! Start করতে Dashboard এ যাও।');
  switchTab('dashboard');
}

async function squadAction(path, body, o) {
  if (busy) { toast('⏳ আগের কাজ চলছে, একটু অপেক্ষা করো'); return; }
  if (o.confirm && !(await askConfirm(o.confirm))) return;
  busy = true;
  toast(o.pending);
  const r = await api(path, {method:'POST', body});
  busy = false;
  if (r.ok) toast(o.done, 'ok'); else toast('❌ ' + (r.error || 'failed'), 'err');
  if (currentTab === 'dashboard') renderDashboard(true);
}

function startSquad(sid) {
  return squadAction('/api/squad/start', {squad_id:sid}, {pending:'⏳ Squad '+sid+' starting...', done:'▶️ Squad '+sid+' started'});
}
function restartSquad(sid) {
  return squadAction('/api/squad/restart', {squad_id:sid}, {confirm:'Restart Squad '+sid+'?', pending:'⏳ Squad '+sid+' restarting...', done:'🔄 Squad '+sid+' restarted'});
}
function stopSquad(sid) {
  return squadAction('/api/squad/stop', {squad_id:sid}, {confirm:'Stop Squad '+sid+'?', pending:'⏳ Squad '+sid+' stopping...', done:'⏹ Squad '+sid+' stopped'});
}
function deleteSquad(sid) {
  return squadAction('/api/squad/delete', {squad_id:sid}, {confirm:'Delete Squad '+sid+'? This will remove all members.', pending:'⏳ Deleting...', done:'🗑️ Squad '+sid+' deleted'});
}
function removeMember(sid, uid) {
  return squadAction('/api/squad/remove', {squad_id:sid, uid}, {confirm:'Remove '+uid+' from Squad '+sid+'?', pending:'⏳ Removing...', done:'🗑️ '+uid+' removed'});
}

let guildGroupCount = 3;
let activeGuildGroup = 1;
let lastGuildHtml = '';
let lastJobs = [];
let guildBusy = false;
const guildGroups = {};

function guildGroupData(n) {
  if (!guildGroups[n]) guildGroups[n] = { clan_id: '', region: 'BD', accounts: '' };
  return guildGroups[n];
}

function parseAccts(text) {
  let ok = 0; const bad = [];
  String(text || '').split(/\r?\n/).forEach((l, i) => {
    l = l.trim(); if (!l || l[0] === '#') return;
    const k = l.indexOf(':');
    if (k > 0 && k < l.length - 1) ok++; else bad.push(i + 1);
  });
  return {ok, bad};
}

function saveGuildFields() {
  const c = document.getElementById('gGroupClan'), r = document.getElementById('gGroupRegion'), a = document.getElementById('gGroupAccounts');
  const g = guildGroupData(activeGuildGroup);
  if (c) g.clan_id = c.value.trim();
  if (r) g.region = r.value;
  if (a) g.accounts = a.value;
}

function updateGCount() {
  const a = document.getElementById('gGroupAccounts'), el = document.getElementById('gCount');
  if (!a || !el) return;
  const p = parseAccts(a.value);
  el.textContent = p.bad.length ? p.ok + ' ready · bad line ' + p.bad.slice(0, 3).join(', ') : p.ok + ' ready';
  el.className = 'gcount' + (p.bad.length || !p.ok ? ' warn' : '');
}

function selectGuildGroup(n) { saveGuildFields(); activeGuildGroup = n; renderGuildGroupEditor(); }
function addGuildGroup() { saveGuildFields(); guildGroupCount++; activeGuildGroup = guildGroupCount; guildGroupData(activeGuildGroup); renderGuildGroupEditor(); }

function renderGuildGroupEditor() {
  const box = document.getElementById('guildEditor'); if (!box) return;
  const g = guildGroupData(activeGuildGroup);
  let tabs = '';
  for (let n = 1; n <= guildGroupCount; n++) tabs += `<button class="chip ${n === activeGuildGroup ? 'on' : ''}" onclick="selectGuildGroup(${n})">Group ${n}</button>`;
  tabs += `<button class="chip" onclick="addGuildGroup()">＋ Group</button>`;
  const regions = ['BD', 'IND', 'SG', 'BR', 'US', 'ID', 'TH', 'PK', 'ME'];
  box.innerHTML = `<div class="chips">${tabs}</div>
    <div class="grow">
      <div><div class="glbl"><span>Clan ID</span></div><input id="gGroupClan" inputmode="numeric" placeholder="Clan ID" value="${esc(g.clan_id)}" oninput="saveGuildFields()"></div>
      <div><div class="glbl"><span>Region</span></div><select id="gGroupRegion" onchange="saveGuildFields()">${regions.map(x => `<option value="${x}" ${g.region === x ? 'selected' : ''}>${x}</option>`).join('')}</select></div>
    </div>
    <div class="glbl"><span>Accounts · uid:pass per line</span><span class="gcount" id="gCount">0 ready</span></div>
    <textarea class="gta" id="gGroupAccounts" spellcheck="false" autocomplete="off" autocapitalize="off" placeholder="123456789:password&#10;987654321:password" oninput="saveGuildFields();updateGCount()">${esc(g.accounts)}</textarea>
    <div class="gact">
      <button class="btn green" id="gJoin" onclick="runGuild('JOIN')">${IC.join}<span>Join clan</span></button>
      <button class="btn rose" id="gLeave" onclick="runGuild('LEAVE')">${IC.out}<span>Leave clan</span></button>
    </div>
    <p class="ghint">One account or many: Join and Leave use the same list, clan ID and region.</p>`;
  updateGCount();
}

async function renderGuild() {
  lastGuildHtml = '';
  document.getElementById('content').innerHTML = `
    <div class="squad-card">
      <div class="gh"><div class="gi">${IC.guild}</div><div><h3>Guild manager</h3><p>Join or leave a clan with your uid:pass accounts.</p></div></div>
      <div id="guildEditor"></div>
    </div>
    <div id="guildResult"></div>`;
  for (let n = 1; n <= guildGroupCount; n++) guildGroupData(n);
  renderGuildGroupEditor();
  await refreshGuild();
}

async function runGuild(action) {
  if (guildBusy) return;
  saveGuildFields();
  const g = guildGroupData(activeGuildGroup), p = parseAccts(g.accounts);
  if (!g.clan_id) return alert('Enter the Clan ID first');
  if (!p.ok) return alert('Add at least one uid:pass line');
  if (p.bad.length) return alert('Bad format on line ' + p.bad.join(', ') + ' (use uid:pass)');
  if (action === 'LEAVE' && !(await askConfirm('Leave clan ' + g.clan_id + ' with ' + p.ok + ' account(s)?'))) return;
  guildBusy = true;
  const btn = document.getElementById(action === 'JOIN' ? 'gJoin' : 'gLeave');
  if (btn) btn.classList.add('load');
  const r = await api('/api/guild/group', {method:'POST', body:{action, group_name:'Group ' + activeGuildGroup, clan_id:g.clan_id, region:g.region, accounts:g.accounts}});
  guildBusy = false;
  if (btn) btn.classList.remove('load');
  if (!r.ok) return alert('Error: ' + r.error);
  alert('✅ ' + (action === 'JOIN' ? 'Join' : 'Leave') + ' started for ' + r.total + ' account(s)');
  lastGuildHtml = '';
  refreshGuild();
}

function keepFailed(jid) {
  const job = lastJobs.find(j => j.id === jid); if (!job) return;
  const bad = new Set(Object.entries(job.results || {}).filter(([, r]) => !r.ok).map(([u]) => String(u)));
  const a = document.getElementById('gGroupAccounts'); if (!a) return;
  const keep = a.value.split(/\r?\n/).filter(l => bad.has(l.split(':')[0].trim()));
  if (!keep.length) { toast('No failed account found in this group list', 'err'); return; }
  a.value = keep.join('\n'); saveGuildFields(); updateGCount();
  toast('Kept ' + keep.length + ' failed account(s). Press Join or Leave to retry.', 'ok');
}

async function refreshGuild() {
  if (!document.getElementById('guildResult')) return;
  const hist = await api('/api/guild/jobs');
  const el = document.getElementById('guildResult'); if (!el) return;
  const jobs = hist && hist.ok ? (hist.jobs || []) : [];
  lastJobs = jobs;
  let h = '';
  if (!jobs.length) h = `<div class="squad-card empty"><b>No guild jobs yet</b><p>Run Join or Leave and live results will appear here.</p></div>`;
  for (const job of jobs.slice().reverse().slice(0, 5)) {
    const total = job.uids.length, res = Object.entries(job.results || {});
    const ok = res.filter(([, r]) => r.ok).length, fail = res.length - ok;
    const pct = total ? Math.round(res.length / total * 100) : 0;
    const act = String(job.action || 'JOIN').toUpperCase(), isL = act === 'LEAVE';
    h += `<section class="squad-card ${job.done ? '' : 'run'}">
      <div class="jobhead"><h3>${esc(job.group_name || 'Job #' + job.id)}</h3><span class="act ${isL ? 'leave' : 'join'}">${esc(act)}</span><span class="sq-meta">Clan ${esc(job.guild_id)}${job.region ? ' · ' + esc(job.region) : ''}</span>${job.done ? '<span class="badge success">DONE</span>' : '<span class="badge connecting">RUNNING</span>'}</div>
      <div class="prog ${isL ? 'leave' : ''}"><i style="width:${pct}%"></i></div>
      <div class="stats three">
        <div class="stat"><div class="num">${total}</div><div class="lbl">Total</div></div>
        <div class="stat"><div class="num" style="color:var(--grn)">${ok}</div><div class="lbl">Success</div></div>
        <div class="stat"><div class="num" style="color:var(--red)">${fail}</div><div class="lbl">Failed</div></div>
      </div>
      ${fail && job.done ? `<div class="row" style="margin:0 0 10px"><button class="btn small violet" onclick="keepFailed(${job.id})">Keep failed only</button></div>` : ''}
      <div class="guild-grid">${res.map(([uid, r]) => `<div class="guild-item ${r.ok ? 'ok' : 'fail'}"><div class="u">${esc(uid)} <span class="badge ${r.ok ? 'success' : 'failed'}">${r.ok ? 'OK' : 'FAIL'}</span></div><div class="m">${esc(r.msg || '')}</div><div class="m">${esc(r.detail || '')}</div></div>`).join('')}</div>
    </section>`;
  }
  if (h !== lastGuildHtml) { el.innerHTML = h; lastGuildHtml = h; }
}

async function renderConsoles() {
  const d = await api('/api/status');
  if (!d.ok || currentTab !== 'consoles') return;
  const c = document.getElementById('content');
  if (!c) return;
  if (!d.squads || d.squads.length === 0) {
    c.innerHTML = `<div class="squad-card empty"><b>No squads yet</b><p>Create a squad to see its live log here.</p><button class="btn gold" onclick="switchTab('create')">Create a squad</button></div>`;
    return;
  }
  if (currentConsoleSquad === null || !d.squads.some(s => s.id === currentConsoleSquad)) currentConsoleSquad = d.squads[0].id;
  c.innerHTML = `<div class="chips">${d.squads.map(s => `<button class="chip ${currentConsoleSquad===s.id?'on':''}" onclick="selectConsole(${s.id})">Squad ${s.id}</button>`).join('')}</div><div id="consoleBox"></div>`;
  await loadConsole(currentConsoleSquad);
}

async function selectConsole(sid) {
  currentConsoleSquad = sid;
  await renderConsoles();
}

async function loadConsole(sid) {
  if (!sid) return;
  const d = await api('/api/squad/logs?squad_id=' + sid);
  const box = document.getElementById('consoleBox');
  if (!box) return;
  if (!d.ok) { box.innerHTML = '<div class="alert-red">Could not load the log. Check the connection and try again.</div>'; return; }
  const old = box.querySelector('.log-panel');
  const stick = !old || old.scrollHeight - old.scrollTop - old.clientHeight < 40;
  const prevTop = old ? old.scrollTop : 0;
  const logs = d.logs || [];
  const lines = logs.length
    ? logs.map(l => `<div class="log-line ${esc(l.lvl)}"><span class="lt">${esc(l.t)}</span>${esc(l.m)}</div>`).join('')
    : '<div style="color:var(--mut)">No log lines yet. Start the squad to see activity.</div>';
  box.innerHTML = `<div class="squad-card"><h3>Squad ${sid} log</h3><div class="log-panel">${lines}</div></div>`;
  const p = box.querySelector('.log-panel');
  if (p) p.scrollTop = stick ? p.scrollHeight : prevTop;
}

async function refreshConsoles() {
  if (currentConsoleSquad) await loadConsole(currentConsoleSquad);
}

function logout() {
  tokClear();
  adminToken='';
  if (pollTimer) clearInterval(pollTimer);
  renderLogin();
}

if (adminToken) {
  api('/api/status').then(d => { if (d.ok) renderMain(); else renderLogin(); }).catch(()=>renderLogin());
} else {
  renderLogin();
}
</script>
</body>
</html>
"""

async def web_index(request):
    return aioweb.Response(text=HTML_PAGE, content_type="text/html")

def _json(data, status=200):
    return aioweb.json_response(data, status=status)

def _client_ip(request):
    xff = request.headers.get("X-Forwarded-For", "")
    return (xff.split(",")[0].strip() if xff else "") or str(getattr(request, "remote", "") or "?")

async def _read_json(request):
    try:
        b = await request.json()
        return b if isinstance(b, dict) else {}
    except Exception:
        return {}

def _need_user(request):
    u = user_store.session_user(request.headers.get("X-Session-Token", ""))
    if not u:
        return None, _json({"ok": False, "error": "Unauthorized"}, 401)
    return u, None

def _need_admin(request):
    u, err = _need_user(request)
    if err: return None, err
    if u.get("role") != "admin":
        return None, _json({"ok": False, "error": "Forbidden"}, 403)
    return u, None

async def web_config(request):
    return _json({"ok": True, "registration": bool(ALLOW_REGISTRATION and len(user_store.users) < MAX_USERS),
                  "min_password": MIN_PASSWORD})

async def web_register(request):
    if not ALLOW_REGISTRATION or len(user_store.users) >= MAX_USERS:
        return _json({"ok": False, "error": "registration_closed"}, 403)
    ip = _client_ip(request)
    if _rate_blocked(f"reg:{ip}", 5, 3600):
        return _json({"ok": False, "error": "rate_limited"}, 429)
    b = await _read_json(request)
    username = str(b.get("username", "")).strip()
    password = str(b.get("password", ""))
    if not USERNAME_RE.match(username):
        return _json({"ok": False, "error": "bad_username"})
    if username.lower() in RESERVED_NAMES or user_store.find(username):
        return _json({"ok": False, "error": "username_taken"})
    if not (MIN_PASSWORD <= len(password) <= 128):
        return _json({"ok": False, "error": "bad_password"})
    _rate_add(f"reg:{ip}")
    pw_hash = await asyncio.to_thread(_hash_pw, password)
    if user_store.find(username):                      # re-check after the await
        return _json({"ok": False, "error": "username_taken"})
    rec = user_store.create(username, pw_hash)
    token = user_store.new_session(rec["id"])
    return _json({"ok": True, "token": token, "user": user_store.public(rec)})

async def web_login(request):
    ip = _client_ip(request)
    b = await _read_json(request)
    # The dashboard's admin login form intentionally asks for password only.
    # Default to the configured admin username when no username is submitted.
    username = str(b.get("username", ADMIN_USERNAME)).strip()[:64] or ADMIN_USERNAME
    password = str(b.get("password", ""))[:128]
    ukey = f"lu:{username.lower()}"
    if _rate_blocked(f"li:{ip}", 30, 600) or _rate_blocked(ukey, 8, 600):
        return _json({"ok": False, "error": "rate_limited"}, 429)
    u = user_store.find(username) if username else None
    good = await asyncio.to_thread(_verify_pw, password, u["pw"] if u else _DUMMY_HASH)
    if not (u and good):
        _rate_add(f"li:{ip}"); _rate_add(ukey)
        return _json({"ok": False, "error": "invalid_credentials"})
    if u.get("disabled"):
        return _json({"ok": False, "error": "disabled"})
    _rate_clear(ukey)
    token = user_store.new_session(u["id"])
    return _json({"ok": True, "token": token, "user": user_store.public(u)})

async def web_logout(request):
    tok = request.headers.get("X-Session-Token", "")
    if tok: user_store.drop_session(tok)
    return _json({"ok": True})

async def web_me(request):
    u, err = _need_user(request)
    if err: return err
    return _json({"ok": True, "user": user_store.public(u)})

async def web_change_password(request):
    u, err = _need_user(request)
    if err: return err
    if u.get("role") == "admin":
        return _json({"ok": False, "error": "admin_password_in_code"})
    if _rate_blocked(f"cp:{u['id']}", 6, 600):
        return _json({"ok": False, "error": "rate_limited"}, 429)
    b = await _read_json(request)
    cur, new = str(b.get("current", ""))[:128], str(b.get("new", ""))
    if not await asyncio.to_thread(_verify_pw, cur, u["pw"]):
        _rate_add(f"cp:{u['id']}")
        return _json({"ok": False, "error": "wrong_password"})
    if not (MIN_PASSWORD <= len(new) <= 128):
        return _json({"ok": False, "error": "bad_password"})
    u["pw"] = await asyncio.to_thread(_hash_pw, new)
    user_store.save()
    user_store.drop_user_sessions(u["id"], keep_token=request.headers.get("X-Session-Token", ""))
    return _json({"ok": True})

async def web_status(request):
    u, err = _need_user(request)
    if err: return err
    owner = u["id"]
    mine = {uid: a for uid, a in bot_state.accounts.items() if a.get("owner") == owner}
    workers = 0
    for uid in mine:
        t = bot_state.account_workers.get(uid)
        if t is not None and not t.done(): workers += 1
    return _json({
        "ok": True,
        "total_squads": squad_mgr.count_for(owner),
        "total_accounts": len(mine),
        "total_matches": sum(a.get("matches", 0) for a in mine.values()),
        "active_workers": workers,
        "squads": squad_mgr.get_squads(owner),
        "failed_uids": [uid for uid, a in mine.items() if a.get("guild_status") == "FAILED"],
    })

async def web_squad_create(request):
    u, err = _need_user(request)
    if err: return err
    try:
        body = await _read_json(request)
        members = []
        for m in (body.get("members") or []):
            if not isinstance(m, dict): continue
            uid_ = str(m.get("uid", "")).strip()[:32]
            pw_ = str(m.get("password", "")).strip()[:128]
            if uid_ and pw_: members.append((uid_, pw_))
        if not members:
            return _json({"ok": False, "error": "No valid members"})
        if len(members) > TEAM_SIZE:
            return _json({"ok": False, "error": f"A squad holds at most {TEAM_SIZE} accounts"})
        if u.get("role") != "admin" and squad_mgr.count_for(u["id"]) >= MAX_SQUADS_PER_USER:
            return _json({"ok": False, "error": f"Squad limit reached ({MAX_SQUADS_PER_USER})"})
        ok, msg, num = await squad_mgr.create_squad(members, u["id"])
        return _json({"ok": ok, "squad_id": num, "msg": msg, "error": None if ok else msg})
    except Exception as e:
        return _json({"ok": False, "error": str(e)})

async def _squad_action(request, method, with_uid=False):
    u, err = _need_user(request)
    if err: return err
    try:
        body = await _read_json(request)
        try: num = int(body.get("squad_id", 0))
        except Exception: num = 0
        sid = squad_mgr.sid_for(u["id"], num)
        if sid is None:
            return _json({"ok": False, "error": "Squad not found"})
        fn = getattr(squad_mgr, method)
        if with_uid:
            ok, msg = await fn(sid, str(body.get("uid", "")).strip(), u["id"])
        else:
            ok, msg = await fn(sid, u["id"])
        return _json({"ok": ok, "error": None if ok else msg})
    except Exception as e:
        return _json({"ok": False, "error": str(e)})

async def web_squad_start(request):   return await _squad_action(request, "start_squad")
async def web_squad_restart(request): return await _squad_action(request, "restart_squad")
async def web_squad_stop(request):    return await _squad_action(request, "stop_squad")
async def web_squad_delete(request):  return await _squad_action(request, "delete_squad")
async def web_squad_remove(request):  return await _squad_action(request, "remove_member", with_uid=True)

async def web_squad_logs(request):
    u, err = _need_user(request)
    if err: return err
    try:
        num = int(request.query.get("squad_id", "0"))
    except Exception:
        num = 0
    sid = squad_mgr.sid_for(u["id"], num)
    if sid is None:
        return _json({"ok": False, "error": "Squad not found"})
    return _json({"ok": True, "logs": bot_state.squad_logs.get(sid, [])})

async def web_guild_group(request):
    u, err = _need_user(request)
    if err: return err
    owner = u["id"]
    try:
        body = await _read_json(request)
        action = str(body.get("action", "JOIN")).strip().upper()
        if action not in ("JOIN", "LEAVE"):
            return _json({"ok": False, "error": "invalid action"})
        group_name = str(body.get("group_name", "Group")).strip()[:40] or "Group"
        clan_id = str(body.get("clan_id", "")).strip()[:32]
        region = str(body.get("region", "BD")).strip().upper()[:4] or "BD"
        raw_accounts = str(body.get("accounts", ""))[:20000]
        if not clan_id:
            return _json({"ok": False, "error": "Clan ID required"})
        accounts = []
        invalid_lines = []
        for line_no, line in enumerate(raw_accounts.splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" not in line:
                invalid_lines.append(line_no)
                continue
            uid, password = line.split(":", 1)
            uid, password = uid.strip(), password.strip()
            if not uid or not password:
                invalid_lines.append(line_no)
                continue
            accounts.append((uid, password))
        if not accounts:
            return _json({"ok": False, "error": "No valid uid:pass entries found", "invalid_lines": invalid_lines})
        if len(accounts) > 100:
            return _json({"ok": False, "error": "Max 100 accounts per run"})
        jid = await bot_state.new_guild_job(clan_id, action, [x for x, _ in accounts], owner)
        bot_state.guild_jobs[jid]["group_name"] = group_name
        bot_state.guild_jobs[jid]["region"] = region
        fn = guild_do_join if action == "JOIN" else guild_do_leave

        def _mark(uid, status, detail):
            a = bot_state.accounts.get(uid)
            if a is not None and a.get("owner") == owner:      # never touch another user's account
                bot_state.update_guild(uid, status, detail)

        async def run_group():
            sem = asyncio.Semaphore(3)
            async def one(uid, password):
                async with sem:
                    try:
                        ok, code, resp_body, ep, _tries = await asyncio.to_thread(
                            guild_call_with_retry, (lambda g_, u_, p_: fn(g_, u_, p_, region)),
                            clan_id, uid, password, 2
                        )
                        msg = guild_result_msg(ok, code, resp_body)
                        detail = f"HTTP {code} | {group_name} | {region}"
                        bot_state.add_guild_result(jid, uid, ok, msg, detail)
                        _mark(uid, "SUCCESS" if ok else "FAILED", detail)
                    except Exception as exc:
                        bot_state.add_guild_result(jid, uid, False, str(exc)[:160], "exception")
                    await asyncio.sleep(0.5)
            await asyncio.gather(*(one(x, p) for x, p in accounts), return_exceptions=True)
            bot_state.finish_guild_job(jid)

        asyncio.create_task(run_group())
        return _json({"ok": True, "job_id": bot_state.guild_jobs[jid]["num"], "total": len(accounts),
                      "invalid_lines": invalid_lines})
    except Exception as e:
        return _json({"ok": False, "error": str(e)})

async def web_guild_jobs(request):
    u, err = _need_user(request)
    if err: return err
    owner = u["id"]
    try:
        jobs = []
        for jid, j in bot_state.guild_jobs.items():
            if j.get("owner") != owner:
                continue
            jobs.append({
                "id": j["num"], "guild_id": j["guild_id"], "action": j["action"],
                "uids": j["uids"], "results": j["results"],
                "started": j["started"], "done": j["done"],
                "group_name": j.get("group_name", ""), "region": j.get("region", ""),
            })
        jobs.sort(key=lambda x: x["started"])
        return _json({"ok": True, "jobs": jobs})
    except Exception as e:
        return _json({"ok": False, "error": str(e)})

# ── admin: manage accounts of the panel (never sees another user's uid/password) ──
async def web_admin_users(request):
    me_, err = _need_admin(request)
    if err: return err
    out = []
    for uid, u in sorted(user_store.users.items(), key=lambda kv: int(kv[0])):
        sq = [s_ for s_ in squad_mgr.squads.values() if s_.get("owner") == uid]
        out.append({
            "id": uid, "username": u["username"], "role": u.get("role", "user"),
            "created": u.get("created", 0), "disabled": bool(u.get("disabled")),
            "squads": len(sq), "accounts": sum(len(s_["uids"]) for s_ in sq),
            "running": sum(1 for s_ in sq if s_["is_started"] and squad_mgr._is_alive(s_)),
        })
    return _json({"ok": True, "users": out})

async def web_admin_action(request):
    me_, err = _need_admin(request)
    if err: return err
    b = await _read_json(request)
    uid = str(b.get("user_id", ""))
    action = str(b.get("action", ""))
    u = user_store.users.get(uid)
    if not u or u.get("role") == "admin":
        return _json({"ok": False, "error": "User not found"})
    if action in ("disable", "delete"):
        for sid in squad_mgr.sids_of(uid):
            await (squad_mgr.stop_squad(sid, uid) if action == "disable" else squad_mgr.delete_squad(sid, uid))
    if action == "disable":
        u["disabled"] = True; user_store.drop_user_sessions(uid); user_store.save()
    elif action == "enable":
        u["disabled"] = False; user_store.save()
    elif action == "delete":
        bot_state.purge_owner(uid); user_store.delete_user(uid)
    elif action == "reset_password":
        new = str(b.get("new_password", ""))
        if not (MIN_PASSWORD <= len(new) <= 128):
            return _json({"ok": False, "error": "bad_password"})
        u["pw"] = await asyncio.to_thread(_hash_pw, new)
        user_store.drop_user_sessions(uid); user_store.save()
    else:
        return _json({"ok": False, "error": "invalid action"})
    return _json({"ok": True})

async def start_web_server():
    if not _HAS_AIOHTTP:
        print_error("aiohttp not installed! Run: pip install aiohttp")
        return None
    try:
        @aioweb.middleware
        async def _security_headers(request, handler):
            try:
                resp = await handler(request)
            except aioweb.HTTPException as ex:
                ex.headers["X-Content-Type-Options"] = "nosniff"
                raise
            resp.headers["X-Content-Type-Options"] = "nosniff"
            resp.headers["X-Frame-Options"] = "DENY"
            resp.headers["Referrer-Policy"] = "no-referrer"
            if request.path.startswith("/api/"):
                resp.headers["Cache-Control"] = "no-store"
            return resp

        app = aioweb.Application(middlewares=[_security_headers])
        app.router.add_get("/", web_index)
        app.router.add_get("/api/config", web_config)
        app.router.add_post("/api/register", web_register)
        app.router.add_post("/api/login", web_login)
        app.router.add_post("/api/logout", web_logout)
        app.router.add_get("/api/me", web_me)
        app.router.add_post("/api/account/password", web_change_password)
        app.router.add_get("/api/status", web_status)
        app.router.add_post("/api/squad/create", web_squad_create)
        app.router.add_post("/api/squad/start", web_squad_start)
        app.router.add_post("/api/squad/restart", web_squad_restart)
        app.router.add_post("/api/squad/stop", web_squad_stop)
        app.router.add_post("/api/squad/delete", web_squad_delete)
        app.router.add_post("/api/squad/remove", web_squad_remove)
        app.router.add_get("/api/squad/logs", web_squad_logs)
        app.router.add_post("/api/guild/group", web_guild_group)
        app.router.add_get("/api/guild/jobs", web_guild_jobs)
        app.router.add_get("/api/admin/users", web_admin_users)
        app.router.add_post("/api/admin/action", web_admin_action)
        runner = aioweb.AppRunner(app)
        await runner.setup()
        site = aioweb.TCPSite(runner, WEB_HOST, WEB_PORT)
        await site.start()
        print_success(f"🌐 Web Dashboard: http://localhost:{WEB_PORT}")
        print_info(f"👤 Admin login: {ADMIN_USERNAME} (password = ADMIN_PASSWORD in the code) | sign-up {'OPEN' if ALLOW_REGISTRATION else 'CLOSED'}")
        return runner
    except Exception as e:
        print_error(f"Web server error: {e}")
        return None

# ═══════════════════════════ MAIN ═══════════════════════════
async def main():
    print_banner()
    user_store.load()
    user_store.ensure_admin()
    squad_mgr.load()
    print_section("⚙️  SYSTEM CONFIGURATION", Colors.PURPLE)
    print_info(f"🎮 Mode          : MANUAL SQUAD + GUILD 🇧🇩")
    print_info(f"🌏 Default Region: {DEFAULT_REGION}")
    print_success(f"👥 SQUAD size={TEAM_SIZE} | manual create/start/stop")
    print_info(f"📡 HTTP Ping     : {'ENABLED' if ENABLE_HTTP_PING else 'DISABLED'}")
    print_info(f"🏃 Speed Movement: {'ENABLED' if ENABLE_SPEED_MOVEMENT else 'DISABLED'}")
    print_info(f"🛡️  Safe Mode     : {'ENABLED' if SAFE_PLAY_MODE else 'DISABLED'}")
    print_info(f"🏰 Guild Tag     : {GUILD_TAG}")
    print_info(f"👥 Users         : {len(user_store.users)} | max squads/user: {MAX_SQUADS_PER_USER}")
    await start_web_server()
    print_colored(f"\n{Colors.BDGREEN}  ✅ {BRAND_WEB_NAME} v5.1 is running — Open http://localhost:{WEB_PORT}{Colors.ENDC}\n")
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print_section("🛑 SHUTTING DOWN", Colors.BDRED)
        for t in list(bot_state.account_workers.values()):
            t.cancel()
        await asyncio.gather(*bot_state.account_workers.values(), return_exceptions=True)
        print_success(f"👋 {BRAND_WEB_NAME} closed. Goodbye! 🇧🇩")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_warning("stopped")