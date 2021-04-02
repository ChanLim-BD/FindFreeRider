# 큐시즘 기업 프로젝트
6조: 강석훈, 김세한, 박근영, 이지수, 임찬, 임학수

# APK
Front-build/app-release_v0.92.apk 를 다운받아 설치하시면 됩니다.
1. App 이름은 'Find out Free Rider' 입니다.
2. React Native를 사용하였습니다.
3. 안드로이드 폴더 형식에 접근하기 때문에 안드로이드 타겟으로 빌드되었습니다.
4. React Native의 특성상 조금의 수정을 거친 후 IOS 빌드가 가능합니다.
5. 안드로이드 OS version 11 에서 테스트 되었습니다.
6. 외부 저장소 열람 권한이 필요합니다. 권한을 따로 요청하지 않는다면 직접 권한을 허용해주세요.
7. 카카오톡 파일을 upload 할 때, 서버로 텍스트 데이터를 보내고 Processing 된 값을 받아옵니다. 인터넷이 연결되어 있어야합니다.

<img src="https://user-images.githubusercontent.com/63851250/113415483-442f7500-93fa-11eb-9278-6af6dbcf6d57.gif" width="30%"><br/>

# Server
1. 서버는 Django를, DB는 SQLite를 사용하였습니다.
2. AWS 클라우드 서버를 이용해 배포합니다.
3. python 3.8.5 버전을 기준으로 합니다.
4. request로 txt파일을 받고, response로 html 포맷 json String을 반환합니다.
5. ./Back-end/dataAnalysis.py 모듈에서 txt파일을 분석합니다.
6. txt파일은 ./Back-end/에 저장됩니다.

# 데이터 분석
1. Python을 사용하였습니다.
2. pandas, numpy 라이브러리와 정규표현식을 지원하는 re 모듈을 사용하였습니다.
3. 채팅 빈도, 보낸 채팅 메시지의 평균 길이, 사과 빈도, 파일 공유 빈도를 바탕으로 각 팀원의 기여도를 평가합니다.
