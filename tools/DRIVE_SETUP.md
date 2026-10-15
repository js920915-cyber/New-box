# Google Drive 업로드 인증 설정 (PPTX 자동 업로드용, 1회)

`tools/upload_drive.py`가 PPTX를 사용자 Drive에 직접 올리기 위한 인증 정보 3개를 만든다.
값은 채팅에 붙여넣지 않고 클라우드 환경 설정에만 넣는다.

## 1. Google Cloud 프로젝트와 Drive API
1. https://console.cloud.google.com 에 Drive를 쓰는 Google 계정으로 로그인 → 상단 프로젝트 선택 → **새 프로젝트** (예: `rsports-cardnews`).
2. **API 및 서비스 → 라이브러리** → `Google Drive API` 검색 → **사용**.

## 2. OAuth 동의 화면
1. **API 및 서비스 → OAuth 동의 화면**(또는 Google 인증 플랫폼) → 사용자 유형 **외부** → 앱 이름·지원 이메일·개발자 이메일 입력.
2. 범위는 비워 둬도 된다.
3. **테스트 사용자**에 본인 Gmail 추가.
4. **게시 상태를 '프로덕션'으로 전환(앱 게시)** 한다. '테스트' 상태로 두면 refresh token이 7일 뒤 만료된다. 본인만 쓰는 앱이라 Google 검증 없이도 동작하며, 로그인 때 "확인되지 않은 앱" 경고가 나오면 **고급 → (앱 이름)(으)로 이동**을 누른다.

## 3. OAuth 클라이언트
1. **API 및 서비스 → 사용자 인증 정보 → 사용자 인증 정보 만들기 → OAuth 클라이언트 ID**.
2. 애플리케이션 유형 **웹 애플리케이션**.
3. **승인된 리디렉션 URI**에 `https://developers.google.com/oauthplayground` 추가 → 만들기.
4. 표시되는 **클라이언트 ID**와 **클라이언트 보안 비밀번호**를 메모.

## 4. refresh token 받기 (OAuth Playground)
1. https://developers.google.com/oauthplayground 접속 → 오른쪽 위 **톱니바퀴** → **Use your own OAuth credentials** 체크 → 3번의 ID·보안 비밀번호 입력.
2. 왼쪽 Step 1 입력칸에 `https://www.googleapis.com/auth/drive` 입력 → **Authorize APIs** → 본인 계정 선택·허용.
3. Step 2에서 **Exchange authorization code for tokens** → **Refresh token** 값을 복사.

## 5. 클라우드 환경에 등록
세션 제목 줄의 환경 메뉴 → **Edit** → Network secrets(없으면 환경 변수)에 추가:

| 이름 | 값 |
|---|---|
| `GDRIVE_CLIENT_ID` | 3번 클라이언트 ID |
| `GDRIVE_CLIENT_SECRET` | 3번 클라이언트 보안 비밀번호 |
| `GDRIVE_REFRESH_TOKEN` | 4번 refresh token |

새 세션부터 적용된다. 등록 후 에이전트가 1탄 PPTX로 시험 업로드하고 크기·md5 일치를 확인한다.

## 주의
- 이 토큰은 Drive 전체 읽기·쓰기 권한이다. 저장소·채팅·문서에 값을 적지 않는다.
- 해지: https://myaccount.google.com/permissions 에서 앱 접근 권한 삭제, 또는 Cloud Console에서 클라이언트 삭제.
- 스크립트는 `R스포츠재활센터 카드뉴스/<주제>/`에만 올리고, 같은 이름 파일은 덮어쓰지 않고 `이전버전_<날짜>`로 옮기며, 공유 설정은 바꾸지 않는다.
