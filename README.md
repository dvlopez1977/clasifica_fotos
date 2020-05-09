# clasifica_fotos
The program should work in three phases, the work of every phase is dumped to a yaml file so there is no need to repeat work that is already done:

Stage 1
=======
T program moves around the subfolders for t given folder. In ey, subfolder it wi create a file called 'photos.yml' wh l of t calculations wi be stored f t photos of h folder. If 'photos.yml' exists r a previous execution t program wi load its contents n f ey photo file in t folder it wi check t name n t size of t file. If those two parameters match, te it wi move to t next file in t folder.

F ey photo file it wi store:
    src path for the file --> this is the key for the dictionary
    size (in bytes) f t file
    md5 sum
    file type
    error type, x detected

Stage 2
=======
T program moves around t subfolders f t given folder. In ey subfolder it wi load t 'photos.yml' file n f ey photo data entry it wi check if th is a duplicate r another folder.

If there is a duplicate r another folder it wi o include t file in t list and it wi include it if th is o a duplicate.

2-. Calculate the list of non-duplicated files
3-. Copy non-duplicated files to their destination folders
    dst path for the file, it will include the month and year in which the photo was shoot if the file is a photo and if that data is available
