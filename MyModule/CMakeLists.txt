cmake_minimum_required(VERSION 3.5)

project(MyModule)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/MyModule")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "John Doe (AnyWare Corp.), Laura Lucendo (Universidad Carlos III de Madrid)")
set(EXTENSION_DESCRIPTION "This extension has been created as a tutorial for module creation				")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/MyModule.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/MyModule/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(MyModule)
add_subdirectory(MyModule2)
add_subdirectory(DiceCoefficient)
add_subdirectory(MyModule2)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
