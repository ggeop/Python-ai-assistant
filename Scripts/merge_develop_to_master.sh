#!/bin/bash

if [ "$TRAVIS_BRANCH" == "develop" ]; then
    git config --global user.email "builds@travis-ci.com"
    git config --global user.name "Travis CI"
    git remote set-branches --add origin master || echo "Set origin master failed"
    git fetch
    git reset --hard
    git checkout master || echo "Git checkout master failed"
    git merge "$TRAVIS_COMMIT" || echo "Merge develop to master failed"
    git push -q https://$GITHUB_TOKEN@github.com/ggeop/Python-ai-assistant master
fi

