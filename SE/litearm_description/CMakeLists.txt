cmake_minimum_required(VERSION 3.8)
project(litearm_description)

find_package(ament_cmake REQUIRED)

# 安装资源目录到 share/litearm_description 下，供 package:// 与 launch 使用
install(
  DIRECTORY config launch meshes urdf rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
