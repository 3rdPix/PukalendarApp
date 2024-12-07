cmake_minimum_required(VERSION 3.16)
project(PukalendarApp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Establece el directorio de salida para los binarios y otros archivos de compilación
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Encuentra Qt6 con los componentes necesarios
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

# Encuentra todos los archivos .cxx y .h recursivamente
file(GLOB_RECURSE SOURCES "src/*.cxx")
file(GLOB_RECURSE HEADERS "src/*.h")
qt_wrap_cpp(MOC_FILES ${HEADERS})

# Crear el ejecutable a partir de todos los archivos fuente
add_executable(PukalendarApp ${SOURCES} ${HEADERS} ${MOC_FILES})

target_include_directories(PukalendarApp PRIVATE src)
# Enlazar las bibliotecas de Qt necesarias
target_link_libraries(PukalendarApp PRIVATE Qt6::Core Qt6::Gui Qt6::Widgets)

# Copiar recursos en la carpeta build
file(COPY resources/images DESTINATION ${CMAKE_BINARY_DIR}/img)
file(COPY resources/qss DESTINATION ${CMAKE_BINARY_DIR}/qss)
file(COPY resources/locale DESTINATION ${CMAKE_BINARY_DIR}/locale)


