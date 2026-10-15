"""카드뉴스 납품물(Express PPTX 등)을 사용자 Google Drive에 직접 업로드한다.

Drive 커넥터는 파일 내용을 base64 텍스트로 손으로 옮겨야 해서 PPTX처럼 큰 파일을
깨지지 않게 올릴 수 없다. 이 스크립트는 Drive API(v3)로 파일을 그대로 올린다.

필요한 환경 변수 (클라우드 환경 설정의 Network secrets/환경 변수에 등록, 채팅에 붙여넣지 않음):
  GDRIVE_CLIENT_ID, GDRIVE_CLIENT_SECRET, GDRIVE_REFRESH_TOKEN
  - Google Cloud OAuth 클라이언트(웹 애플리케이션)와 scope https://www.googleapis.com/auth/drive 로 받은 refresh token (발급 절차: tools/DRIVE_SETUP.md)
  - drive.file 범위로는 Drive 커넥터가 만든 기존 `R스포츠재활센터 카드뉴스` 폴더를 볼 수 없어 중복 폴더가 생기므로 drive 범위가 필요

사용:
  python3 tools/upload_drive.py --topic 2026-10-14_pfp-runners-part2 FILE [FILE ...]
  python3 tools/upload_drive.py --topic ... --dry-run FILE   # 인증 없이 계획만 출력

동작: 내 드라이브의 `R스포츠재활센터 카드뉴스/<topic>/`을 찾고 없으면 만든 뒤,
원본 형식 그대로(변환 없음) 업로드한다. 같은 이름 파일이 있으면 덮어쓰지 않고
`이전버전_<날짜>` 폴더로 옮긴 뒤 새로 올린다. 업로드 후 크기와 md5를 로컬 파일과 대조한다.
공유 권한은 바꾸지 않는다.
"""
import argparse, datetime, hashlib, json, mimetypes, os, sys, urllib.parse, urllib.request, uuid

ROOT_NAME = "R스포츠재활센터 카드뉴스"
FOLDER = "application/vnd.google-apps.folder"
API = "https://www.googleapis.com/drive/v3/files"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,size,md5Checksum,webViewLink"
mimetypes.add_type("application/vnd.openxmlformats-officedocument.presentationml.presentation", ".pptx")


def token():
    need = ["GDRIVE_CLIENT_ID", "GDRIVE_CLIENT_SECRET", "GDRIVE_REFRESH_TOKEN"]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        sys.exit("환경 변수 없음: " + ", ".join(missing) + " — 업로드하지 않았습니다.")
    body = urllib.parse.urlencode({
        "client_id": os.environ["GDRIVE_CLIENT_ID"], "client_secret": os.environ["GDRIVE_CLIENT_SECRET"],
        "refresh_token": os.environ["GDRIVE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", body) as r:
        return json.load(r)["access_token"]


def call(tok, url, method="GET", data=None, headers=None):
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": f"Bearer {tok}", **(headers or {})})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def q_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


def find(tok, name, parent, folder=None):
    q = f"name = '{q_escape(name)}' and '{parent}' in parents and trashed = false"
    if folder is True:
        q += f" and mimeType = '{FOLDER}'"
    elif folder is False:
        q += f" and mimeType != '{FOLDER}'"
    url = API + "?" + urllib.parse.urlencode({"q": q, "fields": "files(id,name)", "spaces": "drive"})
    return call(tok, url)["files"]


def ensure_folder(tok, name, parent):
    hit = find(tok, name, parent, folder=True)
    if hit:
        return hit[0]["id"]
    meta = json.dumps({"name": name, "mimeType": FOLDER, "parents": [parent]}).encode()
    return call(tok, API + "?fields=id", "POST", meta, {"Content-Type": "application/json"})["id"]


def move(tok, file_id, new_parent, old_parent):
    url = f"{API}/{file_id}?" + urllib.parse.urlencode({"addParents": new_parent, "removeParents": old_parent})
    call(tok, url, "PATCH", b"{}", {"Content-Type": "application/json"})


def upload(tok, path, parent):
    name = os.path.basename(path)
    mime = mimetypes.guess_type(name)[0] or "application/octet-stream"
    data = open(path, "rb").read()
    b = uuid.uuid4().hex
    meta = json.dumps({"name": name, "parents": [parent]}).encode()
    body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n".encode() + meta +
            f"\r\n--{b}\r\nContent-Type: {mime}\r\n\r\n".encode() + data + f"\r\n--{b}--".encode())
    res = call(tok, UPLOAD, "POST", body, {"Content-Type": f"multipart/related; boundary={b}"})
    ok = int(res.get("size", -1)) == len(data) and res.get("md5Checksum") == hashlib.md5(data).hexdigest()
    return res, ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True, help="예: 2026-10-14_pfp-runners-part2")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("files", nargs="+")
    a = ap.parse_args()
    for f in a.files:
        if not os.path.isfile(f):
            sys.exit(f"파일 없음: {f}")
    if a.dry_run:
        for f in a.files:
            print(f"[계획] {ROOT_NAME}/{a.topic}/{os.path.basename(f)}  ({os.path.getsize(f)} bytes)")
        return
    tok = token()
    root = ensure_folder(tok, ROOT_NAME, "root")
    topic = ensure_folder(tok, a.topic, root)
    failed = 0
    for f in a.files:
        name = os.path.basename(f)
        old = find(tok, name, topic, folder=False)
        if old:
            arch = ensure_folder(tok, f"이전버전_{datetime.date.today().isoformat()}", topic)
            for o in old:
                move(tok, o["id"], arch, topic)
        res, ok = upload(tok, f, topic)
        failed += not ok
        print(("OK " if ok else "확인 실패 ") + f"{name} size={res.get('size')} md5={res.get('md5Checksum')} {res.get('webViewLink')}")
    print(f"폴더: https://drive.google.com/drive/folders/{topic}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
