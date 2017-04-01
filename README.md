## Sprengel

Download a .hg directory exposed on the web, e.g. http://example.org/.hg/, even if it has directory listing disabled.

## How to download a mercurial hg directory

Follow these steps to download the sources:

* Run the script: `python sprengel.py http://example.com/`
    * it downloads the manifest and changelog files as described in [the documentation](https://www.mercurial-scm.org/wiki/Repository#Structure).
    * then it runs `hg --debug manifest` to get a list of files.
    * then it tries to download all those files.
* You now have an incomplete .hg directory. Use the [convert extension to fix it](https://www.mercurial-scm.org/wiki/RepositoryCorruption#Recovery_using_convert_extension).
    * add the convert extension to the hgrc.
    * run `hg convert --config convert.hg.ignoreerrors=True REPO REPOFIX`
* Now you have a correct mercurial repo. Run `hg update -C` to restore all files.
