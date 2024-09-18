from diffusers import StableDiffusionPipeline
import torch

# Charger le modèle
model_name = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
pipe.to("cuda")

# Générer une image
prompt = "Une belle forêt en automne"
image = pipe(prompt).images[0]

# Sauvegarder l'image
image.save("generated_image.png")
