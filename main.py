# import argparse
# from InquirerPy import inquirer, validator
# from core.api.key import GetimgReger
# from core.api.image import TextToImage, ControlNet


# parser = argparse.ArgumentParser()
# parser.add_argument("prompt",      type=str)
# parser.add_argument("--seed",      type=str,  required=False)
# parser.add_argument("--type",      type=str,  default="texttoimage")
# parser.add_argument("--seeded",    action="store_true", required=False)
# parser.add_argument("--condition", type=str,  default="canny-1.1", required=False)
# args = parser.parse_args()


# if __name__ == "__main__":
#     if args.type == "texttoimage":
#         TextToImage(args.prompt, set_config=True).generate_image()
#     elif args.type == "controlnet":
#         ControlNet(
#             args.prompt,
#             image=args.seed, 
#             condition=args.condition, 
#             seed=args.seed if args.seeded else None,
#             set_config=True
#         ).generate_image()
#     elif args.type == "upscale":
#         pass
#     elif args.type == "facefix":
#         pass

from core.gui.window import start_application

start_application()