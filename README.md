# F1-Track-Gen
We’ve created a blender add-on that allows anyone to generate an F1 circuit without the need to manually model anything. The add-on comes with a simple to use interface that presents the user with the option to select the track that needs to be modeled and the particular sectors that need to be included in the 3D model.

<!-- Adding an image -->
<p align="center">
    <img src="/Images/car.png" width="1920" title="hover text"> 
</p>

## Current Features :
1. **Simple UI:**
As displayed in _Fig 2._ we have a very simple UI that even unexperienced people should be able to use easily. There are quite a few parameters :
    - **Sectors :** The datasets we have used so far have 3 sectors per track (Sector 1 - Start, Sector 2 - Mid, Sector 3 - End).
    - **API Type :** We have linked 3 APIs to get data from (Melbourne, Texas and Sakhir).
    - **Track Type :** This is solely to show the scalability and verstility of the solution, you can swap the track for any track of you liking!.
    - **Pole Distance :** Distance b/w consecutive poles.
    - **Flag Distance :** Distance b/w consecutive flag(s) (5 country flags included as of the moment (Australia, Canada, India, United Kingdom, USA).
    - **Pole Offset :** The distance of the pole from the center of the track.
    - **Flag Offset :** The distance of the flag(s) from the center of the track.
    - **[x] Delete Prev Fillers :** This is to clean up the previously present Fillers (Flags and Poles) before generating new ones. [Recommended to keep checked]
    - **Generate :** The button which makes the magic happen! The track is generated based on the inputs from API Type, Track Type and Sectors.
    - **Generate Fillers :** This will distribute randomly, instances of the Flag(s) and Poles around the track, independent of Track length.

<br> 
<!-- Adding an image -->
<p align="center">
   <img src="/Images/interface.png" width="512" title="hover text"> 
</p>
<br>

2. **Modular Assets:** 
The assets used are completely modular and easily replacable, you can create your own custom assets in the [Base.blend](Base.blend) file under the relevant collections.

<br> 
<!-- Adding an image -->
<p align="center">
   <img src="/Images/collections.png" width="512" title="hover text"> 
</p>
<br>

So suppose you are making another Flag model, place it undr the "Flag" collection and so on. Leaving the fillers, the tracks also follow this approach, hence, making them easy to modify! **(Naming conventions for Pole (Pole) and TrackCollection (Track001, Track002) are necessary)**

- [ ] TODO : Dynamic object/asset registration

3. **Procedural Materials:**
This is one field I specialize in! What could be better than skipping the whole part where you have to go through the painstaking process of unwrapping a model and texture it. We've made it easy for you by including procedural materials! Infinite fidelity and no hassles, easily modifiable too, you can access the panel(s) from the material properties panel in the bottom right represented by the _sphere icon_.

<br> 
<!-- Adding an image -->
<p align="center">
   <img src="/Images/materials.png" width="512" title="hover text"> 
</p>
<br>

You can view various sliders in here :
- **Yellow Distance :** How far away the yellow lines (at the edges) are from each other.
- **Yellow Thicc :** Exactly what the name suggests, how _thicc_ the yellow lines are.
- **Inner Distance :** How far away the center of the road will the separator(s) be.
- **Inner Thicc :** Exactly what the name suggests, how _thicc_ the inner separator lines are.
- **Yellow Color :** The color of the "yellow" (edge) lines.
- **Inner Color :** The color of the center separator line(s).

- [ ] TODO : Make the material properties more easily accessible! Maybe in the UI itself :)

4. **Heavily Commented Code:**
Afraid of reading through chunks of code to understand what's going on? Don't worry, we have taken extra care in commenting out almost every single line along with generic syntax for functions that are specific to [**Blender Python API (bpy)**](https://docs.blender.org/api/current/index.html). But on the rare occasion that you are still unable to understand the code, just feel free to ping me or Nazzal and we'll be more than happy to help you!

<br> 
<!-- Adding an image -->
<p align="center">
   <img src="/Images/code.png" width="512" title="hover text"> 
</p>
<br>

- [x] TODO : Maintain the standard of the code :D
- [ ] TODO : Generate a proper shippable add-on (So that it makes everyone's lives easier)

## How to run this?

**Requirements : [Blender 2.93.0](https://www.blender.org/) or greater**

Yup, that's the only requirement! We have designed and textured everything locally within Blender (Except for the grass and car [Taken from Sketchfab](https://skfb.ly/o8wn7)). {The car was meant for rendering purposes and was not included in this repo}.

- [x] (_**Yes we are planning to make this into a fully shipped add-on, so don't worry!**_) It's here! Just get the [latest release](https://github.com/VKG5/F1-Track-Gen/releases/tag/v1.1.0) and install it like any other Blender add-on!
- How to install a Blender add-on? What's better than the Blender documentary to [learn](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html) this! 

<!-- Might need this later on
<br>
Adding an image
<p align="center">
   <img src="/Images/menuBar.png" width="512" title="hover text"> 
    <img src="/Images/runScript.png" width="512" title="hover text"> 
</p> 
<br>
-->

Just switch back to the Layout workspace after this and you're good to go! You can find the details about the functionality in the above [section](https://github.com/VKG5/F1-Track-Gen/edit/main/README.md#current-features-).

## Results
I can keep on talking about what we have done and get all technical but that's probably not what you're reading this for, so I have attached a few images below for your reference, that this is the kind of result you can expect out of the current add-on.
- [x] Optimized Geometry
- [x] Procedural Texture
- [x] Modular
- [x] Easily modifiable

<br> 
<!-- Adding an image -->
<p align="center">
    <img src="/Images/melbourne .png" width="512" title="hover text"> 
    <img src="/Images/texas.png" width="512" title="hover text"> 
    <img src="/Images/sakhir.png" width="512" title="hover text">
</p>
<br>

That's what we have for now! But we will surely keep on updating this in the future for better results!

## Journey
This started off as a simple Hackathon project for [Hackmakers Formula AI Hack 2022](https://www.hackmakers.com/) but turned out to be too fun, made a lot of new connections, had a lot of fun and sleepless night (Imagine, overworking even in online mode), but that was one of the things about this, the adrenaline inducing ideas, the brainstorming sessions, seeing the output of your efforts take shape (Literally, we are talking about 3D afterall!) 

We'll be updating this repo in the future with better performance, better textures and an overall better product!

## License
Use it however you want to! Just be sure to credit us for our work :D That's all we ask as we are contributing this project the Blender's Open Source Community :heartpulse:

- [x] Be sure to credit the devs for their efforts in whatever repo you use!
