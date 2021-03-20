#!/usr/bin/python3.7

import sys
import os
import time

NAME = "test"
CPPFILENAME = "main"

if sys.argv[1] == '-h' or sys.argv[1] == '--help':
  print("""GConan Usage (python3.7 required):
./gconan.py [<projectName>(default = test) <cppMainFileName>(default = main)]
Example: ./gconan.py testConanApp app""")

  exit(0)
else:
  if len(sys.argv) == 3:
    _ ,NAME, CPPFILENAME = sys.argv
  elif len(sys.argv) == 2:
    _ ,NAME = sys.argv
  else:
    print("Arguments Error: \ntry -> python3 gconan.py [<projectName>(default = test) <cppMainFileName>(default = main)]")

if CPPFILENAME.endswith(".cpp"):
  CPPFILENAME = CPPFILENAME[0:-4]

PROJECT_DIRECTORY = os.path.join(os.getcwd(), NAME)
PROJECT_SRC_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "src")

# print("Name: {0}, \nCPPNAME: {1}, \n INCLUDES: {2}".format(NAME, CPPFILENAME, INCLUDES))

CMAKE_CXX_FLAGS = "${CMAKE_CXX_FLAGS}"
CMAKE_BINARY_DIR = "${CMAKE_BINARY_DIR}"
CONAN_LIBS = "${CONAN_LIBS}"

CMAKEFILE = """cmake_minimum_required(VERSION 2.8.12)
project({0})

if(CMAKE_VERSION VERSION_LESS 3.0.0)
    include(CheckCXXCompilerFlag)
    check_cxx_compiler_flag(-std=c++11 COMPILER_SUPPORTS_CXX11)
    check_cxx_compiler_flag(-std=c++0x COMPILER_SUPPORTS_CXX0X)
    if(COMPILER_SUPPORTS_CXX11)
      set(CMAKE_CXX_FLAGS "{1} -std=c++11")
    elseif(COMPILER_SUPPORTS_CXX0X)
      set(CMAKE_CXX_FLAGS "{1} -std=c++0x")
    endif()
else()
    SET(CMAKE_CXX_STANDARD 11)
    SET(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

include({2}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable({4} src/{4}.cpp)
target_link_libraries({4} {3})
""".format(NAME, CMAKE_CXX_FLAGS, CMAKE_BINARY_DIR, CONAN_LIBS, CPPFILENAME)

CONANFILE = """[requires]
fmt/7.1.3
[generators]
cmake
"""

BUILDSHFILE = """#!/bin/bash

set -e
set -x

rm -rf build
mkdir build
pushd build

conan install .. --build=missing
cmake .. -DCMAKE_BUILD_TYPE=Debug
cmake --build .

bin/{0}
""".format(CPPFILENAME)

BUILDBATFILE = """if "%CMAKE_GENERATOR%"=="" (
    ECHO CMAKE_GENERATOR environment variable not defined. Please define the CMake generator in the CMAKE_GENERATOR environment variable.
)
else (
    @ECHO ON

    RMDIR /Q /S build
    MKDIR build
    PUSHD build

    conan install ..
    cmake .. -G "%CMAKE_GENERATOR%"
    cmake --build . --config Release

    bin\{0}.exe
)
""".format(CPPFILENAME)

CPPMAINFILE = """
/*

  ******************************
  * GCONAN GENERATED MAIN FILE *
  ******************************
  Date: {0};
  File Name: {1}
  Project Name: {2};

*/

#include <fmt/core.h>
// #include <conan-center/library.h>

int main(int argc, char** argv)
{
  fmt::print("Hello, Conan!\\n");
  return 0;
}

"""

def createDirectory():
  
  if not os.path.exists(PROJECT_DIRECTORY):
    os.makedirs(PROJECT_DIRECTORY)
    os.makedirs(PROJECT_SRC_DIRECTORY)
  else:
    print("Error, project is exists!")

def generateFiles():

  with open(PROJECT_DIRECTORY + os.path.sep + "CMakeLists.txt", "w") as cmakeFile:
     cmakeFile.write(CMAKEFILE)
     cmakeFile.close()

  with open(PROJECT_DIRECTORY + os.path.sep + "conanfile.txt", "w") as conanFile:
    conanFile.write(CONANFILE)
    conanFile.close()

  if os.name == 'posix':
    with open(PROJECT_DIRECTORY + os.path.sep + "build.sh", "w") as buildFile:
      buildFile.write(BUILDSHFILE)
      buildFile.close()
    os.system('chmod +x ' + PROJECT_DIRECTORY + os.path.sep + "build.sh")
  elif os.name == 'nt':
    with open(PROJECT_DIRECTORY + os.path.sep + "build.bat", "w") as buildFile:
      buildFile.write(BUILDBATFILE)
      buildFile.close()
  
  with open(PROJECT_DIRECTORY + os.path.sep + "conanfile.txt", "w") as conanFile:
    conanFile.write(CONANFILE)
    conanFile.close()

  with open(PROJECT_DIRECTORY + os.path.sep + "README.md", "w") as readmeFile:
    readmeFile.write(CONANFILE)
    readmeFile.close()
  
  with open(PROJECT_SRC_DIRECTORY + os.path.sep + CPPFILENAME + ".cpp", "w") as cppFile:
    cppFile.write(CPPMAINFILE)
    cppFile.close()

createDirectory()
generateFiles()

print("""
Project Generate Successful!

{0}:
----src:
--------{1}
----{2}
----CMakeLists.txt
----conanfile.txt
""".format(NAME, CPPFILENAME+".cpp", ('build.sh' if os.name == 'posix' else 'build.bat')))