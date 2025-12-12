## How Integrate your C/C++ unit tests with our CI/CD Pipeline

### 1. Create the test directory for your feature inside ```tests/```
  ```
    cd tests
    mkdir <my_feature>

  ```

### 2. Create a new CMakeLists.txt to compile the .cpp files and include the necessary .hpp files for your test."

  - If you are not yet familiar with CMake, you can view the CMakeLists.txt available in tests/car-control/CMakeLists.txt

  #### 2.1 Set your Include directories:

  ```
  # -----------------------------------
# Project include directories
# -----------------------------------
# INCLUIA O DIRETÓRIO PARA OS .hpp
include_directories(
    ../../src/car-control/piracer-cpp/Adafruit_INA219
    ../../src/car-control/piracer-cpp/Adafruit_PCA9685
    ../../src/car-control/piracer-cpp/Gamepad
    ../../src/car-control/piracer-cpp/PiRacer
)
```


  #### 2.2 List the .cpp files you need to compile

```
# -----------------------------------
# Source files for the car-control feature
# -----------------------------------
# INCLUA OS ARQUIVOS .cpp QUE PRECISAM SER COMPILADOS
set(PIRACER_SRC
    ../../src/car-control/piracer-cpp/Adafruit_INA219/Adafruit_INA219.cpp
    ../../src/car-control/piracer-cpp/Adafruit_PCA9685/Adafruit_PCA9685.cpp
    ../../src/car-control/piracer-cpp/PiRacer/PiRacer.cpp
)

```

### 3. Create your tests

- You must create your .cpp/.c test files separated from the src code. You'll put them inside of the tests/<my_feature>.

- Create your tests in the Google Test way (https://google.github.io/googletest/).

### 4. Fetch the necessary dependencies for Google Test to work within your CMakeLists.txt

- You should also use the already mentioned file, tests/car-control/CMakeLists.txt, if you need a template to do this.

#### 4.1 Fetch

```
include(FetchContent)

FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)

# Fetch and make gtest/gmock available
FetchContent_MakeAvailable(googletest)
```

#### 4.1 Link and enable

```
# -----------------------------------
# Link with GoogleTest
# -----------------------------------
target_link_libraries(test_car_control
    PRIVATE
        gtest
        gtest_main
)

# -----------------------------------
# Enable CTest integration
# -----------------------------------
enable_testing()
add_test(NAME car-control-tests COMMAND test_car_control)
```

### 5. Add your tests in the CMakeLists.txt

- At this point, you will tell CMake which files it should use to generate the executable, which in this case is your main test file.

```
# -----------------------------------
# Test executable
# -----------------------------------
#INCLUDE O CAMINHO PARA OS EXECUTAVEIS DE TESTE COM OS SOURCES NECESSERAIO
add_executable(test_car_control
    test_car_control.cpp #your test file
    ${PIRACER_SRC} #src files needed by the test
)
```

### 6. Test if everything is working

- Now you will test if you can manually test your code before integrating it with our GitHub Actions.

```
  cd tests/<my_feature> # move to your feature test folder
  mkdir build
  cd build 
  cmake ..
  make

  ctest #RUN ALL YOUR TESTS
```

If you can see the result, congratulations, Google Test is working and you can now integrate it with our CI/CD pipeline 🎉

### 7. Integrate in our CI workflow

Inside the unit-tests job, you must create a new step following this style:

- Please add your steps as the last step.


```
unit-tests:
    runs-on: ubuntu-latest
    needs: linting-cpp

    steps:
      - name: Build and run Car Control tests
        run: |
          mkdir -p tests/car-control/build
          cd tests/car-control/build
          cmake ..
          cmake --build .
          ctest --output-on-failure
```

---

