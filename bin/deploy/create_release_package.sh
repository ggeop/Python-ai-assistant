#!/bin/bash

echo "Build Jarvis package"
tar -cvf $RELEASE_PACKAGE -T config/package_file_list.txt