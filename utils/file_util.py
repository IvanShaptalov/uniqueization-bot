from icecream import ic


def save_file(file, path):
    import os

    if not os.path.exists(path):
        with open(path, 'wb') as writer:
            writer.write(file)
            writer.close()


def delete_file(path):
    import os
    if os.path.exists(path):
        os.remove(path)
        ic('deleted', path)
    else:
        ic("The file does not exist: ", path)