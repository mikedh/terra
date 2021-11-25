import os
import shutil
import subprocess

import tempfile

if __name__ == '__main__':

    ver = '{}.0.0'.format(os.environ[
        'LLVM_VERSION'].strip().split('.')[0])

    with tempfile.TemporaryDirectory() as f:

        ln = f'llvm-{ver}.src.tar.xz'
        cn = f'clang-{ver}.src.tar.xz'

        base_url = f'https://github.com/llvm/llvm-project/releases/download/llvmorg-{ver}'

        subprocess.check_call(
            f'curl -L -o {f}/{ln} {base_url}/{ln}', shell=True)
        subprocess.check_call(
            f'curl -L -o {f}/{cn} {base_url}/{cn}', shell=True)

        os.chdir(f)
        try:
            subprocess.check_call(['tar', 'xf', ln])
            subprocess.check_call(['tar', 'xf', cn])
        except BaseException:
            from IPython import embed
            embed()
        shutil.move(f'clang-{ver}.src', f'llvm-{ver}.src/tools/clang')

        os.makedirs('build')
        os.makedirs('install')
        os.chdir(f'{f}/build')

        subprocess.check_call(['cmake',
                               f'../llvm-{ver}.src',
                               f'-DCMAKE_INSTALL_PREFIX={f}/install'
                               '-DCMAKE_BUILD_TYPE=Release',
                               '-DLLVM_ENABLE_TERMINFO=OFF',
                               '-DLLVM_ENABLE_LIBEDIT=OFF',
                               '-DLLVM_ENABLE_ZLIB=OFF',
                               '-DLLVM_ENABLE_ASSERTIONS=OFF'])

        subprocess.check_call(['make', 'install', '-j4'])
