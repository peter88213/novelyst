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

- If no yWriter project is specified by dragging and dropping on the program icon,
  the latest project selected is preset. You can change it with **File > Open** or **Ctrl-O**.

#### Move parts, chapters, and scenes

Drag and drop while pressing the **Alt** key. Be aware, there is no "Undo" feature. 
- When moving a normal chapter from the narrative to the "Research" branch, be sure to
  change its type to "Notes".

#### Delete parts, chapters, and scenes

Select item and hit the **Del** key.

- When deleting a part, chapter oder scene, the scenes are moved to the _Trash_ chapter at the bottom. 
- The _Trash_ chapter is created automatically, if needed. 
- When deleting the _Trash_ chapter, all scenes are deleted.

#### Lock and unlock

You can lock the project, so that no changes can be made with *novelyst* while parts of the project are
edited "outsides", e.g. with OpenOffice. In locked status, the window footer displaying the project path
is of dark color with white text. 
 
- You can lock the project with **File > Lock** or **Ctrl-L**. The project is saved when modified.
- You can unlock the project with **File > Unlock** or **Ctrl-U**. 

The project lock status is persistent. This is achieved by automatically creating a lock file 
named `.LOCK.<project name>.yw7#`. If you delete this file while *novelyst* is not running, the project 
will be unlocked upon next start.  

This locking mechanism must not be confused with that of yWriter. When the project is opened in yWriter, 
yWriter creates its own lock file. If *novelyst* finds this, it will neither load nor save the project. 

#### Refresh the tree

Hit the **F5** key to synchronize the tree with the project structure. This ensures for instance, 
that scenes within a "Notes", "Unused", or "To do" chapters are of the same type after moving them there.
- Refreshing the tree may trigger the "Modified" flag.
- When refreshing the tree, "Normal type" chapters in the *Research* tree are moved to the *Narrative* tree.
- When refreshing the tree, parts and chapters are renumbered according to the settings. 

#### Reload the yWriter project

- You can reload the project with **File > Reload** or **Ctrl-R**.
- If the project has changed on disk since last opened, you will get a warning.

#### Save the yWriter project

- You can save the project with **File > Save** or **Ctrl-S**.
- If the project is open in yWriter, you will be asked to exit yWriter first.
- If the project has changed on disk since last opened, you will get a warning.
- It is recommended to refresh the tree (see above) before saving. So you can see how 
  it will look after reloading. 

#### Close the ywriter project

- You can close the project without exiting the program with **File > Close**.
- When closing the project, you will be asked for saving the project, if it has changed.
- If you open another project, the current project is automatically closed.

#### Exit 

- You can exit with **File > Exit** of **Ctrl-Q**.
- When exiting the program, you will be asked for saving the project, if it has changed.

