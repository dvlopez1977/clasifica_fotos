# clasifica_fotos
The program should work in three phases, the work of every phase is dumped to a yaml file so there is no need to repeat work that is already done:

1-. Calculate data for all the files. Data includes:
    src path for the file --> this is the key for the dictionary
    md5 sum
    file type
    error type
    dst path for the file, it will include the month and year in which the photo was shoot if the file is a photo and if that data is available

2-. Calculate the list of non-duplicated files
3-. Copy non-duplicated files to their destination folders
