#!/usr/bin/env bash

#--------------------------------------------------
# Add tag to new release (release based on master)
#-------------------------------------------------
echo "Add tags to new release"
git config --global user.email "builds@travis-ci.com"
git config --global user.name "Travis CI"
export GIT_TAG=Release_v.$TRAVIS_BUILD_NUMBER
git tag $GIT_TAG -a -m "Generated tag from TravisCI for build $TRAVIS_BUILD_NUMBER"
git push -q https://$GITHUB_TOKEN@github.com/ggeop/Python-ai-assistant --tags