import torch

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA runtime: {torch.version.cuda}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    p = torch.cuda.get_device_properties(0)
    print(f"GPU: {p.name}")
    print(f"CUDA capability: {p.major}.{p.minor}")
    print(f"VRAM total: {p.total_memory} bytes ({p.total_memory / 2**30:.2f} GiB)")
    print(f"VRAM allocated: {torch.cuda.memory_allocated(0)} bytes")
    print(f"VRAM reserved: {torch.cuda.memory_reserved(0)} bytes")
