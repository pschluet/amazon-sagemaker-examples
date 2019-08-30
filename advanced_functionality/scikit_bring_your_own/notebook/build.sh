cp ../container/requirements.txt requirements.txt
# Run the docker build command, and remove the requirements.txt file 
# no matter what happens (i.e. if docker build fails, still remove the
# requirements.txt file)
{
    docker build -t jnotebook . &&
    rm requirements.txt

} || {
    rm requirements.txt
}

