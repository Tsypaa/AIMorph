import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
templates = Path(sys.argv[1])
out = root / "workflows"
out.mkdir(exist_ok=True)
positive = ("The same person gradually changes naturally while preserving exact facial identity. "
"Smooth continuous realistic transformation, subtle blinking and breathing, minimal natural head movement, "
"stable camera, coherent facial features, photorealistic, smooth motion.")
negative = ("different person, identity change, distorted face, duplicate face, extra face, deformed eyes, "
"asymmetrical eyes, warped mouth, melting face, flicker, sudden motion, scene cut, camera movement, "
"duplicate body, extra limbs, artifacts")

def by_id(workflow):
    return {node["id"]: node for node in workflow["nodes"]}

workflow = json.loads((templates / "video_wan2_2_5B_ti2v.json").read_text(encoding="utf-8"))
nodes = by_id(workflow)
nodes[37]["type"] = "UnetLoaderGGUF"
nodes[37]["title"] = "Wan2.2 5B Q5_K_M (GTX 1080)"
nodes[37]["widgets_values"] = ["Wan2.2-TI2V-5B-Q5_K_M.gguf"]
nodes[37].setdefault("properties", {}).update({"Node name for S&R":"UnetLoaderGGUF","cnr_id":"comfyui-gguf"})
nodes[38]["type"] = "CLIPLoaderGGUF"
nodes[38]["title"] = "UMT5 XXL Q3_K_M"
nodes[38]["widgets_values"] = ["umt5-xxl-encoder-Q3_K_M.gguf","wan"]
nodes[38].setdefault("properties", {}).update({"Node name for S&R":"CLIPLoaderGGUF","cnr_id":"comfyui-gguf"})
nodes[39]["widgets_values"] = ["wan2.2_vae.safetensors"]
nodes[55]["title"] = "I2V 384x672, 17 frames, batch 1"
nodes[55]["widgets_values"] = [384,672,17,1]
nodes[56]["title"] = "Start Image (enabled for I2V)"
nodes[56]["mode"] = 0
nodes[56]["widgets_values"] = ["example.png","image"]
nodes[6]["widgets_values"] = [positive]
nodes[7]["widgets_values"] = [negative]
nodes[48]["widgets_values"] = [8.0]
nodes[3]["widgets_values"] = [1080,"fixed",8,5.0,"uni_pc","simple",1.0]
nodes[57]["widgets_values"] = [16.0]
nodes[58]["widgets_values"] = ["video/gtx1080_wan22_test","mp4","h264"]
nodes[59]["widgets_values"] = ["GTX 1080 low-memory: Wan2.2 5B Q5_K_M + UMT5 Q3_K_M + official VAE. Load Image enabled for I2V; bypass for T2V."]
workflow.setdefault("extra", {})["gtx1080_profile"] = {"vram":"8 GiB","mode":"lowvram + DynamicVRAM"}
(out/"gtx1080_video_test.json").write_text(json.dumps(workflow,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

prompt = {
"1":{"class_type":"UnetLoaderGGUF","inputs":{"unet_name":"Wan2.2-TI2V-5B-Q5_K_M.gguf"}},
"2":{"class_type":"ModelSamplingSD3","inputs":{"model":["1",0],"shift":8.0}},
"3":{"class_type":"CLIPLoaderGGUF","inputs":{"clip_name":"umt5-xxl-encoder-Q3_K_M.gguf","type":"wan"}},
"4":{"class_type":"CLIPTextEncode","inputs":{"text":positive,"clip":["3",0]}},
"5":{"class_type":"CLIPTextEncode","inputs":{"text":negative,"clip":["3",0]}},
"6":{"class_type":"VAELoader","inputs":{"vae_name":"wan2.2_vae.safetensors"}},
"7":{"class_type":"LoadImage","inputs":{"image":"example.png"}},
"8":{"class_type":"Wan22ImageToVideoLatent","inputs":{"vae":["6",0],"width":384,"height":672,"length":17,"batch_size":1,"start_image":["7",0]}},
"9":{"class_type":"KSampler","inputs":{"model":["2",0],"seed":1080,"steps":8,"cfg":5.0,"sampler_name":"uni_pc","scheduler":"simple","positive":["4",0],"negative":["5",0],"latent_image":["8",0],"denoise":1.0}},
"10":{"class_type":"VAEDecode","inputs":{"samples":["9",0],"vae":["6",0]}},
"11":{"class_type":"CreateVideo","inputs":{"images":["10",0],"fps":16.0}},
"12":{"class_type":"SaveVideo","inputs":{"video":["11",0],"filename_prefix":"video/gtx1080_wan22_smoke","format":"mp4","codec":"h264"}}
}
(out/"gtx1080_video_test_api.json").write_text(json.dumps(prompt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

workflow = json.loads((templates/"video_wan2_2_14B_flf2v.json").read_text(encoding="utf-8"))
nodes = by_id(workflow)
nodes[78]["widgets_values"] = [negative]
nodes[90]["widgets_values"] = [positive]
nodes[81]["widgets_values"] = [480,832,81,1]
nodes[83]["widgets_values"] = ["video/rtx4090_wan22_flf2v","mp4","h264"]
workflow.setdefault("extra", {})["target_hardware"] = "RTX 4090 24GB"
(out/"rtx4090_wan_flf2v.json").write_text(json.dumps(workflow,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("created", *(str(p) for p in out.glob("*.json")), sep="\n")
