---
title: CMake
date: 2021-06-11 14:10:48
tags: CMake
---



### A Basic Starting Point

```cmake
cmake_minimum_required(VERSION 3.10)

#set the project name
project(Tutorial)

#add the executable
add_executable(Tutorial tutorial.cxx)
```

The source code for `tutorial.cxx` is provided in the `Step1` directory .

#### Adding a Version Number and Configured Header File

The first feature we will add is to provide our executable and project with a version number.

```cmake
cmake_minimum_required(VERSION 3.10)

# set the project name and version
project(Tutorial VERSION 1.0)
```

Then, configure a header file to pass the version number to the source code:

```cmake
configure_file(TutorialConfig.h.in TutorialConfig.h)
```

Since the configured file will be written into the binary tree, we must add that directory to the list of paths to search for include files. Add the following lines to the end of the `CMakeLists.txt` file:

```cmake
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )
```

create `TutorialConfig.h.in` in the source directory with the following contents:

```c
// the configured options and settings for Tutorial
#define Tutorial_VERSION_MAJOR @Tutorial_VERSION_MAJOR@
#define Tutorial_VERSION_MINOR @Tutorial_VERSION_MINOR@
```

Next modify `tutorial.cxx` to include the configured header file, `TutorialConfig.h`.

Finally, let's print out the executable name and version number by updating `tutorial.cxx` as follows:

```c++
if (argc < 2) {
    // report version
    std::cout << argv[0] << " Version " << Tutorial_VERSION_MAJOR << "."
              << Tutorial_VERSION_MINOR << std::endl;
    std::cout << "Usage: " << argv[0] << " number" << std::endl;
    return 1;
  }
```

#### Specify the C++ Standard

We will need to explicitly state in the CMake code that it should use the correct flags. 

The easiest way to enable support for a specific C++ standard in CMake is by using the [`CMAKE_CXX_STANDARD`](https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_STANDARD.html#variable:CMAKE_CXX_STANDARD) variable. 

For this tutorial, set the [`CMAKE_CXX_STANDARD`](https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_STANDARD.html#variable:CMAKE_CXX_STANDARD) variable in the `CMakeLists.txt` file to 11 and [`CMAKE_CXX_STANDARD_REQUIRED`](https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_STANDARD_REQUIRED.html#variable:CMAKE_CXX_STANDARD_REQUIRED) to True. 

Make sure to add the `CMAKE_CXX_STANDARD` declarations above the call to `add_executable`.

```cmake
cmake_minimum_required(VERSION 3.10)

# set the project name and version
project(Tutorial VERSION 1.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
```

#### Build and Test

Run the [`cmake`](https://cmake.org/cmake/help/latest/manual/cmake.1.html#manual:cmake(1)) executable

For example, from the command line we could navigate to the `Help/guide/tutorial` directory of the CMake source code tree and create a build directory:

```shell
mkdir step1_build
```

Next, navigate to the build directory and run CMake to configure the project and generate a native build system:

```shell
cd step1_build
cmake ../step1
```

Then call that build system to actually compile/link the project:

```shell
cmake --build .
```

### Adding a Library 

For this tutorial we will put the library into a subdirectory called `MathFunctions`. 

This directory already contains a header file, `MathFunctions.h`, and a source file `mysqrt.cxx`. 

The source file has one function called `mysqrt` that provides similar functionality to the compiler's `sqrt` function.

Add the following one line `CMakeLists.txt` file to the `MathFunctions` directory:

```cmake
add_library(MathFunctions mysqrt.cxx)
```

To make use of the new library we will add an [`add_subdirectory()`](https://cmake.org/cmake/help/latest/command/add_subdirectory.html#command:add_subdirectory) call in the top-level `CMakeLists.txt` file so that the library will get built. 

We add the new library to the executable, and add `MathFunctions` as an include directory so that the `mysqrt.h` header file can be found. 

The last few lines of the top-level `CMakeLists.txt` file should now look like:

```cmake
# add the MathFunctions library
add_subdirectory(MathFunctions)

# add the executable
add_executable(Tutorial tutorial.cxx)

target_link_libraries(Tutorial PUBLIC MathFunctions)

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                          "${PROJECT_BINARY_DIR}"
                          "${PROJECT_SOURCE_DIR}/MathFunctions"
                          )
```

Now let us make the MathFunctions library optional. 

While for the tutorial there really isn't any need to do so, for larger projects this is a common occurrence. 

The first step is to add an option to the top-level `CMakeLists.txt` file.

```cmake
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(TutorialConfig.h.in TutorialConfig.h)
```

This option will be displayed in the [`cmake-gui`](https://cmake.org/cmake/help/latest/manual/cmake-gui.1.html#manual:cmake-gui(1)) and [`ccmake`](https://cmake.org/cmake/help/latest/manual/ccmake.1.html#manual:ccmake(1)) with a default value of ON that can be changed by the user. This setting will be stored in the cache so that the user does not need to set the value each time they run CMake on a build directory.

The next change is to make building and linking the MathFunctions library conditional. To do this we change the end of the top-level `CMakeLists.txt` file to look like the following:

```cmake
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
  list(APPEND EXTRA_INCLUDES "${PROJECT_SOURCE_DIR}/MathFunctions")
endif()

# add the executable
add_executable(Tutorial tutorial.cxx)

target_link_libraries(Tutorial PUBLIC ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           ${EXTRA_INCLUDES}
                           )
```

Note the use of the variable `EXTRA_LIBS` to collect up any optional libraries to later be linked into the executable. 

The variable `EXTRA_INCLUDES` is used similarly for optional header files. 

This is a classic approach when dealing with many optional components, we will cover the modern approach in the next step.

The corresponding changes to the source code are fairly straightforward. 

First, in `tutorial.cxx`, include the `MathFunctions.h` header if we need it:

```c
#ifdef USE_MYMATH
#  include "MathFunctions.h"
#endif
```

Then, in the same file, make `USE_MYMATH` control which square root function is used:

```C
#ifdef USE_MYMATH
  const double outputValue = mysqrt(inputValue);
#else
  const double outputValue = sqrt(inputValue);
#endif
```

Since the source code now requires `USE_MYMATH` we can add it to `TutorialConfig.h.in` with the following line:

```c
#cmakedefine USE_MYMATH
```

Run the [`cmake`](https://cmake.org/cmake/help/latest/manual/cmake.1.html#manual:cmake(1)) executable or the [`cmake-gui`](https://cmake.org/cmake/help/latest/manual/cmake-gui.1.html#manual:cmake-gui(1)) to configure the project and then build it with your chosen build tool. Then run the built Tutorial executable.

Now let's update the value of `USE_MYMATH`. The easiest way is to use the [`cmake-gui`](https://cmake.org/cmake/help/latest/manual/cmake-gui.1.html#manual:cmake-gui(1)) or [`ccmake`](https://cmake.org/cmake/help/latest/manual/ccmake.1.html#manual:ccmake(1)) if you're in the terminal. Or, alternatively, if you want to change the option from the command-line, try:

```shell
cmake ../Step2 -DUSE_MYMATH=OFF
```

### Adding Usage Requirements for Library

Usage requirements allow for far better control over a library or executable's link and include line while also giving more control over the transitive property of targets inside CMake. 

The primary commands that leverage usage requirements are:

- target_compile_definitions()
- target_compile_options()
- target_include_directories()
- target_link_libraries()

Let's refactor our code from Adding a Library to use the modern CMake approach of usage requirements. 

We first state that anybody linking to MathFunctions needs to include the current source directory, while MathFunctions itself doesn't. 

So this can become an `INTERFACE` usage requirement.

Remember `INTERFACE` means things that consumers require but the producer doesn't. // ???? 

Add the following lines to the end of `MathFunctions/CMakeLists.txt`:

```cmake
target_include_directories(MathFunctions
          INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
          )
```

Now that we've specified usage requirements for MathFunctions we can safely remove our uses of the `EXTRA_INCLUDES` variable from the top-level `CMakeLists.txt`, here:

```cmake
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
endif()
```

And here:

```cmake
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )
```

### Installing and Testing

#### Install Rules

The install rules are fairly simple: 

for MathFunctions we want to install the library and header file and 

for the application we want to install the executable and configured header.

So to the end of `MathFunctions/CMakeLists.txt` we add:

```cmake
install(TARGETS MathFunctions DESTINATION lib)
install(FILES MathFunctions.h DESTINATION include)
```

And to the end of the top-level `CMakeLists.txt` we add:

```cmake
install(TARGETS Tutorial DESTINATION bin)
install(FILES "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  DESTINATION include
  )
```

That is all that is needed to create a basic local install of the tutorial.

Then run the install step by using the `install` option of the [`cmake`](https://cmake.org/cmake/help/latest/manual/cmake.1.html#manual:cmake(1)) command (introduced in 3.15, older versions of CMake must use `make install`) from the command line. For multi-configuration tools, don't forget to use the `--config` argument to specify the configuration. If using an IDE, simply build the `INSTALL` target. This step will install the appropriate header files, libraries, and executables. For example:

```cmake
cmake --install .
```

The CMake variable [`CMAKE_INSTALL_PREFIX`](https://cmake.org/cmake/help/latest/variable/CMAKE_INSTALL_PREFIX.html#variable:CMAKE_INSTALL_PREFIX) is used to determine the root of where the files will be installed. If using the `cmake --install` command, the installation prefix can be overridden via the `--prefix` argument. For example:

```cmake
cmake --install . --prefix "/home/myuser/installdir"
```

#### Testing Support

Next let's test our application. At the end of the top-level `CMakeLists.txt` file we can enable testing and then add a number of basic tests to verify that the application is working correctly.

```cmake
enable_testing()

# does the application run
add_test(NAME Runs COMMAND Tutorial 25)

# does the usage message work?
add_test(NAME Usage COMMAND Tutorial)
set_tests_properties(Usage
  PROPERTIES PASS_REGULAR_EXPRESSION "Usage:.*number"
  )

# define a function to simplify adding tests
function(do_test target arg result)
  add_test(NAME Comp${arg} COMMAND ${target} ${arg})
  set_tests_properties(Comp${arg}
    PROPERTIES PASS_REGULAR_EXPRESSION ${result}
    )
endfunction(do_test)

# do a bunch of result based tests
do_test(Tutorial 4 "4 is 2")
do_test(Tutorial 9 "9 is 3")
do_test(Tutorial 5 "5 is 2.236")
do_test(Tutorial 7 "7 is 2.645")
do_test(Tutorial 25 "25 is 5")
do_test(Tutorial -25 "-25 is [-nan|nan|0]")
do_test(Tutorial 0.0001 "0.0001 is 0.01")
```

The first test simply verifies that the application runs, does not segfault or otherwise crash, and has a zero return value. This is the basic form of a CTest test.

The next test makes use of the [`PASS_REGULAR_EXPRESSION`](https://cmake.org/cmake/help/latest/prop_test/PASS_REGULAR_EXPRESSION.html#prop_test:PASS_REGULAR_EXPRESSION) test property to verify that the output of the test contains certain strings. In this case, verifying that the usage message is printed when an incorrect number of arguments are provided.

Lastly, we have a function called `do_test` that runs the application and verifies that the computed square root is correct for given input. For each invocation of `do_test`, another test is added to the project with a name, input, and expected results based on the passed arguments.

Rebuild the application and then cd to the binary directory and run the [`ctest`](https://cmake.org/cmake/help/latest/manual/ctest.1.html#manual:ctest(1)) executable: `ctest -N` and `ctest -VV`. For multi-config generators (e.g. Visual Studio), the configuration type must be specified. To run tests in Debug mode, for example, use `ctest -C Debug -VV` from the build directory (not the Debug subdirectory!). Alternatively, build the `RUN_TESTS` target from the IDE.

### Adding System Introspection

If the platform has `log` and `exp` then we will use them to compute the square root in the `mysqrt` function. We first test for the availability of these functions using the [`CheckSymbolExists`](https://cmake.org/cmake/help/latest/module/CheckSymbolExists.html#module:CheckSymbolExists) module in `MathFunctions/CMakeLists.txt`. On some platforms, we will need to link to the m library. If `log` and `exp` are not initially found, require the m library and try again.

```cmake
include(CheckSymbolExists)
check_symbol_exists(log "math.h" HAVE_LOG)
check_symbol_exists(exp "math.h" HAVE_EXP)
if(NOT (HAVE_LOG AND HAVE_EXP))
  unset(HAVE_LOG CACHE)
  unset(HAVE_EXP CACHE)
  set(CMAKE_REQUIRED_LIBRARIES "m")
  check_symbol_exists(log "math.h" HAVE_LOG)
  check_symbol_exists(exp "math.h" HAVE_EXP)
  if(HAVE_LOG AND HAVE_EXP)
    target_link_libraries(MathFunctions PRIVATE m)
  endif()
endif()
```

If available, use [`target_compile_definitions()`](https://cmake.org/cmake/help/latest/command/target_compile_definitions.html#command:target_compile_definitions) to specify `HAVE_LOG` and `HAVE_EXP` as `PRIVATE` compile definitions.

```cmake
if(HAVE_LOG AND HAVE_EXP)
  target_compile_definitions(MathFunctions
                             PRIVATE "HAVE_LOG" "HAVE_EXP")
endif()
```

If `log` and `exp` are available on the system, then we will use them to compute the square root in the `mysqrt` function. Add the following code to the `mysqrt` function in `MathFunctions/mysqrt.cxx` (don't forget the `#endif` before returning the result!):

```c
#if defined(HAVE_LOG) && defined(HAVE_EXP)
  double result = exp(log(x) * 0.5);
  std::cout << "Computing sqrt of " << x << " to be " << result
            << " using log and exp" << std::endl;
#else
  double result = x;
```

We will also need to modify `mysqrt.cxx` to include `cmath`.

```c
#include <cmath>
```

### Adding a Custom Command and Generated File

Suppose, for the purpose of this tutorial, we decide that we never want to use the platform `log` and `exp` functions and instead would like to generate a table of precomputed values to use in the `mysqrt` function. In this section, we will create the table as part of the build process, and then compile that table into our application.

First, let's remove the check for the `log` and `exp` functions in `MathFunctions/CMakeLists.txt`. Then remove the check for `HAVE_LOG` and `HAVE_EXP` from `mysqrt.cxx`. At the same time, we can remove `#include <cmath>`.

In the `MathFunctions` subdirectory, a new source file named `MakeTable.cxx` has been provided to generate the table.

After reviewing the file, we can see that the table is produced as valid C++ code and that the output filename is passed in as an argument.

The next step is to add the appropriate commands to the `MathFunctions/CMakeLists.txt` file to build the MakeTable executable and then run it as part of the build process. A few commands are needed to accomplish this.

First, at the top of `MathFunctions/CMakeLists.txt`, the executable for `MakeTable` is added as any other executable would be added.

```cmake
add_executable(MakeTable MakeTable.cxx)
```

Then we add a custom command that specifies how to produce `Table.h` by running MakeTable.

```cmake
add_custom_command(
  OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/Table.h
  COMMAND MakeTable ${CMAKE_CURRENT_BINARY_DIR}/Table.h
  DEPENDS MakeTable
  )
```

Next we have to let CMake know that `mysqrt.cxx` depends on the generated file `Table.h`. This is done by adding the generated `Table.h` to the list of sources for the library MathFunctions.

```cmake
add_library(MathFunctions
            mysqrt.cxx
            ${CMAKE_CURRENT_BINARY_DIR}/Table.h
            )
```

We also have to add the current binary directory to the list of include directories so that `Table.h` can be found and included by `mysqrt.cxx`.

```cmake
target_include_directories(MathFunctions
          INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
          PRIVATE ${CMAKE_CURRENT_BINARY_DIR}
          )
```

Now let's use the generated table. First, modify `mysqrt.cxx` to include `Table.h`. Next, we can rewrite the mysqrt function to use the table:

```c
double mysqrt(double x)
{
  if (x <= 0) {
    return 0;
  }

  // use the table to help find an initial value
  double result = x;
  if (x >= 1 && x < 10) {
    std::cout << "Use the table to help find an initial value " << std::endl;
    result = sqrtTable[static_cast<int>(x)];
  }

  // do ten iterations
  for (int i = 0; i < 10; ++i) {
    if (result <= 0) {
      result = 0.1;
    }
    double delta = x - (result * result);
    result = result + 0.5 * delta / result;
    std::cout << "Computing sqrt of " << x << " to be " << result << std::endl;
  }

  return result;
}
```

Run the [`cmake`](https://cmake.org/cmake/help/latest/manual/cmake.1.html#manual:cmake(1)) executable or the [`cmake-gui`](https://cmake.org/cmake/help/latest/manual/cmake-gui.1.html#manual:cmake-gui(1)) to configure the project and then build it with your chosen build tool.

When this project is built it will first build the `MakeTable` executable. It will then run `MakeTable` to produce `Table.h`. Finally, it will compile `mysqrt.cxx` which includes `Table.h` to produce the MathFunctions library.

Run the Tutorial executable and verify that it is using the table.



### Building an Installer 

Next suppose that we want to distribute our project to other people so that they can use it.

 We want to provide both binary and source distributions on a variety of platforms. 

This is a little different from the install we did previously in Installing and Testing , where we were installing the binaries that we had built from the source code. 

In this example we will be building installation packages that support binary installations and package management features. 

To accomplish this we will use CPack to create platform specific installers. Specifically we need to add a few lines to the bottom of our top-level `CMakeLists.txt` file.

```cmake
include(InstallRequiredSystemLibraries)
set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/License.txt")
set(CPACK_PACKAGE_VERSION_MAJOR "${Tutorial_VERSION_MAJOR}")
set(CPACK_PACKAGE_VERSION_MINOR "${Tutorial_VERSION_MINOR}")
include(CPack)
```

That is all there is to it. We start by including [`InstallRequiredSystemLibraries`](https://cmake.org/cmake/help/latest/module/InstallRequiredSystemLibraries.html#module:InstallRequiredSystemLibraries). 

This module will include any runtime libraries that are needed by the project for the current platform. 

Next we set some CPack variables to where we have stored the license and version information for this project. 

The version information was set earlier in this tutorial and the `license.txt` has been included in the top-level source directory for this step.

Finally we include the [`CPack module`](https://cmake.org/cmake/help/latest/module/CPack.html#module:CPack) which will use these variables and some other properties of the current system to setup an installer.

The next step is to build the project in the usual manner and then run the [`cpack`](https://cmake.org/cmake/help/latest/manual/cpack.1.html#manual:cpack(1)) executable. 

To build a binary distribution, from the binary directory run:

```shell
cpack
```

To specify the generator, use the `-G` option. For multi-config builds, use `-C` to specify the configuration. For example:

```shell
cpack -G ZIP -C Debug
```

To create a source distribution you would type:

```shell
cpack --config CPackSourceConfig.cmake
```

Alternatively, run `make package` or right click the `Package` target and `Build Project` from an IDE.

Run the installer found in the binary directory. Then run the installed executable and verify that it works.

### Adding Support for a Dashboard

Adding support for submitting our test results to a dashboard is simple. 

We already defined a number of tests for our project in [Testing Support](https://cmake.org/cmake/help/latest/guide/tutorial/index.html#testing-support). 

Now we just have to run those tests and submit them to a dashboard. 

To include support for dashboards we include the [`CTest`](https://cmake.org/cmake/help/latest/module/CTest.html#module:CTest) module in our top-level `CMakeLists.txt`.

Replace:

```cmake
# enable testing
enable_testing()
```

With:

```cmake
# enable dashboard scripting
include(CTest)
```

The [`CTest`](https://cmake.org/cmake/help/latest/module/CTest.html#module:CTest) module will automatically call `enable_testing()`, so we can remove it from our CMake files.

We will also need to create a `CTestConfig.cmake` file in the top-level directory where we can specify the name of the project and where to submit the dashboard.

```cmake
set(CTEST_PROJECT_NAME "CMakeTutorial")
set(CTEST_NIGHTLY_START_TIME "00:00:00 EST")

set(CTEST_DROP_METHOD "http")
set(CTEST_DROP_SITE "my.cdash.org")
set(CTEST_DROP_LOCATION "/submit.php?project=CMakeTutorial")
set(CTEST_DROP_SITE_CDASH TRUE)
```

The [`ctest`](https://cmake.org/cmake/help/latest/manual/ctest.1.html#manual:ctest(1)) executable will read in this file when it runs. To create a simple dashboard you can run the [`cmake`](https://cmake.org/cmake/help/latest/manual/cmake.1.html#manual:cmake(1)) executable or the [`cmake-gui`](https://cmake.org/cmake/help/latest/manual/cmake-gui.1.html#manual:cmake-gui(1)) to configure the project, but do not build it yet. Instead, change directory to the binary tree, and then run:

> ctest [-VV] -D Experimental

Remember, for multi-config generators (e.g. Visual Studio), the configuration type must be specified:

```shell
ctest [-VV] -C Debug -D Experimental
```

Or, from an IDE, build the `Experimental` target.

The [`ctest`](https://cmake.org/cmake/help/latest/manual/ctest.1.html#manual:ctest(1)) executable will build and test the project and submit the results to Kitware's public dashboard: https://my.cdash.org/index.php?project=CMakeTutorial.

### Mixing Static and Shared

In this section we will show how the [`BUILD_SHARED_LIBS`](https://cmake.org/cmake/help/latest/variable/BUILD_SHARED_LIBS.html#variable:BUILD_SHARED_LIBS) variable can be used to control the default behavior of [`add_library()`](https://cmake.org/cmake/help/latest/command/add_library.html#command:add_library), and allow control over how libraries without an explicit type (`STATIC`, `SHARED`, `MODULE` or `OBJECT`) are built.

To accomplish this we need to add [`BUILD_SHARED_LIBS`](https://cmake.org/cmake/help/latest/variable/BUILD_SHARED_LIBS.html#variable:BUILD_SHARED_LIBS) to the top-level `CMakeLists.txt`. We use the [`option()`](https://cmake.org/cmake/help/latest/command/option.html#command:option) command as it allows users to optionally select if the value should be ON or OFF.

Next we are going to refactor MathFunctions to become a real library that encapsulates using `mysqrt` or `sqrt`, instead of requiring the calling code to do this logic. This will also mean that `USE_MYMATH` will not control building MathFunctions, but instead will control the behavior of this library.

The first step is to update the starting section of the top-level `CMakeLists.txt` to look like:

```cmake
cmake_minimum_required(VERSION 3.10)

# set the project name and version
project(Tutorial VERSION 1.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# control where the static and shared libraries are built so that on windows
# we don't need to tinker with the path to run the executable
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}")

option(BUILD_SHARED_LIBS "Build using shared libraries" ON)

# configure a header file to pass the version number only
configure_file(TutorialConfig.h.in TutorialConfig.h)

# add the MathFunctions library
add_subdirectory(MathFunctions)

# add the executable
add_executable(Tutorial tutorial.cxx)
target_link_libraries(Tutorial PUBLIC MathFunctions)
```

Now that we have made MathFunctions always be used, we will need to update the logic of that library. So, in `MathFunctions/CMakeLists.txt` we need to create a SqrtLibrary that will conditionally be built and installed when `USE_MYMATH` is enabled. Now, since this is a tutorial, we are going to explicitly require that SqrtLibrary is built statically.

The end result is that `MathFunctions/CMakeLists.txt` should look like:

```cmake
# add the library that runs
add_library(MathFunctions MathFunctions.cxx)

# state that anybody linking to us needs to include the current source dir
# to find MathFunctions.h, while we don't.
target_include_directories(MathFunctions
                           INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
                           )

# should we use our own math functions
option(USE_MYMATH "Use tutorial provided math implementation" ON)
if(USE_MYMATH)

  target_compile_definitions(MathFunctions PRIVATE "USE_MYMATH")

  # first we add the executable that generates the table
  add_executable(MakeTable MakeTable.cxx)

  # add the command to generate the source code
  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/Table.h
    COMMAND MakeTable ${CMAKE_CURRENT_BINARY_DIR}/Table.h
    DEPENDS MakeTable
    )

  # library that just does sqrt
  add_library(SqrtLibrary STATIC
              mysqrt.cxx
              ${CMAKE_CURRENT_BINARY_DIR}/Table.h
              )

  # state that we depend on our binary dir to find Table.h
  target_include_directories(SqrtLibrary PRIVATE
                             ${CMAKE_CURRENT_BINARY_DIR}
                             )

  target_link_libraries(MathFunctions PRIVATE SqrtLibrary)
endif()

# define the symbol stating we are using the declspec(dllexport) when
# building on windows
target_compile_definitions(MathFunctions PRIVATE "EXPORTING_MYMATH")

# install rules
set(installable_libs MathFunctions)
if(TARGET SqrtLibrary)
  list(APPEND installable_libs SqrtLibrary)
endif()
install(TARGETS ${installable_libs} DESTINATION lib)
install(FILES MathFunctions.h DESTINATION include)
```

Next, update `MathFunctions/mysqrt.cxx` to use the `mathfunctions` and `detail` namespaces:

```c++
#include <iostream>

#include "MathFunctions.h"

// include the generated table
#include "Table.h"

namespace mathfunctions {
namespace detail {
// a hack square root calculation using simple operations
double mysqrt(double x)
{
  if (x <= 0) {
    return 0;
  }

  // use the table to help find an initial value
  double result = x;
  if (x >= 1 && x < 10) {
    std::cout << "Use the table to help find an initial value " << std::endl;
    result = sqrtTable[static_cast<int>(x)];
  }

  // do ten iterations
  for (int i = 0; i < 10; ++i) {
    if (result <= 0) {
      result = 0.1;
    }
    double delta = x - (result * result);
    result = result + 0.5 * delta / result;
    std::cout << "Computing sqrt of " << x << " to be " << result << std::endl;
  }

  return result;
}
}
}
```

We also need to make some changes in `tutorial.cxx`, so that it no longer uses `USE_MYMATH`:

1. Always include `MathFunctions.h`
2. Always use `mathfunctions::sqrt`
3. Don't include cmath

Finally, update `MathFunctions/MathFunctions.h` to use dll export defines:

```c++
#if defined(_WIN32)
#  if defined(EXPORTING_MYMATH)
#    define DECLSPEC __declspec(dllexport)
#  else
#    define DECLSPEC __declspec(dllimport)
#  endif
#else // non windows
#  define DECLSPEC
#endif

namespace mathfunctions {
double DECLSPEC sqrt(double x);
}
```

At this point, if you build everything, you may notice that linking fails as we are combining a static library without position independent code with a library that has position independent code. The solution to this is to explicitly set the [`POSITION_INDEPENDENT_CODE`](https://cmake.org/cmake/help/latest/prop_tgt/POSITION_INDEPENDENT_CODE.html#prop_tgt:POSITION_INDEPENDENT_CODE) target property of SqrtLibrary to be True no matter the build type.

```cmake
# state that SqrtLibrary need PIC when the default is shared libraries
  set_target_properties(SqrtLibrary PROPERTIES
                        POSITION_INDEPENDENT_CODE ${BUILD_SHARED_LIBS}
                        )

  target_link_libraries(MathFunctions PRIVATE SqrtLibrary)
```

### Adding Generator Expressions 

[`Generator expressions`](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#manual:cmake-generator-expressions(7)) are evaluated during build system generation to produce information specific to each build configuration.

[`Generator expressions`](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#manual:cmake-generator-expressions(7)) are allowed in the context of many target properties, such as [`LINK_LIBRARIES`](https://cmake.org/cmake/help/latest/prop_tgt/LINK_LIBRARIES.html#prop_tgt:LINK_LIBRARIES), [`INCLUDE_DIRECTORIES`](https://cmake.org/cmake/help/latest/prop_tgt/INCLUDE_DIRECTORIES.html#prop_tgt:INCLUDE_DIRECTORIES), [`COMPILE_DEFINITIONS`](https://cmake.org/cmake/help/latest/prop_tgt/COMPILE_DEFINITIONS.html#prop_tgt:COMPILE_DEFINITIONS) and others. They may also be used when using commands to populate those properties, such as [`target_link_libraries()`](https://cmake.org/cmake/help/latest/command/target_link_libraries.html#command:target_link_libraries), [`target_include_directories()`](https://cmake.org/cmake/help/latest/command/target_include_directories.html#command:target_include_directories), [`target_compile_definitions()`](https://cmake.org/cmake/help/latest/command/target_compile_definitions.html#command:target_compile_definitions) and others.
[`Generator expressions`](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#manual:cmake-generator-expressions(7)) may be used to enable conditional linking, conditional definitions used when compiling, conditional include directories and more. The conditions may be based on the build configuration, target properties, platform information or any other queryable information.

There are different types of [`generator expressions`](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#manual:cmake-generator-expressions(7)) including Logical, Informational, and Output expressions.

Logical expressions are used to create conditional output. The basic expressions are the 0 and 1 expressions. A `$<0:...>` results in the empty string, and `<1:...>` results in the content of "...". They can also be nested.

A common usage of [`generator expressions`](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#manual:cmake-generator-expressions(7)) is to conditionally add compiler flags, such as those for language levels or warnings. A nice pattern is to associate this information to an `INTERFACE` target allowing this information to propagate. Let's start by constructing an `INTERFACE` target and specifying the required C++ standard level of `11` instead of using [`CMAKE_CXX_STANDARD`](https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_STANDARD.html#variable:CMAKE_CXX_STANDARD).

So the following code:

```cmake
# specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
```

Would be replaced with:

```cmake
add_library(tutorial_compiler_flags INTERFACE)
target_compile_features(tutorial_compiler_flags INTERFACE cxx_std_11)
```

Next we add the desired compiler warning flags that we want for our project. As warning flags vary based on the compiler we use the `COMPILE_LANG_AND_ID` generator expression to control which flags to apply given a language and a set of compiler ids as seen below:

```cmake
set(gcc_like_cxx "$<COMPILE_LANG_AND_ID:CXX,ARMClang,AppleClang,Clang,GNU>")
set(msvc_cxx "$<COMPILE_LANG_AND_ID:CXX,MSVC>")
target_compile_options(tutorial_compiler_flags INTERFACE
  "$<${gcc_like_cxx}:$<BUILD_INTERFACE:-Wall;-Wextra;-Wshadow;-Wformat=2;-Wunused>>"
  "$<${msvc_cxx}:$<BUILD_INTERFACE:-W3>>"
)
```

Looking at this we see that the warning flags are encapsulated inside a `BUILD_INTERFACE` condition. This is done so that consumers of our installed project will not inherit our warning flags.

### Adding Export Configuration 

During [Installing and Testing (Step 4)](https://cmake.org/cmake/help/latest/guide/tutorial/index.html#installing-and-testing-step-4) of the tutorial we added the ability for CMake to install the library and headers of the project. During [Building an Installer (Step 7)](https://cmake.org/cmake/help/latest/guide/tutorial/index.html#building-an-installer-step-7) we added the ability to package up this information so it could be distributed to other people.

The next step is to add the necessary information so that other CMake projects can use our project, be it from a build directory, a local install or when packaged.

The first step is to update our [`install(TARGETS)`](https://cmake.org/cmake/help/latest/command/install.html#command:install) commands to not only specify a `DESTINATION` but also an `EXPORT`. The `EXPORT` keyword generates and installs a CMake file containing code to import all targets listed in the install command from the installation tree. So let's go ahead and explicitly `EXPORT` the MathFunctions library by updating the `install` command in `MathFunctions/CMakeLists.txt` to look like:

```cmake
set(installable_libs MathFunctions tutorial_compiler_flags)
if(TARGET SqrtLibrary)
  list(APPEND installable_libs SqrtLibrary)
endif()
install(TARGETS ${installable_libs}
        DESTINATION lib
        EXPORT MathFunctionsTargets)
install(FILES MathFunctions.h DESTINATION include)
```

Now that we have MathFunctions being exported, we also need to explicitly install the generated `MathFunctionsTargets.cmake` file. This is done by adding the following to the bottom of the top-level `CMakeLists.txt`:

```cmake
install(EXPORT MathFunctionsTargets
  FILE MathFunctionsTargets.cmake
  DESTINATION lib/cmake/MathFunctions
)
```

At this point you should try and run CMake. If everything is setup properly you will see that CMake will generate an error that looks like:

```shell
Target "MathFunctions" INTERFACE_INCLUDE_DIRECTORIES property contains
path:

  "/Users/robert/Documents/CMakeClass/Tutorial/Step11/MathFunctions"

which is prefixed in the source directory.
```

What CMake is trying to say is that during generating the export information it will export a path that is intrinsically tied to the current machine and will not be valid on other machines. The solution to this is to update the MathFunctions [`target_include_directories()`](https://cmake.org/cmake/help/latest/command/target_include_directories.html#command:target_include_directories) to understand that it needs different `INTERFACE` locations when being used from within the build directory and from an install / package. This means converting the [`target_include_directories()`](https://cmake.org/cmake/help/latest/command/target_include_directories.html#command:target_include_directories) call for MathFunctions to look like:

```cmake
target_include_directories(MathFunctions
                           INTERFACE
                            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
                            $<INSTALL_INTERFACE:include>
                           )
```

Once this has been updated, we can re-run CMake and verify that it doesn't warn anymore.

At this point, we have CMake properly packaging the target information that is required but we will still need to generate a `MathFunctionsConfig.cmake` so that the CMake [`find_package()`](https://cmake.org/cmake/help/latest/command/find_package.html#command:find_package) command can find our project. So let's go ahead and add a new file to the top-level of the project called `Config.cmake.in` with the following contents:

```cmake

@PACKAGE_INIT@

include ( "${CMAKE_CURRENT_LIST_DIR}/MathFunctionsTargets.cmake" )
```

Then, to properly configure and install that file, add the following to the bottom of the top-level `CMakeLists.txt`:

```cmake
install(EXPORT MathFunctionsTargets
  FILE MathFunctionsTargets.cmake
  DESTINATION lib/cmake/MathFunctions
)

include(CMakePackageConfigHelpers)
# generate the config file that is includes the exports
configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/Config.cmake.in
  "${CMAKE_CURRENT_BINARY_DIR}/MathFunctionsConfig.cmake"
  INSTALL_DESTINATION "lib/cmake/example"
  NO_SET_AND_CHECK_MACRO
  NO_CHECK_REQUIRED_COMPONENTS_MACRO
  )
# generate the version file for the config file
write_basic_package_version_file(
  "${CMAKE_CURRENT_BINARY_DIR}/MathFunctionsConfigVersion.cmake"
  VERSION "${Tutorial_VERSION_MAJOR}.${Tutorial_VERSION_MINOR}"
  COMPATIBILITY AnyNewerVersion
)

# install the configuration file
install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/MathFunctionsConfig.cmake
  DESTINATION lib/cmake/MathFunctions
  )
```

At this point, we have generated a relocatable CMake Configuration for our project that can be used after the project has been installed or packaged. If we want our project to also be used from a build directory we only have to add the following to the bottom of the top level `CMakeLists.txt`:

```cmake
export(EXPORT MathFunctionsTargets
  FILE "${CMAKE_CURRENT_BINARY_DIR}/MathFunctionsTargets.cmake"
)
```

With this export call we now generate a `Targets.cmake`, allowing the configured `MathFunctionsConfig.cmake` in the build directory to be used by other projects, without needing it to be installed.

### Packaging Debug and Release

**Note:** This example is valid for single-configuration generators and will not work for multi-configuration generators (e.g. Visual Studio).

By default, CMake's model is that a build directory only contains a single configuration, be it Debug, Release, MinSizeRel, or RelWithDebInfo. It is possible, however, to setup CPack to bundle multiple build directories and construct a package that contains multiple configurations of the same project.

First, we want to ensure that the debug and release builds use different names for the executables and libraries that will be installed. Let's use d as the postfix for the debug executable and libraries.

Set [`CMAKE_DEBUG_POSTFIX`](https://cmake.org/cmake/help/latest/variable/CMAKE_DEBUG_POSTFIX.html#variable:CMAKE_DEBUG_POSTFIX) near the beginning of the top-level `CMakeLists.txt` file:

```cmake
set(CMAKE_DEBUG_POSTFIX d)

add_library(tutorial_compiler_flags INTERFACE)
```

And the [`DEBUG_POSTFIX`](https://cmake.org/cmake/help/latest/prop_tgt/DEBUG_POSTFIX.html#prop_tgt:DEBUG_POSTFIX) property on the tutorial executable:

```cmake
add_executable(Tutorial tutorial.cxx)
set_target_properties(Tutorial PROPERTIES DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX})

target_link_libraries(Tutorial PUBLIC MathFunctions)
```

Let's also add version numbering to the MathFunctions library. In `MathFunctions/CMakeLists.txt`, set the [`VERSION`](https://cmake.org/cmake/help/latest/prop_tgt/VERSION.html#prop_tgt:VERSION) and [`SOVERSION`](https://cmake.org/cmake/help/latest/prop_tgt/SOVERSION.html#prop_tgt:SOVERSION) properties:

```cmake
set_property(TARGET MathFunctions PROPERTY VERSION "1.0.0")
set_property(TARGET MathFunctions PROPERTY SOVERSION "1")
```

From the `Step12` directory, create `debug` and `release` subbdirectories. The layout will look like:

```cmake
- Step12
   - debug
   - release
```

Now we need to setup debug and release builds. We can use [`CMAKE_BUILD_TYPE`](https://cmake.org/cmake/help/latest/variable/CMAKE_BUILD_TYPE.html#variable:CMAKE_BUILD_TYPE) to set the configuration type:

```shell
cd debug
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build .
cd ../release
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build .
```

Now that both the debug and release builds are complete, we can use a custom configuration file to package both builds into a single release. In the `Step12` directory, create a file called `MultiCPackConfig.cmake`. In this file, first include the default configuration file that was created by the [`cmake`](https://cmake.org/cmake/help/latest/manual/cmake.1.html#manual:cmake(1)) executable.

Next, use the `CPACK_INSTALL_CMAKE_PROJECTS` variable to specify which projects to install. In this case, we want to install both debug and release.

```cmake
include("release/CPackConfig.cmake")

set(CPACK_INSTALL_CMAKE_PROJECTS
    "debug;Tutorial;ALL;/"
    "release;Tutorial;ALL;/"
    )
```

From the `Step12` directory, run [`cpack`](https://cmake.org/cmake/help/latest/manual/cpack.1.html#manual:cpack(1)) specifying our custom configuration file with the `config` option:

```cmake
cpack --config MultiCPackConfig.cmake
```

