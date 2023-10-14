
# Gnome Wallpaper Setter

### An effortless wallpaper downloader and setter application


The Linux Wallpaper Changer is a Python script designed to download and set wallpapers for Linux devices. It uses the Unsplash API (for now) to fetch high-quality images from the user specified image collection.

The script is intended to be run in the background and automatically change the wallpaper every week.
## Acknowledgements

 - This app uses the Unsplash API for now. However, there is a plan to allow users to download wallpapers from any other API soon.

## Make sure to create a Wallpapers directory in the Pictures directory before running the application 

You can do such with

```console
foo@yourPC:~/$ mkdir Pictures/Wallpapers
```

## Installation

Upon downloading the package do head to the directory that the package is downloaded to then run:

```console
foo@yourPC:~/PathOfDownload$ sudo dpkg -i GnomeWallpaperSetter.deb
```

Before running the program make sure to get your API key from Unsplash

Then proceed to get the collection code in the following form:

```console
https://unsplash.com/collections/NqP3YvqA-vg/abstract
```
hich means the code is:

```console
NqP3YvqA-vg
```

And finally specify the home direcotry in the following format

```console
"home/user"
```

where user can be found using:

```console
foo@yourPC:~/$ whoami
```

Then use the following command:

```console
foo@yourPC:~/$ GnomeWallpaperSetter -config
```

and set the specified values.


## Running

To run the program just type the following

```console
foo@yourPC:~/$ GnomeWallpaperSetter
```

To run the program on every startup, follow your operating system's startup application procedure

### Command line arguments

To force a wallpaper change:

```console
foo@yourPC:~/$ GnomeWallpaperSetter -f
```


To edit API key:

```console
foo@yourPC:~/$ GnomeWallpaperSetter -a "your API key"
```

To change collection code:

```console
foo@yourPC:~/$ GnomeWallpaperSetter -c "collection code"
```

To edit home directory:

```console
foo@yourPC:~/$ GnomeWallpaperSetter -h "your home directory"
```

To access config file:

```console
foo@yourPC:~/$ GnomeWallpaperSetter -config"
```
