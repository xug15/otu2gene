echo git config --global user.name "your_github_username"
echo git config --global user.email "your_github_email"
echo git config -l
version=`date`
echo ${version}
git add -A
git commit -m "${version}"
git branch -M main
git push -u origin main
