@echo off
set URL:https://s245vla.storage.yandex.net/rdisk/a019b2e94a06669722ad58ecbdcbc6aed78d42eb763e4bd7f56389f909885472/682b6f0c/nPq-bpK-tDdpRv1HPEfWXaigHOsQEoseLWcjppGk51Fu8iT5boUIV-zKixSLOwveFYKzdqD_WnSNuVi1JuxzBQ==?uid=0&filename=MI13T_EEA_OS2.0.103.0_15.0_Mod2.zip&disposition=attachment&hash=o0MVSTvSDGUBo4QY4PHtPSNkYUq6F82tlT3Wntpi6PYAX5avc%2B7FrmDUijmp5/Tfq/J6bpmRyOJonT3VoXnDag%3D%3D&limit=0&content_type=application%2Fzip&owner_uid=197900013&fsize=5469026192&hid=b3346c124309234d6eeff05bdddbae25&media_type=compressed&tknv=v3&ts=63580bf30db00&s=3b2baaa746cd698d856f787f35980be122f71a7312527151dd8c4973c70b3878&pb=U2FsdGVkX1-NvoZnenxptlaENKIWivDdP3sgLqb0vlBq5rRMpiF2pP-jCNmyKTZkqGrZNeSaLVE6yJAEmfGz7c2qq3OjEoNlnAJnQipma74
set FOLDER=C:\ProshivkaTool\На основе официальных прошивок
set FILENAME=MI13T_EEA_OS2.0.103.0_15.0_Mod2.zip

:: Создать папку если не существует
if not exist "%FOLDER%" mkdir "%FOLDER%"

:: Скачать файл
curl -L -o "%FOLDER%\%FILENAME%" "%URL%"

:: Проверка ошибок
if errorlevel 1 (
    echo Ошибка загрузки файла
    pause
    exit /b 1
)

echo Файл успешно загружен!
pause