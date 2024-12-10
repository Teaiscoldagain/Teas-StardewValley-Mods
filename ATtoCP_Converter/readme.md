# AT >> CP Converter<br><br>

### Data Schema based on CP [Furniture Fields in SDV Wiki](https://stardewvalleywiki.com/Modding:Items#Furniture:~:text=for%20this%20entry.-,Furniture,-Furniture%20are%20decorative)<br><br>

Definitions of additional values that will be derived from available AT data to facilitate CP Conversion:

| Auxiliary Values | Formula | Definition in context of AT |
| --- | --- | --- |
| ModID | AT ModID + cp.conv | Original ModID will be extracted from the manifest and concatenated with “cp.conv” string to set the cp conversion reference for unique identifier |
| Texture Index | IF: textures as individual pngs: extract final digits (e.g. texture_0 > texture_index = 0)<br><br><br>IF: textures as single file: split textures using PILLOW, assign texture_index retrospectively to slices | To provide unique identification and ability to refer to Manual Variations we will extract the numerical reference from the existing texture_x.png file, if possible. If the textures.png (collective) is used instead the png will be first sliced into individual texture pngs and named using the AT convention of texture_x.png |

<br><br>
Definitions of data conversions needed to build a CP model of an item based on data available n the AT version of the mod:

| CP | Formula | Definition in context of AT |
| --- | --- | --- |
| key >> unique item ID | {{ModID}}.[1 type].[texture index] | AT does not require that each texture has a unique id key, as such we will derive it using a preferred formula guaranteeing uniqueness:  |
| [0] name | Manual Variations: Name > Manual Variations > Keywords > texture.json keywowrds > CP [1 type] | CP Internal Name - this s not the actual Display Name of the item and does not currently make any difference - the display name will be passed to the i18n token - but, to make the object easier to recognize in the json file we will use the same value as the i18n token value for simplicity and easy of troubleshooting.<br><br>As AT in itself does not require a display name (it’s an optional key under manual variations only so very rarely present) initially we will derive a placeholder by looking for a few potentially existing keys in the texture json - but ultimately I want to provide an easy gui for a quick manual review and adjustments of display names to make them more user friendly.<br><br>Placeholder logic, in order:<br><br>1. Check if “Name” exists: <br>> does “Manual Variations” object exist in texture.json; if so does corresponding texture key exist; is so does “name” exist; if so retrieve “name” and set as [0 name]<br><br>2. Check if individual texture level keywords exist:<br>> does “Manual Variations” object exist in texture.json; if so does corresponding texture key exist; is so does “keywords” object exist; if so concatenate values in “keywords” dictionary and set as [0 name]<br><br>3. Check if texture.json level keywords exist:<br>- does “keywords” object exist; if so concatenate values in “keywords” dictionary and set as [0 name]<br><br>4. If none above exists user [1 type] value as [0 name] |
| [1] type | ItemName > Item ID > CollectiveNames > Collective IDs | AT uses these four keys (one has to be present in each AT texture.json) to match against the vanilla object - we will extract it and match against a db of vanilla values to populate the furniture **[type]** |
| [2] tilesheet size | -1  | Static value set as -1 (default vanilla)<br><br>As AT requires that provided textures are the exact vanilla tilesheet sizes (in order to paste over them) we can safely use the default vanilla fallback |
| [3] bounding box size | -1  | Static value set as -1 (default vanilla)<br><br>As AT requires that provided textures are the exact vanilla tilesheet sizes (in order to paste over them) we can safely use the default vanilla fallback for the bounding box as well |
| [4] rotations | -1  | Static value set as -1 (default vanilla)<br><br>As AT requires that provided textures are the exact vanilla tilesheet sizes (in order to paste over them) we can safely use the default vanilla fallback for the rotations as well |
| [5] price | 100 (fallback) / user defined variable | The default fallback price will be set to 100, but the converter will prompt for a variable value to be set by the user if preferred |
| [6] placement restriction | -1  / user defined variable | The default fallback will be set to -1 to match existing vanilla restriction, but the converter will prompt for a variable value to be set by the user if preferred in case the user wants to restrict or relax the condition |
| [7] display name | i18n key = CP key<br>i18n value = [0 name] | For simplicity and ease of troubleshooting we are re-using existing values |
| [8] sprite index | assigned by texture_stitch method | Final furniture spritesheet will be automatically stitched by the texture_stitch method, during which the exactly x y coordinates will be recorded for each texture added and recalculated into tile indices  |
| [9] texture | furniture.png or user provided variable.png | As all textures will be stitched into a single png file we can assign a static file name, or use user provided variable |
| [10] off limits for random sale | false or user provided variable as true | User will have an option to specify if they want to exclude it, otherwise it will default to false |
| [11] context tags | {{ModID}}_collection<br>+<br>user provided variables | By default a modid+collection tag will be added to facilitate a custom catalogue creation (optional) by means of Calcifer dependency, other tags can be provided as user variables |
