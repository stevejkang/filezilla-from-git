# filezilla-from-git
> [한국어](https://github.com/stevejkang/filezilla-from-git/blob/master/README.ko.md)

💻 Automation script for easy upload local files that changed at specific git commit hash, to a remote server using XML formatted queue file.

## 📚 Usage
1. Clone the repository
    ```bash
    $ git clone https://github.com/stevejkang/filezilla-from-git.git
    $ cd filezilla-from-git
    ```
2. Copy the script to your project root. (same level as `.git/`)
    ```bash
    $ cp filezilla-from-git.py /foo/bar/project/
    ```
3. Modify the global variables defined in `filezilla-from-git.py` to fit your ftp configuration.
    ```python
    FTP_HOST = 'localhost'
    FTP_PORT = '22220'
    FTP_PTCL = '1' # 0: FTP, 1: SFTP
    FTP_TYPE = '0' # DEFAULT
    FTP_USER = 'root'
    FTP_KEYFILE_PATH = '/home/key.ppk' # ONLY FTP_LOGON_TYPE = 5
    FTP_LOGON_TYPE = '5' # 2: Ask for password, 5: Key file
    FTP_ENCODING_TYPE = 'Auto' # DEFAULT
    FTP_BYPASS_PROXY = '0' # DEFAULT
    FTP_NAME = 'SERVER' # NOT NECESSARY
    FTP_REMOTE_PATH = '/var/www/html/project/' # Ends with slash(/)
    ```
4. Run script with specific commit hash.
    ```bash
    $ python filezilla-from-git.py '<git_commit_hash>'
    ```
5. Import the created file(`queue.xml`) and check the queue.

## ❗️ Caution
- Make sure that the local file tree and remote file tree are the same. This is assumed to be all the same under the defined project root path. Otherwise, the xml created will proceed with the upload based on the local file.
- This script does not provide ignoration of specific files. It reflects all the files that were changed.
- This script is a file made for automation, but it is hard to ensure that it always provides accurate files and content. Please check again.
