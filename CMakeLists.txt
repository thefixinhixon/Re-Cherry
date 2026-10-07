
# re_cherry - ReXGlue Recompiled Project
#
# This file is yours to edit. 'rexglue migrate' will NOT overwrite it.
# SDK boilerplate lives in generated/rexglue.cmake.

cmake_minimum_required(VERSION 3.25)
project(re_cherry LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Linux needs SSSE3/SSE4.1 for the SDK memory.cpp (same fix as Pacific Rim / Condemned 2)
if(NOT WIN32)
    add_compile_options(-mssse3 -msse4.1)
endif()

include(generated/rexglue.cmake)

# Sources
set(RECHERRY_SOURCES
    src/main.cpp
    src/hooks.cpp
    src/costume_switcher.cpp
    src/xbox_live_bypass.cpp
)

if(WIN32)
    add_executable(re_cherry WIN32 ${RECHERRY_SOURCES})
else()
    add_executable(re_cherry ${RECHERRY_SOURCES})
endif()

rexglue_setup_target(re_cherry)

# imgui headers ship inside the SDK tree but are not added to the include
# path by rexglue_setup_target; src/counter.h includes imgui.h directly,
# so add them explicitly (same fix as Pacific Rim).
if(REXSDK_DIR)
    target_include_directories(re_cherry PRIVATE
        "${REXSDK_DIR}/thirdparty/imgui"
    )
endif()

if(TARGET imgui::imgui)
    target_link_libraries(re_cherry PRIVATE imgui::imgui)
elseif(TARGET imgui)
    target_link_libraries(re_cherry PRIVATE imgui)
endif()
