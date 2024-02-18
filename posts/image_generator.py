from monsterapi import client
from django.conf import settings


def generate_from_prompt(prompt):
    api_key = settings.MONSTERAPI_KEY

    monster_client = client(api_key)


    # user_input = input("What is your mood: ")
    # user_input2 = input("What do you feel like doing ")

    model = 'txt2img'
    input_data = {
        'prompt': 'Generate an abstract image for my mood, Currently my mood is ' + prompt + ', I feel like',
        'negprompt': 'Do not give images with hex code= #000000 or hex code= #FFFFFF',
        'samples': 2,
        'steps': 100,
        'aspect_ratio': 'square',
        'guidance_scale': 50,
        'seed': 2414,
    }

    result = monster_client.generate(model, input_data)
    # Get the list of image URLs from the response
    image_urls = result['output']
    print(image_urls)
    return image_urls[1]