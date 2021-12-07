set bname=wen_dev
set bmain=develop
git checkout %bmain%
git branch -d %bname%
git fetch
git pull
git push --delete origin %bname%

REM create my local and remote branches.
git checkout -b %bname%
git push --set-upstream origin %bname%

; set a local inited git repository to a origin url
; git remote add staging git@github.com:david7dong/workspace-migration.git
; git remote you will see the added remote, e.g. 
origin
staging