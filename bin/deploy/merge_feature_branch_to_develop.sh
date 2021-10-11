#!/bin/bash

if [ "$TRAVIS_BRANCH" != "develop" ] && [ "$TRAVIS_BRANCH" != "master" ]; then
    git config --global user.email "builds@travis-ci.com"
    git config --global user.name "Travis CI"
    git remote set-branches --add origin develop || echo "Set origin develop failed"
    git fetch
    git reset --hard
    git checkout develop || echo "Git checkout master failed"
    git merge "$TRAVIS_COMMIT" || echo "Merge feature branch to develop failed"
    git push -q https://$GITHUB_TOKEN@github.com/ggeop/Python-ai-assistant develop
fi
