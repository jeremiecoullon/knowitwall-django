import unidecode
import os

def seasons_image_directory_path(instance, filename):
    return 'Season_images/{0}/{1}'.format(instance.title, filename)

def episode_image_directory_path(instance, filename):
    # Episode images will be uploaded to MEDIA_ROOT/Episode_image-id_<id>/<filename>
    return 'Episodes_images/episode_id-{0}/{1}'.format(instance.unique_id, filename)

def author_image_directory_path(instance, filename):
    # Author images will be uploaded to MEDIA_ROOT/Author_images/<author_name>/<filename>
    unaccented_author_name =  unidecode.unidecode(instance.name)
    return 'Author_images/{0}/{1}'.format(unaccented_author_name, filename)
    # return 'Author_images/{0}/{1}'.format(instance.name, filename)


def create_youtube_embed(url):
    """
    Parses URL to youtube video and returns the embeded link.
    """
    if 'www.youtube.com' not in url:
        return ""
    if 'youtube.com/embed' in url:
        if "?" in url:
            url = url.split("?")[0]
        url = url.split('embed/')[-1]
        # return url
    if 'watch' in url:
        url = url.split("=")[1]
    if "&" in url:
        url = url.split("&")[0]
    return os.path.join('https://www.youtube.com','embed',url+'?autoplay=1')