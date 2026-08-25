# Age Transition AI Video

Локальный open-source стек для генерации оживлённых переходов между фотографиями одного человека в разном возрасте.

Главная идея проекта:

```text
фотография A — человек младше
              ↓
     AI-сгенерированный переход
              ↓
фотография B — человек старше
```

Промежуточные кадры должны создаваться генеративной видеомоделью, а не обычным crossfade или optical flow. Проект построен вокруг [ComfyUI](https://github.com/Comfy-Org/ComfyUI) и семейства моделей [Wan 2.2](https://docs.comfy.org/tutorials/video/wan/wan2_2).

## Статус проекта

| Конфигурация | Состояние | Назначение |
|---|---|---|
| GTX 1080 8 GB | Работает и протестировано | Image-to-Video из одной начальной фотографии |
| RTX 4090 24 GB | Workflow подготовлен | First/Last Frame переход между двумя фотографиями |
| 2× RTX 4090 | Планируется | Параллельная обработка задач и более тяжёлые FLF2V-рендеры |

Важно: установленная на GTX 1080 модель Wan 2.2 TI2V-5B принимает только начальное изображение. Она используется для проверки локального CUDA/ComfyUI/video-конвейера и генерации I2V. Настоящий переход между младшей и старшей фотографией требует Wan 2.2 FLF2V 14B и рассчитан на RTX 4090.

## Возможности

- полностью локальный запуск без отправки фотографий в облачные сервисы;
- ComfyUI с доступом только через `http://127.0.0.1:8188`;
- генерация Image-to-Video на GTX 1080 8 GB;
- GGUF-квантизация и CPU/model offload для старой Pascal GPU;
- сохранение результата в H.264 MP4;
- готовый First/Last Frame workflow для RTX 4090;
- диагностические и автоматические smoke-test скрипты;
- переносимая структура проекта и фиксированные версии компонентов.

## Проверенная конфигурация

- Windows 10 x64;
- NVIDIA GeForce GTX 1080, 8 GB VRAM;
- 16 GB RAM;
- NVIDIA Driver 582.28;
- Python 3.11.9;
- PyTorch 2.13.0+cu126;
- CUDA runtime 12.6;
- ComfyUI v0.30.0;
- FFmpeg 9.0;
- ComfyUI-GGUF.

### Результаты тестов

| Разрешение | Кадры | Steps | Время | Результат |
|---|---:|---:|---:|---|
| 384×672 | 17 | 8 | 218,5 с | Успешно |
| 480×832 | 17 | 8 | 263,3 с | Успешно |

Оба теста завершились без CUDA OOM. Получены H.264 MP4 с 17 уникальными кадрами.

## Структура

```text
ai-video/
├── ComfyUI/                       # ComfyUI и custom nodes
├── workflows/
│   ├── gtx1080_video_test.json    # I2V/T2V для GTX 1080
│   └── rtx4090_wan_flf2v.json     # две фотографии, Wan 2.2 FLF2V 14B
├── scripts/
│   ├── start_comfyui.bat
│   ├── check_gpu.py
│   ├── smoke_test.py
│   └── prepare_workflows.py
├── ai_video_setup/
│   └── system_info.txt
├── logs/
├── models-download/
├── MODEL_MANIFEST.md
└── README.md
```

Веса моделей, виртуальное окружение, логи и результаты генерации не должны храниться в Git.

## Быстрый запуск готовой установки

Запустите:

```powershell
.\scripts\start_comfyui.bat
```

Откройте:

```text
http://127.0.0.1:8188
```

Для GTX 1080 загрузите через меню `Workflow → Open`:

```text
workflows\gtx1080_video_test.json
```

В правильном графе должны отображаться модели:

```text
Wan2.2-TI2V-5B-Q5_K_M.gguf
umt5-xxl-encoder-Q3_K_M.gguf
wan2.2_vae.safetensors
```

В узле `Load Image` выберите фотографию, затем нажмите `Run` или `Ctrl+Enter`. Результат сохраняется в:

```text
ComfyUI\output\video\
```

Безопасные начальные параметры для GTX 1080:

```yaml
resolution: 384x672
frames: 17
steps: 8
batch: 1
fps: 16
```

## Автоматический smoke-test

Сначала запустите ComfyUI, затем выполните:

```powershell
.\.venv\Scripts\python.exe .\scripts\smoke_test.py
```

Скрипт:

1. проверяет доступность backend;
2. отправляет Wan 2.2 I2V workflow через API;
3. отслеживает температуру, загрузку и VRAM;
4. ожидает завершения генерации;
5. сохраняет результат и лог.

Лог находится в `logs\smoke_test.log`.

Проверка CUDA и GPU:

```powershell
.\.venv\Scripts\python.exe .\scripts\check_gpu.py
```

## Установка с нуля

### Требования

- Windows 10/11 x64;
- NVIDIA GPU и совместимый драйвер;
- Python 3.11;
- Git;
- FFmpeg;
- минимум 25 GB свободного места для GTX-конфигурации;
- рекомендуется не менее 16 GB RAM.

### ComfyUI и окружение

```powershell
git clone --branch v0.30.0 --depth 1 https://github.com/Comfy-Org/ComfyUI.git ComfyUI
py -3.11 -m venv .venv

.\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\.venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
.\.venv\Scripts\python.exe -m pip install -r .\ComfyUI\requirements.txt huggingface_hub
```

CUDA Toolkit отдельно устанавливать необязательно: официальный PyTorch wheel содержит необходимый CUDA runtime.

### ComfyUI-GGUF

```powershell
git clone --depth 1 https://github.com/city96/ComfyUI-GGUF.git .\ComfyUI\custom_nodes\ComfyUI-GGUF
.\.venv\Scripts\python.exe -m pip install -r .\ComfyUI\custom_nodes\ComfyUI-GGUF\requirements.txt
```

ComfyUI Manager не требуется: GTX workflow использует только один явно зафиксированный custom node.

## Модели для GTX 1080

Все используемые модельные файлы распространяются под Apache-2.0.

| Файл | Источник | Каталог |
|---|---|---|
| `Wan2.2-TI2V-5B-Q5_K_M.gguf` | [QuantStack/Wan2.2-TI2V-5B-GGUF](https://huggingface.co/QuantStack/Wan2.2-TI2V-5B-GGUF) | `ComfyUI/models/diffusion_models/` |
| `umt5-xxl-encoder-Q3_K_M.gguf` | [city96/umt5-xxl-encoder-gguf](https://huggingface.co/city96/umt5-xxl-encoder-gguf) | `ComfyUI/models/text_encoders/` |
| `wan2.2_vae.safetensors` | [Comfy-Org/Wan_2.2_ComfyUI_Repackaged](https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged) | `ComfyUI/models/vae/` |

Точные размеры и SHA-256 находятся в [MODEL_MANIFEST.md](MODEL_MANIFEST.md).

## Переход между двумя фотографиями на RTX 4090

Целевой workflow:

```text
workflows\rtx4090_wan_flf2v.json
```

Он содержит два узла `Load Image`:

1. первое изображение — человек младше;
2. второе изображение — тот же человек старше.

Оба изображения поступают в `WanFirstLastFrameToVideo`. Модель генерирует промежуточное движение и трансформацию с учётом начального и конечного кадров.

Необходимые модели:

```text
wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors
wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors
umt5_xxl_fp8_e4m3fn_scaled.safetensors
wan_2.1_vae.safetensors
```

14B-веса намеренно не включены в репозиторий и не загружаются при установке GTX-профиля.

## Ограничения GTX 1080

- Wan 2.2 5B не имеет входа для последнего изображения;
- полноценный FLF2V 14B слишком тяжёл для комфортной работы на 8 GB Pascal;
- отсутствуют Tensor Cores и эффективное BF16/FP8-ускорение;
- генерация медленная, GPU может сильно нагреваться;
- batch должен оставаться равным 1;
- рекомендуется начинать с 384×672 и 17 кадров.

Попытка запустить 14B GGUF на GTX 1080 возможна экспериментально, но при 16 GB RAM приведёт к интенсивному использованию pagefile, очень долгой генерации и возможным OOM.

## Рекомендованный .gitignore

Перед публикацией добавьте в `.gitignore`:

```gitignore
.venv/
ComfyUI/
models-download/
logs/
tools/
**/models/
**/input/
**/output/
*.safetensors
*.ckpt
*.pt
*.pth
*.gguf
*.mp4
*.webm
*.mov
__pycache__/
*.pyc
```

Если ComfyUI должен быть частью репозитория, лучше подключить его как Git submodule, а не коммитить вложенную копию целиком.

Никогда не публикуйте фотографии людей без их согласия.

## Roadmap

- перенос FLF2V workflow на RTX 4090;
- end-to-end тест перехода между двумя возрастными фотографиями;
- подбор prompt/negative prompt для сохранения идентичности лица;
- автоматическая подготовка и выравнивание входных портретов;
- несколько последовательных возрастных этапов;
- очередь задач для 2× RTX 4090;
- воспроизводимый installer без хранения весов в Git.

## Лицензии и благодарности

- [ComfyUI](https://github.com/Comfy-Org/ComfyUI) — GPL-3.0;
- [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) — Apache-2.0;
- модели Wan 2.2 и перечисленные GGUF-конверсии — Apache-2.0;
- лицензия собственных скриптов и workflow должна быть указана отдельным файлом `LICENSE`.

Публичный репозиторий без файла `LICENSE` доступен для просмотра, но юридически не предоставляет другим пользователям разрешение изменять и распространять код. Для открытого проекта рекомендуется явно выбрать MIT, Apache-2.0 или другую подходящую лицензию.
