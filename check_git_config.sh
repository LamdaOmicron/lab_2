#!/bin/bash

echo "Проверка конфигурации git..."

# Получаем текущие значения
user_name=$(git config --global user.name)
user_email=$(git config --global user.email)

need_name=false
need_email=false

# Проверка user.name
if [ -z "$user_name" ]; then
    echo "⚠️ user.name не задан. Устанавливаю значение по умолчанию: LamdaOmicron"
    git config --global user.name "LamdaOmicron"
    user_name="LamdaOmicron"
    need_name=true
else
    echo "✅ user.name = $user_name"
fi

# Проверка user.email
if [ -z "$user_email" ]; then
    echo "⚠️ user.email не задан. Устанавливаю значение по умолчанию: genaz0983@gmail.com"
    git config --global user.email "genaz0983@gmail.com"
    user_email="genaz0983@gmail.com"
    need_email=true
else
    echo "✅ user.email = $user_email"
fi

echo ""
if [ "$need_name" = true ] || [ "$need_email" = true ]; then
    echo "✓ Настройки git обновлены:"
    echo "   user.name  = $user_name"
    echo "   user.email = $user_email"
else
    echo "✓ Все параметры git уже настроены корректно."
fi

echo ""
read -p "Нажмите Enter для выхода..."