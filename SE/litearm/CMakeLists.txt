cmake_minimum_required(VERSION 3.5)

project(litearm)

find_package(ament_cmake REQUIRED)

foreach(dir config launch meshes urdf rviz)
  install(DIRECTORY ${dir}/
    DESTINATION share/${PROJECT_NAME}/${dir})
endforeach()

ament_package()
