# F1-Track-Gen
We’ve created a blender add-on that allows anyone to generate an F1 circuit without the need to manually model anything. The add-on comes with a simple to use interface that presents the user with the option to select the track that needs to be modeled and the particular sectors that need to be included in the 3D model.

<!-- Adding an image -->
<p align="center">
    <img src="https://yt3.ggpht.com/ytc/AKedOLSvLgntU68OOYUb-DPPQ48Bdh_tTDbhPBvXzXbc=s900-c-k-c0x00ffffff-no-rj" width="512" title="hover text"> 
</p>

## Current Features :
1. **Simple UI:**
As displayed in _Fig 2._ we have a very simple UI that even unexperienced people should be able to use easily. There are quite a few parameters :
    - **Sectors :** The datasets we have used so far have 3 sectors per track (Sector 1 - Start, Sector 2 - Mid, Sector 3 - End)
    - **API Type :** We have linked 3 APIs to get data from (Melbourne, Texas and Sakhir)
    - **Track Type :** This is solely to show the scalability and verstility of the solution, you can swap the track for any track of you liking!
    - **Pole Distance :** Distance b/w consecutive poles
    - **Flag Distance :** Distance b/w consecutive flag(s) (5 country flags included as of the moment : Australia, Canada, India, United Kingdom, USA)
    - **Pole Offset :** The distance of the pole from the center of the track
    - **Flag Offset :** The distance of the flag(s) from the center of the track
    - **[x] Delete Prev Fillers :** This is to clean up the previously present Fillers (Flags and Poles) before generating new ones [Recommended to keep checked]
    - **Generate :** The button which makes the magic happen! The track is generated based on the inputs from API Type, Track Type and Sectors
    - **Generate Fillers :** This will distribute randomly, instances of the Flag(s) and Poles around the track, independent of Track length
    
- [x] #739
