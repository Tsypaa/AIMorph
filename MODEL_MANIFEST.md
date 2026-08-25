# Model manifest

All installed files use Apache-2.0.

| File | Hugging Face repository | ComfyUI directory | Bytes | SHA-256 |
|---|---|---|---:|---|
| Wan2.2-TI2V-5B-Q5_K_M.gguf | QuantStack/Wan2.2-TI2V-5B-GGUF | models/diffusion_models | 3810603360 | 4424633a876511b9be58a41119f7c9d762ea92b3cb74649cdb43cac850e42dba |
| umt5-xxl-encoder-Q3_K_M.gguf | city96/umt5-xxl-encoder-gguf | models/text_encoders | 3055097696 | b7e2ca4c493c9d51fa951005e8ceba2f4b6b6877cfb4c36a8955c6cd68a1dba7 |
| wan2.2_vae.safetensors | Comfy-Org/Wan_2.2_ComfyUI_Repackaged | models/vae | 1409400960 | e40321bd36b9709991dae2530eb4ac303dd168276980d3e9bc4b6e2b75fed156 |

RTX 4090 FLF2V files (not downloaded): wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors and wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors in models/diffusion_models; umt5_xxl_fp8_e4m3fn_scaled.safetensors in models/text_encoders; wan_2.1_vae.safetensors in models/vae.

Sources:
- https://huggingface.co/QuantStack/Wan2.2-TI2V-5B-GGUF
- https://huggingface.co/city96/umt5-xxl-encoder-gguf
- https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged
- https://docs.comfy.org/tutorials/video/wan/wan2_2
