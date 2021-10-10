if [ "$TRAVIS_BRANCH" == "develop" ]; then
    git config --global user.email "builds@travis-ci.com"
    git config --global user.name "Travis CI"
    git checkout https://github.com/ggeop/Python-ai-assistant/tree/master || echo "master checkout failed"
    git merge "$TRAVIS_COMMIT" || echo "Merge develop to master failed"
    git push -q https://$GITHUB_TOKEN@github.com/ggeop/Python-ai-assistant
fi