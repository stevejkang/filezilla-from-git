# filezilla-from-git
> [ENGLISH](https://github.com/stevejkang/filezilla-from-git/blob/master/README.md)

💻 특정 깃 커밋에서 변경된 파일들을 손쉽게 로컬에서 서버로 올릴 수 있도록 Queue 파일을 만들어내는 자동화 스크립트.

## 📚 사용법
1. 레포지토리를 클론합니다.
    ```bash
    $ git clone https://github.com/stevejkang/filezilla-from-git.git
    $ cd filezilla-from-git
    ```
2. 스크립트를 로컬의 프로젝트 루트 위치로 복사합니다. (`.git/`과 동일한 위치)
    ```bash
    $ cp filezilla-from-git.py /foo/bar/project/
    ```
3. `filezilla-from-git.py`에 정의된 전역변수를 FTP 설정에 맞게 수정합니다.
    ```python
    FTP_HOST = 'localhost'
    FTP_PORT = '22220'
    FTP_PTCL = '1' # 0: FTP, 1: SFTP
    FTP_TYPE = '0' # DEFAULT
    FTP_USER = 'root'
    FTP_KEYFILE_PATH = '/home/key.ppk' # ONLY FTP_LOGON_TYPE = 5
    FTP_LOGON_TYPE = '5' # 2: Ask for password, 5: Key file
    FTP_ENCODING_TYPE = 'Auto' # 기본 값
    FTP_BYPASS_PROXY = '0' # 기본 값
    FTP_NAME = 'SERVER' # 필수 아님
    FTP_REMOTE_PATH = '/var/www/html/project/' # 슬래시(/)로 끝나는 경로
    ```
4. 특정 커밋 해시를 입력하여 스크립트를 실행합니다.
    ```bash
    $ python filezilla-from-git.py '<git_commit_hash>'
    ```
5. `queue.xml`을 FileZilla에 임포트하고 queue를 확인합니다.

## ❗️ 주의
- 로컬의 파일 구조와 리모트의 파일 구조가 동일한 지 확인합니다. 이 스크립트는 정의된 루트 아래로는 모두 동일하다고 가정합니다. 그렇지 않다면, 생성된 xml 파일은 로컬에 변경된 파일 경로 기준으로 업로드가 진행됩니다.
- 현재, 이 스크립트는 특정 파일에 대한 무시(ignoration)를 제공하고 있지 않습니다. 커밋에서 변경된 모든 파일을 반영합니다.
- 이 스크립트는 자동화를 위해 만들어졌지만, 매번 정확한 파일과 내용을 제공한다고 보장하긴 어렵습니다. 만들어진 내용에 대해 한 번 더 확인합니다.
