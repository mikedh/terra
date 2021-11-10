
curl -L -o llvm.z7 "https://github.com/%BINARY_SOURCE_USER%/llvm-package-windows/releases/download/clang-%LLVM_VERSION%-nvptx/llvm-%LLVM_VERSION%-windows-amd64-msvc%VS_MAJOR_VERSION%-msvcrt.7z"

7z x llvm.7z

set LLVM_DIR=%CD%\llvm-%LLVM_VERSION%-windows-amd64-msvc%VS_MAJOR_VERSION%-msvcrt
set CLANG_RESOURCE_DIRECTORY=%LLVM_DIR%\lib\clang\%LLVM_VERSION%

set CMAKE_PREFIX_PATH=%LLVM_DIR%

:: TODO : re-enable cude if
if /I "%USE_CUDA%" EQU "1" (curl -L -o cuda.exe "https://developer.nvidia.com/compute/cuda/9.2/Prod2/local_installers2/cuda_9.2.148_windows")
if /I "%USE_CUDA%" EQU "1" (.\cuda -s nvcc_9.2 cudart_9.2)
if /I "%USE_CUDA%" EQU "1" (set CUDA_DIR=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v9.2)

set TERRA_DIR=%CD%


cd build
cmake .. -DCMAKE_INSTALL_PREFIX=%CD%\..\install -DCMAKE_GENERATOR_PLATFORM=x64
cmake --build . --target INSTALL --config Release
cd ..

set TERRA_SHARE_PATH=%TERRA_DIR%\install\share\terra

cd tests
..\install\bin\terra run
cd ..
