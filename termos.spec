# termos.spec — configuração PyInstaller para o projeto Termos Justos

# Importações padrão do PyInstaller
block_cipher = None

a = Analysis(
    ['app.py'],  # arquivo principal
    pathex=[],
    binaries=[],
    datas=[
        # Inclui todos os HTML da pasta templates
        ('templates/*.html', 'templates'),
        # Inclui todos os CSS/JS da pasta static
        ('static/*', 'static'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='termos',  # nome do executável
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # se quiser abrir terminal junto
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='termos'
)
