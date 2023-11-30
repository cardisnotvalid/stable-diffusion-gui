# Models

-   Text to image

    -   AbsoluteReality v1.8.1  = `absolute-reality-v1-8-1`
    -   DreamShaper v8          = `dream-shaper-v8`
    -   Realistic Vision v5.1   = `realistic-vision-v5-1`
    -   ICBINP SECO             = `icbinp-seco`
    -   Dark Sushi Mix v2.25    = `dark-sushi-mix-v2-25`
    -   AbsoluteReality v1.6    = `absolute-reality-v1-6`
    -   SynthwavePunk v2        = `synthwave-punk-v2`
    -   Arcane Diffusion        = `arcane-diffusion`
    -   MoonFilm Reality v3     = `moonfilm-reality-v3`
    -   MoonFilm Utopia v3      = `moonfilm-utopia-v3`
    -   MoonFilm FilmGrain v1   = `moonfilm-film-grain-v1`
    -   Openjourney v4          = `openjourney-v4`
    -   Realistic Vision v3     = `realistic-vision-v3`
    -   ICBINP Final            = `icbinp-final`
    -   ICBINP Relapse          = `icbinp-relapse`
    -   ICBINP Afterburn        = `icbinp-afterburn`
    -   InteriorDesign          = `xsarchitectural-interior-design`
    -   Modern Disney Diffusion = `mo-di-diffusion`
    -   RPG                     = `anashel-rpg`
    -   Anime Diffusion         = `eimis-anime-diffusion-v1-0`
    -   Something V2.2          = `something-v2-2`
    -   ICBINP                  = `icbinp`
    -   Analog Diffusion        = `analog-diffusion`
    -   NeverEnding Dream       = `neverending-dream`
    -   Van Gogh Diffusion      = `van-gogh-diffusion`
    -   Openjourney             = `openjourney-v1-0`
    -   Realistic Vision v1.3   = `realistic-vision-v1-3`
    -   Stable Diffusion v2.1   = `stable-diffusion-v2-1`
    -   Stable Diffusion v1.5   = `stable-diffusion-v1-5`

-   ControlNet

    -   AbsoluteReality v1.8.1 = `absolute-reality-v1-8-1`
    -   DreamShaper v8 = `dream-shaper-v8`
    -   Realistic Vision v5.1 = `realistic-vision-v5-1`
    -   ICBINP SECO = `icbinp-seco`
    -   Dark Sushi Mix v2.25 = `dark-sushi-mix-v2-25`
    -   AbsoluteReality v1.6 = `absolute-reality-v1-6`
    -   SynthwavePunk v2 = `synthwave-punk-v2`
    -   Arcane Diffusion = `arcane-diffusion`
    -   MoonFilm Reality v3 = `moonfilm-reality-v3`
    -   MoonFilm Utopia v3 = `moonfilm-utopia-v3`
    -   MoonFilm FilmGrain v1 = `moonfilm-film-grain-v1`
    -   Openjourney v4 = `openjourney-v4`
    -   Realistic Vision v3 = `realistic-vision-v3`
    -   ICBINP Final = `icbinp-final`
    -   ICBINP Relapse = `icbinp-relapse`
    -   ICBINP Afterburn = `icbinp-afterburn`
    -   InteriorDesign = `xsarchitectural-interior-design`
    -   Modern Disney Diffusion = `mo-di-diffusion`
    -   RPG = `anashel-rpg`
    -   Anime Diffusion = `eimis-anime-diffusion-v1-0`
    -   Something V2.2 = `something-v2-2`
    -   ICBINP = `icbinp`
    -   Analog Diffusion = `analog-diffusion`
    -   NeverEnding Dream = `neverending-dream`
    -   Van Gogh Diffusion = `van-gogh-diffusion`
    -   Openjourney = `openjourney-v1-0`
    -   Realistic Vision v1.3 = `realistic-vision-v1-3`
    -   Stable Diffusion v1.5 = `stable-diffusion-v1-5`

-   ControlNet (conditioning)

    -   canny         = `canny-1.1`
    -   softedge      = `softedge-1.1`
    -   mlsd          = `mlsd-1.1`
    -   normal        = `normal-1.1`
    -   depth         = `depth-1.1`
    -   openpose      = `openpose-1.1`
    -   openpose full = `openpose-full-1.1`
    -   scribble      = `scribble-1.1`
    -   lineart       = `lineart-1.1`
    -   lineart anime = `lineart-anime-1.1`
    -   mediapipeface = `mediapipeface`

-   Upscale

    -   Real-ESRGAN = `real-esrgan-4x`

-   Face Fix
    -   GFPGAN v1.3 = `gfpgan-v1-3`

# Parameters

-   Scheduler

    -   `euler_a`
    -   `euler`
    -   `lms`
    -   `ddim`
    -   `dpmsolver++`
    -   `pndm"`

-   Output format
    -   `jpeg`
    -   `png`

# Example config

```toml
[text_to_image]
model = "absolute-reality-v1-8-1"
width = 512
height = 512
steps = 20
scheduler = "euler_a"
output_format = "png"

[controlnet]
model = "absolute-reality-v1-8-1"
controlnet = "canny-1.1"
```
