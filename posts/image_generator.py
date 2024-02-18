from django.conf import settings

from monsterapi import client
 
def generate_from_prompt(prompt1, prompt2):
    api_key = settings.MONSTERAPI_KEY
    monster_client = client(api_key)
    
    model = 'txt2img'
    input_data = {
        'prompt': 'Generate an abstract image for my mood, Currently my mood is ' + prompt1 + ', and I feel like ' + prompt2 + '. Show an abstract image related to ' + prompt1 + ' and ' + prompt2,
        'negprompt': 'give images with hex code= #000000 or hex code= #FFFFFF',
        'samples': 2,
        'steps': 100,
        'aspect_ratio': 'square',
        'guidance_scale': 50,
        'seed': 2414,
    }
    
    result = monster_client.generate(model, input_data)
    
    # Get the list of image URLs from the response
    image_urls = result['output']

    return image_urls[1]