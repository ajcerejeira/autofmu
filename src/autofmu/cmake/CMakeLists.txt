cmake_minimum_required(VERSION 3.10)
project(${CMAKE_PROJECT_NAME})
add_library(${CMAKE_PROJECT_NAME} SHARED sources/fmi2Functions.c)
set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "")
