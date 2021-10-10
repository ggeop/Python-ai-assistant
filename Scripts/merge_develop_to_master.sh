if [ "$TRAVIS_BRANCH" == "develop" ]; then
    git config --global user.email "builds@travis-ci.com"
    git config --global user.name "Travis CI"
    git checkout master || exit
    git merge "$TRAVIS_COMMIT" || exit
    git push -q https://$GITHUB_TOKEN@github.com/ggeop/Python-ai-assistant
fi