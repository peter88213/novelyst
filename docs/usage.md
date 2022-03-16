[Project homepage](https://peter88213.github.io/novelyst)

--- 

The *novelyst* Python program provides a tree view for yWriter projects.

## Usage

The included installation script prompts you to create a shortcut on the desktop. 

You can either

- launch the program by double-clicking on the shortcut icon, or
- launch the program by dragging a yWriter project file and dropping it on the shortcut icon.


### Operation

#### Open a yWriter project

- If no yWriter project is specified by dragging and dropping on the program icon, the latest project selected is preset. You can change it with **File > Open** or **Ctrl-o***.

#### Move parts, chapters, and scenes

Drag and drop while pressing the **Shift** key.

#### Delete parts, chapters, and scenes

Select item and hit the **Del** key.

- When deleting a part, chapter oder scene, the scenes are moved to the _Trash_ chapter at the bottom. 
- The _Trash_ chapter is created automatically, if needed. 
- When deleting the _Trash_ chapter, all scenes are deleted.

#### Reload the yWriter project

- You can reload the project with **File > Reload** or **Ctrl-r***.
- If the project has changed on disk since last opened, you will get a warning.

#### Save the yWriter project

- You can save the project with **File > Save** or **Ctrl-s***.
- If the project is open in yWriter, you will be asked to exit yWriter first.
- If the project has changed on disk since last opened, you will get a warning.

#### Close the ywriter project

- You can close the project without exiting the program with **File > Close**.
- When closing the project, you will be asked for saving the project, if it has changed.
- If you open another project, the current project is automatically closed.

#### Exit 

- You can exit with **File > Exit** of **Ctrl-q**.
- When exiting the program, you will be asked for saving the project, if it has changed.

