import os
import sys
import subprocess
import shutil

def run_command(command, shell=False):
    try:
        subprocess.check_call(command, shell=shell)
    except subprocess.CalledProcessError as e:
        print(f'Error executing command: {e}')
        sys.exit(1)

def install_requirements():
    print('[*] Installing required build dependencies...')
    run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', 'pyinstaller', 'customtkinter'])

def clean_build_dirs():
    print('[*] Cleaning old build files...')
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    if os.path.exists('KeySpace.spec'):
        os.remove('KeySpace.spec')

def build_mac():
    print('[*] Building for macOS...')
    pyinstaller_cmd = [
        sys.executable, '-m', 'PyInstaller', '--noconfirm', '--windowed', '--name', 'KeySpace',
        '--add-data', 'Vault:Vault', '--icon', 'Vault/Logo.ico', '--target-architecture', 'universal2', 'KeySpace.py'
    ]
    
    # Try universal2 build first
    try:
        subprocess.check_call(pyinstaller_cmd)
    except subprocess.CalledProcessError:
        print('[!] Universal build failed. Falling back to default architecture...')
        pyinstaller_cmd.remove('--target-architecture')
        pyinstaller_cmd.remove('universal2')
        run_command(pyinstaller_cmd)

    app_path = os.path.join('dist', 'KeySpace.app')
    if os.path.exists(app_path):
        print('[+] macOS app bundle created successfully.')
        
        # Check if hdiutil is available (standard on macOS)
        if shutil.which('hdiutil'):
            print('[*] Creating DMG installer...')
            dmg_layout = os.path.join('dist', 'dmg_layout')
            os.makedirs(dmg_layout, exist_ok=True)
            
            # Copy app to layout
            shutil.copytree(app_path, os.path.join(dmg_layout, 'KeySpace.app'))
            # Create Applications symlink
            os.symlink('/Applications', os.path.join(dmg_layout, 'Applications'))
            
            dmg_path = os.path.join('dist', 'KeySpace.dmg')
            if os.path.exists(dmg_path):
                os.remove(dmg_path)
                
            run_command([
                'hdiutil', 'create', '-volname', 'KeySpace Installer', 
                '-srcfolder', dmg_layout, '-ov', '-format', 'UDZO', dmg_path
            ])
            
            shutil.rmtree(dmg_layout)
            print(f'[+] Success! DMG Installer created at: {dmg_path}')
        else:
            print('[-] hdiutil not found, skipping DMG creation. App is in dist/ folder.')
    else:
        print('[X] macOS build failed.')

def build_windows():
    print('[*] Building for Windows...')
    pyinstaller_cmd = [
        sys.executable, '-m', 'PyInstaller', '--noconfirm', '--windowed', '--onefile', '--name', 'KeySpace',
        '--add-data', 'Vault;Vault', '--icon', 'Vault/Logo.ico', 'KeySpace.py'
    ]
    run_command(pyinstaller_cmd)
    
    exe_path = os.path.join('dist', 'KeySpace.exe')
    if os.path.exists(exe_path):
        print(f'\n[+] Success! Windows executable created at: {exe_path}')
        print('[i] End users can simply run this .exe file without needing Python installed!')
    else:
        print('[X] Windows build failed.')

def build_linux():
    print('[*] Building for Linux...')
    pyinstaller_cmd = [
        sys.executable, '-m', 'PyInstaller', '--noconfirm', '--windowed', '--onefile', '--name', 'KeySpace',
        '--add-data', 'Vault:Vault', '--icon', 'Vault/Logo.ico', 'KeySpace.py'
    ]
    run_command(pyinstaller_cmd)
    
    bin_path = os.path.join('dist', 'KeySpace')
    if os.path.exists(bin_path):
        print(f'\n[+] Success! Linux binary created at: {bin_path}')
    else:
        print('[X] Linux build failed.')

def main():
    print('========================================')
    print('      KeySpace Cross-Platform Builder   ')
    print('========================================')
    
    install_requirements()
    clean_build_dirs()
    
    if sys.platform == 'darwin':
        build_mac()
    elif sys.platform == 'win32':
        build_windows()
    elif sys.platform.startswith('linux'):
        build_linux()
    else:
        print(f'[X] Unsupported platform: {sys.platform}')

if __name__ == '__main__':
    main()