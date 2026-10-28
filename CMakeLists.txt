cmake_minimum_required(VERSION 3.21)
project(samsho2 VERSION 0.1.0 LANGUAGES C CXX)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# SDL2 gives the player its window, sound and gamepads.  On Windows the
# official SDL2 VC development package is expected under deps/sdl2/<ver>/;
# pass -DSAMSHO2_BUNDLED_SDL2=OFF to use another one (for example
# -DSDL2_DIR=<...>/cmake).  Without SDL2 the player still builds,
# headless-only.  The bundled copy wins over a registry/prefix hit, which on
# a machine with MSYS2 installed can otherwise pick up a MinGW build that
# cannot link with the MSVC toolchain.
option(SAMSHO2_BUNDLED_SDL2 "Prefer the SDL2 development package in deps/sdl2" ON)
if(WIN32 AND SAMSHO2_BUNDLED_SDL2)
    file(GLOB samsho2_sdl_cmake "${CMAKE_CURRENT_SOURCE_DIR}/deps/sdl2/*/cmake/sdl2-config.cmake")
    if(samsho2_sdl_cmake)
        list(GET samsho2_sdl_cmake 0 samsho2_sdl_config)
        get_filename_component(samsho2_sdl_dir "${samsho2_sdl_config}" DIRECTORY)
        set(SDL2_DIR "${samsho2_sdl_dir}" CACHE PATH "SDL2 CMake package directory" FORCE)
        list(APPEND CMAKE_PREFIX_PATH "${samsho2_sdl_dir}")
        message(STATUS "samsho2: using bundled SDL2 at ${samsho2_sdl_dir}")
    endif()
endif()

# The neogeorecomp toolkit: the vendored copy (a submodule in a clean
# checkout), or a checkout next to this project.
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/neogeorecomp/CMakeLists.txt)
    set(ng_default ${CMAKE_CURRENT_SOURCE_DIR}/neogeorecomp)
else()
    set(ng_default ${CMAKE_CURRENT_SOURCE_DIR}/../neogeorecomp)
endif()
set(NEOGEORECOMP_DIR ${ng_default} CACHE PATH "neogeorecomp checkout")
add_subdirectory(${NEOGEORECOMP_DIR} neogeorecomp_build)

# Your ROM files: the MAME "samsho2" set and the required "neogeo" system
# ROMs (sp-s2.sp1, sfix.sfix, sm1.sm1, 000-lo.lo), unzipped into one
# directory.  Without this the player builds interpreter-only.
set(SAMSHO2_ROM_DIR "" CACHE PATH "Directory with your samsho2 and Neo Geo BIOS ROM files")
# Optional: entry points a previous run found at runtime (--dump-misses).
set(SAMSHO2_ENTRIES "${CMAKE_BINARY_DIR}/entries.txt" CACHE FILEPATH "Extra entry points for the recompiler")

# Stage 1: the generator.
add_executable(samsho2_recomp src/recomp_main.c src/game.c)
target_link_libraries(samsho2_recomp PRIVATE m68krecomp_core)
target_include_directories(samsho2_recomp PRIVATE src)

# Stage 2: the player, with the generated C when ROMs are available.
set(GAME_SOURCES src/main.c)
set(GEN_DIR ${CMAKE_BINARY_DIR}/generated)
set(GEN_FILES 16)
if(SAMSHO2_ROM_DIR)
    set(GEN_SOURCES ${GEN_DIR}/recomp_table.c)
    math(EXPR last "${GEN_FILES} - 1")
    foreach(i RANGE ${last})
        if(i LESS 10)
            list(APPEND GEN_SOURCES ${GEN_DIR}/recomp_0${i}.c)
        else()
            list(APPEND GEN_SOURCES ${GEN_DIR}/recomp_${i}.c)
        endif()
    endforeach()
    # The entry list starts empty; the `profile` target fills it from a
    # scripted play session and the next build regenerates with it.
    if(NOT EXISTS ${SAMSHO2_ENTRIES})
        file(WRITE ${SAMSHO2_ENTRIES} "")
    endif()
    file(MAKE_DIRECTORY ${GEN_DIR})
    add_custom_command(
        OUTPUT ${GEN_SOURCES} ${GEN_DIR}/recomp_common.h
        COMMAND samsho2_recomp --rom-path ${SAMSHO2_ROM_DIR} --out ${GEN_DIR} --files ${GEN_FILES}
                --entries ${SAMSHO2_ENTRIES}
        DEPENDS samsho2_recomp ${SAMSHO2_ENTRIES}
        COMMENT "Recompiling samsho2 from ${SAMSHO2_ROM_DIR}")
    list(APPEND GAME_SOURCES ${GEN_SOURCES})
endif()

add_executable(samsho2 ${GAME_SOURCES} src/game.c)
set_target_properties(samsho2 PROPERTIES OUTPUT_NAME "Samsho2")
target_link_libraries(samsho2 PRIVATE neogeorecomp)
target_include_directories(samsho2 PRIVATE src ${GEN_DIR})
if(SAMSHO2_ROM_DIR)
    # Play the scripted sessions and record the entry points that only show
    # up at runtime (computed jumps into unrolled code), then rebuild.
    add_custom_target(profile
        COMMAND $<TARGET_FILE:samsho2> --headless --rom-path ${SAMSHO2_ROM_DIR} --frames 6000 --dump-misses ${SAMSHO2_ENTRIES}
        COMMAND $<TARGET_FILE:samsho2> --headless --rom-path ${SAMSHO2_ROM_DIR} --frames 24000
                --input ${CMAKE_CURRENT_SOURCE_DIR}/tests/play_long.txt --dump-misses ${SAMSHO2_ENTRIES}
        DEPENDS samsho2
        COMMENT "Profiling a scripted session for runtime-only entry points")
    # Correctness: re-run every native block in Musashi and compare.
    add_custom_target(verify
        COMMAND $<TARGET_FILE:samsho2> --headless --verify --rom-path ${SAMSHO2_ROM_DIR} --frames 3000
                --input ${CMAKE_CURRENT_SOURCE_DIR}/tests/coin_start.txt
        DEPENDS samsho2
        COMMENT "Verifying recompiled blocks against Musashi")
    target_compile_definitions(samsho2 PRIVATE SAMSHO2_HAVE_RECOMP)
    if(MSVC)
        # Generated routines are large; /bigobj lifts the section limit.
        # /O1 /Ob1 keeps the giant dispatch functions tractable: MSVC's
        # optimizer grows superlinearly with them at /O2.
        set_source_files_properties(${GEN_SOURCES} PROPERTIES COMPILE_OPTIONS "/bigobj;/O1;/Ob1")
    elseif(CMAKE_C_COMPILER_ID MATCHES "Clang")
        set_source_files_properties(${GEN_SOURCES} PROPERTIES COMPILE_OPTIONS "-O2")
    else()
        # GCC: -O2 keeps the giant dispatch functions tractable; -O3 is
        # superlinear on them and gains little for this kind of code.
        set_source_files_properties(${GEN_SOURCES} PROPERTIES COMPILE_OPTIONS "-O2")
    endif()
endif()
if(MSVC)
    target_compile_definitions(samsho2 PRIVATE _CRT_SECURE_NO_WARNINGS)
    target_compile_definitions(samsho2_recomp PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()

# Ship the SDL2 DLL (when the window is built) next to the executable.
if(WIN32 AND TARGET SDL2::SDL2)
    add_custom_command(TARGET samsho2 POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_RUNTIME_DLLS:samsho2> $<TARGET_FILE_DIR:samsho2>
        COMMAND_EXPAND_LISTS)
endif()
