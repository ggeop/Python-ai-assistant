#!/usr/bin/env bash

#--------------------------------------------------
# Add tag to new release (release based on master)
#-------------------------------------------------
echo "Build Jarvis package"
tar -cvf jarvis_package.tar -T config/package_file_list.txt
echo "Add tags to new release"
git config --global user.email "builds@travis-ci.com"
git config --global user.name "Travis CI"
export GIT_TAG=$TRAVIS_BRANCH-$TRAVIS_BUILD_NUMBER
git tag $GIT_TAG -a -m "Generated tag from TravisCI for build $TRAVIS_BUILD_NUMBER"
git push -q https://$GITHUB_TOKEN@github.com/ggeop/Python-ai-assistant --tags